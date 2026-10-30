"""Write the LaTeX tables of the version-3 report from results_*.json."""
import json
import numpy as np

T = '../report/tables/'


def sci(x, d=1):
    if x is None or not np.isfinite(x):
        return r'$\infty$'
    if x == 0:
        return '0'
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    if round(m, d) >= 10:
        m, e = m / 10, e + 1
    return rf'${m:.{d}f}\!\times\!10^{{{e}}}$'


def lamr(r):
    if np.isclose(r['lam_min'], r['lam_max']):
        return sci(r['lam_max'])
    return sci(r['lam_min']) + ' -- ' + sci(r['lam_max'])


def pct(x, d=2):
    """percent with d significant figures, plain or scientific."""
    if not np.isfinite(x):
        return r'$\infty$'
    x = 100 * x
    return f'{x:.{d}g}' if 1e-2 <= abs(x) < 1e3 else sci(x, d - 1)


def f3(x):
    """a value already in percent, 3 significant figures"""
    return f'{x:.3g}' if x >= 1e-2 else sci(x, 2)


def w(name, s):
    open(T + name, 'w').write(s)


def lorenz():
    d = json.load(open('results_lorenz.json'))
    names = d['names']
    for case, v in d['cases'].items():
        s = [r'\begin{tabular}{lrrrrrrrrr}\toprule',
             r'$\lambda$ range & terms & wrong & missing & max coef.\ err. & $E_{train}$ & $E_{dv}$ & '
             r'$E_{sim}(0.5)$ & $E_{sim}(1)$ & $E_{sim}(2)$\\\midrule']
        for i, r in enumerate(v['rows']):
            row = [lamr(r), str(r['terms']), str(r['wrong']), str(r['missing']), sci(r['coef_err']),
                   sci(r['E_train']), sci(r['E_dv'])] + [sci(r['E_sim'][k]) for k in ('0.5', '1.0', '2.0')]
            line = ' & '.join(row) + r'\\'
            if i == v['selected']:
                line = r'\rowcolor{sel}' + line
            s.append(line)
        s.append(r'\bottomrule\end{tabular}')
        w(f'lorenz_sweep_{case}.tex', '\n'.join(s))
    # rules
    s = [r'\begin{tabular}{llcccc}\toprule Case & Error & R1 & R2 & R3 & R4\\\midrule']
    for case, v in d['cases'].items():
        for key, lab in (('E_dv', '$E_{dv}$'), ('E_sim1', '$E_{sim}(T{=}1)$')):
            cells = []
            for R in ('R1', 'R2', 'R3', 'R4'):
                r = v['rows'][v['rules'][key][R]]
                cells.append(f"{r['terms']} ({r['wrong']})")
            s.append(f'{case} & {lab} & ' + ' & '.join(cells) + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('lorenz_rules.tex', '\n'.join(s))
    # rule applied
    s = [r'\begin{tabular}{llrrcc}\toprule Case & Score & terms & wrong & $\lambda$ range of the selected model & selected $\lambda$\\\midrule']
    for case, v in d['cases'].items():
        for key, lab in (('E_dv', r'$E_{dv}$ (main)'), ('E_sim1', '$E_{sim}(T{=}1)$')):
            r = v['rows'][v['rules'][key]['R4']]
            s.append(f"{case} & {lab} & {r['terms']} & {r['wrong']} & {lamr(r)} & {sci(r['lam_max'], 2)}" + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('lorenz_rule_applied.tex', '\n'.join(s))
    # coefficients
    true = {('x', 0): -10, ('y', 0): 10, ('x', 1): 28, ('y', 1): -1, ('xz', 1): -1, ('z', 2): -8 / 3, ('xy', 2): 1}
    s = [r'\begin{tabular}{llrrrr}\toprule Equation & Term & True & A (exact) & C2 (2nd order) & C4 (4th order)\\\midrule']
    for (term, eq), tv in true.items():
        vals = [np.array(d['cases'][c]['Xi_selected'])[names.index(term), eq] for c in ('A', 'C2', 'C4')]
        s.append(rf'$\dot {"xyz"[eq]}$ & ${term}$ & {tv:.4f} & ' + ' & '.join(f'{x:.6f}' for x in vals) + r'\\')
    s.append(r'\midrule max $|\xi_{\rm SINDy}-\xi_{\rm true}|$ & & & ' + ' & '.join(
        sci(d['cases'][c]['rows'][d['cases'][c]['selected']]['coef_err']) for c in ('A', 'C2', 'C4')) + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('lorenz_coefs.tex', '\n'.join(s))
    # test
    s = [r'\begin{tabular}{lllcccc}\toprule Case & Model & & $E_{dv}$ & $E_{sim}(0.5)$ & $E_{sim}(1)$ & $E_{sim}(2)$\\\midrule']
    for case, v in d['cases'].items():
        for key, lab in (('test', 'SINDy, selected (7 terms)'), ('test_true', 'true Lorenz equations')):
            t = v[key]
            s.append(f'{case} & {lab} & & {sci(t["E_dv"])} & ' + ' & '.join(sci(t['E_sim'][k]) for k in ('0.5', '1.0', '2.0')) + r'\\')
        if case != 'C4':
            s.append(r'\addlinespace')
    s.append(r'\bottomrule\end{tabular}')
    w('lorenz_test.tex', '\n'.join(s))
    # knee margins
    out = {}
    for case, v in d['cases'].items():
        e = np.log10([max(r['E_dv'], 1e-300) for r in v['rows']])
        dr = np.sort(e[:-1] - e[1:])[::-1]
        out[case] = dr[:2].tolist()
    json.dump(out, open('knee_margins.json', 'w'))
    print('knee margins (decades)', out)


def pde():
    d = json.load(open('results_pde.json'))
    VN = ('cos', 'sin late', 'sin ph', 'cos ph')
    s = [r'\begin{tabular}{rlrrrc|rrrr|r|rr}\toprule',
         r' & & \multicolumn{3}{c}{coefficients} & & \multicolumn{5}{c|}{$E_{sim}$ (\%) on validation runs} & \multicolumn{2}{c}{derivative error (\%)}\\',
         r'$\omega$ & $\lambda$ range & $C_s$ & $C_{avg}$ & $\delta$ & stable & cos & sin late & sin ph & cos ph & stacked & $E_{dv}$, stacked & $E_{train}$\\\midrule']
    for wk, v in d['omegas'].items():
        for i, r in enumerate(v['rows']):
            xi = r['xi']
            row = [f'{float(wk):g}', lamr(r)] + [f'{x:+.3f}' for x in xi] + ['yes' if r['stable'] else 'no'] + \
                  [pct(r['E_sim'][k]) for k in VN] + [pct(r['E_sim_stacked']), pct(r['E_dv_stacked'], 3), pct(r['E_train'], 3)]
            line = ' & '.join(row) + r'\\'
            if i == v['chosen']:
                line = r'\rowcolor{sel}' + line
            s.append(line)
        if wk != '100.0':
            s.append(r'\midrule')
    s.append(r'\bottomrule\end{tabular}')
    w('pde_models.tex', '\n'.join(s))
    # selection
    keys = ['E_sim cos', 'E_sim sin late', 'E_sim sin ph', 'E_sim cos ph', 'E_sim stacked',
            'E_dv stacked, step 4 skipped', 'E_dv stacked']
    s = [r'\begin{tabular}{r|ccccc|cc|cc}\toprule',
         r' & \multicolumn{5}{c|}{$E_{sim}$ on} & \multicolumn{2}{c|}{$E_{dv}$, stacked} & & \\',
         r'$\omega$ & cos & sin late & sin ph & cos ph & \textbf{stacked} & step 4 skipped & step 4 used & $\lambda$ range & selected $\lambda$\\\midrule']
    for wk, v in d['omegas'].items():
        cells = []
        for k in keys:
            r = v['rows'][v['selections'][k]]
            c = f"{r['terms']}" + ('' if r['stable'] else r', \textbf{unstable}')
            cells.append(c)
        r = v['rows'][v['chosen']]
        s.append(f'{float(wk):g} & ' + ' & '.join(cells) + f' & {lamr(r)} & {sci(r["lam_max"], 1)}' + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('pde_selection.tex', '\n'.join(s))
    # test
    s = [r'\begin{tabular}{r|cc|cc|c}\toprule',
         r' & \multicolumn{2}{c|}{$E_{sim}$ (\%)} & \multicolumn{2}{c|}{$E_{dv}$ (\%)} & \\',
         r'$\omega$ & Galerkin & SINDy & Galerkin & SINDy & $E_{sim}$: Galerkin / SINDy\\\midrule']
    for wk, v in d['omegas'].items():
        g, t = v['test_galerkin'], v['test']
        s.append(f'{float(wk):g} & {pct(g["E_sim"], 3)} & {pct(t["E_sim"], 3)} & {pct(g["E_dv"], 3)} & {pct(t["E_dv"], 3)} & {g["E_sim"] / t["E_sim"]:.2g}' + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('pde_test.tex', '\n'.join(s))
    # coefficients
    s = [r'\begin{tabular}{llrrr}\toprule & derivative & $C_s$ & $C_{avg}$ & $\delta$\\\midrule',
         r'Galerkin & -- & $-35$ & $+35$ & $-10$\\\midrule']
    for wk, v in d['omegas'].items():
        s.append(rf'$\omega={float(wk):g}$ & 2nd order & ' + ' & '.join(f'{x:+.3f}' for x in v['xi']) + r'\\')
        s.append(r' & 4th order & ' + ' & '.join(f'{x:+.3f}' for x in v['xi4']) + r'\\')
        s.append(r' & 2nd order, end points dropped & ' + ' & '.join(f'{x:+.3f}' for x in v['xi_interior']) + r'\\')
        if wk != '100.0':
            s.append(r'\addlinespace')
    s.append(r'\bottomrule\end{tabular}')
    w('pde_coefs.tex', '\n'.join(s))
    # cross test
    s = [r'\begin{tabular}{l|cc|cc|cc|cc}\toprule',
         r' & \multicolumn{2}{c|}{test $\omega=0.1$} & \multicolumn{2}{c|}{test $\omega=1$} & \multicolumn{2}{c|}{test $\omega=10$} & \multicolumn{2}{c}{test $\omega=100$}\\',
         r'Model' + r' & $C_s$ & gap' * 4 + r'\\\midrule']
    for name, v in d['cross'].items():
        label = name.replace('w = ', r'$\omega = ') + ('$' if 'w = ' in name else '')
        cells = []
        for wk in ('0.1', '1.0', '10.0', '100.0'):
            cs, gp = v[wk]
            cells += [f3(cs), f3(gp)]
        s.append(label + ' & ' + ' & '.join(cells) + r'\\')
    s.append(r'\bottomrule\end{tabular}')
    w('pde_cross.tex', '\n'.join(s))


if __name__ == '__main__':
    import os
    os.makedirs(T, exist_ok=True)
    lorenz()
    pde()
