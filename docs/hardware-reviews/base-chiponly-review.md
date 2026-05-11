# Design Review — BaseChipOnly
Date: 2026-03-28 | Automated review with KiCad Skill

---

## ⛔ SHORT-CIRCUIT ROOT CAUSE — FOUND

The short circuit is caused by **vias placed on the wrong pad** of multiple decoupling capacitors.
In all cases, the GND via landed on the supply rail pad (pad 1) instead of the GND pad (pad 2).
During soldering, solder wicks into the via hole and shorts the supply rail to the GND plane on B.Cu.

---

## CONFIRMED SHORT CIRCUITS

| Component | Pad | Net on pad | Net on via | Distance | Effect |
|---|---|---|---|---|---|
| **C2** (100nF) | 1 | **+5V** | GND | 0.000 mm | **+5V shorted to GND** |
| **COUT1** (47µF) | 1 | **+3V3** | GND | 0.037 mm | **+3V3 shorted to GND** |
| **COUT1** (47µF) | 2 | **GND** | +3V3 | 0.038 mm | (same via, opposite direction) |
| **C3** (100nF) | 1 | **+3V3** | GND | 0.101 mm | **+3V3 shorted to GND (high risk)** |

### Visual explanation

```
COUT1 (47µF) — 90° orientation — center at (134.45, 47.68)

  Pad 1 → (+3V3) @ y≈46.68      ← GND VIA @ y=46.645  ⚠️ SHORT!
  ─────────────────────────────
  Capacitor body
  ─────────────────────────────
  Pad 2 → (GND) @ y≈48.68       ← +3V3 VIA @ y=48.720 ⚠️ SHORT!
```

Vias were intended to connect pad 2 (GND) to the GND plane on B.Cu, but were placed on pad 1 (supply rail).

---

## ADDITIONAL SHORT CIRCUITS (signal)

| Component | Pad | Net on pad | Net on via | Distance | Effect |
|---|---|---|---|---|---|
| **Rbot1** (1.2k) | 1 | /FB_NODE | GND | 0.071 mm | FB_NODE shorted to GND → regulator out of control |
| **Rbot1** (1.2k) | 2 | GND | /FB_NODE | 0.000 mm | (same via, opposite direction) |
| **Rtop1** (2.0k) | 2 | +3V3 | /FB_NODE | 0.000 mm | +3V3 directly connected to FB → wrong Vout |

> **Rbot/Rtop consequence**: the LM2596S FB node is pulled to GND by the misplaced via on Rbot1.
> The regulator would raise the output voltage to maximum, potentially damaging the ESP32.

---

## HOW TO DIAGNOSE THE SHORT ON AN ASSEMBLED BOARD

### Quick diagnosis with multimeter

1. **Disconnect power**
2. Measure resistance between **+5V and GND**:
   - if < 10 Ω → C2 is almost certainly shorted (GND via on +5V pad)
3. Measure resistance between **+3V3 and GND**:
   - if < 10 Ω → COUT1 or C3 is shorted

### Where to look on the board

Use a magnifier or microscope and inspect:

| Component | PCB position | What to look for |
|---|---|---|
| **C2** (100nF) | x=142.4, y=76.3 | Solder in via hole next to top pad (+5V) |
| **COUT1** (47µF) | x=134.5, y=47.7 | Solder in via holes on both pads |
| **C3** (100nF) | x=131.5, y=47.7 | Solder in via hole next to top pad (+3V3) |

> Note: all three capacitors are oriented at 90°. Pad 1 (+5V or +3V3) is the top pad (lower y value). The problematic via is on the top edge of the component.

### Rework on an assembled board

1. Desolder C2, COUT1, C3 one at a time
2. Use desoldering wick + flux to clean pads and especially the via holes
3. Verify with multimeter that the short is gone before resoldering
4. Resolder carefully, preventing solder from wicking into the vias adjacent to the supply pad

---

## PCB FILE FIX (KiCad)

For each affected capacitor, move the GND via from pad 1 to pad 2:

**COUT1** (47µF):
- Delete GND via at (134.45, 46.645) — was on pad 1 (+3V3)
- Delete +3V3 via at (134.45, 48.720) — was on pad 2 (GND)
- Add a GND via adjacent to pad 2 (y ≈ 48.68) to connect to B.Cu GND plane
- The +3V3 via is not needed (+3V3 plane is on F.Cu, not B.Cu)

**C2** (100nF):
- Delete GND via at (142.4, 75.282) — was on pad 1 (+5V)
- Add GND via adjacent to pad 2 (y ≈ 77.28)

**C3** (100nF):
- Delete GND via at (131.4, 46.782) — was on pad 1 (+3V3)
- Add GND via adjacent to pad 2 (y ≈ 48.70)

**Rbot1** (1.2k):
- Delete GND via at (131.4, 50.932) — was on pad 1 (FB_NODE)
- Remove /FB_NODE via on pad 2 (131.35, 52.882) — no via needed on a GND pad

---

## ADDITIONAL SCHEMATIC ISSUES

### USBLC6-2SC6 (U3) — GND pin unconnected ⚠️
Pin 2 (GND) of the USBLC6-2SC6 is not connected to the GND net in the schematic.
VBUS (pin 5) and I/O2 (pins 3, 4) are also floating.
Only I/O1 (pins 1 and 6) is connected.

**Effect**: the ESD protection circuit is non-functional. The USBLC6-2SC6 requires GND and VBUS
to be connected. Without GND, the internal clamping diodes have no reference.

**Fix**: connect pin 2 to GND and pin 5 to +5V (VBUS). Also connect pins 3/4 (I/O2) to the
second USB data line if this is a full USB interface.

### SMF5.0A with bidirectional TVS symbol ⚠️
The KiCad symbol used (`Device:D_TVS`) is classified as **bidirectional** (pins A1, A2),
but the SMF5.0A is **unidirectional** (suffix "A" = unidirectional; "CA" = bidirectional).

Current connection: A1→+5V, A2→GND.
In `Diode_SMD:D_SMA`, pad 1 = cathode, pad 2 = anode (KiCad convention).
Therefore: **cathode→+5V, anode→GND → reverse bias = correct for a TVS on +5V**.

The part is electrically connected correctly, but using a bidirectional symbol for a unidirectional
component can cause confusion during BOM ordering and assembly.
**Recommendation**: use `Device:D_Zener` or `Device:D_TVS_Unidirectional` with the correct part number.

> **Note on Reference/Value in PCB**: many components have Reference and Value fields swapped
> in the PCB file (e.g. Reference="470Ω", Value="R0" instead of Reference="R0", Value="470Ω").
> No electrical impact, but it confuses annotation, silkscreen, and BOM generation.

### Polyfuse (12A) oversized ⚠️
The 12A polyfuse does not protect the LM2596S (3A max) or the ESP32. Replace with 1–2A.

### LM2596S Vout slightly high ℹ️
With Rtop=2.0k, Rbot=1.2k, Vref=1.285V:
`Vout = 1.285 × (1 + 2.0/1.2) = 3.43V` instead of 3.3V (+3.9%).

Within tolerance for most systems, but verify the ESP32 can handle this voltage.
For exactly 3.3V, use Rbot=1.1k (Vout = 1.285 × 2.818 = 3.32V).

### +3V3 traces too narrow ⚠️
All +3V3 traces are **0.2mm**. A 3A regulator needs at least 0.6–1.0mm.
At 0.2mm on 2oz copper the safe current is ~0.5A. Widen power traces.

---

## PRIORITY SUMMARY

| Priority | Issue | Action |
|---|---|---|
| 🔴 CRITICAL | GND via on C2 pad +5V | Remove via, repair short |
| 🔴 CRITICAL | GND via on COUT1 pad +3V3 | Remove via, repair short |
| 🔴 CRITICAL | GND via on C3 pad +3V3 | Remove via, repair short |
| 🟠 HIGH | GND via on Rbot1 pad FB_NODE | Fix routing, risk of regulator damage |
| 🟠 HIGH | USBLC6-2SC6 GND floating | Connect pin 2→GND, pin 5→+5V |
| 🟡 MEDIUM | +3V3 traces at 0.2mm | Widen to ≥0.6mm in PCB |
| 🟡 MEDIUM | Polyfuse 12A too large | Replace with 1–2A |
| 🟡 MEDIUM | Reference/Value swapped in PCB | Fix annotation |
| 🔵 LOW | Vout 3.43V instead of 3.3V | Adjust Rbot optionally |
| 🔵 LOW | SMF5.0A on bidirectional symbol | Use correct symbol |
