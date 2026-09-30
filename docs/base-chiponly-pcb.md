# BaseChipOnly — how the board works

Base board of the Yggdrasill lamp: an ESP32-WROOM-32U running WLED drives the 9 leaf boards (`PCB/Foglia`). Sources: `PCB/BaseChipOnly copia MCP/` (fixed 2026-09-30, see `FIX_LOG.md` there).

## Block diagram

```
5V PSU ─► J1 barrel jack ─► Polyfuse1 ─► +5V bus ─┬─► J2 terminal (VIN/GND) ─► 9 leaves in parallel
                                                   ├─► C1 1000µF bulk, C2 100nF, D_TVS1 SMAJ5.0A (clamp)
                                                   ├─► R0 + D1  (power-on LED)
                                                   └─► U4 LM2596-ADJ buck ─► L1 100µH ─► +3V3 ─► ESP32 (U1)
ESP32 GPIO13 ─► R5 470Ω ─► U3 USBLC6 (ESD) ─► J2 "Data" ─► DIN of the first WS2812B on every leaf
J3 (GND 3V3 TX0 RX0 DTR RTS) ─► USB-UART adapter; DTR/RTS drive the auto-reset transistors
SW1 BOOT (IO0→GND), SW2 RESET (EN→GND)
```

## Blocks

**Power input.** J1 (GCT DCJ200-10, rated 5 A) → polyfuse → +5V. The +5V rail feeds the LEDs directly; only the ESP32 goes through the buck. D_TVS1 clamps spikes on +5V, C1 buffers the LED current steps.

**3.3 V regulator.** LM2596-ADJ, 150 kHz buck. Vout = 1.23 V × (1 + Rtop1/Rbot1) = 1.23 × (1 + 2.0k/1.2k) ≈ 3.28 V. D2 (SS34) is the catch diode (cathode on SW). L1 Bourns SRN6045TA-101M (Isat 1.33 A). COUT1 47 µF MLCC + COUT2 220 µF tantalum: the tantalum's ESR keeps the LM2596 loop stable. With only 5 V in, the LM2596 runs near dropout — fine for the ESP32's ~0.5 A peaks.

**ESP32.** U1 WROOM-32U (external antenna via U.FL). LED data is **GPIO13** = module pin 16 (set 13 in WLED, not 16).

**Programming / auto-reset.** J3 carries TX0/RX0/DTR/RTS. Two NPN transistors in the standard cross-coupled arrangement: DTR=1,RTS=0 → EN low (reset); DTR=0,RTS=1 → IO0 low (bootloader). esptool drives this sequence automatically. R3/R4 pull IO0/EN up, C4 delays EN at power-on. BOOT/RESET buttons are the manual fallback (hold BOOT, tap RESET).

**LED data.** R5 damps ringing on the long wires to the leaves; U3 protects the ESP32 pin from ESD coming back up the leaf wiring.

**Status LED.** D1 via R0 470 Ω from +5V → about 4–6 mA. That is **not** too much current (0805 LEDs take 20 mA). D1 stays dark on the first assembled board for a reason still undiagnosed: check that R0 is fitted and reads 470 Ω, then measure the LED-anode pad against GND with the board on (≈5 V = no current; ≈2–3 V = current flowing, LED faulty). On the old layout the LED's GND pad has a via in the middle of the pad that sucks solder into the ground plane — a dry joint there is a likely cause. The new files move every GND via beside its pad.

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

## Layout (re-done 2026-09-30)

Board outline, the four mounting holes, J1, J2, J3, U1 and C1 are where they always were, so the printed base and the PCB mount (`TasselloFissaggioPCB.stl`) still fit. Everything else was re-placed in functional blocks:

- **Left column — 3.3 V buck.** U4 with its pins pointing up; directly above the pins D2 (catch diode), L1 and the output caps COUT1/COUT2/C3, so the switching loop U4 OUT → D2 → GND is a few millimetres long. Rtop1/Rbot1 sit next to the FB pin. CIN1/C2 are right at the VIN pin.
- **Bottom left — input.** Jack → polyfuse (2920) → a 3 mm +5V bus that runs across the board to C1 and up to the regulator, with a 2 mm branch to J2. TVS and the power LED hang off the bus.
- **Under the ESP32 — auto-reset.** R1–R4, C4, the two transistors, then R5/U3 feeding J2 "Data".
- **Top edge — RESET and BOOT buttons**, next to the programming header (silkscreen labels beside them).
- **Back — solid GND plane.** Only a few short signal jumpers cross it (DTR/RTS lanes from J3, EN and IO0 under the module, IO13). Every GND pad has its via beside the pad, not in it (easier hand soldering, no solder wicking — see the D1 note above).
- The credit text stays on the front, right edge; the logo stays on the back.

Rebuild recipe (deterministic, all routing by hand): `PCB/BaseChipOnly copia MCP/BaseChipOnly-backups/relayout-work/relayout.py` + `build.sh`.

## Known limits

- The ESP32 drives 3.3 V data into WS2812B powered at 5 V (spec wants ≥3.5 V). It works in practice on this build; if leaves flicker, the fix is a 74AHCT1G125 buffer powered from +5V between GPIO13 and R5.
- 12 DRC "drill 0.2 mm" items: thermal vias of the ESP32 footprint, same as the board already made.
