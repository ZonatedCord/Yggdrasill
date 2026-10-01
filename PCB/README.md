# PCB — Hardware Variants

KiCad 8 projects. ESP32 + WS2812B/SK6812 addressable LEDs.

| Folder | Description | Status | Gerbers |
|---|---|---|---|
| `BaseDevKit/` | ESP32 dev kit carrier | Active | `BaseDevKit/Esportazione/` |
| `BaseChipOnly/` | Bare ESP32-WROOM-32, compact — rev 1.03 as fabricated | Superseded by the next rev | `BaseChipOnly/Esportazione/` |
| `BaseChipOnly_rev2/` | BaseChipOnly HW Rev 2.0: all bring-up fixes + new layout (see its `README.md`) | Verified on paper (DRC/ERC/simulation), not yet fabricated | `BaseChipOnly_rev2/Esportazione-2026-09-30/` |
| `BaseUSB-C_rev0.1/` | USB-C power input | Early rev | — |
| `Foglia/` | Leaf-shaped decorative board | Active | `Foglia/Esportazione/` |
| `Impronte/` | Custom KiCad footprint library | Library | — |

For fabrication details and BOM see [docs/hardware.md](../docs/hardware.md).

How BaseChipOnly works: [docs/base-chiponly-pcb.md](../docs/base-chiponly-pcb.md). For the design review see [docs/hardware-reviews/base-chiponly-review.md](../docs/hardware-reviews/base-chiponly-review.md).
