* Shared buck power stage (values from BaseChipOnly.kicad_sch, 2026-09-30)
* Input: PSU 5 V behind cable + barrel jack + polyfuse (~0.15 ohm total)
RSRC psu vplus 0.15
* +5V rail parts
C1   vplus c1n 1000u
RC1  c1n 0 50m
C2   vplus 0 100n
CIN1 vplus cin1n 22u
RCIN1 cin1n 0 5m
* LED strip load on +5V (set by ILED in each deck)
ILEDS vplus 0 {ILED}
* Regulator
D2 0 sw SS34
L1 sw l1b 100u
RL1 l1b v33 0.456
* Output: COUT1 47 uF 0805 X5R derated to ~20 uF at 3.3 V bias, COUT2 220 uF tantalum ESR 0.1
COUT1 v33 co1n 20u
RCO1 co1n 0 5m
COUT2 v33 co2n 220u
RCO2 co2n 0 0.1
C3 v33 0 100n
* Feedback divider
RTOP v33 fb 2.0k
RBOT fb 0 1.2k
