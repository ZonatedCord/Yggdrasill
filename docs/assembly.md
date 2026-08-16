# Assembly Guide

> Work in progress.

---

## Steps (draft)

1. Print `VasoGiusto.stl`, `BaseVaso.stl`, `Foglia.stl`, `TasselloFissaggioPCB.stl` — see [3d-printing.md](3d-printing.md) for settings
2. Fabricate PCB — see [hardware.md](hardware.md) for Gerber files and fab notes
3. Flash WLED firmware to ESP32 via USB
4. Solder LED strip to PCB (DATA, +5V, GND)
5. Route LED strip through vase body channels
6. Mount PCB in base with `TasselloFissaggioPCB` or foam tape
7. Connect power (5V, 2A minimum)
8. Install iOS app — see [ios-app.md](ios-app.md)
9. App auto-discovers device via mDNS

---

## Power requirements

- LEDs: ~60 mA per LED at full white (WS2812B)
- Total depends on LED count per build
- Minimum recommended PSU: **5V 2A** (10W)
