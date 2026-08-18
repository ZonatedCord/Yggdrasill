# 3D Printing Guide

---

## Files

| File | Description | Status |
|---|---|---|
| `3D/VasoGiusto.stl` | Main vase body | WIP — top/bottom attach points fail, MB engraving needs rework |
| `3D/BaseVaso.stl` | Vase base | Ready |
| `3D/Foglia.stl` | Decorative leaf, pairs with `PCB/Foglia/` | Ready |
| `3D/TasselloFissaggioPCB.stl` | PCB mounting dowel | Ready |

---

## Recommended settings

| Parameter | Value |
|---|---|
| Layer height | 0.2 mm |
| Infill | 20% (gyroid or honeycomb) |
| Material | PETG (preferred) or PLA |
| Supports | Not required for body |
| Perimeters | 3 |
| Print speed | 50–60 mm/s |

**PETG preferred** — better heat resistance near LEDs and less brittle than PLA for mechanical fit.

---

## Assembly notes

The `Foglia` PCB is designed to fit inside / alongside the vase body. The LED strip routes through the internal channels of `VasoGiusto`. Secure PCB with `TasselloFissaggioPCB` or adhesive foam tape.

The `Foglia.stl` decorative leaf mirrors the `PCB/Foglia/` board shape.

---

## Estimated print time

- **VasoGiusto:** ~6–9 h (depends on printer speed)
- **BaseVaso:** ~1–2 h
- **Foglia:** ~1–2 h
- **TasselloFissaggioPCB:** <1 h
