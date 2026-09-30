# Design Review — BaseChipOnly

Original review: 2026-03-28 (automated). **Rewritten 2026-09-30** after the bring-up proved its main finding false.

---

## Retraction: the "via-on-pad short circuits" do not exist

The 2026-03-28 version of this document named vias on C2, C3, COUT1, Rbot1 and Rtop1 as the "SHORT-CIRCUIT ROOT CAUSE", claiming each GND via had landed on the supply pad. **That is wrong.** Every one of those vias sits in its pad deliberately and carries the *same* net as the pad, to drop to the B.Cu ground plane.

Disproved two independent ways during the 2026-07/08 bring-up:

- The bare board measures no short between any rail and GND.
- The X2 attributes in the fabricated `F_Cu.gbr` (`%TO.P,comp,pin%` / `%TO.N,net%`) show pad and via on the same net at every flagged location — e.g. `COUT1 pin 2 net=GND`, and the via there is also `GND`.

The false finding came from hand-computing pad positions with the wrong rotation sign, which mirrors every pad about its footprint centre and pairs each via with the opposite pad. The error was self-consistent, which is why it looked convincing. Lesson: never derive pad-to-net mapping from footprint rotation math — read it from Gerber X2 attributes or `kicad-cli`.

The short that actually happened on the first assembled board was a **solder bridge between ESP32 module pins 1 (GND) and 2 (3V3)** — an assembly defect, not a design one. See `base-chiponly-fixes.md`.

---

## Findings that were valid, and their status

All of the following are fixed in the KiCad sources in `PCB/BaseChipOnly copia MCP/` (2026-09-30). Full log: `PCB/BaseChipOnly copia MCP/FIX_LOG.md`.

| Finding | Status |
|---|---|
| U3 (USBLC6-2SC6) GND pin unconnected | Fixed — pin 2 on GND. VBUS (pin 5) now on +5V as well, so the clamp has its rail reference. |
| Polyfuse 12 A protects nothing | Fixed — 1.5 A hold / 3 A trip, Bourns MF-MSMF150/8X, 1812. The old 0603 footprint could not hold any realistic PTC. **Note:** the polyfuse also feeds the LED strip through J2, so the hold current must cover the strip's real draw. |
| +3V3 traces 0.2 mm | Fixed — +3V3 tracks widened to 0.5 mm. |
| Reference/Value swapped in the PCB | Fixed — Reference on F.Silkscreen, Value on F.Fab. Footprints are linked to their schematic symbols again, so BOM, pick-and-place and Update-PCB-from-Schematic work. |
| SMF5.0A on a bidirectional TVS symbol | Fixed — replaced with SMAJ5.0A (unidirectional, SMA package). SMF5.0A is an SOD-123F part and never matched the D_SMA footprint anyway. |

The Vout note in the old review used Vref = 1.285 V. The LM2596-ADJ reference is **1.23 V**, so Rtop = 2.0 k / Rbot = 1.2 k gives ≈ 3.28 V. No change needed.

---

## Defects found later (bring-up), also fixed

See `base-chiponly-fixes.md` for evidence. Fixed in the sources on 2026-09-30:

- D2 (SS34 catch diode) reversed
- D1 (status LED) reversed
- Auto-reset transistors wired with both emitters to GND — now the standard cross-coupled DTR/RTS circuit
- No BOOT/RESET buttons — SW1 (BOOT, IO0→GND) and SW2 (RESET, EN→GND) added
- L1 1008 inductor unable to carry the current — now Bourns SRN6045TA-101M (100 µH, Isat 1.33 A)
- COUT1 47 µF MLCC alone on the LM2596 output — COUT2 220 µF tantalum added
