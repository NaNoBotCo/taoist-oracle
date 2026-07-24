#!/usr/bin/env python3
"""Inject the canonical Zhouyi corpus (data/zhouyi.json) into oracle.html as a
JS constant. Idempotent: run again after editing the JSON to refresh.

    python3 build_web.py
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "data" / "zhouyi.json").read_text(encoding="utf-8"))
html = (ROOT / "oracle.html").read_text(encoding="utf-8")

block = ("/*ZHOUYI_DATA_START*/\nconst ZHOUYI_DATA = "
         + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
         + ";\n/*ZHOUYI_DATA_END*/")

marker = re.compile(r"/\*ZHOUYI_DATA_START\*/.*?/\*ZHOUYI_DATA_END\*/", re.S)
if marker.search(html):
    html = marker.sub(lambda _: block, html)
else:
    # insert right after the "use strict"; line
    html = html.replace('"use strict";', '"use strict";\n' + block, 1)

(ROOT / "oracle.html").write_text(html, encoding="utf-8")
print(f"injected {len(data)} hexagrams into oracle.html")
