# Assembly Guide

> Work in progress.

---

## Steps (draft)

1. Print the modular parts from `3D/STL_stampa/`: `Vaso.stl`, `Base.stl`, `Coperchio.stl`, `Ramo_1.stl`, `Ramo_2.stl`, `Ramo_3.stl` — see [3d-printing.md](3d-printing.md) for settings and orientation notes. `Foglia.stl` (×9): some already printed.
2. **Print bayonet test rings for base + lid first** and confirm the snap-fit before committing filament to the full-size `Base.stl`/`Coperchio.stl` — the joint has only been verified in simulation
3. Fabricate PCB — see [hardware.md](hardware.md) for Gerber files and fab notes
4. Flash WLED firmware to ESP32 via USB
5. Solder LED strip to PCB (DATA, +5V, GND)
6. Route LED strip through the trunk (`Vaso.stl`) internal channels
7. Assemble base → trunk → branches (bayonet joints) → leaves (9×) → lid, per the assembly animations in `3D/Vaso/animazioni/`
8. Mount PCB in base with `TasselloFissaggioPCB.stl` (fit against the new `Base.stl` still unconfirmed — see [3d-printing.md](3d-printing.md)) or foam tape
9. Connect power (5V, 2A minimum)
10. Install iOS app — see [ios-app.md](ios-app.md)
11. App auto-discovers device via mDNS

---

## Power requirements

- LEDs: ~60 mA per LED at full white (WS2812B)
- Total depends on LED count per build
- Minimum recommended PSU: **5V 2A** (10W)
