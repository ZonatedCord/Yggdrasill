# BaseChipOnly — Defects and Fixes

Bring-up session, 2026-07-28 → 2026-08-01. Board reached a working state: 5 V and 3.3 V rails correct, ESP32 boots, WiFi connects, WLED 16.0.1 drives the LED strip.

This file records every defect found, how it was verified, and the proposed fix. Nothing here has been applied to the KiCad sources yet.

> Written in English per the project convention in `CONTEXT.md`.

---

## Verification method

Findings below were confirmed against authoritative sources, not derived by hand:

- **Netlist**: `kicad-cli sch export netlist --format kicadsexpr BaseChipOnly.kicad_sch` — gives `pinfunction` per node
- **Fabricated copper**: X2 attributes (`%TO.P,comp,pin%`, `%TO.N,net%`) in `Esportazione/BaseChipOnly-F_Cu.gbr`
- **Hardware**: multimeter on the assembled board

Hand-computing pad coordinates from `.kicad_pcb` footprint rotation is unreliable — see the correction note at the bottom.

---

## Defects to fix in the KiCad sources

| # | Problem | Evidence | Proposed fix | Severity |
|---|---|---|---|---|
| 1 | **D2 (SS34) reversed.** Catch diode has cathode on GND, anode on /SW. An LM2596 buck needs cathode on SW. As drawn, the diode shorts SW to GND during the switch on-time and provides no freewheel path during off-time. | Netlist: `D2 pin 1 pinfunction "K"` on GND, `pin 2 pinfunction "A"` on /SW | Rotate D2 180°, re-route | **Critical** |
| 2 | **D1 (status LED) reversed.** Anode on GND, cathode through R0 to +5 V. Reverse-biased, never lights. | Netlist: `D1 pin 2 pinfunction "A"` on GND; `Net-(D1-K)` carries `D1 pin 1` + `R0 pin 2` | Rotate D1 180° | Medium |
| 2b | **D1 still does not light after being fitted rotated.** The reversal in #2 is confirmed by the netlist, so it is a real defect — but it is evidently not the only fault on this branch. **Open, not diagnosed.** | Hardware: LED replaced once and later fitted rotated; dark in both cases | See "Open issues" below for the measurement that splits the causes | Medium |
| 3 | **Auto-reset circuit non-functional.** Both transistor emitters go to GND, so esptool cannot drive EN and IO0 in the sequence it expects. Every flash needs a manual jumper. | Netlist: `EN_CTRL1 pin 2 (E)` and `IO0_CTRL1 pin 2 (E)` both on GND. Confirmed on hardware — auto-reset never entered download mode. | Use the cross-coupled circuit: EN transistor base ← DTR, emitter ← RTS; IO0 transistor base ← RTS, emitter ← DTR. Note this **swaps the base assignments** relative to the current design, in addition to lifting the emitters off GND. Derived from esptool's classic reset sequence with FTDI active-low DTR#/RTS# — **bench-verify before committing.** Also add #3b. | **High** |
| 3b | **No BOOT or RESET button.** When auto-reset fails there is no fallback: entering download mode means jumpering module pin 25 to GND by hand while power-cycling. Every error message from flashing tools ("hold the BOOT button…") assumes buttons that don't exist here. | Bring-up experience | Add two tactile switches: **BOOT** (IO0 → GND) and **RESET** (EN → GND), each with the pull-up already present (R3 on IO0, R4 on EN). Cheap, tiny, and independent of whether the auto-reset rework in #3 proves correct — worth having even if #3 works. Keep them reachable once the board is inside the pot. | Medium |
| 4 | **L1 has no value and no MPN**, and the 1008 footprint cannot carry the current. A 1008 inductor is rated well under the LM2596's ~3 A current limit. The fitted part burned out during bring-up. | Schematic value field is just `L`; footprint `Inductor_SMD:L_1008_2520Metric` | ~100 µH, Isat ≥ 1 A, footprint 1210 or 1812. The 3V3 rail feeds only the ESP32 — the LED strip runs off +5 V through J2, so ~500 mA peak is the requirement. | **High** |
| 5 | **Polyfuse is 12 A** — protects neither the LM2596 (3 A max) nor the ESP32. | Schematic value | 1.5 A, after measuring real draw with the intended strip at full brightness | Medium |
| 6 | **U3 (USBLC6-2SC6) GND pin unconnected.** ESD clamping is inoperative. The data signal still passes, because pins 1 and 6 are both `I/O1` and internally the same node. | Netlist: U3 pins 2–5 each on their own unnamed net | Connect the GND pin | Medium |
| 7 | **+3V3 traces too narrow.** | Carried over from the earlier review | Widen | Low |
| 8 | **Reference and Value fields are swapped**, deliberately, so the silkscreen shows component values for hand assembly. Side effect: BOM and pick-and-place exports are wrong, and the board can't be discussed by designator. | Footprint properties | Reference on `F.SilkS`, Value on `F.Fab`, then export an assembly-drawing PDF showing values for hand assembly. Same benefit, no corrupted exports. | Medium |
| 9 | **D_TVS1 uses the bidirectional TVS symbol** (pins A1/A2) but SMF5.0A is a unidirectional part. | Netlist pin functions | Use the unidirectional symbol, or change the part | Low |
| 10 | **COUT1 is a 47 µF ceramic alone** on the LM2596 output. That regulator's compensation expects some ESR; an all-MLCC output is marginal for loop stability. | Design review | Add an electrolytic alongside, or re-check against the LM2596 datasheet's recommended output capacitance | Low |

---

## Bring-up log — what actually failed

**Smoke from L1.** Root cause was a **solder bridge between GND and +3V3 underneath the ESP32 module** (pins 1 and 2 are adjacent). The 3.3 V rail was shorted, the buck drove into that short, and L1 — the only current-limiting element in the path — overheated.

Casualties: L1, and U4 was replaced as a precaution. The ESP32 module survived: the rail was pulled to 0 V, never over-voltage.

Diagnosis path that worked, for next time:

1. Measure +3V3 ↔ GND on the **bare** board first — establishes whether a short is copper or assembly
2. Remove components on the rail one at a time, cumulatively, re-measuring after each. Do not put them back between steps.
3. `< 1 Ω` means a solder bridge or a punctured MLCC; a few ohms means a dead semiconductor

Useful probe points: J3 holes `GND` and `3v3` are plated and on-net even with no header fitted.

---

## Open issues

**D1 status LED is still dark**, even fitted rotated 180° from the silkscreen, and with a replacement LED. The schematic reversal (#2) is confirmed by the netlist and is genuine, but something else on this branch is also wrong. Not yet diagnosed.

Branch under test: `+5V → R0 (470 Ω) → D1 anode … D1 cathode → GND`. For the LED to conduct, the anode must sit on the **left** pad (the R0 side) and the cathode on the **right** pad (GND).

Next measurement — board powered, DC volts, black probe on GND, red probe on the **left** LED pad:

| Reading | Meaning |
|---|---|
| ~5 V | No current flowing. LED still backwards, open, or dead. |
| ~2–3 V | Current *is* flowing and the LED should be glowing. Suspect a dim or faulty LED, or the wrong part fitted. |
| ~0 V | R0 is open or was never populated. Check R0 across its own pads — should read 470 Ω. |

Worth ruling out first: 0805 LED cathode markings are ambiguous between manufacturers (green bar underneath, notch, or a mark on the top face), so "rotated" may not have meant what it looked like. A diode-mode check on the loose LED identifies its anode with certainty before fitting.

Expected current when working: (5 − 2) / 470 ≈ 6.4 mA.

---

## Workarounds for the currently assembled board

These apply to the physical board as built, until the sources are fixed:

- **D2**: cathode band on the **lower** pad (the one toward L1), i.e. opposite the silkscreen
- **D1**: cathode mark toward the GND pad — but see "Open issues", this alone did not make it light
- **Flashing**: see below

---

## Flashing procedure (current board)

Auto-reset does not work, and there is no BOOT button. Manual entry into download mode:

1. Close any serial monitor — `pkill -9 screen`. A held port produces `Failed to open serial port`.
2. Wire the USB-UART adapter: `GND`→`GND`, adapter `RXD`→`TX0`, adapter `TXD`→`RX0`. Leave `3v3` disconnected and power the board from the barrel jack — an FT232RL's 3V3OUT supplies only 50 mA, far short of the ESP32's WiFi peaks.
3. **Disconnect DTR and RTS.** If connected, esptool's reset attempt knocks the chip back out of download mode.
4. Jumper **module pin 25 (IO0)** — the bottom-most castellated pad on the module's right edge — to `GND` on J3.
5. Holding the jumper: unplug the barrel jack, plug it back in, wait a second, release the jumper.
6. Flash. https://install.wled.me works; select the `FT232R USB UART` port, `Plain` build.
7. Power-cycle by hand afterwards to run the new firmware.

**WLED configuration**: LED data is **GPIO 13**. Module pin 16 is GPIO13 — do not confuse the module pin number with the GPIO number. Chain: U1 pin 16 (`IO13`) → R5 470 Ω → U3 → J2 pin 1, the terminal silkscreened `Data`.

J2 terminal block: pin 1 `Data`, pin 2 `VIN` (+5 V), pin 3 `GDN` (GND — typo in the silkscreen, worth fixing too).

---

## Correction to the existing review document

`base-chiponly-review.md` names via-on-pad short circuits on C2, C3, COUT1, Rbot1 and Rtop1 as the "SHORT-CIRCUIT ROOT CAUSE". **Those shorts do not exist.** Those vias sit inside the pads deliberately, on the *same* net, to reach the ground plane.

Disproved two ways:

- The bare board measures no short between any rail and GND
- X2 attributes in the fabricated `F_Cu.gbr` show pad and via carrying the same net at every flagged location — e.g. `COUT1 pin 2 net=GND` with the via at that position also `net=GND`

The false finding came from computing pad positions with the wrong rotation sign, which mirrors every pad about its footprint centre and pairs each via with the opposite pad. The error is self-consistent and survives cross-checks against the schematic, which is why it looked convincing.

Two consequences:

- `base-chiponly-review.md` needs rewriting
- `CONTEXT.md` states the issue was "fixed in HW rev 1.03+", which rests on the same false premise and should be removed

Still valid from that document: the oversized polyfuse, the unconnected U3 GND pin, the narrow +3V3 traces, and the bidirectional TVS symbol.
