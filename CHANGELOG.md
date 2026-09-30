# Changelog

All notable changes to Yggdrasill are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Repository structure, docs/, CHANGELOG, CONTRIBUTING, LICENSE-NOTICES
- iOS app Liquid Glass redesign (iOS 26 material system)
- iOS app fork published publicly: [ZonatedCord/WLED-iOS](https://github.com/ZonatedCord/WLED-iOS) (`origin`; `upstream` = Moustachauve/WLED-iOS), embedded as a git submodule tracking the `liquid-glass-redesign` branch
- 3D: vase redesigned as a modular assembly (base + lid + trunk + 3 branches + leaves) with bayonet/snap-fit joints, replacing the single-piece `VasoGiusto` body; Fusion 360 source in `3D/Vaso/`, print-ready STLs in `3D/STL_stampa/`
- 3D: assembly animation renders (leaf insertion, branch assembly, full assembly) in `3D/Vaso/animazioni/`
- Hardware: BaseChipOnly next revision in `PCB/BaseChipOnly copia MCP/` — D1/D2 polarity fixed, cross-coupled DTR/RTS auto-reset, BOOT/RESET buttons, L1 SRN6045TA-101M, polyfuse MF-LSMF400/12X (4 A), SMAJ5.0A TVS, 220 µF output cap, USBLC6 GND/VBUS; new tidy layout with solid GND plane; fab files in `Esportazione-2026-09-30/` (not yet fabricated)
- Docs: `docs/base-chiponly-pcb.md` — how the board works, power budget for the 9 leaves, WLED settings

### Changed
- Docs (`README.md`, `3D/README.md`, `docs/3d-printing.md`, `docs/assembly.md`) updated to reflect the modular vase design
- Docs: power requirements corrected for 135 LEDs (5 V 4 A PSU + WLED limiter 3000 mA, was "5 V 2 A")

### Fixed
- Docs: retracted the false BaseChipOnly "via-on-pad short circuit" finding (`base-chiponly-review.md`, `hardware.md`, `CONTEXT.md`)

### Removed
- `3D/VasoGiusto.stl`, `3D/BaseVaso.stl`, old `3D/Foglia.stl`/`Foglia.3mf` — superseded by the modular design's `3D/STL_stampa/` parts
- Intermediate animation frame dumps (~400 MB of PNGs) and the earlier "montaggio" animation take, superseded by the current renders in `3D/Vaso/animazioni/`

---

## [0.1.0] - 2026-04-23

### Added
- Hardware: BaseDevKit, BaseChipOnly, BaseUSB-C rev0.1, Foglia PCB variants (KiCad)
- 3D: vase body (VASO_Corpo.stl), cap WIP (VASO-tappo_DaRivedere.stl)
- iOS app: fork of Moustachauve/WLED-iOS with WLED JSON API + WebSocket
- Dual license: CC BY-NC-SA 4.0 (hardware/3D) + GPL v3 (iOS)
