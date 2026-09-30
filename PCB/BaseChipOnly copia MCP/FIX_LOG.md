# BaseChipOnly — Log fix pre-fab

## ✅ Sessione 2026-09-30 (seconda parte) — layout rifatto, polyfuse 4 A, foglie analizzate

**Il PCB del progetto è ora il nuovo layout ordinato.** Verifiche sul file del progetto:
- DRC con parità schematico: **0 errori elettrici, 0 non connessi, 0 differenze di parità** (restano i 12 fori 0.2 mm dei via termici ESP32, uguali alla scheda già prodotta, e 6 avvisi solo estetici di serigrafia: logo retro + etichetta COUT1).
- Gerber X2 del nuovo `F_Cu`: **120 pad controllati contro lo schematico, 0 differenze.**
- File di produzione rigenerati in `Esportazione-2026-09-30/` (+ anteprime `preview-front-copper.png` / `preview-back-copper.png`).

Cosa è cambiato:
- Foglie (`PCB/Foglia`, solo analizzate): 15 WS2812B ciascuna, 9 in parallelo = 135 LED, fino a ~7.4 A a bianco pieno → alimentatore 5 V 4 A + limitatore WLED a 3000 mA. Spiegazione completa: `docs/base-chiponly-pcb.md`.
- Polyfuse → **MF-LSMF400/12X** (4 A hold / 8 A trip, 12 V, 2920), schematico e PCB.
- Layout a blocchi: regolatore con pin in alto e anello di commutazione cortissimo, ingresso/protezioni in basso a sinistra, bus +5V da 3 mm, auto-reset sotto l'ESP32, **pulsanti RESET/BOOT in alto accanto a J3** con scritte in serigrafia, piano GND pieno sul retro, via GND sempre accanto ai pad (mai dentro). Contorno, fori, J1/J2/J3/U1/C1 invariati (il case stampato va ancora bene). Scritta "BARLAROK…" rimessa nella posizione originale sul fronte.
- Tutto il routing è fatto a mano in `BaseChipOnly-backups/relayout-work/relayout.py`, ricostruibile con `build.sh` partendo da `BaseChipOnly-after-fixes-2026-09-30.kicad_pcb`. Versione precedente del PCB: `BaseChipOnly-backups/BaseChipOnly-before-relayout.kicad_pcb`.

Ancora da fare: controllo finale in KiCad GUI, prova al banco dell'auto-reset con esptool, misure sul LED D1 della scheda attuale.

## ✅ Sessione 2026-09-30 — tutti i fix applicati a schematico **e** PCB

**Stato: sorgenti corretti e verificati. Pronto per una revisione finale in KiCad GUI e poi per l'ordine — ma NON ancora testato su hardware.** Le sezioni più sotto (2026-09-28) sono storiche: diverse affermazioni lì sono superate (vedi "Correzioni al log precedente").

Backup pre-sessione: `BaseChipOnly-backups/pre-2026-09-30/`. Lo script che applica tutte le modifiche PCB partendo da quel backup: `BaseChipOnly-backups/fixpcb_2026-09-30.py` (rieseguibile).
Nuovi file di produzione (Gerber, drill, BOM, posizioni, PDF montaggio con valori, PDF schematico): `Esportazione-2026-09-30/`. La vecchia `Esportazione/` non è stata toccata (corrisponde alla scheda già prodotta).

### Schematico (via MCP KiCad)
| # | Fix | Dettaglio |
|---|---|---|
| 9 | TVS | `D_TVS1` → simbolo unidirezionale `Diode:SMAJ5.0A` (SMA). SMF5.0A è in package SOD-123F e non corrispondeva al footprint D_SMA. Catodo (pin 1) su +5V. |
| 4 | L1 | 100µH **Bourns SRN6045TA-101M** (Isat 1.33 A, Irms 0.92 A, DCR 456 mΩ — da datasheet), footprint `L_Bourns_SRN6045TA`. L'MPN precedente (SRP1245A, 12.5 mm) non entrava nel 1210. |
| 5 | Polyfuse1 | 1.5 A hold / 3 A trip, **MF-MSMF150/8X** (8 V, 1812 — da datasheet). MF-RX150 era un radiale THT, incompatibile con lo 0603. ⚠️ Il polyfuse alimenta anche la striscia LED (J2): scegliere la taglia in base all'assorbimento reale della striscia (la serie MSMF arriva a 2.5 A in 1812). |
| 3b | Pulsanti | SW1 **BOOT** (IO0→GND), SW2 **RESET** (EN→GND), C&K PTS810. Reti nominate `IO0` ed `EN`. |
| 10 | COUT2 | 220 µF 6.3 V tantalio case C (6032), in parallelo a COUT1 su +3V3. ESR 0.1–0.5 Ω (non polimero ultra-low-ESR). |
| nuovo | U3 VBUS | Pin 5 di USBLC6 collegato a +5V (riferimento del clamp ESD). |
| — | Rtop1 | Footprint 1210 → 0805 (serve spazio per L1 più grande). |
| — | ERC | No-connect sui 31 pin inutilizzati + PWR_FLAG su +5V/GND/+3V3: **ERC da 39 errori a 0** (restano solo warning di librerie esterne e 6 fili fuori griglia della sessione precedente). |

D1, D2 e circuito auto-reset erano già corretti sullo schematico (sessione 2026-09-28); verificati di nuovo via netlist.

### PCB
| # | Fix |
|---|---|
| 8 | Reference/Value rimessi a posto su tutti i footprint (Reference su F.Silkscreen, Value su F.Fab) e **ricollegati ai simboli dello schematico** (UUID). La parità schematico↔PCB ora è pulita: prima 23 footprint "extra", 19 "mancanti", 20 conflitti di rete. Update-PCB-from-Schematic torna utilizzabile. Per il montaggio a mano: `Esportazione-2026-09-30/BaseChipOnly-assembly-values.pdf` (layer Fab con i valori). |
| 1 | D1 ruotato 180° → K su GND, A verso R0. |
| 2 | D2 ruotato 180° → K su /SW, A su GND (la serigrafia ora è corretta). |
| 3 | Auto-reset rifatto sul rame: RTS → R1 (base IO0_CTRL1) + emettitore EN_CTRL1; DTR → R2 (base EN_CTRL1) + emettitore IO0_CTRL1. Incrocio DTR/RTS con un ponticello su B.Cu; IO13 ri-instradato su B.Cu per liberare il canale; DTR/RTS a 0.15 mm dove corrono a passo 0.4 mm accanto a /SW. |
| 3b | SW1/SW2 sul bordo destro (vicino a J2), vias GND sul piano B.Cu. La scritta "BARLAROK / SmartPlant Trunk / Designed by…" spostata sulla serigrafia **retro** (specchiata, zona x 130–137 / y 65–87) per liberare lo spazio. |
| 4 | L1 nuovo footprint 6×6 mm, COUT1 spostato di 0.5 mm, Rtop1 0805 riposizionato sotto L1; +3V3/SW/FB ri-collegati. Tratti /SW verso L1 e D2 allargati a 0.5 mm. |
| 5 | Polyfuse 1812 in linea con le piste da 3 mm esistenti. |
| 6 | U3 pin 2 → via GND; pin 5 (VBUS) → pista +5V. |
| 7 | Tutte le piste +3V3 portate a 0.5 mm (erano 0.2). |
| 10 | COUT2 in alto a sinistra, collegato a J3 pin 2 (+3V3) e via GND. |
| — | Footprint ESP32: i 12 fori termici del pad esposto (`40_x`) non avevano rete → ora GND. Eliminati 27 errori di clearance, 24 solder-mask-bridge e un "non connesso" preesistenti. |
| — | Serigrafia "GDN" → "GND" (J1 e J2). |

### Verifiche (tutte ripetute sul file finale)
- **Netlist**: diff prima/dopo — cambiano solo le connessioni volute (COUT2, SW1, SW2, U3.5); nessuna fusione di reti.
- **ERC**: 0 errori.
- **DRC con parità schematico** (`kicad-cli pcb drc --schematic-parity`): 0 clearance, 0 corti, 0 non connessi, 0 differenze di parità. Prima: 27 clearance, 23 corti, 4 non connessi, 73 problemi di parità.
- **Gerber X2** del nuovo `F_Cu`: pad→rete verificati per D1, D2, TVS, transistor, R1/R2, U3, L1, polyfuse, SW1/SW2, COUT2 — tutti come da schematico.
- **MCP** `get_component_pads`: stessa conferma per D1, D2, J3, R1, R2, IO0_CTRL1, EN_CTRL1.

### Rimane aperto
- **12 errori DRC "drill 0.2 mm"**: sono i fori termici del footprint ESP32, identici alla scheda già prodotta (la regola della board è 0.3 mm). Accettabili se il fornitore fa fori da 0.2 mm; altrimenti allargarli nel footprint.
- Warning solo estetici di serigrafia (testi sovrapposti/su rame, altezza testo) — da rifinire a mano in KiCad GUI se si vuole.
- 6 fili fuori griglia nello schematico (sessione precedente): solo igiene grafica.
- **LED D1 spento anche montato girato** (vedi `docs/hardware-reviews/base-chiponly-fixes.md`, "Open issues"): la polarità ora è giusta, ma la causa del guasto sulla scheda attuale non è ancora diagnosticata.
- **Auto-reset**: il circuito incrociato è quello standard, ma va verificato al banco con esptool prima di ordinare in quantità.
- Taglia del polyfuse rispetto alla corrente della striscia LED (vedi sopra).
- MPN di COUT2 da scegliere al momento dell'ordine.
- Le librerie `USBC` (ESP32, barrel jack, morsetto) non sono nella tabella librerie del progetto: warning ERC/DRC `footprint_link_issues`, nessun effetto sul rame.

### Correzioni al log precedente (2026-09-28)
- "L1 footprint aggiornato su schematico e PCB": **falso per il PCB** — il footprint PCB era ancora 1008. Corretto ora.
- "MPN SRP1245A-101M (1210)": l'SRP1245A misura 12.5 mm, non 1210. Sostituito.
- "MF-RX150" su footprint 0603: incompatibile (radiale THT). Sostituito.

---

# Log sessioni precedenti (2026-09-28) — storico

Progetto: `BaseChipOnly copia MCP/BaseChipOnly.kicad_pro`
Lista fix originale: batch concordato durante il bring-up 2026-07/08 (vedi memoria `basechiponly-pending-fixes`).

**Stato generale: NON pronto per una nuova produzione.** Sessione di follow-up in corso (2026-09-28, seconda parte): D2 ora corretto **sullo schematico** (verificato via netlist), ma il fix **non è ancora propagato al PCB** — vedi punto 2 aggiornato sotto per una scoperta importante che blocca la sincronizzazione automatica schema→PCB su questo progetto.

---

## Fatto e verificato (via netlist re-esportato, non solo per lettura del file)

### 4. L1 (induttore buck) — ✅ FATTO
- Valore: `100µH`, MPN proposto `SRP1245A-101M` (Bourns, 1210, Isat dichiarato ~1.5A)
- Footprint aggiornato su schematico e PCB: `Inductor_SMD:L_1210_3225Metric`
- **Da verificare ancora**: datasheet del MPN non recuperato in questa sessione (verificare Isat/DCR prima di ordinare); clearance/courtyard con COUT1 e U4 non ricontrollata dopo il cambio di footprint più grande.

### 5. Polyfuse1 (12A → 1.5A) — ✅ FATTO
- Valore: `1.5A`, MPN proposto `MF-RX150` (Bourns)
- **Da verificare**: datasheet del MPN non controllato; footprint/package non validato per compatibilità con l'impronta esistente.

### 6. U3 (USBLC6-2SC6) pin GND scollegato — ✅ FATTO e confermato
- Il pin 2 (GND) era su una rete isolata propria, non collegato al GND globale.
- Aggiunto stub/etichetta di rete: ora il pin 2 risulta correttamente sulla rete `GND`.
- Modifica additiva, a basso rischio (non toccava wire esistenti).

---

## NON fatto — bloccato deliberatamente per rischio

### 1. D1 (LED di stato invertito) — ✅ SCHEMATICO FATTO e verificato (2026-09-28, seconda sessione), PCB non ancora aggiornato
- Fix fatto a livello di wire (non rotazione): cancellati i due stub di filo ai pin di D1, ridisegnati con un piccolo detour per scambiare le connessioni senza attraversare l'altro pin (che avrebbe causato un corto pin1-pin2):
  - Filo dal ramo R0 ora arriva al pin 2 (A) invece che al pin 1 (K)
  - Filo dal simbolo GND (#PWR06) ora arriva al pin 1 (K) invece che al pin 2 (A)
- **Verificato via netlist re-esportato**: D1 ora `K→GND`, `A→(rete verso R0)→+5V`. Catena corretta: +5V → R0 → anodo → catodo → GND. Rete GND: 48 pin, rete +5V: 16 pin — nessuna fusione anomala rispetto al baseline.
- **PCB non ancora aggiornato** — stesso blocco descritto al punto 2 (sync_schematic_to_board non sicuro su questo progetto finché il punto 8 non è risolto).
- Nota indipendente dalla polarità, ancora valida: durante il bring-up il LED restava spento **anche con polarità invertita manualmente e con LED sostituito** — quindi il fix schematico non garantisce che il LED si accenda; serve comunque un retest su hardware fisico per la causa non diagnosticata.

### 2. D2 (diodo di catch SS34 invertito) — ⚠️ SCHEMATICO FATTO e verificato, PCB ancora NO
**Schematico — fatto 2026-09-28, verificato via netlist:**
- Niente rotazione automatica questa volta (quella tentata nella sessione precedente aveva quasi fuso /SW con GND — vedi nota storica sotto). Fix fatto a livello di wire, senza muovere il simbolo D2:
  1. Cancellato il filo diagonale che collegava il pin 2 (A) di D2 al nodo /SW.
  2. Spostato il simbolo di potenza `#PWR035` (GND) dalla posizione del pin 1 (K) a quella del pin 2 (A).
  3. Ridisegnato il filo dal pin 1 (K) verso il nodo /SW (giunzione con il filo esistente verso L1/U4).
- **Verificato via netlist re-esportato**: D2 ora `K→SW`, `A→GND`. Rete GND: 48 pin (nessuna fusione anomala), rete SW: 3 pin (U4 OUT, L1 pin1, D2 K) — corretto, nessun corto introdotto.

**PCB — non ancora aggiornato, e scoperto un blocco serio per la sincronizzazione automatica:**
- Ho provato a propagare la modifica al PCB con `sync_schematic_to_board` (equivalente a F8 "Update PCB from Schematic"). Il risultato è stato pericoloso: ha tentato di aggiungere **17 footprint duplicati** (inclusi un secondo D2, un secondo D_TVS1, ecc.) invece di aggiornare quelli esistenti.
- **Causa**: lo strumento abbina schematico↔PCB per *reference designator*, ma su questo PCB — a causa del bug del punto 8 — molti footprint hanno il campo **Reference interno** impostato al valore (es. il footprint di D2 ha come Reference "SS34", non "D2"), non solo la serigrafia. Quindi lo schematico "D2" non trova corrispondenza e viene aggiunto come nuovo componente orfano.
- **Non è stato salvato su disco** (il backend ha rifiutato l'auto-save perché il file PCB era cambiato esternamente nel frattempo, probabilmente perché aperto anche in KiCad GUI) — quindi nessun danno permanente. Ho ricaricato il progetto e confermato che il PCB su disco è tornato pulito (31 footprint, nessun duplicato).
- **Conclusione operativa**: finché il punto 8 (Reference/Value scambiati) non è corretto, `sync_schematic_to_board`/F8 **non è sicuro da usare su questo progetto** — rischia di duplicare footprint invece di aggiornarli. Il fix del PCB per D2 (ri-orientare il footprint fisico + eventualmente le tracce di rame già instradate sul vecchio net) va quindi fatto **manualmente**, dopo aver sistemato il punto 8.
- **Fino ad allora resta valida la nota della sessione precedente**: saldare l'SS34 con la banda del catodo sul pad inferiore (verso L1/pin2 LM2596), opposto alla serigrafia — vedi memoria `basechiponly-d2-reversed`.

*Nota storica (sessione precedente, 2026-09-28 prima parte)*: un primo tentativo aveva usato `rotate_schematic_component` per "ruotare" D2 di 180°, che invece di scambiare le reti ha fuso /SW con GND (quasi-corto). Annullato subito. Il fix di questa sessione ha evitato del tutto quel tool, usando editing esplicito dei fili — vedi memoria `kicad-mcp-rotate-tool-unreliable`.

### 3. Circuito auto-reset (DTR/RTS incrociati) — ✅ SCHEMATICO FATTO e verificato (2026-09-28, seconda sessione)
Stato di partenza confermato:
- J3 pin 5 = DTR, pin 6 = RTS
- IO0_CTRL1 base ← DTR (via R1); EN_CTRL1 base ← RTS (via R2)
- Entrambi gli emettitori → GND (bug: mai va in download mode)

**Modifiche fatte** (editing esplicito dei fili, nessuna rotazione):
1. R1 pin1: scollegato da DTR, ricollegato a RTS (J3 pin6) → base IO0_CTRL1 ora ← RTS
2. R2 pin2: scollegato da RTS, ricollegato a DTR (J3 pin5) → base EN_CTRL1 ora ← DTR
3. Emettitore IO0_CTRL1: rimosso il simbolo GND dedicato (`#PWR017`, era coincidente col pin), ricollegato a DTR (J3 pin5)
4. Emettitore EN_CTRL1: scollegato dal ramo GND, ricollegato a RTS (J3 pin6)

**Incidente rilevato e corretto durante il fix**: il primo routing del filo dell'emettitore IO0_CTRL1 verso DTR passava in verticale esattamente sopra il pin RTS di J3 (stesso x, range y che lo attraversava), **fondendo DTR e RTS in un'unica rete**. Rilevato immediatamente ri-esportando il netlist (DTR e RTS risultavano sullo stesso net), cancellato il filo e ridisegnato con una colonna x diversa che evita la fila di pin di J3. Riverificato: DTR e RTS di nuovo su reti separate.

**Verificato via netlist finale**:
- IO0_CTRL1: base←RTS (via R1), emettitore←DTR, collettore invariato (rete IO0/R3 pull-up)
- EN_CTRL1: base←DTR (via R2), emettitore←RTS, collettore invariato (rete EN/R4 pull-up)
- Corrisponde esattamente al target incrociato. Nessun emettitore più su GND.

Tabella di verità (logica diretta, non invertita, da chip USB-seriale):

| DTR | RTS | EN tirato basso (reset) | IO0 tirato basso (bootloader) |
|---|---|---|---|
| 1 | 1 | No | No |
| 1 | 0 | Sì | No |
| 0 | 1 | No | Sì |
| 0 | 0 | No | No |

**PCB non ancora aggiornato** — stesso blocco del punto 2 (sync schema→PCB non sicuro finché il punto 8 non è risolto). Il circuito di auto-reset resta corretto solo sullo schematico per ora.

### 3b. Pulsanti BOOT/RESET — ❌ NON TENTATO
Rimandato: dipende dal punto 3 (serve sapere su quali reti finali attestare i pulsanti prima di piazzarli).

### 7. Tracce +3V3 troppo strette — ❌ NON TENTATO (tempo)

### 8. Reference/Value scambiati sul silkscreen — ❌ NON CORRETTO, confermato presente
Osservato direttamente: i riferimenti mostrati sul PCB sono letteralmente i *valori* dei componenti (`12A`, `470Ω`, `2.1mm`) invece dei designatori (`Polyfuse1`, `R0`, `MountingHole1`). Questo corrompe BOM e file pick-and-place. Da correggere su tutti i 31 footprint — non fatto per tempo.

### 9. D_TVS1 (simbolo bidirezionale su SMF5.0A unidirezionale) — ❌ NON TENTATO
Stesso rischio di modifica-simbolo dei punti 1-2, rimandato.

### 10. COUT1 — aggiunta capacità bulk per stabilità anello LM2596 — ❌ NON TENTATO (tempo)

### 11. Correzione doc `docs/hardware-reviews/base-chiponly-review.md` — ❌ NON TENTATO
Percorso del documento non individuato in questa sessione (da cercare nel repo principale, fuori da questa cartella copia-MCP).

---

## Verifiche fatte

- **LM2596 Vout — calcolato, non simulato**: Vout = 1.23V × (1 + Rtop1/Rbot1) = 1.23 × (1 + 2.0k/1.2k) ≈ **3.28V**. Il partitore di feedback (Rtop1=2.0k, Rbot1=1.2k) è dimensionato correttamente, nessuna modifica necessaria lì. Nota: calcolo a mano, non una simulazione SPICE reale — utile solo come controllo di coerenza.
- **ERC/DRC**: eseguiti dopo le modifiche — 44 violazioni ERC (39 errori, per lo più pin GPIO ESP32 non connessi + percorsi libreria footprint mancanti, sembrano preesistenti) e 93 violazioni DRC. **Non è stato catturato un baseline pre-modifica**, quindi non è possibile distinguere con certezza cosa fosse già presente prima da cosa (se qualcosa) sia stato introdotto dalle modifiche di questa sessione. Da rifare con baseline per un giudizio pulito.
- **ERC ri-eseguito dopo la seconda sessione (D1/D2/auto-reset)**: 50 violazioni (39 errori, 11 warning), conteggio errori identico alla sessione precedente (39) — coerente col fatto che le nuove modifiche non abbiano introdotto nuovi errori critici. Compaiono nuovi **warning "pin/capo filo fuori griglia"** su alcuni dei nuovi fili aggiunti (i jog di routing usati per evitare di attraversare altri pin non sono sempre caduti sulla griglia standard 1.27mm) — non è un errore di connettività (verificato via netlist, non via griglia), ma andrebbe ripulito in KiCad GUI per igiene dello schematico prima del fab.

## ⚠️ Incidente serio (2026-09-28, seconda sessione): footprint duplicati salvati su disco
Il tentativo di `sync_schematic_to_board` della sessione precedente aveva aggiunto 17 footprint duplicati (non piazzati, a coordinate 0,0) a causa del bug del punto 8 (vedi sopra). Nonostante il messaggio "auto-save refused" ricevuto allora, **questi duplicati risultavano effettivamente salvati su disco**: il file PCB è passato da 31 a 48 blocchi footprint. Questa cartella "copia MCP" **non è tracciata da git**, quindi non c'era uno storico da cui recuperare.

Ho rimosso 15 dei 17 duplicati nella sessione precedente. **I 2 rimanenti (D2 e COUT1 orfani a coordinate 0,0) sono stati rimossi con conferma esplicita dell'utente** (2026-09-28, terza sessione): verificati via `find_component` (matchCount:1, posizione 0,0, distinti dagli originali reali "SS34"@143.45,49.53 e "47µF"@134.25,46.85), cancellati con `delete_component`, board salvata e ricontata: **31 footprint sul file su disco — corretto**.
**Stato attuale: risolto. Il PCB ha di nuovo il conteggio footprint corretto (31).**

## File modificati in questa sessione (aggiornato, seconda sessione 2026-09-28)
- `BaseChipOnly.kicad_sch`: 
  - D1: polarità corretta (fix wire-level, verificato via netlist)
  - D2: polarità corretta (fix wire-level, verificato via netlist)
  - Circuito auto-reset: IO0_CTRL1/EN_CTRL1 base ed emettitore ricablati (DTR/RTS incrociati), verificato via netlist
  - L1 (valore/MPN), Polyfuse1 (valore/MPN), U3 (stub GND aggiunto) — dalla sessione precedente, ancora validi
- `BaseChipOnly.kicad_pcb`:
  - footprint L1 aggiornato (sessione precedente)
  - **15 footprint duplicati orfani rimossi** (residuo pericoloso del tentativo di sync della sessione precedente, che risultava salvato su disco nonostante l'avviso contrario)
  - **2 footprint duplicati (D2, COUT1) ancora presenti — richiedono rimozione manuale**, vedi sezione incidente sopra
  - D1, D2, circuito auto-reset: **fix NON ancora propagati al PCB** (bloccato dal bug del punto 8, vedi sopra)

## Conclusione
**Non ordinare Gerber/fab da questo stato.** Lato schematico, i tre fix più critici (D1, D2, auto-reset) sono ora corretti e verificati via netlist. Ma:
1. Nessuno di questi fix è ancora arrivato al PCB (il rame è ancora instradato secondo la vecchia connettività bacata).
2. ~~Il PCB ha ancora 2 footprint duplicati orfani da rimuovere manualmente.~~ **Risolto 2026-09-28**: i 2 duplicati rimasti sono stati rimossi con conferma dell'utente, PCB tornato a 31 footprint corretti.
3. Il bug del punto 8 (Reference/Value scambiati) blocca la sincronizzazione automatica schema→PCB e va risolto per primo prima di ogni altro lavoro sul PCB.
4. Punti 3b, 4 (già fatto), 5 (già fatto), 7, 9, 10, 11 restano da fare come da sezioni sopra.

**Prossimo passo consigliato**: risolvere il punto 8 (Reference/Value sui footprint) — è un fix a basso rischio (campi testo, non fili) e sblocca la sincronizzazione sicura schema→PCB necessaria per portare D1/D2/auto-reset dallo schematico al rame reale.
