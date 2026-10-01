# Hardware — PCB Variants

All boards are designed in **KiCad 8**. ESP32 + addressable LEDs (WS2812B / SK6812).

---

## Variants

| Folder | Description | Power | Status | Gerbers |
|---|---|---|---|---|
| `BaseDevKit` | ESP32 dev kit carrier board | 5V barrel/USB | Active | `BaseDevKit/Esportazione/` |
| `BaseChipOnly` | Compact bare ESP32-WROOM-32 | 5V | Rev 1.03 fabricated | `BaseChipOnly/Esportazione/` |
| `BaseChipOnly_rev2` | BaseChipOnly HW Rev 2.0: all fixes + new layout | 5V | Verified on paper only, not yet fabricated | `BaseChipOnly_rev2/Esportazione-2026-09-30/` |
| `BaseUSB-C_rev0.1` | USB-C powered, rev 0.1 | 5V USB-C | Early rev | — |
| `Foglia` | Leaf-shaped decorative board | 5V | Active | `Foglia/Esportazione/` |
| `Impronte` | Custom KiCad footprint library | — | Library | — |

**Recommended for new builds:** `BaseChipOnly` HW Rev 2.0 in `PCB/BaseChipOnly_rev2/` (see its [README](../PCB/BaseChipOnly_rev2/README.md) for the tests done and the not-yet-tested-on-hardware caveat) (all bring-up fixes, BOOT/RESET buttons, working auto-reset). How it works, power budget and WLED settings: [base-chiponly-pcb.md](base-chiponly-pcb.md).

---

## BOM (generic)

| Component | Description | Notes |
|---|---|---|
| ESP32-WROOM-32 | Main microcontroller | WLED firmware |
| WS2812B / SK6812 | Addressable RGB LEDs | SK6812 supports RGBW |
| AMS1117-3.3 or LDO | 3.3V regulator | Per schematic (BaseChipOnly uses an LM2596-ADJ buck) |
| 100nF + 47µF decoupling caps | Power filtering | See schematic |
| USB-C connector | Power input (BaseUSB-C only) | GCT USB4135 or similar |

For detailed BOM per variant, open the KiCad schematic.

---

## Fabrication notes

- **Layer count:** 2 layers
- **Min trace:** 0.2 mm
- **Min drill:** 0.3 mm
- **Surface finish:** HASL or ENIG
- **Thickness:** 1.6 mm

Upload the `Esportazione/` folder contents (or zip) to JLCPCB / PCBWay directly.

---

## Known issues

- `BaseChipOnly` as fabricated: D1 and D2 reversed, auto-reset non-functional, no BOOT/RESET buttons, undersized L1. All fixed in the sources in `PCB/BaseChipOnly_rev2/` (2026-09-30), not yet re-fabricated — see `docs/hardware-reviews/base-chiponly-fixes.md`. The older "via-on-pad short circuit" finding was false; see `docs/hardware-reviews/base-chiponly-review.md`.
