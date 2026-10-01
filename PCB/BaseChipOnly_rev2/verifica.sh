#!/bin/bash
# Pre-order checks for BaseChipOnly: ERC, DRC + schematic parity, fab outputs, Gerber X2 pad->net vs schematic.
# usage: ./verifica.sh        (regenerates Esportazione-2026-09-30/)
set -e
cd "$(dirname "$0")"
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
O=Esportazione-2026-09-30
T=$(mktemp -d)
$CLI sch erc --format json -o $T/erc.json BaseChipOnly.kicad_sch >/dev/null 2>&1
$CLI pcb drc --schematic-parity --severity-all --format json -o $T/drc.json BaseChipOnly.kicad_pcb >/dev/null 2>&1
mkdir -p $O; find $O -type f ! -name 'preview-*' -delete
$CLI pcb export gerbers -o "$O/" BaseChipOnly.kicad_pcb >/dev/null 2>&1
$CLI pcb export drill -o "$O/" BaseChipOnly.kicad_pcb >/dev/null 2>&1
$CLI sch export bom -o "$O/BaseChipOnly-BOM.csv" --fields 'Reference,Value,Footprint,MPN,Manufacturer,${QUANTITY}' --group-by Value,Footprint BaseChipOnly.kicad_sch >/dev/null 2>&1
$CLI pcb export pos --format csv --units mm -o "$O/BaseChipOnly-pos.csv" BaseChipOnly.kicad_pcb >/dev/null 2>&1
$CLI pcb export pdf --layers F.Fab,Edge.Cuts,F.Silkscreen --mode-single -o "$O/BaseChipOnly-assembly-values.pdf" BaseChipOnly.kicad_pcb >/dev/null 2>&1
$CLI sch export pdf -o "$O/BaseChipOnly-schematic.pdf" BaseChipOnly.kicad_sch >/dev/null 2>&1
$CLI sch export netlist --format kicadxml -o $T/net.xml BaseChipOnly.kicad_sch >/dev/null 2>&1
python3 - "$T" "$O" <<'PY'
import json, re, sys, collections, xml.etree.ElementTree as ET
T, O = sys.argv[1:3]; fail = 0
e = json.load(open(f'{T}/erc.json'))
erc = [v for s in e['sheets'] for v in s['violations'] if v['severity'] == 'error']
print(f'ERC errors: {len(erc)}'); fail += len(erc)
d = json.load(open(f'{T}/drc.json'))
errs = [v for v in d['violations'] if v['severity'] == 'error' and v['type'] != 'drill_out_of_range']
print(f"DRC errors: {len(errs)}  (+{sum(v['type']=='drill_out_of_range' for v in d['violations'])} known 0.2 mm ESP32 thermal-via drills)")
print(f"unconnected: {len(d['unconnected_items'])}   schematic parity issues: {len(d.get('schematic_parity', []))}")
fail += len(errs) + len(d['unconnected_items']) + len(d.get('schematic_parity', []))
exp = {}
for n in ET.parse(f'{T}/net.xml').getroot().find('nets'):
    nm = n.get('name')
    if nm.startswith(('unconnected-(', 'Net-(')): nm = nm.replace('/', '{slash}')
    for x in n: exp[(x.get('ref'), x.get('pin'))] = nm
got = {}; cur = {'P': None, 'N': None}
for line in open(f'{O}/BaseChipOnly-F_Cu.gtl'):
    line = line.strip()
    m = re.match(r'%TO\.P,([^,*]+),([^,*]+)', line)
    if m: cur['P'] = (m.group(1), m.group(2))
    m = re.match(r'%TO\.N,([^*]*)\*%', line)
    if m: cur['N'] = m.group(1)
    if line.startswith('%TD*%'): cur = {'P': None, 'N': None}
    if line.endswith('D03*') and cur['P']: got.setdefault(cur['P'], set()).add(cur['N'])
bad = [k for k, v in got.items() if k in exp and v != {exp[k]}]
print(f'Gerber X2: {sum(k in exp for k in got)} pads checked against the schematic, mismatches: {len(bad)}')
fail += len(bad)
print('RESULT:', 'PASS' if fail == 0 else f'FAIL ({fail})')
PY
