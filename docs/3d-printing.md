# 3D Printing Guide

The vase is a **modular design**: base + lid + trunk/vase body + 3 branches + leaves, joined with bayonet/snap-fit joints. Fusion 360 source (STEP) lives in `3D/Vaso/`; print-ready STLs live in `3D/STL_stampa/`.

---

## Files (`3D/STL_stampa/`)

| File | Description | Bed footprint (X×Y×Z mm) | Status |
|---|---|---|---|
| `Vaso.stl` | Trunk / vase body | 150×150×167 | Print capovolto (upside down); cable slot on bed |
| `Base.stl` | Vase base — carries the PCB mounting points | 135×135×25 | Bayonet joint to lid — clearances unverified empirically. **Designed for `BaseChipOnly` only** — see PCB compatibility below |
| `Coperchio.stl` | Lid | 143×143×18 | Bayonet joint to base — clearances unverified empirically |
| `Ramo_1.stl` | Branch 1 | 101×129×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) |
| `Ramo_2.stl` | Branch 2 | 157×128×335 | Too tall for upright printing on a 256 mm-Z printer (P2S) |
| `Ramo_3.stl` | Branch 3 | 99×153×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) |
| `Foglia.stl` | Decorative leaf, pairs with `PCB/Foglia/` | 83×27×135 | Some already printed — need 9 total |

---

## Recommended settings

| Parameter | Value |
|---|---|
| Layer height | 0.2 mm |
| Infill | 20% (gyroid or honeycomb) |
| Material | PETG (preferred) or PLA |
| Supports | Not required for `Vaso`/`Base`/`Coperchio`; branches may need supports depending on chosen orientation |
| Perimeters | 3 |
| Print speed | 50–60 mm/s |
| Skin/texture | Rough/textured skin on branches only — **exclude** it from the tenons ("codoli") and the square mounting boss ("cubotto"), or the joints won't fit |

**PETG preferred** — better heat resistance near LEDs and less brittle than PLA for mechanical fit.

---

## Branches: orientation

`Ramo_1`, `Ramo_2`, and `Ramo_3` (up to 335 mm on their longest axis) exceed the printable Z-height of a 256 mm-build-volume printer (e.g. P2S) if printed upright. They must be printed lying down or at an angle. If a branch still doesn't fit the bed/angle in your slicer, a hidden joint/graft can be added in Fusion to split it into two printable pieces — re-export STLs if this is done.

---

## Bayonet joints: test before committing filament

The base/lid and branch-tenon bayonet/snap-fit joints have only been verified in simulation, not printed. **Print small bayonet test rings for base + lid before printing the full-size parts.** Starting clearances to validate empirically:

- Bosses ("cubotto"): 0.2 mm/side
- Base: 0.225 mm

If a test print doesn't fit, adjust the clearance parameter in Fusion and re-export the affected STL(s).

---

## PCB compatibility

The 3D files in this repo — specifically **`Base.stl`** (which carries the PCB mounting points) and **`TasselloFissaggioPCB.stl`** — are designed to match the **`BaseChipOnly`** PCB variant (see [docs/hardware.md](hardware.md)).

If you're building with a different variant (`BaseDevKit`, `BaseUSB-C`), the board outline and mounting-hole positions differ, so **the base's PCB mounting points need to be redesigned in Fusion** (and `TasselloFissaggioPCB.stl` re-checked/re-exported) before printing — they won't line up as-is.

---

## Assembly notes

The `Foglia` PCB is designed to fit inside / alongside the vase body. The LED strip routes through the internal channels of the trunk (`Vaso.stl`).

The `Foglia.stl` decorative leaf mirrors the `PCB/Foglia/` board shape. Some already printed; 9 total needed.

`TasselloFissaggioPCB.stl` (PCB mounting dowel, `3D/`) mounts the PCB inside the base (`Base.stl`), matching `BaseChipOnly`'s mounting holes. Fit against the current `Base.stl` design is still unconfirmed by a physical print — verify when assembling.

---

## Estimated print time

- **Vaso (trunk):** ~6–9 h (depends on printer speed)
- **Base:** ~1–2 h
- **Coperchio:** ~1 h
- **Ramo (each):** ~4–6 h (depends on orientation/supports)
- **Foglia (each, ×9):** ~1 h
