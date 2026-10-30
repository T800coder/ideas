"""Error measure, STLSQ and the lambda-selection rule (R4) shared by all experiments."""
import numpy as np


def rel_err(pred, ref):
    """Agreed error: for each variable (column), RMS(pred - ref) / (max ref - min ref),
    both over the same window; then the mean over variables. Returned as a fraction.
    Non-finite predictions give inf."""
    pred = np.atleast_2d(np.asarray(pred, float).T).T
    ref = np.atleast_2d(np.asarray(ref, float).T).T
    if not np.all(np.isfinite(pred)):
        return np.inf
    rms = np.sqrt(np.mean((pred - ref) ** 2, axis=0))
    band = ref.max(axis=0) - ref.min(axis=0)
    return float(np.mean(rms / band))


def stlsq(Theta, dX, lam, n_iter=10):
    """Sequentially thresholded least squares (Brunton et al. 2016), unnormalised library."""
    Xi = np.linalg.lstsq(Theta, dX, rcond=None)[0]
    for _ in range(n_iter):
        small = np.abs(Xi) < lam
        Xi[small] = 0
        for j in range(dX.shape[1]):
            big = ~small[:, j]
            if big.any():
                Xi[big, j] = np.linalg.lstsq(Theta[:, big], dX[:, j], rcond=None)[0]
    return Xi


def lambda_grid(lo_exp, hi, per_decade=4):
    """lambda = 10^(k/per_decade) from 10^lo_exp up to hi, listed from largest to smallest."""
    k = np.arange(lo_exp * per_decade, int(np.floor(np.log10(hi) * per_decade + 1e-9)) + 1)
    lam = 10.0 ** (k / per_decade)
    if lam[-1] < hi * (1 - 1e-12):
        lam = np.append(lam, hi)
    return lam[::-1]


def sweep(Theta, dX, lams):
    """Run STLSQ for every lambda (largest first) and merge equal supports into one model.
    Returns list of dicts: Xi, lam_max, lam_min, support."""
    models = []
    for lam in lams:
        Xi = stlsq(Theta, dX, lam)
        supp = Xi != 0
        if models and np.array_equal(models[-1]['support'], supp):
            models[-1]['lam_min'] = lam
        else:
            models.append(dict(Xi=Xi, support=supp, lam_max=lam, lam_min=lam))
    return models


def select_R4(errors, stable=None):
    """R4 'knee' rule. errors: one error per model, models ordered from largest to smallest
    lambda. Unstable models (stable[i] False) are discarded first (step 4).
    Returns the index of the model just after the largest drop in log10(error)."""
    idx = [i for i in range(len(errors)) if stable is None or stable[i]]
    e = np.log10(np.maximum(np.array([errors[i] for i in idx]), 1e-300))
    drops = e[:-1] - e[1:]
    return idx[int(np.argmax(drops)) + 1]


def select_tol(errors, factor):
    """R1 (factor 1.1) / R2 (factor 10): largest lambda whose error <= factor * min error."""
    e = np.array(errors)
    return int(np.where(e <= factor * e[np.isfinite(e)].min())[0][0])


def select_level(errors, level):
    """R3: largest lambda whose error is below a fixed level."""
    e = np.array(errors)
    ok = np.where(e < level)[0]
    return int(ok[0]) if len(ok) else None
