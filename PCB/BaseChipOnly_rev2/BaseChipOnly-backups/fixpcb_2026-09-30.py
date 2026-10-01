"""Apply the 2026-09-30 BaseChipOnly PCB fixes.
Always starts from the pre-session backup so it can be re-run.
usage: python3 fixpcb.py <backup.kicad_pcb> <netlist.xml> <out.kicad_pcb>
"""
import sys, math, xml.etree.ElementTree as ET
import pcbnew

SRC, NETXML, OUT = sys.argv[1:4]
FPLIB = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
b = pcbnew.LoadBoard(SRC)
MM = pcbnew.FromMM
def P(x, y): return pcbnew.VECTOR2I(MM(x), MM(y))
def mm(v): return round(pcbnew.ToMM(v), 3)
F, B = pcbnew.F_Cu, pcbnew.B_Cu
log = []
GRAVE = []  # keep removed items alive: letting SWIG free them corrupts the type table

# ---------------------------------------------------------------- schematic
root = ET.parse(NETXML).getroot()
comps = {}
for c in root.find('components'):
    comps[c.get('ref')] = dict(value=c.findtext('value'), fp=c.findtext('footprint'),
                               uuid=c.find('tstamps').text.strip())
padnet = {}
for n in root.find('nets'):
    for x in n:
        nm = n.get('name')
        if nm.startswith(('unconnected-(', 'Net-(')):
            nm = nm.replace('/', '{slash}')
        padnet[(x.get('ref'), x.get('pin'))] = nm

def net(name):
    ni = b.FindNet(name)
    if ni is None:
        ni = pcbnew.NETINFO_ITEM(b, name); b.Add(ni)
    return ni

# ---------------------------------------------------------------- identify footprints
BYPOS = {(137.40,76.28):'R0',(157.90,63.37):'R4',(148.45,73.43):'U3',(135.05,51.88):'Rtop1',
 (139.25,48.69):'L1',(137.90,72.95):'D1',(139.40,82.78):'D_TVS1',(148.40,63.39):'R1',
 (131.35,51.88):'Rbot1',(148.50,68.83):'R5',(142.40,76.28):'C2',(131.34,46.85):'C3',
 (133.90,88.78):'Polyfuse1',(143.45,49.53):'D2',(141.60,95.93):'J1',(151.55,63.38):'R2',
 (157.30,50.62):'U1',(153.46,68.28):'IO0_CTRL1',(159.96,68.28):'EN_CTRL1',(134.25,46.85):'COUT1',
 (160.90,63.28):'C4',(141.34,70.28):'CIN1',(156.40,90.28):'C1',(131.78,42.78):'J3',
 (154.80,63.37):'R3',(154.37,78.36):'J2',(136.25,60.38):'U4',
 (131.40,37.88):'H1',(165.20,37.88):'H2',(131.40,101.43):'H3',(165.20,101.43):'H4'}
fps = {}
for f in list(b.GetFootprints()):
    k = (round(pcbnew.ToMM(f.GetPosition().x),2), round(pcbnew.ToMM(f.GetPosition().y),2))
    ref = BYPOS.get(k)
    if ref is None:
        raise SystemExit(f"unmapped footprint at {k}: {f.GetReference()}")
    fps[ref] = f
assert len(fps) == 31, len(fps)

NEEDED = ['Inductor_SMD:L_Bourns_SRN6045TA', 'Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder',
          'Fuse:Fuse_1812_4532Metric_Pad1.30x3.40mm_HandSolder', 'Capacitor_Tantalum_SMD:CP_EIA-6032-28_Kemet-C_HandSolder',
          'Button_Switch_SMD:SW_SPST_PTS810', 'Button_Switch_SMD:SW_SPST_PTS810']
PRE = []
for libid in NEEDED:
    lib, name = libid.split(':')
    PRE.append((libid, pcbnew.FootprintLoad(f"{FPLIB}/{lib}.pretty", name)))
def load_fp(libid):
    for i, (l, f) in enumerate(PRE):
        if l == libid:
            PRE.pop(i); return f
    raise SystemExit('not preloaded ' + libid)

def replace_fp(ref, libid, pos=None, rot=None):
    old = fps[ref]
    new = load_fp(libid)
    new.SetPosition(old.GetPosition() if pos is None else P(*pos))
    new.SetOrientationDegrees(old.GetOrientationDegrees() if rot is None else rot)
    b.Remove(old); GRAVE.append(old); b.Add(new); fps[ref] = new
    log.append(f"replaced {ref} -> {libid}")
    return new

def add_fp(ref, libid, pos, rot):
    new = load_fp(libid); new.SetPosition(P(*pos)); new.SetOrientationDegrees(rot)
    b.Add(new); fps[ref] = new; log.append(f"added {ref} {libid} at {pos} rot {rot}")
    return new

# ---------------------------------------------------------------- footprint swaps / moves
replace_fp('L1', 'Inductor_SMD:L_Bourns_SRN6045TA', pos=(138.2, 48.08), rot=90)
replace_fp('Rtop1', 'Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder', pos=(134.4, 52.65), rot=180)
replace_fp('Polyfuse1', 'Fuse:Fuse_1812_4532Metric_Pad1.30x3.40mm_HandSolder', pos=(133.6, 88.78), rot=180)
fps['COUT1'].SetPosition(P(133.75, 46.85))
for r in ('D1', 'D2'):
    fps[r].SetOrientationDegrees(fps[r].GetOrientationDegrees() + 180)
    log.append(f"rotated {r} 180deg")
add_fp('COUT2', 'Capacitor_Tantalum_SMD:CP_EIA-6032-28_Kemet-C_HandSolder', (138.3, 37.7), 0)
add_fp('SW2', 'Button_Switch_SMD:SW_SPST_PTS810', (164.2, 72.5), 0)
add_fp('SW1', 'Button_Switch_SMD:SW_SPST_PTS810', (164.2, 79.0), 0)

# ---------------------------------------------------------------- fields, links, pad nets
for ref, f in fps.items():
    f.SetReference(ref)
    rt, vt = f.Reference(), f.Value()
    rt.SetLayer(pcbnew.F_SilkS); rt.SetVisible(ref not in ('J1', 'J2', 'J3'))  # connectors keep their own silk labels
    vt.SetLayer(pcbnew.F_Fab)
    if ref.startswith('H'):
        f.SetValue('MountingHole_2.1mm'); f.SetBoardOnly(True); rt.SetVisible(False)
        continue
    c = comps[ref]
    f.SetValue(c['value'])
    f.SetPath(pcbnew.KIID_PATH('/' + c['uuid']))
    f.SetSheetfile('BaseChipOnly.kicad_sch'); f.SetSheetname('')
    if str(f.GetFPID().GetUniStringLibId()) != c['fp']:
        f.SetFPID(pcbnew.LIB_ID(*c['fp'].split(':')))
    if ref == 'U1':
        # thermal vias of the exposed pad had no number/net: tie them to the GND pad
        for p in f.Pads():
            if p.GetNumber().startswith('40_'):
                p.SetNumber('39_5')
    for p in f.Pads():
        num = p.GetNumber()
        if not num:
            continue
        nn = padnet.get((ref, num))
        if nn is None and not p.GetNetname():
            continue  # footprint-only pads (e.g. U1 thermal via pads 40_x)
        if nn is None:
            raise SystemExit(f"no schematic net for {ref}.{num}")
        p.SetNet(net(nn))

def pad(ref, num, which=0):
    ps = [p for p in fps[ref].Pads() if p.GetNumber() == num]
    ps.sort(key=lambda p: (p.GetPosition().x, p.GetPosition().y))
    q = ps[which].GetPosition(); return (mm(q.x), mm(q.y))

# ---------------------------------------------------------------- track helpers
def find_track(layer, a, c, via=False):
    hits = []
    for t in b.GetTracks():
        isvia = t.GetClass() == 'PCB_VIA'
        if isvia != via: continue
        if not via and t.GetLayer() != layer: continue
        s, e = (mm(t.GetStart().x), mm(t.GetStart().y)), (mm(t.GetEnd().x), mm(t.GetEnd().y))
        close = lambda u, v: abs(u[0]-v[0]) < 0.015 and abs(u[1]-v[1]) < 0.015
        if (close(s, a) and close(e, c)) or (close(s, c) and close(e, a)):
            hits.append(t)
    return hits

def delete(layer, a, c):
    h = find_track(layer, a, c)
    if len(h) != 1: raise SystemExit(f"delete: {len(h)} matches for {a}->{c}")
    b.Remove(h[0]); GRAVE.append(h[0])

def delete_via(a):
    h = find_track(None, a, a, via=True)
    if len(h) < 1: raise SystemExit(f"delete_via: none at {a}")
    for t in h: b.Remove(t); GRAVE.append(t)

NEW = []
def seg(layer, pts, w, netname=None):
    for a, c in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(P(*a)); t.SetEnd(P(*c))
        t.SetWidth(MM(w)); t.SetLayer(layer)
        if netname: t.SetNet(net(netname))
        b.Add(t); NEW.append(t)

def via(pt, netname=None):
    v = pcbnew.PCB_VIA(b); v.SetPosition(P(*pt)); v.SetWidth(MM(0.6)); v.SetDrill(MM(0.3))
    v.SetLayerPair(F, B)
    if netname: v.SetNet(net(netname))
    b.Add(v); NEW.append(v)

# ---------------------------------------------------------------- L1 / COUT1 / Rtop1 / C3 area (+3V3, SW, FB)
for a, c in [((139.25,47.53),(139.25,45.68)), ((139.25,45.68),(139.15,45.58)),
             ((139.25,53.12),(139.25,49.86)),
             ((134.25,47.89),(136.15,45.99)), ((134.40,48.04),(134.25,47.89)), ((134.40,49.68),(134.40,48.04)),
             ((135.05,50.33),(134.40,49.68)), ((133.78,50.33),(131.34,47.89)), ((135.05,50.33),(133.78,50.33)),
             ((131.30,48.00),(131.29,48.01)), ((134.25,45.81),(134.25,45.80))]:
    delete(F, a, c)
delete(B, (134.25,45.80), (134.60,45.80))
# old L1 +3V3 via and its B.Cu tail to J3 pin 2 (J3.2 is still fed on F.Cu)
delete(B, (139.15,45.58), (137.60,45.58)); delete(B, (137.60,45.58), (134.80,42.78)); delete(B, (134.80,42.78), (134.32,42.78))
delete(B, (139.15,45.58), (145.85,45.58))
delete_via((139.15,45.58)); delete_via((134.25,45.80))

L1p1, L1p2 = pad('L1','1'), pad('L1','2')
log.append(f"L1 pad1(SW)={L1p1} pad2(+3V3)={L1p2}")
C1p1, C1p2 = pad('COUT1','1'), pad('COUT1','2')
Rt1, Rt2 = pad('Rtop1','1'), pad('Rtop1','2')
log.append(f"Rtop1 pad1(FB)={Rt1} pad2(+3V3)={Rt2}")
# +3V3: C3 -> COUT1 -> L1, Rtop1 -> COUT1, L1 -> B.Cu trunk to ESP32
seg(F, [pad('C3','1'), C1p1], 0.5)
seg(F, [C1p1, (C1p1[0]+0.95, 46.94), (L1p2[0]-1.9, 46.94)], 0.5)
seg(F, [Rt2, (Rt2[0], 48.3)], 0.5)
seg(F, [(L1p2[0]+2.0, L1p2[1]), (141.2, 45.0)], 0.5); via((141.2, 45.0))
seg(B, [(141.2, 45.0), (141.78, 45.58), (145.85, 45.58)], 0.5)
# COUT1 GND via moved with the part
seg(F, [C1p2, (C1p2[0], 44.55)], 0.4); via((C1p2[0], 44.55))
# FB: Rtop1 pad1 to the existing FB via
seg(F, [Rt1, (135.05, 53.43)], 0.3)
# SW: re-land on the new L1 pad
seg(F, [(139.25,53.12), (139.25, L1p1[1]+0.4)], 0.5)

# SW trunk: pull the vertical away from DTR and widen it
# (U4 pads reach x~146, so the SW trunk keeps its original 0.2 mm path past them; the open
#  segments between D2, L1 and the trunk are widened below)
for a, c in [((143.45,53.40),(143.45,51.53)), ((143.40,53.45),(139.58,53.45)), ((139.58,53.45),(139.25,53.12))]:
    for t in find_track(F, a, c): t.SetWidth(MM(0.5))

# ---------------------------------------------------------------- auto-reset: cross DTR/RTS
delete(F, (147.30,60.00), (149.76,62.46)); delete(F, (149.76,62.46), (151.90,62.46))
delete(F, (146.90,60.98), (148.40,62.48))
delete(B, (149.50,68.83), (149.50,63.33)); delete(B, (149.50,63.33), (152.85,59.97))
RTS = padnet[('J3','6')]; DTR = padnet[('J3','5')]
# RTS -> R1.1 and EN_CTRL1 emitter
seg(F, [(147.30,60.00), (147.90,60.60)], 0.2); via((147.90,60.60))
seg(B, [(147.90,60.60), (147.30,61.20), (147.30,62.48)], 0.2); via((147.30,62.48))
seg(F, [(147.30,62.48), pad('R1','1')], 0.2)
seg(B, [(147.30,62.48), (147.30,70.50), (159.05,70.50), (159.05,69.23)], 0.2)
# DTR -> R2.2 and IO0_CTRL1 emitter
seg(F, [(146.90,60.98), (146.90,61.30), (148.70,61.30), (151.00,61.30), (151.55,61.85), pad('R2','2')], 0.2)
via((148.70,61.30))
seg(B, [(148.70,61.30), (148.70,69.70), (152.50,69.70), (152.50,69.28)], 0.2)
# IO13 re-routed on B.Cu to free the channel
seg(B, [(149.50,68.83), (149.50,66.60), (152.85,63.25), (152.85,59.97)], 0.2)

# ---------------------------------------------------------------- U3: GND and VBUS
U3g, U3v = pad('U3','2'), pad('U3','5')
seg(F, [U3g, (U3g[0], 71.2), (U3g[0]-0.5, 70.7), (146.30, 70.7)], 0.25); via((146.30, 70.7))
seg(F, [U3v, (U3v[0], 77.4)], 0.3)

# ---------------------------------------------------------------- buttons
s2a, s2g = pad('SW2','1',0), pad('SW2','2',1)
seg(F, [(162.50,66.68), (162.50,70.9), s2a], 0.25)
seg(F, [s2g, (s2g[0], 75.0)], 0.3); via((s2g[0], 75.0))
seg(F, [pad('SW2','1',0), pad('SW2','1',1)], 0.25); seg(F, [pad('SW2','2',0), pad('SW2','2',1)], 0.25)
fps['SW2'].Reference().SetPosition(P(164.2, 70.0))
s1a, s1g = pad('SW1','1',0), pad('SW1','2',1)
seg(F, [pad('SW1','1',0), pad('SW1','1',1)], 0.25); seg(F, [pad('SW1','2',0), pad('SW1','2',1)], 0.25)
fps['SW1'].Reference().SetPosition(P(164.2, 82.5))
seg(B, [(163.85,65.48), (163.85,76.2), (163.2,76.8)], 0.25); via((163.2,76.8))
seg(F, [(163.2,76.8), s1a], 0.25)
seg(F, [s1g, (s1g[0], 81.5)], 0.3); via((s1g[0], 81.5))

# ---------------------------------------------------------------- COUT2 (bulk output cap for the LM2596)
c2p, c2n = pad('COUT2','1'), pad('COUT2','2')
fps['COUT2'].Reference().SetPosition(P(146.0, 37.7))
seg(F, [c2p, (134.32, 39.9), (134.32, 42.78)], 0.5)
seg(F, [c2n, (142.7, c2n[1])], 0.5); via((142.7, c2n[1]))

# ---------------------------------------------------------------- net assignment by connectivity
items = [t for t in b.GetTracks()]
allpads = [p for f in b.GetFootprints() for p in f.Pads()]
parent = {id(t): id(t) for t in items}
byid = {id(t): t for t in items}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, c): parent[find(a)] = find(c)
def anchors(t):
    return [t.GetPosition()] if t.GetClass() == 'PCB_VIA' else [t.GetStart(), t.GetEnd()]
def onlayer(t, layer):
    return t.GetClass() == 'PCB_VIA' or t.GetLayer() == layer
for i, t in enumerate(items):
    for u in items[i+1:]:
        for layer in (F, B):
            if not (onlayer(t, layer) and onlayer(u, layer)): continue
            if any(u.HitTest(a, 0) for a in anchors(t)) or any(t.HitTest(a, 0) for a in anchors(u)):
                union(id(t), id(u)); break
clusternets = {}
for t in items:
    for p in allpads:
        if not p.GetNetname(): continue
        for layer in (F, B):
            if not onlayer(t, layer) or not p.IsOnLayer(layer): continue
            if any(p.HitTest(a) for a in anchors(t)) or (t.GetClass() == 'PCB_VIA' and p.HitTest(t.GetPosition())):
                clusternets.setdefault(find(id(t)), set()).add(p.GetNetname()); break
problems = []
for t in items:
    ns = clusternets.get(find(id(t)), set())
    if len(ns) == 1:
        t.SetNet(net(next(iter(ns))))
    elif len(ns) > 1:
        problems.append((sorted(ns), mm(anchors(t)[0].x), mm(anchors(t)[0].y)))
    else:
        problems.append((['<no pad>', t.GetNetname()], mm(anchors(t)[0].x), mm(anchors(t)[0].y)))

# ---------------------------------------------------------------- widen +3V3
for t in b.GetTracks():
    if t.GetClass() == 'PCB_TRACK' and t.GetNetname() == '+3V3' and t.GetWidth() < MM(0.5):
        if t.GetLength() > MM(0.3):
            t.SetWidth(MM(0.5))

# ---------------------------------------------------------------- silkscreen typo
for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and 'GDN' in d.GetText():
        d.SetText(d.GetText().replace('GDN', 'GND')); log.append('fixed GDN board text')
for f in b.GetFootprints():
    for d in f.GraphicalItems():
        if isinstance(d, pcbnew.PCB_TEXT) and 'GDN' in d.GetText():
            d.SetText(d.GetText().replace('GDN', 'GND')); log.append(f'fixed GDN text in {f.GetReference()}')

# tie each former 40_x thermal via to the neighbouring GND pad on F.Cu
u1 = fps['U1']
smd = [p for p in u1.Pads() if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD and p.GetNumber().startswith('39_')]
for p in u1.Pads():
    if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH and p.GetNumber() == '39_5':
        q = min(smd, key=lambda s_: (s_.GetPosition() - p.GetPosition()).EuclideanNorm())
        a_, c_ = p.GetPosition(), q.GetPosition()
        seg(F, [(mm(a_.x), mm(a_.y)), (mm(c_.x), mm(c_.y))], 0.3, 'GND')

# DTR/RTS run at 0.4 mm pitch next to /SW: 0.15 mm keeps >0.2 mm clearance
for t in b.GetTracks():
    if t.GetClass() == 'PCB_TRACK' and t.GetNetname() in (RTS, DTR):
        t.SetWidth(MM(0.15))

# credit text moves to the back silkscreen to free the right edge for the buttons
for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetText().startswith('BARLAROK'):
        d.SetLayer(pcbnew.B_SilkS); d.SetMirrored(True)
        c = d.GetBoundingBox().GetCenter()
        d.Move(pcbnew.VECTOR2I(MM(134.0) - c.x, MM(76.0) - c.y))
        r = d.GetBoundingBox()
        log.append(f'credit text -> B.Silkscreen bbox {mm(r.GetLeft())},{mm(r.GetTop())}..{mm(r.GetRight())},{mm(r.GetBottom())}')

# silkscreen reference tidy-up for moved parts
fps['L1'].Reference().SetPosition(P(138.2, 48.08)); fps['L1'].Reference().SetTextAngleDegrees(0)
fps['D2'].Reference().SetPosition(P(143.45, 49.53)); fps['D2'].Reference().SetTextAngleDegrees(90)
fps['COUT1'].Reference().SetPosition(P(133.75, 44.0))
fps['Rtop1'].Reference().SetPosition(P(131.6, 55.4))
fps['Polyfuse1'].Reference().SetPosition(P(133.8, 91.6))

# drop nets no longer used
filler = pcbnew.ZONE_FILLER(b); filler.Fill(b.Zones())
pcbnew.SaveBoard(OUT, b)
print('\n'.join(log))
seen = set()
for pr in problems:
    k = tuple(pr[0])
    if k in seen: continue
    seen.add(k); print('CLUSTER PROBLEM', pr)
print('saved', OUT)
