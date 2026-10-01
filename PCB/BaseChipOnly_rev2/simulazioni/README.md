# BaseChipOnly — circuit simulations (2026-09-30)

SPICE simulations of every analog block of the base board, run with **ngspice 47** (`brew install ngspice`) in PSpice-compatibility mode (`.spiceinit`). Component values and nets are taken from `../BaseChipOnly.kicad_sch`.

What a SPICE simulation can and cannot tell you: it checks voltages, currents and timing of the circuit around the ESP32. It does **not** run the ESP32 firmware — "does the chip boot" is answered by checking that EN and IO0 reach the right levels at the right time, which is exactly what the ESP32 needs to boot or enter download mode.

## Results

| # | Block | Result | Verdict |
|---|---|---|---|
| 01 | **Auto-reset** (esptool UnixTight + Classic sequences) | EN pulled to 0.07 V during reset; when EN is released, IO0 is at 0.07 V and stays low for 36–48 ms after EN crosses 2.475 V → **download mode**. Serial monitor opening with DTR=RTS=1 → no reset. | ✅ works |
| 01b | Auto-reset **as fabricated (rev 1.03)** | Idle adapter holds EN at 0.04 V (chip stuck in reset); the esptool sequence never pulls EN low. Explains the bring-up ("disconnect DTR/RTS or it won't work"). | ❌ confirmed broken |
| 01c | Auto-reset with **C4 = 1 µF** | Same as 01, EN crosses the threshold 13.7 ms after release, IO0 still low for another 36 ms. | ✅ works |
| 02 | **LM2596 buck**, nominal 5 V in, ESP32 load 60/250/500 mA | +3V3 = **3.280 V**, ripple 0.8 mV p-p, minimum 3.263 V during 500 mA TX bursts, L1 peak 0.6 A in steady state. | ✅ |
| 02b | Buck, **LEDs drawing 3 A** from +5V (WLED limiter) + real switch saturation + 500 mA TX | +5V sags to 4.51 V (0.15 Ω cable+jack+fuse), +3V3 stays 3.28 V, **minimum 3.21 V** during TX. | ✅ small margin |
| 02c | Buck **minimum input voltage** at 500 mA | Regulates down to **~4.5 V** in; 4.3 V in → 3.11 V out; below ~4.2 V the ESP32 minimum (3.0 V) is lost. | ⚠️ see note |
| 02d | Buck start-up with a real adapter (5 V in 10 ms) | L1 peak **0.86 A** (< Isat 1.33 A), +3V3 in 6.9 ms, overshoot 3.43 V (< 3.6 V max). With a 1 ms edge (hot-plugging into a live PSU) L1 briefly reaches ~3 A, limited by the LM2596 current limit. | ✅ |
| 03 | **Power-on**, EN delay vs +3V3 (C4 100 nF) | EN crosses 2.475 V 1.05 ms after +3V3 is up (adapter unplugged). With the adapter connected and idle, EN is back-fed to 1.7 V before power and rises only **65 µs** after +3V3 (spec ≥ 50 µs). | ⚠️ marginal |
| 03b | Power-on with **C4 = 1 µF** | EN 13.7 ms after +3V3 (3.3 ms with the adapter connected). IO0 high → normal boot. | ✅ |
| 04 | **Status LED** D1 (R0 470 Ω from 5 V) | 6.7 mA (red) / 4.6 mA (white/blue). Not too much current; D1 being dark on the rev 1.03 board is not an electrical-design problem. | ✅ |
| 05 | **LED data line** to 9 leaves in parallel | With R5 = 470 Ω the pulses seen at a leaf (2.5 V threshold) shrink: 0.3 m wires → "0" ≈ 265 ns, "1" ≈ 670 ns; 0.6 m → "0" ≈ 190 ns, "1" ≈ 600 ns (WS2812B limits: T0H ≥ 220 ns, T1H ≥ 580 ns). With **R5 = 100 Ω**: "0" 350–370 ns, "1" 750–770 ns, no ringing. | ⚠️ → fixed with 100 Ω |

## Changes made because of these results

- **C4 100 nF → 1 µF** (EN RC = 10 kΩ + 1 µF, Espressif hardware design guidelines). Removes the 65 µs power-on margin; auto-reset re-verified (01c).
- **R5 470 Ω → 100 Ω** (LED data series resistor). Restores full-width pulses at the leaves.
- **IO0_CTRL1 / EN_CTRL1 = MMBT3904** — the transistors had no part number at all.

Same footprints: only values change, the layout is untouched.

## Note on the LM2596 at 5 V input (02c)

The LM2596 switch is a Darlington with ~1 V saturation, so with 5 V in it needs **≥ ~4.5 V at its VIN pin** to hold 3.3 V at 500 mA. Everything between the PSU and U4 eats into that: PSU tolerance, cable, barrel jack, polyfuse. With the LEDs at 3 A and 0.15 Ω of path resistance it still works (02b), but a long thin cable or a sagging PSU would drop the ESP32 into brown-out. Practical rules:

- use a decent 5 V 4 A supply (a 5.1–5.2 V one is even better) with a short, thick cable;
- keep the WLED current limiter on (3000 mA).

For a future revision, a 1 A LDO (e.g. AP7361C-33, ~0.36 V dropout) would be a better fit than a buck at 5 V → 3.3 V: at ~250 mA average the LDO dissipates < 0.5 W.

## Files

| File | What |
|---|---|
| `01_autoreset.cir`, `01b_…rev103.cir`, `01c_…C4_1u.cir` | auto-reset (new circuit / as fabricated / C4 1 µF) |
| `02_buck_nominal.cir`, `02b_…ledload_vsat.cir`, `02c_…dropout.cir`, `02d_…slowramp.cir` | LM2596 buck (share `buck_common.inc`) |
| `03_poweron.cir`, `03b_poweron_C4_1u.cir` | power-on EN delay (uses `v33.inc` = +3V3 start-up from 02) |
| `04_status_led.cir` | status LED current |
| `05_dataline.cir` | LED data line to 9 leaves |
| `models/get_lm2596_model.sh` | downloads TI's LM2596_3P3 unencrypted transient model (SNVMA65) and derives `models/LM2596_ADJ.lib` (internal divider removed → ADJ version; `LM2596_ADJ_VSAT` adds the datasheet switch saturation). The TI file itself is not stored in the repo |
| `models/transistors.lib` | MMBT3904, SS34, LED models |
| `grafici/*.png` | plots (from `plot.py`) |

## Credits

The LM2596 regulator simulations use Texas Instruments' **LM2596_3P3 Unencrypted PSpice Transient Model** (SNVMA65, © 2015 Texas Instruments Incorporated, [ti.com/product/LM2596](https://www.ti.com/product/LM2596)). The model is not stored in this repository; `models/get_lm2596_model.sh` downloads it from TI and turns it into the adjustable version (internal divider removed, optional switch-saturation drop added). See also `LICENSE-NOTICES.md`.

## Re-run

```sh
cd "PCB/BaseChipOnly_rev2/simulazioni"
models/get_lm2596_model.sh                    # once: downloads TI's model and builds models/LM2596_ADJ.lib
for f in 0*.cir; do ngspice -b "$f"; done     # buck decks take ~4-5 min each
python3 plot.py                               # needs matplotlib + numpy
```

Assumptions worth knowing: COUT1 (47 µF 0805 X5R) derated to 20 µF at 3.3 V bias; 0.15 Ω from PSU to the +5V rail; leaf wires 0.3/0.6 m at ~50 pF/m, WS2812B input ~10 pF; USB-UART adapter outputs 3.3 V with 50 Ω.
