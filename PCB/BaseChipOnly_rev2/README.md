# BaseChipOnly — HW Rev 2.0

Base board of the Yggdrasill lamp: ESP32-WROOM-32U running WLED, 5 V input, drives the 9 leaf boards (`../Foglia`, 15 WS2812B each, wired in parallel). This is the second revision of `../BaseChipOnly` (rev 1.03, the board that was actually fabricated and brought up).

How the board works, power budget and WLED settings: [`docs/base-chiponly-pcb.md`](../../docs/base-chiponly-pcb.md).

> ## ⚠️ Limitation: verified on paper, not on a real board
>
> Rev 2.0 has **not been fabricated or assembled yet**. Everything below was checked with design-rule tools, file cross-checks and circuit simulation — nothing has been measured on hardware. Simulations use component models (TI's LM2596 model, generic MMBT3904/SS34/LED models) and assumptions (cable resistance, wire length to the leaves, capacitor derating) that may differ from reality. The firmware/boot of the ESP32 cannot be simulated: "it boots" means EN and IO0 reach the right levels at the right time.
>
> Before trusting it, build one board and follow the **first power-up procedure** in `docs/base-chiponly-pcb.md`, then test the auto-reset with `esptool.py flash_id`.

## Status

| | |
|---|---|
| Schematic | complete, ERC 0 errors |
| PCB | complete, DRC 0 errors, schematic ↔ PCB parity clean |
| Fab files | `Esportazione-2026-09-30/` (Gerbers, drill, BOM with MPNs, pick-and-place, assembly PDF with values, schematic PDF, 3D preview) |
| Fabricated | **no** |
| Tested on hardware | **no** |

## Tests performed (all theoretical)

| Test | Tool | Result |
|---|---|---|
| Electrical rules check | KiCad ERC | 0 errors |
| Design rules check + schematic parity | KiCad DRC `--schematic-parity` | 0 errors, 0 unconnected, 0 parity issues (12 known items: 0.2 mm thermal-via drills of the ESP32 footprint, same as rev 1.03) |
| Copper vs schematic | Gerber X2 pad attributes of the exported front copper | 120 / 120 pads on the right net |
| Pinout of every active part vs datasheet | netlist + datasheets | 0 mismatches (LM2596S-ADJ, USBLC6-2SC6, MMBT3904, diodes, polarised caps, connectors, ESP32) |
| ESP32 strapping pins | netlist review | IO0 pull-up + BOOT; IO2/IO12 floating (download mode OK, 3.3 V flash); IO5/IO15 internal pull-ups |
| Trace current capacity | IPC-2221, 1 oz outer layer, +10 °C | all power traces above their current (e.g. +5V bus 3 mm → 5.3 A for ~3.3 A) |
| Fab limits | JLCPCB rules | tracks ≥ 0.2 mm, vias 0.6/0.3, copper ≥ 1 mm from edge, silkscreen ≥ 0.8 mm / 0.15 mm |
| Mechanical / visual | KiCad 3D render | polarity marks, orientation, ≥ ~1 mm between parts in the regulator block, ≥ 1.1 mm from the ESP32 |
| Auto-reset (both esptool sequences) | ngspice | enters download mode; serial monitor does not reset the board |
| Power-on EN timing | ngspice | EN rises 13.7 ms after 3.3 V (spec ≥ 50 µs) |
| 3.3 V regulator: nominal, LEDs at 3 A, minimum input, start-up | ngspice + Texas Instruments LM2596 model (SNVMA65, credited in `LICENSE-NOTICES.md`) | 3.28 V, ≥ 3.21 V worst case; needs ≥ ~4.5 V at its input |
| Status LED current | ngspice | 4.6–6.7 mA |
| LED data line to 9 parallel leaves | ngspice | clean ~370/770 ns pulses with R5 = 100 Ω |

Re-run the checks with `./verifica.sh` (ERC + DRC/parity + fab export + Gerber cross-check). Simulations: `simulazioni/README.md` (run `simulazioni/models/get_lm2596_model.sh` once to fetch the TI model).

## Changes from rev 1.03

**Bugs fixed (all seen during the rev 1.03 bring-up)**

| Rev 1.03 | Rev 2.0 |
|---|---|
| D2 (SS34 catch diode) reversed — shorts the regulator switch node | correct polarity, silkscreen matches |
| D1 (status LED) reversed | correct polarity; GND via moved out of the pad (likely cause of the dark LED) |
| Auto-reset wired wrong: both emitters to GND — idle adapter held the ESP32 in reset, esptool could never enter download mode | standard cross-coupled DTR/RTS circuit, like ESP32 DevKit boards |
| No BOOT / RESET buttons | SW1 BOOT, SW2 RESET (C&K PTS810), centred on the top edge |
| L1 1008 inductor, no value — burned out | Bourns SRN6045TA-101M, 100 µH, Isat 1.33 A |
| Polyfuse 12 A in 0603 — protects nothing | Bourns MF-LSMF400/12X, 4 A hold, 2920 |
| U3 (USBLC6) GND pin unconnected — no ESD protection | GND connected, VBUS to +5V (ST reference circuit) |
| TVS: bidirectional symbol, SMF5.0A part on an SMA footprint | SMAJ5.0A, unidirectional, matches the footprint |
| Reference and Value swapped on the PCB, footprints not linked to the schematic | fixed: correct BOM / pick-and-place, Update-PCB-from-Schematic works |
| 12 ESP32 thermal vias with no net | tied to GND |
| Silkscreen typo "GDN" | "GND" |

**Improvements**

- COUT2 220 µF tantalum (Kyocera AVX TPSC227M006R0100) next to the 47 µF MLCC, for LM2596 loop stability.
- C4 100 nF → 1 µF (EN delay, Espressif guideline) — from the simulations.
- R5 470 Ω → 100 Ω (clean data pulses to the 9 parallel leaves) — from the simulations.
- Auto-reset transistors specified as MMBT3904 (no part number before).
- +3V3 traces 0.2 → 0.5–1.0 mm; SW node 1.2–1.5 mm.
- New layout: functional blocks, regulator with a short switching loop and room for hand soldering, solid GND plane on the back, no via-in-pad on GND, silkscreen to fab minimums, HW Rev 2.0 printed on the board.

**Unchanged on purpose:** board outline and mounting holes (the printed base and `TasselloFissaggioPCB.stl` still fit), J1 barrel jack, J2 terminal, J3 programming header (external USB-UART adapter, no USB-C), ESP32 position, C1, LED data on GPIO13.

## Known limits

- The LM2596 needs ≥ ~4.5 V at its input at 500 mA: use a good 5 V 4 A PSU with a short, thick cable and keep the WLED current limiter at 3000 mA.
- The USB-UART adapter must break out **DTR and RTS** at 3.3 V for the auto-reset; otherwise use BOOT/RESET.
- Button reachability inside the printed base not checked.

## Folder contents

| Path | What |
|---|---|
| `BaseChipOnly.kicad_pro/.kicad_sch/.kicad_pcb` | KiCad 9 project |
| `Esportazione-2026-09-30/` | fabrication files for rev 2.0 |
| `verifica.sh` | all automatic checks in one go |
| `simulazioni/` | ngspice decks, plots, results |
| `FIX_LOG.md` | session-by-session log of every change (Italian) |
| `BaseChipOnly-backups/fixpcb_2026-09-30.py`, `relayout-work/relayout.py`, `build.sh` | scripts that generated the PCB (record of every edit; their input boards live in the local, git-ignored `BaseChipOnly-backups/`) |
| `FileImpronte/` | ESP32-WROOM-32U symbol / footprint / 3D model |
