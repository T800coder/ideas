"""Experiment 6, part 1: SINDy on the Lorenz system with the agreed error measures.

E_train, E_dv, E_sim(T) all use rel_err (per-variable RMS / band, averaged over x, y, z).
Lambda chosen by R4 on E_dv; the chosen model is then scored once on 3 unseen test runs.
"""
import json
from itertools import combinations_with_replacement
import numpy as np
from scipy.integrate import solve_ivp
from common import rel_err, sweep, select_R4, select_tol, select_level, lambda_grid

SIG, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
DT = 1e-3
X0_TRAIN = (-8.0, 7.0, 27.0)
X0_VAL = [(5.0, -5.0, 20.0), (-3.0, 4.0, 30.0), (8.0, 8.0, 15.0)]
X0_TEST = [(1.0, -1.0, 25.0), (-6.0, 6.0, 18.0), (10.0, 3.0, 32.0)]
T_SIM = (0.5, 1.0, 2.0)

# library: all monomials in x, y, z up to order 5 (56 terms)
POWERS = [(0, 0, 0)]
for order in range(1, 6):
    for combo in combinations_with_replacement(range(3), order):
        POWERS.append(tuple(combo.count(v) for v in range(3)))
POWERS = np.array(POWERS)
NAMES = ['1' if p.sum() == 0 else ''.join(v + (f'^{k}' if k > 1 else '')
         for v, k in zip('xyz', p) if k) for p in POWERS]


def lorenz(t, s):
    x, y, z = s
    return [SIG * (y - x), x * (RHO - z) - y, x * y - BETA * z]


def true_xi():
    Xi = np.zeros((len(POWERS), 3))
    ix = {n: i for i, n in enumerate(NAMES)}
    Xi[ix['x'], 0], Xi[ix['y'], 0] = -SIG, SIG
    Xi[ix['x'], 1], Xi[ix['y'], 1], Xi[ix['xz'], 1] = RHO, -1, -1
    Xi[ix['z'], 2], Xi[ix['xy'], 2] = -BETA, 1
    return Xi


def theta(X):
    X = np.atleast_2d(X)
    return np.prod(X[:, None, :] ** POWERS[None, :, :], axis=2)


def simulate_true(x0, tmax):
    t = np.arange(0, round(tmax / DT) + 1) * DT
    sol = solve_ivp(lorenz, (0, t[-1]), x0, method='DOP853', t_eval=t, rtol=1e-13, atol=1e-13)
    return t, sol.y.T


def derivative(X, t, case):
    """Returns (rows kept, Xdot) for case 'A' (exact), 'C2', 'C4'."""
    if case == 'A':
        return slice(None), np.array([lorenz(0, s) for s in X])
    if case == 'C2':
        return slice(1, -1), (X[2:] - X[:-2]) / (2 * DT)
    return slice(2, -2), (-X[4:] + 8 * X[3:-1] - 8 * X[1:-3] + X[:-4]) / (12 * DT)


def simulate_model(Xi, x0, tmax):
    t = np.arange(0, round(tmax / DT) + 1) * DT
    active = np.any(Xi != 0, axis=1)
    P, C = POWERS[active], Xi[active]

    def rhs(_, s):
        return np.prod(s[None, :] ** P, axis=1) @ C

    blow = lambda _, s: 1e4 - np.abs(s).max()
    blow.terminal = True
    sol = solve_ivp(rhs, (0, t[-1]), x0, method='DOP853', t_eval=t, rtol=1e-10, atol=1e-10,
                    events=blow)
    if sol.status != 0 or sol.y.shape[1] != len(t):
        return t, None
    return t, sol.y.T


def score(Xi, runs, case):
    """E_dv and E_sim(T) of one model, each the mean over the given runs."""
    edv, esim = [], {T: [] for T in T_SIM}
    for x0, t, X in runs:
        keep, dX = derivative(X, t, case)
        edv.append(rel_err(theta(X[keep]) @ Xi, dX))
        _, Xm = simulate_model(Xi, x0, max(T_SIM))
        for T in T_SIM:
            n = round(T / DT) + 1
            esim[T].append(np.inf if Xm is None else rel_err(Xm[:n], X[:n]))
    return float(np.mean(edv)), {T: float(np.mean(v)) for T, v in esim.items()}


def main():
    t, X = simulate_true(X0_TRAIN, 100.0)
    val = [(x0,) + simulate_true(x0, 20.0) for x0 in X0_VAL]
    test = [(x0,) + simulate_true(x0, 20.0) for x0 in X0_TEST]
    Xi_true = true_xi()
    lams = lambda_grid(-12, 10 ** 1.5)
    out = dict(names=NAMES, lams=lams.tolist(), cases={})
    for case in ('A', 'C2', 'C4'):
        keep, dX = derivative(X, t, case)
        Th = theta(X[keep])
        models = sweep(Th, dX, lams)
        rows = []
        for m in models:
            Xi = m['Xi']
            supp, true_supp = Xi != 0, Xi_true != 0
            edv, esim = score(Xi, val, case)
            rows.append(dict(
                lam_max=m['lam_max'], lam_min=m['lam_min'], terms=int(supp.sum()),
                wrong=int((supp & ~true_supp).sum()), missing=int((~supp & true_supp).sum()),
                coef_err=float(np.abs(Xi - Xi_true).max()),
                E_train=rel_err(Th @ Xi, dX), E_dv=edv,
                E_sim={str(T): v for T, v in esim.items()},
                stable=bool(np.isfinite(esim[max(T_SIM)]))))
            print(case, f"{m['lam_max']:.2e}", rows[-1]['terms'], rows[-1]['wrong'],
                  f"{rows[-1]['E_train']:.2e} {edv:.2e} {esim[1.0]:.2e}", flush=True)
        stable = [r['stable'] for r in rows]
        Edv = [r['E_dv'] for r in rows]
        Esim1 = [r['E_sim']['1.0'] for r in rows]
        rules = {}
        for name, E in (('E_dv', Edv), ('E_sim1', Esim1)):
            rules[name] = dict(R1=select_tol(E, 1.1), R2=select_tol(E, 10),
                               R3=select_level(E, 1e-3), R4=select_R4(E, stable))
        sel = rules['E_dv']['R4']
        Xi = models[sel]['Xi']
        edv_t, esim_t = score(Xi, test, case)
        # Galerkin-style reference: the true equations scored on the same test runs
        edv_true, esim_true = score(Xi_true, test, case)
        out['cases'][case] = dict(
            rows=rows, rules=rules, selected=sel, Xi_selected=Xi.tolist(),
            test=dict(E_dv=edv_t, E_sim={str(T): v for T, v in esim_t.items()}),
            test_true=dict(E_dv=edv_true, E_sim={str(T): v for T, v in esim_true.items()}))
    # figure data: the three error curves per lambda grid value
    json.dump(out, open('results_lorenz.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
