#!/bin/bash
# Downloads TI's unencrypted LM2596_3P3 transient model (SNVMA65, from ti.com/product/LM2596)
# and derives models/LM2596_ADJ.lib (internal divider removed -> ADJ version, plus a variant with
# the datasheet switch saturation). The TI file is not redistributed in this repo.
set -e
cd "$(dirname "$0")"
curl -sL -A "Mozilla/5.0" -o snvma65.zip "https://www.ti.com/lit/zip/snvma65"
unzip -o -q snvma65.zip -d snvma65
python3 - <<'PY'
s = open('snvma65/LM2596_3P3_TRANS.LIB', encoding='latin-1').read()
s = s.replace('.SUBCKT LM2596_3P3_TRANS VIN FB OUT GND ON_OFF_N', '.SUBCKT LM2596_ADJ VIN FB OUT GND ON_OFF_N')
s = s.replace('.ENDS LM2596_3P3_TRANS', '.ENDS LM2596_ADJ')
s = s.replace('R_RFB1         GND FB_INT  2.5k TC=0,0 \n', '')
s = s.replace('R_RFB2         FB_INT FB  4.2k TC=0,0 ', 'R_RFB2         FB_INT FB  1m')
i = s.find('.SUBCKT LM2596_ADJ'); j = s.find('.ENDS LM2596_ADJ') + len('.ENDS LM2596_ADJ')
v = s[i:j].replace('.SUBCKT LM2596_ADJ', '.SUBCKT LM2596_ADJ_VSAT').replace('.ENDS LM2596_ADJ', '.ENDS LM2596_ADJ_VSAT')
v = v.replace('X_U1_S1    U1_N16909798 0 N16780168 OUT Soft_Start_U1_S1',
              'X_U1_S1    U1_N16909798 0 N16780168 SWINT Soft_Start_U1_S1\n* added: Darlington switch saturation (datasheet Vsat ~1.16 V typ @ 3 A)\nD_VSAT SWINT OUT DVSAT\n.model DVSAT D(IS=5.7e-7 N=2.4 RS=0.1)')
assert 'D_VSAT' in v and 'R_RFB1' not in s
s = ('* LM2596-ADJ derived from TI LM2596_3P3 unencrypted transient model (SNVMA65):\n'
     '* internal feedback divider removed so FB is the 1.235 V reference input.\n' + s +
     '\n*$\n* Same model plus a series drop that reproduces the datasheet switch saturation voltage\n' + v + '\n')
open('LM2596_ADJ.lib', 'w').write(s)
print('models/LM2596_ADJ.lib written')
PY
