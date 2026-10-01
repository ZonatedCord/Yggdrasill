# BaseChipOnly — how the board works

Base board of the Yggdrasill lamp: an ESP32-WROOM-32U running WLED drives the 9 leaf boards (`PCB/Foglia`). This describes **HW Rev 2.0**, sources in `PCB/BaseChipOnly_rev2/` — tests done, changes from rev 1.03 and the *not yet tested on hardware* caveat are in [its README](../PCB/BaseChipOnly_rev2/README.md).

## Block diagram

```
5V PSU ─► J1 barrel jack ─► Polyfuse1 ─► +5V bus ─┬─► J2 terminal (VIN/GND) ─► 9 leaves in parallel
                                                   ├─► C1 1000µF bulk, C2 100nF, D_TVS1 SMAJ5.0A (clamp)
                                                   ├─► R0 + D1  (power-on LED)
                                                   └─► U4 LM2596-ADJ buck ─► L1 100µH ─► +3V3 ─► ESP32 (U1)
ESP32 GPIO13 ─► R5 100Ω ─► U3 USBLC6 (ESD) ─► J2 "Data" ─► DIN of the first WS2812B on every leaf
J3 (GND 3V3 TX0 RX0 DTR RTS) ─► USB-UART adapter; DTR/RTS drive the auto-reset transistors
SW1 BOOT (IO0→GND), SW2 RESET (EN→GND)
```

## Blocks

**Power input.** J1 (GCT DCJ200-10, rated 5 A) → polyfuse → +5V. The +5V rail feeds the LEDs directly; only the ESP32 goes through the buck. D_TVS1 clamps spikes on +5V, C1 buffers the LED current steps.

**3.3 V regulator.** LM2596-ADJ, 150 kHz buck. Vout = 1.23 V × (1 + Rtop1/Rbot1) = 1.23 × (1 + 2.0k/1.2k) ≈ 3.28 V. D2 (SS34) is the catch diode (cathode on SW). L1 Bourns SRN6045TA-101M (Isat 1.33 A). COUT1 47 µF MLCC + COUT2 220 µF tantalum: the tantalum's ESR keeps the LM2596 loop stable. Simulated (TI model): 3.280 V, 0.8 mV ripple, ≥ 3.26 V during 500 mA WiFi bursts. With only 5 V in, the LM2596 runs close to dropout: it needs **≥ ~4.5 V at its input** to hold 3.3 V at 500 mA (its switch drops ~1 V) — see *Known limits*.

**ESP32.** U1 WROOM-32U (external antenna via U.FL). LED data is **GPIO13** = module pin 16 (set 13 in WLED, not 16).

**Programming / auto-reset.** J3 carries TX0/RX0/DTR/RTS. Two NPN transistors in the standard cross-coupled arrangement: DTR=1,RTS=0 → EN low (reset); DTR=0,RTS=1 → IO0 low (bootloader). esptool drives this sequence automatically. R3/R4 pull IO0/EN up; C4 (1 µF, with R4 = the 10 kΩ + 1 µF recommended by Espressif) delays EN at power-on. Verified by simulation for both esptool reset sequences: EN goes to 0.07 V, IO0 is still low when EN comes back up → download mode; opening a serial monitor does not reset the board. BOOT/RESET buttons are the manual fallback (hold BOOT, tap RESET).

**LED data.** R5 (100 Ω) damps ringing on the long wires to the leaves — it was 470 Ω, but with 9 leaves in parallel that RC shrank the WS2812B pulses close to their minimum width (simulated); 100 Ω delivers clean ~370/770 ns pulses; U3 protects the ESP32 pin from ESD coming back up the leaf wiring.

**Status LED.** D1 via R0 470 Ω from +5V → 6.7 mA for a red LED, 4.6 mA for white/blue (simulated). That is **not** too much current (0805 LEDs take 20 mA). D1 stays dark on the first assembled board for a reason still undiagnosed: check that R0 is fitted and reads 470 Ω, then measure the LED-anode pad against GND with the board on (≈5 V = no current; ≈2–3 V = current flowing, LED faulty). On the old layout the LED's GND pad has a via in the middle of the pad that sucks solder into the ground plane — a dry joint there is a likely cause. The new files move every GND via beside its pad.

## The leaves (PCB/Foglia) and the power budget

Each leaf: 15 × WS2812B daisy-chained, 100 nF per LED, 3-pad connector (+5V, Data, GND). The last LED's DOUT is not brought out, so the **9 leaves are wired in parallel** on the same data line: WLED is configured for 15 LEDs and all leaves show the same pattern.

| | |
|---|---|
| LEDs | 9 × 15 = 135 WS2812B |
| Worst case (full white, ~55 mA/LED) | ≈ 7.4 A |
| ESP32 (from +5V, via the buck) | ≈ 0.3 A peak |
| Barrel jack limit | 5 A |

So full white at full brightness is **not possible** on this hardware — WLED's current limiter must be on:

- **PSU: 5 V 4 A** (20 W) recommended
- **WLED → LED preferences → Automatic Brightness Limiter: max current 3000 mA**, LED current 55 mA (5 V WS2812)
- Polyfuse MF-LSMF400/12X (4 A hold, 8 A trip, 2920) — above the 3 A limiter plus ESP32, below the fault currents

If you use a smaller PSU, lower the WLED limit to about 80 % of its rating.

## Layout (re-done 2026-09-30, spaced out 2026-10-01)

Board outline, the four mounting holes, J1, J2, J3, U1 and C1 are where they always were, so the printed base and the PCB mount (`TasselloFissaggioPCB.stl`) still fit. Everything else was re-placed in functional blocks:

- **Left column — 3.3 V buck.** U4 with its pins pointing up; directly above the pins D2 (catch diode), L1 and the output caps COUT1/COUT2/C3, so the switching loop U4 OUT → D2 → GND is a few millimetres long. Rtop1/Rbot1 sit next to the FB pin. CIN1/C2 are right at the VIN pin. The block keeps ~1 mm between parts so it can be hand-soldered with an iron.
- **Bottom left — input.** Jack → polyfuse (2920) → a 3 mm +5V bus that runs across the board to C1 and up to the regulator, with a 2 mm branch to J2. The TVS sits on the bus next to the polyfuse.
- **Bottom right — power LED** (R0 + D1) next to C1, fed by a thin branch of the +5V bus.
- **Under the ESP32 — auto-reset.** R1–R4, C4, the two transistors, then R5/U3 feeding J2 "Data".
- **Top edge — RESET and BOOT buttons**, centred on the board, with RESET/BOOT printed on either side.
- **Back — solid GND plane.** Only a few short signal jumpers cross it (DTR/RTS lanes from J3, EN and IO0 under the module, IO13). Every GND pad has its via beside the pad, not in it (easier hand soldering, no solder wicking — see the D1 note above).
- The credit text stays on the front, right edge; the logo stays on the back.

Rebuild recipe (deterministic, all routing by hand): `PCB/BaseChipOnly_rev2/BaseChipOnly-backups/relayout-work/relayout.py` + `build.sh`.

## Simulations

Every analog block was simulated in ngspice (TI's LM2596 model, MMBT3904 transistors): auto-reset, power-on EN timing, the 3.3 V buck (nominal, LEDs at 3 A, minimum input voltage, start-up), status LED, LED data line. Results, plots and decks: `PCB/BaseChipOnly_rev2/simulazioni/README.md`. Three values changed because of them: **C4 100 nF → 1 µF**, **R5 470 Ω → 100 Ω**, transistors specified as **MMBT3904**.

## Pre-order checks (2026-09-30)

Run `PCB/BaseChipOnly_rev2/verifica.sh` after any change: ERC, DRC with schematic parity, regenerates the fab files and cross-checks every pad of the exported front-copper Gerber against the schematic. Last run: **PASS** (0 ERC errors, 0 DRC errors, 0 unconnected, 0 parity issues, 120/120 pads match).

Also checked by hand:

- **Pinouts** of every active part against its datasheet: LM2596S-ADJ (1 VIN, 2 OUT, 3 GND, 4 FB, 5 ON/OFF), USBLC6-2SC6, MMBT3904 SOT-23 (1 B, 2 E, 3 C), SS34/SMAJ5.0A/LED (pad 1 = cathode), tantalum and C1 (pad 1 = +), J2/J3 order, ESP32 power/EN/IO0/IO13/UART pins.
- **ESP32 strapping pins:** IO0 pulled up + BOOT button; IO2 and IO12 floating (download mode allowed, flash at 3.3 V); IO5/IO15 floating (internal pull-ups).
- **Trace current (IPC-2221, 1 oz outer, +10 °C):** +5V bus 3.0 mm → 5.3 A; J2 branch and jack input 2.0 mm → 4.0 A; SW node ≥ 1.2 mm → 2.7 A; +3V3 ≥ 0.6 mm → 1.7 A. LED current returns through the solid GND plane.
- **Fab limits (JLCPCB):** min track 0.2 mm, vias 0.6/0.3 mm, copper ≥ 1.07 mm from the edge, silkscreen ≥ 0.8 mm / 0.15 mm line. The 12 ESP32 thermal vias are 0.2 mm (same as the rev 1.03 order).
- **3D view:** diode bands, tantalum +, regulator orientation, button access (`Esportazione-2026-09-30/preview-3d-top.png`).
- **Every part has an MPN** except generic resistors/capacitors (value + size is enough).

Not verifiable from the files: the fit of the new buttons in the printed base (they sit on the top edge next to J3), and the USB-UART adapter (must break out DTR **and** RTS at 3.3 V).

## First power-up (recommended)

1. Before soldering the ESP32 module: fit the power section only (J1, polyfuse, TVS, C1/C2/CIN1, U4, D2, L1, COUT1/COUT2/C3, Rtop1/Rbot1).
2. Measure +5V↔GND and +3V3↔GND with the multimeter: anything under ~100 Ω means a solder bridge.
3. Power it (bench supply limited to ~300 mA if available): +3V3 must read 3.25–3.30 V.
4. Fit the ESP32, the auto-reset parts and the buttons; repeat step 2 on +3V3 (the rev 1.03 short was a bridge between module pins 1 and 2).
5. Connect the adapter (3.3 V, GND/TX/RX/DTR/RTS; leave its 3V3 unconnected), flash WLED; the board should enter download mode by itself.

## Known limits

- The ESP32 drives 3.3 V data into WS2812B powered at 5 V (spec wants ≥3.5 V). It works in practice on this build; if leaves flicker, the fix is a 74AHCT1G125 buffer powered from +5V between GPIO13 and R5.
- **LM2596 input headroom.** The regulator needs ≥ ~4.5 V at its input at 500 mA. With the LEDs at the 3 A limit, the +5V rail sits at ~4.5 V (0.15 Ω of cable + jack + polyfuse) and the 3.3 V rail still holds (≥ 3.21 V) — but a long thin cable or a weak PSU would brown out the ESP32. Use a good 5 V 4 A supply (5.1–5.2 V is better) with a short thick cable, and keep the WLED limiter on. A future revision could use a 1 A LDO (e.g. AP7361C-33) instead of the buck.
- 12 DRC "drill 0.2 mm" items: thermal vias of the ESP32 footprint, same as the board already made.
