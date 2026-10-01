# Assembly Guide

> Work in progress.

> **PCB compatibility:** the STL files here (base mounting points + `TasselloFissaggioPCB.stl`) are designed for the **`BaseChipOnly`** PCB variant. Other variants (`BaseDevKit`, `BaseUSB-C`) need the base's PCB mounting points redesigned first — see [3d-printing.md](3d-printing.md#pcb-compatibility).

---

## Steps (draft)

1. Print the modular parts from `3D/STL_stampa/`: `Vaso.stl`, `Base.stl`, `Coperchio.stl`, `Ramo_1.stl`, `Ramo_2.stl`, `Ramo_3.stl` — see [3d-printing.md](3d-printing.md) for settings and orientation notes. `Foglia.stl` (×9): some already printed.
2. **Print bayonet test rings for base + lid first** and confirm the snap-fit before committing filament to the full-size `Base.stl`/`Coperchio.stl` — the joint has only been verified in simulation
3. Fabricate PCB — see [hardware.md](hardware.md) for Gerber files and fab notes (`BaseChipOnly` matches the current mounting points as-is)
4. Flash WLED firmware to ESP32 via a USB-UART adapter on J3 (GND, TX0, RX0, DTR, RTS; leave 3V3 unconnected and power from the barrel jack). The next BaseChipOnly rev resets into the bootloader automatically; if not, hold **BOOT**, tap **RESET**, release BOOT. Rev 1.03 boards need the manual procedure in [base-chiponly-fixes.md](hardware-reviews/base-chiponly-fixes.md#flashing-procedure-current-board). In WLED: data pin **GPIO13**, **15 LEDs**
5. Solder LED strip to PCB (DATA, +5V, GND)
6. Route LED strip through the trunk (`Vaso.stl`) internal channels
7. Assemble base → trunk → branches (bayonet joints) → leaves (9×) → lid, per the assembly animations in `3D/Vaso/animazioni/`
8. Mount PCB inside the base (`Base.stl`) with `TasselloFissaggioPCB.stl` — fit against the current `Base.stl` design still unconfirmed by a physical print, see [3d-printing.md](3d-printing.md)
9. Connect power: 5 V, **4 A** recommended — see power requirements below
10. Install iOS app — see [ios-app.md](ios-app.md)
11. App auto-discovers device via mDNS

---

## Power requirements

- Leaves: 9 × `Foglia_Led`, 15 WS2812B each, wired in parallel on the same data line = **135 LEDs**
- Worst case at full white: ~55 mA per LED → **~7.4 A**, more than the barrel jack (5 A) allows
- Recommended PSU: **5 V 4 A** (20 W; 5.1–5.2 V output is even better) on a **short, thick cable**, with WLED → LED Preferences → Automatic Brightness Limiter set to **3000 mA** (LED current 55 mA)
- With a smaller PSU, set the limiter to ~80 % of its rating
- The board's polyfuse (4 A hold) protects against wiring faults, not against running the LEDs without the limiter
- Why the cable matters: the 3.3 V regulator needs ≥ ~4.5 V at its input; at 3 A of LED current every 0.1 Ω of cable costs 0.3 V (simulated, see `PCB/BaseChipOnly_rev2/simulazioni/`)

Details: [base-chiponly-pcb.md](base-chiponly-pcb.md).
