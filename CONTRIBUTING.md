# Contributing to PiantaSmart

Thank you for your interest. Contributions are welcome across all three pillars: hardware, 3D models, and the iOS app.

---

## License obligations

| Component | License | What it means for contributions |
|---|---|---|
| `PCB/`, `3D/` | CC BY-NC-SA 4.0 | Your contributions inherit the same license. Commercial use requires written permission from Marco Barlera. |
| `WLED-iOS/` | GPL v3 | Copyleft — any derivative must remain GPL v3. |
| `docs/` | CC BY-NC-SA 4.0 | Same as hardware. |

By submitting a contribution you agree to these terms.

---

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

| Type | Use for |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `chore` | Build/repo maintenance |
| `hw` | Hardware (PCB, schematic) changes |
| `3d` | 3D model changes |

Examples:
```
hw(base-chiponly): fix via placement on decoupling caps
feat(ios): add Liquid Glass effect to device list
docs: update 3d-printing material recommendations
```

---

## Getting started

### iOS app

```bash
git clone --recurse-submodules https://github.com/YOUR_FORK/PiantaSmart
open WLED-iOS/wled.xcodeproj  # Xcode 15+
```

> Note: `WLED-iOS/` is managed as a git submodule once the fork is linked.

### Hardware (KiCad)

Open any project in `PCB/<variant>/*.kicad_pro`. KiCad 8+ recommended.

Gerbers for fabrication are in `PCB/<variant>/Esportazione/`.

---

## Submitting changes

1. Fork the repo
2. Create a branch: `git checkout -b feat/my-feature`
3. Commit with conventional style
4. Open a pull request against `main`

For commercial licensing inquiries: barleramarco2@gmail.com
