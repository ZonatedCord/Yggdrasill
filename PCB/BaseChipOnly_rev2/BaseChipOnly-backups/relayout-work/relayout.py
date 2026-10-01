"""BaseChipOnly re-layout (2026-09-30): tidy functional placement + hand-routed power.
Signals are routed afterwards by Freerouting (see route.sh).
usage: python3 relayout.py <in.kicad_pcb> <out.kicad_pcb>
Input must be the board after fixpcb_2026-09-30.py (correct nets / refs).
"""
import sys
import pcbnew

SRC, OUT = sys.argv[1:3]
FPLIB = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
b = pcbnew.LoadBoard(SRC)
MM = pcbnew.FromMM
def P(x, y): return pcbnew.VECTOR2I(MM(x), MM(y))
def mm(v): return round(pcbnew.ToMM(v), 3)
F, B = pcbnew.F_Cu, pcbnew.B_Cu
GRAVE = []  # removed items must stay referenced (SWIG type table corrupts otherwise)
PRE = pcbnew.FootprintLoad(f"{FPLIB}/Fuse.pretty", "Fuse_2920_7451Metric_Pad2.10x5.45mm_HandSolder")

fps = {f.GetReference(): f for f in b.GetFootprints()}

# ---------------------------------------------------------------- clear all copper routing
for t in list(b.GetTracks()):
    b.Remove(t); GRAVE.append(t)

# ---------------------------------------------------------------- polyfuse -> 2920
old = fps['Polyfuse1']
PRE.SetReference('Polyfuse1'); PRE.SetValue('4A'); PRE.SetFPID(pcbnew.LIB_ID('Fuse', 'Fuse_2920_7451Metric_Pad2.10x5.45mm_HandSolder')); PRE.SetPath(old.GetPath())
PRE.SetSheetfile(old.GetSheetfile()); PRE.SetSheetname(old.GetSheetname())
PRE.Value().SetLayer(pcbnew.F_Fab)
for p in PRE.Pads():
    p.SetNet(b.FindNet('Net-(J1-V_IN_RAW)') if p.GetNumber() == '1' else b.FindNet('+5V'))
b.Remove(old); GRAVE.append(old); b.Add(PRE); fps['Polyfuse1'] = PRE

# ---------------------------------------------------------------- values changed after the simulations (2026-09-30)
for ref, val in {'C4': '1µF', 'R5': '100Ω', 'IO0_CTRL1': 'MMBT3904', 'EN_CTRL1': 'MMBT3904'}.items():
    fps[ref].SetValue(val)

# ---------------------------------------------------------------- placement
# v2 (2026-10-01): regulator block spread out for hand soldering (~1 mm between courtyards),
# status LED moved next to C1, TVS moved left, buttons centred on the top edge.
PLACE = {
    # buck regulator block, pins pointing up
    'U4':    (136.0, 71.5, -90),
    'D2':    (137.2, 56.8, 90),     # K (pin1) down to SW, A up to GND
    'L1':    (143.0, 56.8, 90),     # pad1 SW at the bottom, pad2 +3V3 at the top
    'COUT2': (142.4, 50.4, 180),    # + on the right
    'COUT1': (143.4, 46.3, 180),    # + on the right, GND left
    'C3':    (137.5, 46.3, 0),      # + on the left, GND right (shares a via with COUT1)
    'Rbot1': (133.5, 57.0, 90),     # FB down, GND up
    'Rtop1': (130.8, 57.0, 90),     # FB down, +3V3 up
    'CIN1':  (143.2, 63.8, 90),     # +5V down, GND up
    'C2':    (145.6, 63.8, 90),
    # input / protection block
    'Polyfuse1': (133.0, 90.5, 90), # VIN bottom, +5V top
    'D_TVS1':    (132.5, 81.6, 90), # K down on the +5V bus
    # power-on LED, bottom right next to C1
    'R0':        (164.5, 92.5, -90),# +5V up
    'D1':        (164.5, 96.3, 90), # A up (to R0), K down (to GND)
    # BOOT / RESET centred on the top edge (pads '1' at the bottom)
    'SW2':       (145.1, 37.9, 180),
    'SW1':       (151.5, 37.9, 180),
}
for ref, (x, y, r) in PLACE.items():
    f = fps[ref]; f.SetPosition(P(x, y)); f.SetOrientationDegrees(r)

def pad(ref, num, which=0):
    ps = sorted([p for p in fps[ref].Pads() if p.GetNumber() == num],
                key=lambda p: (p.GetPosition().x, p.GetPosition().y))
    q = ps[which].GetPosition(); return (mm(q.x), mm(q.y))

# ---------------------------------------------------------------- routing helpers (locked)
def seg(layer, pts, w, net):
    ni = b.FindNet(net)
    assert ni is not None, net
    for a, c in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(P(*a)); t.SetEnd(P(*c)); t.SetWidth(MM(w))
        t.SetLayer(layer); t.SetNet(ni); t.SetLocked(True); b.Add(t)

def via(pt, net, d=0.6, drill=0.3):
    v = pcbnew.PCB_VIA(b); v.SetPosition(P(*pt)); v.SetWidth(F, MM(d)); v.SetWidth(B, MM(d)); v.SetDrill(MM(drill))
    v.SetLayerPair(F, B); v.SetNet(b.FindNet(net)); v.SetLocked(True); b.Add(v)

def gnd_stub(frm, to, w=0.5):
    seg(F, [frm, to], w, 'GND'); via(to, 'GND')

VIN = 'Net-(J1-V_IN_RAW)'
# VIN: jack -> polyfuse
seg(F, [pad('J1','1'), (136.6, 89.38), (134.2, 91.8), (133.0, 93.6)], 2.0, VIN)
# +5V: polyfuse -> bus -> C1, J2, regulator input
seg(F, [pad('Polyfuse1','2'), (133.0, 84.5)], 3.0, '+5V')
seg(F, [(133.0, 84.5), (156.4, 84.5), pad('C1','1')], 3.0, '+5V')
seg(F, [(144.5, 84.5), (144.5, 65.5)], 2.5, '+5V')
seg(F, [(144.5, 78.5), (155.8, 78.5)], 2.0, '+5V')
seg(F, [(155.8, 78.5), pad('J2','2')], 2.0, '+5V')
seg(F, [pad('U4','1'), (139.4, 65.5), (145.6, 65.5)], 1.5, '+5V')
seg(F, [pad('CIN1','1'), (143.2, 65.5)], 1.0, '+5V')
seg(F, [pad('C2','1'), (145.6, 65.5)], 1.0, '+5V')
seg(F, [pad('D_TVS1','1'), (132.5, 84.5)], 1.5, '+5V')
seg(F, [pad('U3','5'), (148.45, 78.5)], 0.4, '+5V')
seg(F, [(156.4, 86.0), (163.0, 86.0), (164.5, 87.5), pad('R0','1')], 0.5, '+5V')
# SW node: regulator OUT -> catch diode K -> inductor
seg(F, [(137.7, 61.8), (137.7, 60.6), (137.2, 60.1), pad('D2','1')], 1.2, '/SW')
seg(F, [pad('D2','1'), pad('L1','1')], 1.5, '/SW')
# +3V3 trunk: L1 -> COUT2 -> COUT1 -> ESP32 3V3
seg(F, [pad('L1','2'), (145.0, 54.7), (145.0, 47.2), pad('COUT1','1')], 1.0, '+3V3')
seg(F, [(145.0, 50.4), pad('COUT2','1')], 1.0, '+3V3')
seg(F, [pad('COUT1','1'), (145.64, 45.0), (147.1, 43.48), pad('U1','2')], 0.6, '+3V3')
# status LED: R0 -> D1
seg(F, [pad('R0','2'), pad('D1','2')], 0.3, 'Net-(D1-A)')

# ---------------------------------------------------------------- GND: vias beside the pads (no via-in-pad)
seg(F, [pad('D2','2'), (137.2, 51.6), (138.0, 50.4), pad('COUT2','2')], 1.0, 'GND')
via((137.2, 51.6), 'GND'); via((136.2, 51.0), 'GND'); seg(F, [(137.2, 51.6), (136.2, 51.0)], 0.6, 'GND')
seg(F, [pad('C3','2'), (140.7, 46.3), pad('COUT1','2')], 0.8, 'GND'); via((140.7, 46.3), 'GND')
gnd_stub(pad('Rbot1','2'), (133.5, 54.6))
gnd_stub(pad('U4','5'), (132.6, 60.6))
seg(F, [(136.0, 65.5), (136.0, 69.0)], 1.0, 'GND')   # GND pin -> tab
seg(F, [pad('CIN1','2'), (144.4, 62.76), pad('C2','2')], 0.8, 'GND'); via((144.4, 62.76), 'GND')
gnd_stub(pad('D_TVS1','2'), (131.0, 79.6), 0.8)
gnd_stub(pad('D1','1'), (165.9, pad('D1','1')[1]), 0.4)
for x in (133.0, 136.0, 139.0):          # thermal vias under the regulator tab
    for y in (70.0, 73.0, 76.0):
        via((x, y), 'GND')
gnd_stub(pad('U1','1'), (147.2, 42.0), 0.4)
gnd_stub(pad('U1','38'), (166.05, 41.2), 0.4)
gnd_stub(pad('U1','15'), (150.4, 59.6), 0.4)   # under the module edge, tented
seg(F, [pad('U1','15'), (151.59, 57.0), (154.4, 54.2), pad('U1','39_7')], 0.4, 'GND')  # pocket between DTR/RTS/+3V3: tie to the module GND pad
gnd_stub(pad('C4','2'), (159.9, 65.2), 0.4)
gnd_stub(pad('U3','2'), (148.45, 73.43), 0.3)  # under the IC body, between pad rows
for sw in ('SW1', 'SW2'):
    seg(F, [pad(sw, '2', 0), pad(sw, '2', 1)], 0.3, 'GND')
seg(F, [pad('SW2', '2', 1), (148.3, 36.825), pad('SW1', '2', 0)], 0.3, 'GND'); via((148.3, 36.825), 'GND')
for sw, n in (('SW1', '/IO0'), ('SW2', '/EN')):
    seg(F, [pad(sw, '1', 0), pad(sw, '1', 1)], 0.3, n)
# U1 thermal pad: tie the former 40_x via pads to the GND grid (see fixpcb)
u1 = fps['U1']
smd = [p for p in u1.Pads() if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD and p.GetNumber().startswith('39_')]
for p in u1.Pads():
    if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH and p.GetNumber() == '39_5':
        for q in smd:   # every SMD sub-pad adjacent (0.7 mm) to this via pad
            if (q.GetPosition() - p.GetPosition()).EuclideanNorm() < MM(0.75):
                seg(F, [(mm(p.GetPosition().x), mm(p.GetPosition().y)), (mm(q.GetPosition().x), mm(q.GetPosition().y))], 0.3, 'GND')

# ---------------------------------------------------------------- auto-reset: DTR/RTS from J3, crossed once
DTR, RTS = 'Net-(IO0_CTRL1-E)', 'Net-(EN_CTRL1-E)'
# DTR: B.Cu lane x=144.9, hop to F.Cu below L1, then R2.2 (F.Cu) and IO0_CTRL1 emitter (B.Cu)
seg(B, [pad('J3','5'), (141.94, 44.2), (144.9, 47.2), (144.9, 61.0)], 0.25, DTR); via((144.9, 61.0), DTR)
seg(F, [(144.9, 61.0), (147.2, 61.0), (148.7, 61.3)], 0.25, DTR); via((148.7, 61.3), DTR)
seg(F, [(148.7, 61.3), (151.0, 61.3), (151.55, 61.85), pad('R2','2')], 0.25, DTR)
seg(B, [(148.7, 61.3), (148.7, 69.7), (151.3, 69.7)], 0.25, DTR); via((151.3, 69.7), DTR)
seg(F, [(151.3, 69.7), pad('IO0_CTRL1','2')], 0.25, DTR)
# RTS: B.Cu lane x=145.8 down, R1.1 via a short F.Cu stub, then around the bottom to EN_CTRL1 emitter
seg(B, [pad('J3','6'), (145.8, 44.1), (145.8, 58.8), (147.3, 60.3), (147.3, 62.48)], 0.25, RTS); via((147.3, 62.48), RTS)
seg(F, [(147.3, 62.48), pad('R1','1')], 0.25, RTS)
seg(B, [(147.3, 62.48), (147.3, 70.5), (157.8, 70.5), (157.8, 69.3)], 0.25, RTS); via((157.8, 69.3), RTS)
seg(F, [(157.8, 69.3), pad('EN_CTRL1','2')], 0.25, RTS)
# IO13 (LED data): U1 pad 16 -> R5, on B.Cu between the DTR lane and the transistors
IO13 = 'Net-(U1-IO13)'
seg(F, [pad('U1','16'), (152.85, 61.2)], 0.25, IO13); via((152.85, 61.2), IO13)
seg(B, [(152.85, 61.2), (152.85, 63.25), (149.5, 66.6), (149.5, 67.4)], 0.25, IO13); via((149.5, 67.4), IO13)
seg(F, [(149.5, 67.4), pad('R5','1')], 0.25, IO13)

# ---------------------------------------------------------------- remaining signals (hand-routed, proven paths)
W = 0.25
TX, RX = 'Net-(J3-TX0)', 'Net-(J3-RX0)'
seg(F, [pad('J3','3'), (139.39, 40.25), (156.10, 40.25), (161.87, 46.02), pad('U1','35')], 0.2, TX)
seg(F, [pad('J3','4'), (141.48, 40.70), (154.57, 40.70), (161.16, 47.29), pad('U1','34')], 0.2, RX)
# EN: ESP32 pin 3 -> (B.Cu under the module) -> C4, R4, EN_CTRL1 collector; B.Cu hop up to RESET
seg(F, [pad('U1','3'), (147.1, 44.9)], W, '/EN'); via((147.1, 44.9), '/EN')
seg(B, [(147.1, 44.9), (150.2, 48.0), (150.2, 48.88), (160.9, 59.58), (160.9, 61.3)], W, '/EN'); via((160.9, 61.3), '/EN')
seg(F, [(160.9, 61.3), pad('C4','1'), (161.8, 63.32), (161.8, 68.28)], W, '/EN')
seg(B, [(147.1, 44.9), (147.9, 44.1), (147.9, 39.5)], W, '/EN'); via((147.9, 39.5), '/EN')
seg(F, [(147.9, 39.5), pad('SW2','1',1)], W, '/EN')
seg(F, [pad('EN_CTRL1','3'), (161.8, 68.28)], W, '/EN')
seg(F, [pad('R4','1'), (160.9, 67.28), pad('EN_CTRL1','3')], W, '/EN')
# IO0: ESP32 pin 25 -> (B.Cu) -> R3, IO0_CTRL1 collector; B.Cu up the right side to BOOT
seg(F, [pad('U1','25'), (166.05, 60.0)], W, '/IO0'); via((166.05, 60.0), '/IO0')
seg(B, [(166.05, 60.0), (163.85, 62.2), (163.85, 66.2), (155.4, 66.2)], W, '/IO0'); via((155.4, 66.2), '/IO0')
seg(F, [(155.4, 66.2), pad('R3','1')], W, '/IO0')
seg(B, [(155.4, 66.2), (155.6, 68.6)], W, '/IO0'); via((155.6, 68.6), '/IO0')
seg(F, [(155.6, 68.6), pad('IO0_CTRL1','3')], W, '/IO0')
seg(B, [(166.05, 60.0), (164.4, 58.35), (164.4, 42.4), (160.2, 38.97)], W, '/IO0'); via((160.2, 38.97), '/IO0')
seg(F, [(160.2, 38.97), pad('SW1','1',1)], W, '/IO0')
# transistor bases
seg(F, [pad('R1','2'), (148.40, 64.61), (149.31, 64.61), (152.03, 67.33), pad('IO0_CTRL1','1')], W, 'Net-(IO0_CTRL1-B)')
seg(F, [pad('R2','1'), (151.90, 64.28), (154.95, 67.33), pad('EN_CTRL1','1')], W, 'Net-(EN_CTRL1-B)')
# LED data: R5 -> U3 -> J2 pin 1
seg(F, [pad('R5','2'), (147.5, 70.3), (149.4, 70.3), pad('U3','1')], W, 'Net-(R5-Pad2)')
seg(F, [pad('U3','6'), (150.40, 75.78), pad('J2','1')], W, 'Net-(J2-Pin_1)')

# FB divider
seg(F, [(134.3, 62.0), (134.3, 59.0), pad('Rbot1','1'), pad('Rtop1','1')], 0.3, '/FB_NODE')
# +3V3 branches: C3, J3 pin 2, Rtop1, pull-ups R3/R4
V33 = '+3V3'
seg(F, [pad('C3','1'), (136.46, 44.6), (145.2, 44.6), (145.64, 45.0)], 0.5, V33)
seg(F, [(136.46, 44.6), (135.5, 44.6), pad('J3','2')], 0.5, V33)
seg(F, [pad('Rtop1','2'), (130.8, 46.0), (131.3, 45.5), (133.4, 43.7), pad('J3','2')], 0.4, V33)
seg(F, [(145.0, 53.0), (146.6, 53.0)], 0.5, V33); via((146.6, 53.0), V33)
seg(B, [(146.6, 53.0), (152.3, 58.7), (153.9, 60.3), (153.9, 61.3)], 0.5, V33); via((153.9, 61.3), V33)
seg(F, [(153.9, 61.3), pad('R3','2'), pad('R4','2')], 0.4, V33)

# ---------------------------------------------------------------- credit text: original front position
for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetText().startswith('BARLAROK'):
        d.SetLayer(pcbnew.F_SilkS); d.SetMirrored(False)
        d.SetText(d.GetText().replace('HW Rev 1.03', 'HW Rev 2.0'))
        c = d.GetBoundingBox().GetCenter()
        d.Move(pcbnew.VECTOR2I(MM((159.970 + 166.848) / 2) - c.x, MM((69.295 + 90.369) / 2) - c.y))

# ---------------------------------------------------------------- silkscreen references: small, tidy
for f in b.GetFootprints():
    t = f.Reference()
    t.SetTextSize(P(0.8, 0.8)); t.SetTextThickness(MM(0.15))   # JLCPCB minimum: 0.8 mm height, 0.15 mm line
REFPOS = {  # hand-placed where the default position hit the edge or another part
    'Rtop1': (131.0, 59.6, 0), 'Rbot1': (134.8, 57.0, 90), 'C3': (135.0, 46.3, 90), 'C2': (145.6, 67.1, 0), 'CIN1': (141.9, 63.8, 90), 'COUT1': (143.4, 47.9, 0),
    'Polyfuse1': (133.0, 97.0, 0), 'U1': (157.3, 62.3, 0) if False else None,
}
for ref, v in REFPOS.items():
    if v:
        t = fps[ref].Reference(); t.SetPosition(P(v[0], v[1])); t.SetTextAngleDegrees(v[2])
fps['U1'].Reference().SetPosition(P(157.3, 45.0))
for ref in ('SW1', 'SW2'):   # designator under the switch body, function name beside it
    fps[ref].Reference().SetPosition(fps[ref].GetPosition()); fps[ref].Reference().SetTextAngleDegrees(0)
for txt, x in (('RESET', 139.4), ('BOOT', 157.2)):
    t = pcbnew.PCB_TEXT(b); t.SetText(txt); t.SetLayer(pcbnew.F_SilkS); t.SetPosition(P(x, 37.9))
    t.SetTextSize(P(1.0, 1.0)); t.SetTextThickness(MM(0.15)); b.Add(t)
for d in b.GetDrawings():   # J3 pin labels were 0.5 mm high: below the fab minimum
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS and d.GetText().strip() in ('GND', '3v3', 'TX0', 'RX0', 'DTR', 'RTS'):
        d.SetTextSize(P(0.8, 0.8)); d.SetTextThickness(MM(0.15))
        name = d.GetText().strip(); d.SetText(name)                      # centred over its pin
        x = {'GND': 131.78, '3v3': 134.32, 'TX0': 136.86, 'RX0': 139.40, 'DTR': 141.94, 'RTS': 144.48}[name]
        d.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER); d.SetPosition(P(x, 41.0))
filler = pcbnew.ZONE_FILLER(b); filler.Fill(b.Zones())

pcbnew.SaveBoard(OUT, b)
print('saved', OUT)
