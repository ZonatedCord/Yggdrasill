# 3D Printing Guide

---

## Files

| File | Description | Status |
|---|---|---|
| `3D/VASO_Corpo.stl` | Main vase body | Ready |
| `3D/VASO-tappo_DaRivedere.stl` | Vase cap | WIP — needs revision |

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

The `Foglia` PCB is designed to fit inside / alongside the vase body. The LED strip routes through the internal channels of `VASO_Corpo`. Secure PCB with M2 screws or adhesive foam tape.

The cap (`VASO-tappo`) is under revision — current STL may need scaling or support adjustment before printing.

---

## Estimated print time

- **VASO_Corpo:** ~6–9 h (depends on printer speed)
- **VASO-tappo:** ~1–2 h
