# Yggdrasill

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Hardware%2F3D-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![iOS App: GPL v3](https://img.shields.io/badge/iOS%20App-GPL%20v3-blue.svg)](WLED-iOS/LICENSE)
[![Platform: iOS 26+](https://img.shields.io/badge/iOS-26%2B-black?logo=apple)](docs/ios-app.md)
[![Hardware: ESP32](https://img.shields.io/badge/MCU-ESP32-red)](docs/hardware.md)

**Smart LED plant pot** — custom ESP32 PCB, WS2812B / SK6812 addressable LEDs, WLED firmware, 3D-printed vase, and a native iOS app with Apple's Liquid Glass design.

---

<!-- Hero image placeholder — add docs/images/hero.png -->

---

## Three pillars

| | Component | Description |
|---|---|---|
| **Hardware** | ESP32 PCB (`PCB/`) | 4 board variants in KiCad. LED strip driver + power. |
| **iOS App** | WLED Native (`WLED-iOS/`) | Liquid Glass redesign (iOS 26). mDNS discovery + WebSocket control. |
| **3D** | Printable vase (`3D/`) | Body, base, leaf & mount ready. FDM-printable in PETG or PLA. |

---

## Status

| Component | Status |
|---|---|
| BaseDevKit PCB | Active |
| BaseChipOnly PCB (rev 1.03+) | Active — **recommended** |
| BaseUSB-C rev0.1 PCB | Early revision |
| Foglia PCB | Active |
| Vase body (VasoGiusto.stl) | Ready |
| Vase base (BaseVaso.stl) | Ready |
| Leaf (Foglia.stl) | Ready |
| PCB mount (TasselloFissaggioPCB.stl) | Ready |
| iOS app (Liquid Glass) | In development |

---

## Repository structure

```
Yggdrasill/
├── PCB/               KiCad projects — 4 board variants + footprint library
├── 3D/                STL files for FDM printing
├── WLED-iOS/          iOS app (Liquid Glass, GPL v3) — future git submodule
├── docs/              Hardware, iOS, 3D, and assembly documentation
│   └── hardware-reviews/  PCB analysis notes
├── LICENSE            CC BY-NC-SA 4.0 (hardware + 3D)
├── LICENSE-NOTICES.md Dual-license clarification
├── CHANGELOG.md
└── CONTRIBUTING.md
```

---

## Quick start

### iOS app

Requires **Xcode 16+** and an **iOS 26+** device or simulator.

```bash
git clone --recurse-submodules https://github.com/YOUR/Yggdrasill
open WLED-iOS/wled.xcodeproj
```

> Note: `WLED-iOS/` submodule link is set up once the fork is published on GitHub.

### Hardware

Gerber files are in `PCB/<variant>/Esportazione/`. Upload to JLCPCB or PCBWay.

Open the KiCad project in **KiCad 8+** for schematic / PCB editing.

See [docs/hardware.md](docs/hardware.md) for full variant table and BOM.

### 3D printing

See [docs/3d-printing.md](docs/3d-printing.md) for settings. PETG recommended, 0.2 mm layers.

---

## Documentation

- [Hardware variants & BOM](docs/hardware.md)
- [iOS app architecture & Liquid Glass](docs/ios-app.md)
- [3D printing guide](docs/3d-printing.md)
- [Assembly guide](docs/assembly.md)
- [BaseChipOnly hardware review](docs/hardware-reviews/base-chiponly-review.md)

---

## License

### Hardware & 3D Models (`PCB/`, `3D/`, `docs/`)

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**
Copyright (c) 2025 Marco Barlera

Free for personal and maker use. Commercial use requires explicit written permission.
See [LICENSE](LICENSE) · [creativecommons.org/licenses/by-nc-sa/4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### iOS App (`WLED-iOS/`)

**GNU General Public License v3.0** — inherited from [Moustachauve/WLED-iOS](https://github.com/Moustachauve/WLED-iOS). Copyleft; cannot be changed.
See [WLED-iOS/LICENSE](WLED-iOS/LICENSE)

See [LICENSE-NOTICES.md](LICENSE-NOTICES.md) for full dual-license details.

---

## Author

**Marco Barlera** — barleramarco2@gmail.com

Commercial licensing inquiries: contact via email.
