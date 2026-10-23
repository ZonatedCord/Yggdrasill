#!/usr/bin/env python3
"""Regenerate the 3D renders of BaseChipOnly Rev 1.03 and Rev 2.0.

Usage (from anywhere):  python3 PCB/render/make_renders.py

Only the Python standard library and kicad-cli (KiCad 9) are needed; nothing
is downloaded or installed. kicad-cli is looked up in PATH, then in
/Applications/KiCad/KiCad.app/Contents/MacOS.

What it does: each .kicad_pcb is copied into a temporary folder, the missing
3D models (ESP32 module U1, barrel jack J1 and, on Rev 2.0 only, the 2920
polyfuse and the two PTS810 buttons, the last two as simplified hand-made
VRML models in PCB/render/models/) are added to the COPY, and kicad-cli
renders top and bottom views into <board>/render/top.png and bottom.png
(existing files are overwritten). The board files in the repo are never
modified.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PCB = HERE.parent
MODELS = HERE / "models"
STD = "${KICAD9_3DMODEL_DIR}/"
KICAD_APP_BIN = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

# ref -> (model path, offset xyz, rotate xyz)
COMMON = {
    "U1": (STD + "RF_Module.3dshapes/ESP32-WROOM-32U.wrl", "0 0.155 0", "0 0 0"),
    "J1": (STD + "Connector_BarrelJack.3dshapes/BarrelJack_Horizontal.wrl", "0 6.55 0", "0 0 -90"),
}
REV2_EXTRA = {
    "Polyfuse1": (str(MODELS / "Fuse_2920_7451Metric.wrl"), "0 0 0", "0 0 0"),
    "SW1": (str(MODELS / "SW_SPST_PTS810.wrl"), "0 0 0", "0 0 0"),
    "SW2": (str(MODELS / "SW_SPST_PTS810.wrl"), "0 0 0", "0 0 0"),
}
BOARDS = [
    ("Rev 1.03", PCB / "BaseChipOnly", COMMON),
    ("Rev 2.0", PCB / "BaseChipOnly_rev2", {**COMMON, **REV2_EXTRA}),
]


def block_end(text, start):
    """Index of the ')' closing the '(' at text[start] (balanced)."""
    depth = 0
    for j in range(start, len(text)):
        c = text[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j
    raise ValueError("unbalanced parentheses")


def set_model(text, ref, model, offset, rotate):
    i = text.find('(property "Reference" "%s"' % ref)
    if i < 0:
        raise SystemExit("footprint %s not found" % ref)
    s = text.rfind("(footprint", 0, i)
    e = block_end(text, s)
    blk = text[s:e]
    while True:  # drop existing (model ...) blocks
        k = blk.find("(model ")
        if k < 0:
            break
        blk = blk[:k] + blk[block_end(blk, k) + 1:]
    blk = blk.rstrip() + (
        '\n\t\t(model "%s"\n\t\t\t(offset (xyz %s))\n\t\t\t(scale (xyz 1 1 1))'
        "\n\t\t\t(rotate (xyz %s))\n\t\t)\n\t" % (model, offset, rotate)
    )
    return text[:s] + blk + text[e:]


def find_cli():
    cli = shutil.which("kicad-cli")
    if cli:
        return cli
    if Path(KICAD_APP_BIN).exists():
        return KICAD_APP_BIN
    raise SystemExit("kicad-cli not found (PATH or %s)" % KICAD_APP_BIN)


def main():
    cli = find_cli()
    print("kicad-cli:", cli)
    with tempfile.TemporaryDirectory() as tmp:
        for name, folder, models in BOARDS:
            src = folder / "BaseChipOnly.kicad_pcb"
            text = src.read_text()
            for ref, (m, off, rot) in models.items():
                print("  %s: model added to %s (temporary copy)" % (name, ref))
                text = set_model(text, ref, m, off, rot)
            tmp_pcb = Path(tmp) / (folder.name + ".kicad_pcb")
            tmp_pcb.write_text(text)
            out_dir = folder / "render"
            out_dir.mkdir(exist_ok=True)
            for side in ("top", "bottom"):
                out = out_dir / (side + ".png")
                print("  %s: rendering %s -> %s" % (name, side, out.relative_to(PCB.parent)))
                subprocess.run(
                    [cli, "pcb", "render", "--side", side, "--background", "transparent",
                     "--quality", "high", "-w", "1600", "-h", "1200",
                     "-o", str(out), str(tmp_pcb)],
                    check=True,
                )
    print("Done. Board files untouched.")


if __name__ == "__main__":
    sys.exit(main())
