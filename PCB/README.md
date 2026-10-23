# PCB — Hardware Variants

KiCad 9 projects (saved with KiCad 9; KiCad 8 cannot open them). ESP32 + WS2812B/SK6812 addressable LEDs.

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

## Regenerating the renders

```bash
python3 PCB/render/make_renders.py
```

The script regenerates top and bottom renders of BaseChipOnly Rev 1.03, Rev 2.0 and the leaf board Foglia (standard library only; it finds `kicad-cli` in the PATH or in `/Applications/KiCad/KiCad.app/Contents/MacOS`).

KiCad lacks some 3D models, so the script adds them to temporary copies of the boards: the ESP32 module and the barrel jack (both revisions) and, for Rev 2.0, the 2920 polyfuse and the PTS810 buttons as simplified hand-made models (`PCB/render/models/`). The board files are never modified.
