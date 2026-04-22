# Hardware — PCB Variants

All boards are designed in **KiCad 8**. ESP32 + addressable LEDs (WS2812B / SK6812).

---

## Variants

| Folder | Description | Power | Status | Gerbers |
|---|---|---|---|---|
| `BaseDevKit` | ESP32 dev kit carrier board | 5V barrel/USB | Active | `BaseDevKit/Esportazione/` |
| `BaseChipOnly` | Compact bare ESP32-WROOM-32 | 5V | Active (HW rev 1.03+) | `BaseChipOnly/Esportazione/` |
| `BaseUSB-C_rev0.1` | USB-C powered, rev 0.1 | 5V USB-C | Early rev | — |
| `Foglia` | Leaf-shaped decorative board | 5V | Active | `Foglia/Esportazione/` |
| `Impronte` | Custom KiCad footprint library | — | Library | — |

**Recommended for new builds:** `BaseChipOnly` HW rev 1.03+ (most compact, good Gerber coverage).

---

## BOM (generic)

| Component | Description | Notes |
|---|---|---|
| ESP32-WROOM-32 | Main microcontroller | WLED firmware |
| WS2812B / SK6812 | Addressable RGB LEDs | SK6812 supports RGBW |
| AMS1117-3.3 or LDO | 3.3V regulator | Per schematic |
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

- `BaseChipOnly` early revisions: via-on-pad short circuits on decoupling caps. Fixed in HW rev 1.03+. See `docs/hardware-reviews/base-chiponly-review.md` for full analysis.
