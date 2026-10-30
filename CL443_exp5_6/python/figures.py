"""Figures for the version-3 report."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pde import PDE, galerkin
from pde_sindy import random_input, N_VAL, PTS, simulate, run_pde

BLUE, ORANGE, AQUA, GREY, INK = '#2a78d6', '#eb6834', '#1baf7a', '#8a8a85', '#3a3a38'
plt.rcParams.update({'font.size': 8, 'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'axes.grid': True,
                     'grid.color': '#e4e3df', 'grid.linewidth': 0.6, 'lines.linewidth': 1.4,
                     'axes.spines.top': False, 'axes.spines.right': False})


def lorenz_fig():
    d = json.load(open('results_lorenz.json'))
    lams = np.array(d['lams'])
    fig, ax = plt.subplots(2, 3, figsize=(7.2, 3.6), sharex=True,
                           gridspec_kw=dict(height_ratios=[2.2, 1], hspace=0.12, wspace=0.28))
    titles = {'A': 'A: exact derivative', 'C2': 'C2: 2nd-order differences',
              'C4': 'C4: 4th-order differences'}
    for j, (case, v) in enumerate(d['cases'].items()):
        rows = v['rows']
        # expand merged models back onto the lambda grid
        pick = [next(r for r in rows if r['lam_min'] <= l * (1 + 1e-9) and l <= r['lam_max'] * (1 + 1e-9))
                for l in lams]
        for key, lab, c in (('E_train', r'$E_{train}$', INK), ('E_dv', r'$E_{dv}$', BLUE),
                            ('E_sim', r'$E_{sim}(T{=}1)$', ORANGE)):
            y = [p[key]['1.0'] if key == 'E_sim' else p[key] for p in pick]
            ax[0, j].plot(lams, y, '-', color=c, label=lab, lw=1.2 if key == 'E_train' else 1.6)
        sel = rows[v['selected']]
        ax[0, j].axvline(sel['lam_max'], color=GREY, ls=':', lw=1)
        ax[0, j].set_xscale('log'); ax[0, j].set_yscale('log'); ax[0, j].invert_xaxis()
        ax[0, j].set_title(titles[case], fontsize=8.5, color=INK)
        ax[0, j].set_ylim(1e-17, 3)
        ax[1, j].step(lams, [p['terms'] for p in pick], where='mid', color=GREY)
        ax[1, j].set_yscale('symlog', linthresh=10); ax[1, j].set_ylim(0, 100)
        ax[1, j].set_yticks([0, 7, 30, 60]); ax[1, j].set_yticklabels(['0', '7', '30', '60'])
        ax[1, j].set_xlabel(r'$\lambda$  (decreasing $\rightarrow$)')
    ax[0, 0].set_ylabel('relative error (fraction)')
    ax[1, 0].set_ylabel('terms')
    h, l = ax[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc='upper center', ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.06))
    fig.savefig('../report/figs/lorenz_sweep.pdf', bbox_inches='tight')


def test_fig():
    d = json.load(open('results_pde.json'))
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.4), gridspec_kw=dict(wspace=0.25))
    for j, w in enumerate((1.0, 100.0)):
        P = 2 * np.pi / w
        t = np.linspace(0, N_VAL * P, N_VAL * PTS + 1)
        run = run_pde(random_input(w), t)
        Gs, _ = simulate(np.array([-35.0, 35.0, -10.0]), run)
        Ss, _ = simulate(np.array(d['omegas'][str(w)]['xi']), run)
        m = t >= 8 * P - 1e-12
        ax[j].plot(t[m] / P, run['Cs'][m], color=INK, lw=2.4, label='PDE')
        ax[j].plot(t[m] / P, Gs[m], color=ORANGE, label='Galerkin')
        ax[j].plot(t[m] / P, Ss[m], color=BLUE, ls='--', label='SINDy, trained at the same $\\omega$')
        ax[j].set_title(f'test input, $\\omega = {w:g}$ (last two periods)', fontsize=8.5, color=INK)
        ax[j].set_xlabel(r'$\tau / P$')
    ax[0].set_ylabel(r'$C_s$')
    fig.legend(*ax[1].get_legend_handles_labels(), loc='upper center', ncol=3, frameon=False,
               fontsize=8, bbox_to_anchor=(0.5, 1.1))
    fig.savefig('../report/figs/pde_test.pdf', bbox_inches='tight')


if __name__ == '__main__':
    lorenz_fig()
    test_fig()
