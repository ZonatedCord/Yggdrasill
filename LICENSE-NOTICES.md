# License Notices

Yggdrasill uses a dual-license structure. This file clarifies which license applies to each component.

---

## Hardware & 3D Models — CC BY-NC-SA 4.0

**Applies to:** `PCB/`, `3D/`, `docs/`

**Copyright (c) 2025 Marco Barlera**

Licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

You may share and adapt these files for **non-commercial** purposes, provided you give attribution and distribute derivatives under the same license.

Full terms: see [LICENSE](LICENSE).

---

## iOS App — GNU General Public License v3.0

**Applies to:** `WLED-iOS/`

The iOS app is a fork of [Moustachauve/WLED-iOS](https://github.com/Moustachauve/WLED-iOS), which is licensed under the GNU GPL v3. This license is **copyleft** and cannot be changed — any derivative must remain GPL v3.

Full terms: see `WLED-iOS/LICENSE`.

---

## Third-party simulation models

**Used by:** `PCB/BaseChipOnly_rev2/simulazioni/` (ngspice simulations of the BaseChipOnly Rev 2.0 board)

- **LM2596 transient model** — © 2015 Texas Instruments Incorporated, *LM2596_3P3 Unencrypted PSpice Transient Model* (SNVMA65), available from the [TI LM2596 product page](https://www.ti.com/product/LM2596). Provided by TI "as is" as a design aid. It is **not redistributed** in this repository: `simulazioni/models/get_lm2596_model.sh` downloads it from ti.com and derives the adjustable-output version used in the simulations.
- **MMBT3904 / SS34 / LED models** — generic public-domain SPICE parameter sets (2N3904 die model, typical Schottky and LED parameters), in `simulazioni/models/transistors.lib`.

---

## Commercial use

Commercial use of the hardware or 3D designs requires explicit written permission from the copyright holder.

Contact: **barleramarco05@gmail.com**
