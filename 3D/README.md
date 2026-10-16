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
| `Ramo_1.stl` | Branch 1 | 101×129×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle — **printed, OK**  |
| `Ramo_2.stl` | Branch 2 | 157×128×335 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle — **printing in progress**  |
| `Ramo_3.stl` | Branch 3 | 99×153×324 | Too tall for upright printing on a 256 mm-Z printer (P2S) — must lie down or print at an angle |
| `Foglia.stl` | Decorative leaf, pairs with `PCB/Foglia/` | 83×27×135 | Printed (9 total) |

## Print status (first physical print, Oct 2026)

Vase body, base and lid were printed in **PLA on a Bambu Lab P2S** (smooth walls, no fuzzy skin). The three parts fit together: the bayonet/snap-fit joints were very tight at first and went together after the mating surfaces were smoothed. Clearances are therefore on the tight side (a small increase would avoid the manual smoothing). The fit of `TasselloFissaggioPCB.stl` and the PCB in the base is still unverified.

Leaves (`Foglia`) are already printed; Branch 1 is printed and OK, branch 2 is printing, branch 3 is still to do:

| Part | Nozzle | Filament |
|---|---|---|
| Vase, branches | 0.4 mm | Bambu Lab official PLA |
| Leaves (`Foglia`) | 0.4 mm | Bambu Lab PLA, white (same as the vase) |
| Base | 0.4 mm | Any colour (not visible) |
| Lid (`Coperchio`) | 0.4 mm | Bambu Lab PLA, Bambu green |

### Print files and optimisation

- **Branches:** `3D/STL_stampa/Rami.3mf` is the plate exactly as it was printed (orientation, supports, fuzzy skin excluded from the joints). It is a working starting point, **feel free to optimise it** (orientation, supports, settings).
- **Vase body and lid:** rotate them **180°** compared with the supplied STL orientation to save on supports.
- **Leaves (`Foglia`):** no supports needed.

### Important print details

- **Rough/textured skin** on the branches applies **only** to the branch bodies — it must be **excluded** from the tenons ("codoli") and the square mounting boss ("cubotto"), or the joints won't fit.
- Fit clearances: 0.2 mm/side on the bosses, 0.225 mm on the base. Base + lid + vase body were printed in PLA and fit (tight at first, see print status above). Branch joints are still unverified.
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
