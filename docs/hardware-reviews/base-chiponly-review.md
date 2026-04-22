# Design Review — BaseChipOnly
Data: 2026-03-28 | Revisione automatica con KiCad Skill

---

## ⛔ CAUSA DEL CORTO — TROVATA

Il cortocircuito è causato da **vias piazzate sul pad sbagliato** di più condensatori di disaccoppiamento.
In tutti i casi, la via GND è finita sul pad del rail di alimentazione (pad 1) invece che sul pad GND (pad 2).
Quando si salda, lo stagno scola nel foro della via e cortocircuita il rail di alimentazione con la massa del piano B.Cu.

---

## CORTOCIRCUITI CONFERMATI

| Componente | Pad | Rete pad | Rete via | Distanza | Effetto |
|---|---|---|---|---|---|
| **C2** (100nF) | 1 | **+5V** | GND | 0.000 mm | **+5V in corto con GND** |
| **COUT1** (47µF) | 1 | **+3V3** | GND | 0.037 mm | **+3V3 in corto con GND** |
| **COUT1** (47µF) | 2 | **GND** | +3V3 | 0.038 mm | (stessa via al contrario) |
| **C3** (100nF) | 1 | **+3V3** | GND | 0.101 mm | **+3V3 in corto con GND (rischio alto)** |

### Spiegazione visiva

```
COUT1 (47µF) — orientamento 90° — centro a (134.45, 47.68)

  Pad 1 → (+3V3) @ y≈46.68      ← VIA GND @ y=46.645  ⚠️ CORTO!
  ─────────────────────────────
  Corpo condensatore
  ─────────────────────────────
  Pad 2 → (GND) @ y≈48.68       ← VIA +3V3 @ y=48.720 ⚠️ CORTO!
```

Le vias dovevano andare sul pad 2 (GND) per raccordarsi al piano GND su B.Cu, ma
sono state posizionate sul pad 1 (rail di alimentazione).

---

## CORTOCIRCUITI AGGIUNTIVI (segnale)

| Componente | Pad | Rete pad | Rete via | Distanza | Effetto |
|---|---|---|---|---|---|
| **Rbot1** (1.2k) | 1 | /FB_NODE | GND | 0.071 mm | FB_NODE in corto con GND → regolatore fuori controllo |
| **Rbot1** (1.2k) | 2 | GND | /FB_NODE | 0.000 mm | (stessa via al contrario) |
| **Rtop1** (2.0k) | 2 | +3V3 | /FB_NODE | 0.000 mm | +3V3 collegato direttamente a FB → Vout errata |

> **Conseguenza Rbot/Rtop**: il nodo FB del LM2596S viene tirato a GND dalla via sbagliata su Rbot1.
> Il regolatore alzerebbe la tensione in uscita al massimo (potenziale danno all'ESP32).

---

## COME TROVARE IL CORTO SULLA SCHEDA SALDATA

### Diagnosi rapida con multimetro

1. **Scollegare l'alimentazione**
2. Misurare resistenza tra **+5V e GND**:
   - se < 10 Ω → C2 quasi certamente in corto (via GND sul pad +5V)
3. Misurare resistenza tra **+3V3 e GND**:
   - se < 10 Ω → COUT1 o C3 in corto

### Dove guardare sulla scheda

Con lente o microscopio, controllare:

| Componente | Posizione PCB | Cosa cercare |
|---|---|---|
| **C2** (100nF) | x=142.4, y=76.3 | Stagno nel foro via accanto al pad superiore (+5V) |
| **COUT1** (47µF) | x=134.5, y=47.7 | Stagno nei fori via su entrambi i pad |
| **C3** (100nF) | x=131.5, y=47.7 | Stagno nel foro via accanto al pad superiore (+3V3) |

> Nota: tutti e tre i condensatori sono orientati a 90°. Il pad 1 (+5V o +3V3) è quello
> in alto (y minore). La via problematica è sul bordo superiore del componente.

### Riparazione sulla scheda saldata

1. Dissaldare i condensatori C2, COUT1, C3 uno alla volta
2. Con pasta dissaldante (flux + wick), ripulire i pad e soprattutto i fori delle vias
3. Verificare con multimetro che il corto sia scomparso prima di risaldare
4. Risaldare con attenzione, evitando che lo stagno scoli nelle vias vicine al pad di alimentazione

---

## CORREZIONE NEL FILE PCB (KiCad)

Per ogni condensatore con il problema, spostare la via GND dal pad 1 al pad 2:

**COUT1** (47µF):
- Eliminare la via GND a (134.45, 46.645) — era su pad 1 (+3V3)
- Eliminare la via +3V3 a (134.45, 48.720) — era su pad 2 (GND)
- Aggiungere una via GND adiacente al pad 2 (y ≈ 48.68) per il raccordo con B.Cu
- La via +3V3 non serve (il piano +3V3 è su F.Cu, non B.Cu)

**C2** (100nF):
- Eliminare la via GND a (142.4, 75.282) — era su pad 1 (+5V)
- Aggiungere via GND adiacente al pad 2 (y ≈ 77.28)

**C3** (100nF):
- Eliminare la via GND a (131.4, 46.782) — era su pad 1 (+3V3)
- Aggiungere via GND adiacente al pad 2 (y ≈ 48.70)

**Rbot1** (1.2k):
- Eliminare la via GND a (131.4, 50.932) — era su pad 1 (FB_NODE)
- La via /FB_NODE su pad 2 (131.35, 52.882) va rimossa (non serve via su pad GND)

---

## ALTRI PROBLEMI DELLO SCHEMA

### USBLC6-2SC6 (U3) — Pin GND non collegato ⚠️
Il pin 2 (GND) della USBLC6-2SC6 non è connesso alla rete GND nello schema.
Anche VBUS (pin 5) e I/O2 (pin 3, 4) sono flottanti.
Solo I/O1 (pin 1 e 6) è utilizzato.

**Effetto**: la protezione ESD è non funzionale. La USBLC6-2SC6 richiede GND e VBUS
collegati per funzionare. Senza GND, i diodi interni non hanno riferimento.

**Fix**: collegare pin 2 a GND e pin 5 a +5V (VBUS) nello schema. Collegare anche
pin 3/4 (I/O2) alla seconda linea dati USB se si tratta di un'interfaccia USB full.

### SMF5.0A con simbolo TVS bidirezionale ⚠️
Il simbolo KiCad usato (`Device:D_TVS`) è classificato come **bidirezionale** (pin A1, A2),
ma il componente SMF5.0A è **unidirezionale** (suffix "A" = unidirectional; "CA" = bidirectional).

Il collegamento attuale: A1→+5V, A2→GND.
In `Diode_SMD:D_SMA`, pad 1 = catodo, pad 2 = anodo (convenzione KiCad).
Quindi: **catodo→+5V, anodo→GND → polarizzazione inversa = corretto per una TVS su +5V**.

Il componente sembra collegato nella direzione giusta elettricamente, ma l'uso del simbolo
bidirezionale per una parte unidirezionale può creare confusione in fase di ordine/assemblaggio.
**Raccomandazione**: usare `Device:D_Zener` o `Device:D_TVS_Unidirectional` con il
part number corretto.

> **Nota su Reference/Value nel PCB**: molti componenti hanno i campi Reference e Value
> invertiti nel file PCB (es. Reference="470Ω", Value="R0" invece di Reference="R0", Value="470Ω").
> Questo non causa problemi elettrici ma confonde l'annotazione, il silkscreen e il BOM.

### Polyfuse (12A) sovradimensionata ⚠️
La polyfuse da 12A non protegge il LM2596S (max 3A) né l'ESP32. Sostituire con 1A–2A.

### Tensione Vout LM2596S leggermente alta ℹ️
Con Rtop=2.0k, Rbot=1.2k, Vref=1.285V:
`Vout = 1.285 × (1 + 2.0/1.2) = 3.43V` invece di 3.3V (+3.9%).

Entro la tolleranza di molti sistemi, ma verificare se l'ESP32 supporta questa tensione.
Per avere esattamente 3.3V usare Rbot=1.1k (Vout = 1.285 × 2.818 = 3.32V).

### Tracce +3V3 troppo sottili ⚠️
Tutte le tracce +3V3 sono a **0.2mm**. Per un regolatore da 3A, serve almeno 0.6–1.0mm.
Con 0.2mm su 2oz rame si raggiungono ~0.5A in sicurezza. Ampliare le tracce di alimentazione.

---

## RIEPILOGO PRIORITÀ

| Priorità | Problema | Azione |
|---|---|---|
| 🔴 CRITICO | Via GND su C2 pad +5V | Rimuovere via, riparare corto |
| 🔴 CRITICO | Via GND su COUT1 pad +3V3 | Rimuovere via, riparare corto |
| 🔴 CRITICO | Via GND su C3 pad +3V3 | Rimuovere via, riparare corto |
| 🟠 ALTO | Via GND su Rbot1 pad FB_NODE | Correggere routing, rischio danno regolatore |
| 🟠 ALTO | USBLC6-2SC6 GND flottante | Collegare pin 2→GND, pin 5→+5V |
| 🟡 MEDIO | Tracce +3V3 0.2mm | Ampliare a ≥0.6mm nel PCB |
| 🟡 MEDIO | Polyfuse 12A troppo grande | Sostituire con 1–2A |
| 🟡 MEDIO | Reference/Value invertiti nel PCB | Correggere annotation |
| 🔵 BASSO | Vout 3.43V invece di 3.3V | Aggiustare Rbot opzionalmente |
| 🔵 BASSO | SMF5.0A su simbolo bidirezionale | Usare simbolo corretto |
