# 3D Models

FDM-printable parts for the Yggdrasill LED plant pot. The vase is now a **modular design** (base + lid + trunk/vase + 3 branches + leaves) with bayonet/snap-fit joints, replacing the earlier single-piece `VasoGiusto` body.

## Folder layout

- `3D/Vaso/` — Fusion 360 source of truth: STEP files (`Base.step`, `Coperchio.step`, `Vaso.step`, `Vaso_senza_texture.step`), the raw CAD-orientation STL exports, and `animazioni/` (assembly animation renders).
- `3D/STL_stampa/` — **print-ready** STLs, reoriented/optimized per part for the slicer. Use these for printing.

## Parts (`3D/STL_stampa/`)

| File | Description | Bed footprint (X×Y×Z mm) | Print notes |
|---|---|---|---|
| `Vaso.stl` | Trunk / vase body | 150×150×167 | Print **capovolto** (upside down) — cable slot must be on the print bed |
| `Base.stl` | Vase base — carries the PCB mounting points | 135×135×25 | Bayonet joint to lid — see clearances below. **Designed for `BaseChipOnly` only**, see PCB compatibility below |
| `Coperchio.stl` | Lid | 143×143×18 | Bayonet joint to base — see clearances below |
| `Ramo_1.stl` | Branch 1 | 101×129×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle |
| `Ramo_2.stl` | Branch 2 | 157×128×335 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle |
| `Ramo_3.stl` | Branch 3 | 99×153×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle |
| `Foglia.stl` | Decorative leaf, pairs with `PCB/Foglia/` | 83×27×135 | Some already printed — need **9 total** |

### Important print details

- **Rough/textured skin** on the branches applies **only** to the branch bodies — it must be **excluded** from the tenons ("codoli") and the square mounting boss ("cubotto"), or the joints won't fit.
- Fit clearances are simulated but **not yet verified empirically**: 0.2 mm/side on the bosses, 0.225 mm on the base. **Print small bayonet test rings for base + lid first**, before committing filament to the full-size parts — the snap-fit has only been checked in simulation.
- If a branch doesn't fit the print bed/angle in your slicer, a hidden joint/graft can be added to shorten it for printing in two pieces — re-export from Fusion if so.

## PCB compatibility

These files (`Base.stl`'s PCB mounting points, and `TasselloFissaggioPCB.stl`) are designed for the **`BaseChipOnly`** PCB variant only (see [PCB/BaseChipOnly](../PCB/BaseChipOnly)). Using `BaseDevKit` or `BaseUSB-C` instead requires redesigning the base's mounting points in Fusion to match that board's outline/holes before printing.

## Assembly animations

Lightweight renders for the README live in `3D/Vaso/animazioni/`:
- `yggdrasill_foglia_readme.gif` — leaf insertion
- `yggdrasill_rami_readme.gif` — branch assembly
- `yggdrasill_totale_readme.gif` — full assembly

Full-quality versions (`*.mp4`/non-`_readme` `.gif`) are also kept in the same folder for reference/editing.

For print settings and assembly notes see [docs/3d-printing.md](../docs/3d-printing.md).
