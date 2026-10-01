#!/bin/bash
# deterministic build: placement + all routing by hand (relayout.py) -> zone fill -> DRC with schematic parity
set -e
cd "$(dirname "$0")"
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
$PY relayout.py ../BaseChipOnly-after-fixes-2026-09-30.kicad_pcb final.kicad_pcb 2>&1 | grep -E "saved|rror|Trace"
cp placed.kicad_pro final.kicad_pro; cp ../../BaseChipOnly.kicad_sch final.kicad_sch
$CLI pcb drc --schematic-parity --severity-all --format json -o drc_final.json final.kicad_pcb >/dev/null 2>&1
python3 - <<'PY'
import json,collections
d=json.load(open('drc_final.json'))
print(dict(collections.Counter((v['severity'],v['type']) for v in d['violations'])))
print('unconnected',len(d['unconnected_items']),'parity',len(d.get('schematic_parity',[])))
for v in d['unconnected_items']+d.get('schematic_parity',[])+[x for x in d['violations'] if x['type'] not in ('drill_out_of_range','lib_footprint_issues','text_height')]:
    print(' ',v['type'],'|',' || '.join(f"{i['description'][:55]} @({i['pos']['x']:.2f},{i['pos']['y']:.2f})" for i in v['items']))
PY
