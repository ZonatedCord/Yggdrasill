"""Plots for the BaseChipOnly simulations (reads out/*.dat written by ngspice wrdata)."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load(f, n):
    a = np.loadtxt(f)
    return a[:, 0], [a[:, 2 * k + 1] for k in range(n)]

def style(ax, title, ylabel):
    ax.set_title(title, fontsize=10, loc='left'); ax.set_ylabel(ylabel); ax.grid(alpha=.3)

# 01 auto-reset: new circuit vs rev 1.03
for fn, tag in (('01_autoreset', 'nuovo circuito (C4 100 nF)'), ('01c_autoreset_C4_1u', 'nuovo circuito, C4 = 1 µF'),
                ('01b_autoreset_rev103', 'rev 1.03 come prodotta')):
    t, (dtr, rts, en, io0) = load(f'out/{fn}.dat', 4)
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    ax[0].plot(t*1e3, dtr, label='pin DTR'); ax[0].plot(t*1e3, rts, '--', label='pin RTS')
    style(ax[0], f'Auto-reset — {tag}: segnali dall\'adattatore', 'V'); ax[0].legend(loc='right', fontsize=8)
    ax[1].plot(t*1e3, en, label='EN (CHIP_PU)'); ax[1].plot(t*1e3, io0, label='IO0')
    ax[1].axhline(2.475, color='gray', ls=':', lw=1); ax[1].text(805, 2.5, 'soglia alta 2.475 V', fontsize=7, ha='right')
    for x, s in ((10, 'esptool\nUnixTight'), (300, 'esptool\nClassic'), (600, 'monitor seriale\n(DTR=RTS=1)')):
        ax[1].annotate(s, (x, 3.45), fontsize=7)
    style(ax[1], 'ESP32', 'V'); ax[1].set_xlabel('ms'); ax[1].set_ylim(-0.2, 4.1); ax[1].legend(loc='right', fontsize=8)
    fig.tight_layout(); fig.savefig(f'grafici/{fn}.png', dpi=110); plt.close(fig)

# 02 buck
t, (v33, vp, il, sw) = load('out/02_buck_nominal.dat', 4)
fig, ax = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
ax[0].plot(t*1e3, vp, label='+5V'); ax[0].plot(t*1e3, v33, label='+3V3'); style(ax[0], 'LM2596 — avvio e carichi ESP32 (60 / 250 / 500 mA)', 'V'); ax[0].legend(fontsize=8)
ax[1].plot(t*1e3, v33); ax[1].set_ylim(3.2, 3.35); style(ax[1], '+3V3 zoom', 'V')
ax[2].plot(t*1e3, il); ax[2].axhline(1.33, color='r', ls=':'); ax[2].text(24.5, 1.4, 'Isat L1 1.33 A', fontsize=7, ha='right', color='r')
style(ax[2], 'corrente in L1 (avvio con 5 V in 1 ms)', 'A'); ax[2].set_xlabel('ms')
fig.tight_layout(); fig.savefig('grafici/02_buck_nominal.png', dpi=110); plt.close(fig)

t, (v33, vp, il) = load('out/02b_buck_ledload_vsat.dat', 3)
fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
ax[0].plot(t*1e3, vp, label='+5V (LED da 0 a 3 A a 4-6 ms)'); ax[0].plot(t*1e3, v33, label='+3V3'); style(ax[0], 'Caso peggiore: LED a 3 A + Vsat reale + TX WiFi 500 mA (12-13 ms)', 'V'); ax[0].legend(fontsize=8)
ax[1].plot(t*1e3, v33); ax[1].axhline(3.0, color='r', ls=':'); ax[1].set_ylim(2.9, 3.45); style(ax[1], '+3V3 zoom (minimo ESP32 3.0 V)', 'V'); ax[1].set_xlabel('ms')
fig.tight_layout(); fig.savefig('grafici/02b_buck_ledload_vsat.png', dpi=110); plt.close(fig)

t, (v33, vp) = load('out/02c_buck_dropout.dat', 2)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t*1e3, vp, label='+5V (regolatore VIN)'); ax.plot(t*1e3, v33, label='+3V3 @ 500 mA'); ax.axhline(3.0, color='r', ls=':')
style(ax, 'Tensione minima in ingresso: 5.0 → 4.0 V a gradini, carico 500 mA, Vsat reale', 'V'); ax.set_xlabel('ms'); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('grafici/02c_buck_dropout.png', dpi=110); plt.close(fig)

t, (v33, vp, il) = load('out/02d_buck_slowramp.dat', 3)
fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
ax[0].plot(t*1e3, vp, label='+5V'); ax[0].plot(t*1e3, v33, label='+3V3'); style(ax[0], 'Avvio con alimentatore reale (5 V in 10 ms)', 'V'); ax[0].legend(fontsize=8)
ax[1].plot(t*1e3, il); ax[1].axhline(1.33, color='r', ls=':'); style(ax[1], 'corrente in L1', 'A'); ax[1].set_xlabel('ms')
fig.tight_layout(); fig.savefig('grafici/02d_buck_slowramp.png', dpi=110); plt.close(fig)

# 03 power-on
for fn, tag in (('03_poweron', 'C4 100 nF'), ('03b_poweron_C4_1u', 'C4 1 µF')):
    t, (v33, ena, io0a, enb, io0b, enc, io0c) = load(f'out/{fn}.dat', 7)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t*1e3, v33, 'k', label='+3V3'); ax.plot(t*1e3, ena, label='EN, adattatore scollegato')
    ax.plot(t*1e3, enc, '--', label='EN, adattatore collegato a riposo'); ax.plot(t*1e3, io0c, ':', label='IO0, adattatore collegato')
    ax.axhline(2.475, color='gray', ls=':', lw=1)
    style(ax, f'Accensione — {tag}', 'V'); ax.set_xlabel('ms'); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(f'grafici/{fn}.png', dpi=110); plt.close(fig)

# 04 status LED
a = np.loadtxt('out/04_status_led.dat')
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(a[:, 0], a[:, 1]*1e3, label='LED rosso'); ax.plot(a[:, 0], a[:, 3]*1e3, label='LED bianco/blu')
style(ax, 'LED di stato D1 con R0 470 Ω', 'mA'); ax.set_xlabel('tensione +5V (V)'); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('grafici/04_status_led.png', dpi=110); plt.close(fig)

# 05 data line
t, (g, a_, b_, c_, d_) = load('out/05_dataline.dat', 5)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t*1e6, g, 'k', lw=1, label='GPIO13')
for y, l in ((a_, 'R5 470 Ω, cavo 0.3 m'), (b_, 'R5 470 Ω, cavo 0.6 m'), (c_, 'R5 100 Ω, cavo 0.3 m'), (d_, 'R5 100 Ω, cavo 0.6 m')):
    ax.plot(t*1e6, y, label=l)
ax.axhline(2.5, color='gray', ls=':', lw=1)
style(ax, 'Linea dati alle foglie (9 in parallelo), bit 0 1 0 1 1 0 a 800 kHz', 'V'); ax.set_xlabel('µs'); ax.legend(fontsize=8, loc='upper right')
fig.tight_layout(); fig.savefig('grafici/05_dataline.png', dpi=110); plt.close(fig)
print('ok')
