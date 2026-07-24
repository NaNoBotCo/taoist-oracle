#!/usr/bin/env python3
"""Export the self-contained oracle app into the wichaa (manuscript-wiki) repo.

Single source of truth: edit oracle.html here, run this, rebuild wichaa. The
wichaa build (build_static.py) serves the copy at /divination/app.html and wraps
a chrome page (divination.py) around it. Mirrors the jovilabe project's
export_wichaa.py pattern — the tool lives in its own repo, wichaa gets a copy.

    python3 export_wichaa.py
"""

import pathlib
import shutil

HERE = pathlib.Path(__file__).parent
SRC = HERE / "oracle.html"
DST = HERE.parent / "manuscript-wiki" / "content" / "divination-app.html"

if not DST.parent.parent.is_dir():
    raise SystemExit(f"wichaa repo not found at {DST.parent.parent}")
DST.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(SRC, DST)
print(f"exported {SRC.name} -> {DST}")
