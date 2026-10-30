"""Experiment 6, part 2: SINDy on the PDE, one frequency at a time.

Training: delta = A sin(w tau), 5 periods, dtau = P/200 (1001 points).
Library {Cs, Cavg, delta}; dCs/dtau by 2nd-order central differences.
Validation (10 periods each): cos, sin late, sin ph, cos ph -> E_sim (Rel of Cs, whole run)
and E_dv; lambda chosen by R4 on the stacked (mean) E_sim, unstable models removed first.
Test (used once, after lambda is fixed): random multisine, 10 periods.
Cross-test: every selected model on the cosine run at every w, last period, Cs and gap.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from common import rel_err, sweep, select_R4, lambda_grid
from pde import PDE, galerkin, A_FLUX

OMEGAS = (0.1, 1.0, 10.0, 100.0)
PTS = 200                      # points per period
N_TRAIN, N_VAL = 5, 10         # periods
VAL_NAMES = ('cos', 'sin late', 'sin ph', 'cos ph')
RANDOM = {0.1: ((0.82, 0.74, 0.75), (4.62, 3.09, 0.48)),
          1.0: ((0.54, 0.91, 0.82), (1.24, 3.70, 5.63)),
          10.0: ((0.91, 0.53, 0.69), (4.99, 2.70, 4.75)),
          100.0: ((0.62, 0.97, 0.53), (1.31, 0.81, 2.65))}
TERMS = ('Cs', 'Cavg', 'delta')
pde = PDE(61)


def random_input(w):
    a, ph = RANDOM[w]
    wk = (w / 2, w, 2 * w)
    raw = lambda s: sum(ak * np.sin(k * s + p) for ak, k, p in zip(a, wk, ph))
    tt = np.linspace(0, N_VAL * 4 * np.pi / w, 200001)   # 2P is the common period
    scale = A_FLUX / np.abs(raw(tt)).max()
    return lambda s: scale * raw(s)


def d2(y, t):
    """2nd-order differences at every point: central inside, one-sided 2nd-order at the ends
    (numpy.gradient, edge_order=2; the same derivative as in version 2)."""
    return np.gradient(y, t, edge_order=2)


def d4(y, t):
    """4th-order differences at every point: central inside, one-sided 4th-order at the ends."""
    h = t[1] - t[0]
    d = np.empty_like(y)
    d[2:-2] = (-y[4:] + 8 * y[3:-1] - 8 * y[1:-3] + y[:-4]) / (12 * h)
    d[0] = (-25 * y[0] + 48 * y[1] - 36 * y[2] + 16 * y[3] - 3 * y[4]) / (12 * h)
    d[1] = (-3 * y[0] - 10 * y[1] + 18 * y[2] - 6 * y[3] + y[4]) / (12 * h)
    d[-1] = (25 * y[-1] - 48 * y[-2] + 36 * y[-3] - 16 * y[-4] + 3 * y[-5]) / (12 * h)
    d[-2] = (3 * y[-1] + 10 * y[-2] - 18 * y[-3] + 6 * y[-4] - y[-5]) / (12 * h)
    return d


def run_pde(delta, t, u0=None):
    Cs, Ca, uend = pde.solve(delta, t, u0)
    return dict(t=t, d=delta(t), Cs=Cs, Ca=Ca, uend=uend, delta=delta)


def simulate(xi, run):
    """SINDy model for Cs; Cavg from the exact mass balance dCavg = -3 delta."""
    c, ca, cd = xi
    delta, t = run['delta'], run['t']
    rhs = lambda s, y: [c * y[0] + ca * y[1] + cd * delta(s), -3 * delta(s)]
    blow = lambda s, y: 10 - abs(y[0])
    blow.terminal = True
    sol = solve_ivp(rhs, (t[0], t[-1]), [run['Cs'][0], run['Ca'][0]], method='Radau',
                    t_eval=t, rtol=1e-10, atol=1e-12, events=blow)
    if sol.status != 0 or sol.y.shape[1] != len(t):
        return None, None
    return sol.y[0], sol.y[1]


def scores(xi, run):
    Cs, _ = simulate(xi, run)
    esim = np.inf if Cs is None else rel_err(Cs, run['Cs'])
    Th = np.column_stack([run['Cs'], run['Ca'], run['d']])
    edv = rel_err(Th @ xi, d2(run['Cs'], run['t']))
    return esim, edv


def last_period(xi, w, galerkin_model=False):
    """Cosine run, 10 periods; Rel of Cs and of the gap Cs - Cavg over the last period."""
    P = 2 * np.pi / w
    t = np.linspace(0, N_VAL * P, N_VAL * PTS + 1)
    run = run_pde(lambda s: A_FLUX * np.cos(w * s), t)
    Cs, Ca = simulate(xi, run)
    m = t >= (N_VAL - 1) * P - 1e-12
    return (100 * rel_err(Cs[m], run['Cs'][m]),
            100 * rel_err(Cs[m] - Ca[m], run['Cs'][m] - run['Ca'][m]))


def main():
    lams = lambda_grid(-6, 1e3)
    out = dict(lams=lams.tolist(), omegas={})
    xi_gal = np.array([-35.0, 35.0, -10.0])
    for w in OMEGAS:
        P = 2 * np.pi / w
        t_tr = np.linspace(0, N_TRAIN * P, N_TRAIN * PTS + 1)
        sin = lambda s, w=w: A_FLUX * np.sin(w * s)
        train = run_pde(sin, t_tr)
        t_val = np.linspace(0, N_VAL * P, N_VAL * PTS + 1)
        val = {
            'cos': run_pde(lambda s, w=w: A_FLUX * np.cos(w * s), t_val),
            'sin late': run_pde(sin, N_TRAIN * P + t_val, u0=train['uend']),
            'sin ph': run_pde(lambda s, w=w: A_FLUX * np.sin(w * s + np.pi / 4), t_val),
            'cos ph': run_pde(lambda s, w=w: A_FLUX * np.cos(w * s + np.pi / 4), t_val)}
        test = run_pde(random_input(w), t_val)

        Th = np.column_stack([train['Cs'], train['Ca'], train['d']])
        dCs = d2(train['Cs'], t_tr)[:, None]
        models = sweep(Th, dCs, lams)
        rows = []
        for m in models:
            xi = m['Xi'][:, 0]
            es, ed = zip(*(scores(xi, val[k]) for k in VAL_NAMES))
            rows.append(dict(lam_max=m['lam_max'], lam_min=m['lam_min'], xi=xi.tolist(),
                             terms=int((xi != 0).sum()),
                             E_sim=dict(zip(VAL_NAMES, es)), E_dv=dict(zip(VAL_NAMES, ed)),
                             E_sim_stacked=float(np.mean(es)), E_dv_stacked=float(np.mean(ed)),
                             E_train=rel_err(Th @ xi, dCs[:, 0]),
                             stable=bool(np.all(np.isfinite(es)))))
        stable = [r['stable'] for r in rows]
        sel = {}
        for k in VAL_NAMES:
            sel['E_sim ' + k] = select_R4([r['E_sim'][k] for r in rows], stable)
        sel['E_sim stacked'] = select_R4([r['E_sim_stacked'] for r in rows], stable)
        sel['E_dv stacked, step 4 skipped'] = select_R4([r['E_dv_stacked'] for r in rows])
        sel['E_dv stacked'] = select_R4([r['E_dv_stacked'] for r in rows], stable)
        chosen = sel['E_sim stacked']
        xi = np.array(rows[chosen]['xi'])
        # 4th-order derivative fit with the same support, for comparison
        supp = xi != 0
        xi4 = np.zeros(3)
        xi4[supp] = np.linalg.lstsq(Th[:, supp], d4(train['Cs'], t_tr), rcond=None)[0]
        # check of the start-up explanation: the same fit without the two end points
        xi_in = np.zeros(3)
        xi_in[supp] = np.linalg.lstsq(Th[1:-1][:, supp], dCs[1:-1, 0], rcond=None)[0]
        t_es, t_ed = scores(xi, test)
        g_es, g_ed = scores(xi_gal, test)
        out['omegas'][str(w)] = dict(rows=rows, selections=sel, chosen=chosen, xi=xi.tolist(),
                                     xi4=xi4.tolist(), xi_interior=xi_in.tolist(),
                                     test=dict(E_sim=t_es, E_dv=t_ed),
                                     test_galerkin=dict(E_sim=g_es, E_dv=g_ed))
        print(w, [(f"{r['lam_max']:.2g}-{r['lam_min']:.2g}", r['terms'], np.round(r['xi'], 3).tolist(),
                   f"{r['E_sim_stacked']:.3g}", f"{r['E_dv_stacked']:.3g}") for r in rows],
              {k: rows[i]['terms'] for k, i in sel.items()},
              'test', t_es, t_ed, 'gal', g_es, g_ed, flush=True)
    # cross-test
    cross = {}
    models = {'Galerkin': xi_gal}
    for w in OMEGAS:
        models[f'SINDy, trained at w = {w:g}'] = np.array(out['omegas'][str(w)]['xi'])
    for name, xi in models.items():
        cross[name] = {str(w): last_period(xi, w) for w in OMEGAS}
        print(name, cross[name], flush=True)
    out['cross'] = cross
    json.dump(out, open('results_pde.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
