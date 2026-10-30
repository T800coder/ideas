"""Spherical particle diffusion PDE and the Galerkin (two-state) model.

PDE (dimensionless):  dC/dtau = f * (1/r^2) d/dr( r^2 dC/dr ),   0 < r < 1
                      dC/dr(0) = 0,   f * dC/dr(1) = -delta(tau),   C(r,0) = 1
Outputs: Cs = C(1,tau),  Cavg = 3 * int_0^1 C r^2 dr.

Solved by Chebyshev collocation on -1 <= x <= 1 (even solution, so r = 0 is
never a collocation point) and an implicit stiff integrator.
"""
import numpy as np
from scipy.integrate import solve_ivp

A_FLUX = 0.025


def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1 / c) / (dX + np.eye(N + 1))
    D -= np.diag(D.sum(axis=1))
    return D, x


class PDE:
    def __init__(self, N=61, f=1.0):
        # Chebyshev grid with N odd: x_j = cos(j pi/N); keep the M = (N+1)/2 points
        # with x > 0 (r_j = x_j) and fold the matrices for an even solution.
        assert N % 2 == 1
        D, x = cheb(N)
        M = (N + 1) // 2
        D2 = D @ D
        fold = lambda A: A[:M, :M] + A[:M, ::-1][:, :M]
        De, D2e, r = fold(D), fold(D2), x[:M]
        self.r, self.f, self.M = r, f, M
        # node 0 is r = 1; Neumann: De[0,:] u = -delta/f
        I = np.arange(1, M)
        Op = f * (D2e + np.diag(2 / r) @ De)
        p = -De[0, I] / De[0, 0]                  # u0 = p.uI + q*delta
        q = -1 / (f * De[0, 0])
        self.p, self.q, self.I = p, q, I
        self.L = Op[np.ix_(I, I)] + np.outer(Op[I, 0], p)
        self.b = Op[I, 0] * q
        # Clenshaw-Curtis on [-1,1] folded: Cavg = 1.5 * int_{-1}^{1} u x^2 dx
        w = self._ccweights(N) * x ** 2
        self.w = 1.5 * (w[:M] + w[::-1][:M])

    @staticmethod
    def _ccweights(N):
        theta = np.pi * np.arange(N + 1) / N
        w = np.zeros(N + 1)
        v = np.ones(N - 1)
        ii = np.arange(1, N)
        if N % 2 == 0:
            w[0] = w[N] = 1 / (N ** 2 - 1)
            for k in range(1, N // 2):
                v -= 2 * np.cos(2 * k * theta[ii]) / (4 * k * k - 1)
            v -= np.cos(N * theta[ii]) / (N ** 2 - 1)
        else:
            w[0] = w[N] = 1 / N ** 2
            for k in range(1, (N - 1) // 2 + 1):
                v -= 2 * np.cos(2 * k * theta[ii]) / (4 * k * k - 1)
        w[ii] = 2 * v / N
        return w

    def full(self, uI, d):
        return np.concatenate([[self.p @ uI + self.q * d], uI])

    def solve(self, delta, t_eval, u0=None, rtol=1e-10, atol=1e-12):
        """delta: callable tau -> flux. Returns Cs, Cavg at t_eval, final interior state."""
        uI0 = np.ones(self.M - 1) if u0 is None else u0
        L, b = self.L, self.b
        sol = solve_ivp(lambda t, u: L @ u + b * delta(t), (t_eval[0], t_eval[-1]), uI0,
                        method='Radau', jac=L, t_eval=t_eval, rtol=rtol, atol=atol)
        assert sol.success, sol.message
        Cs = np.empty(len(t_eval)); Ca = np.empty(len(t_eval))
        for k, t in enumerate(sol.t):
            u = self.full(sol.y[:, k], delta(t))
            Cs[k] = u[0]; Ca[k] = self.w @ u
        return Cs, Ca, sol.y[:, -1]


def galerkin(delta, t_eval, Cs0=1.0, Ca0=1.0, cs=-35.0, ca=35.0, cd=-10.0, f=1.0):
    """dCavg = -3 delta ; dCs = cs*f*Cs + ca*f*Cavg + cd*delta (Galerkin: -35, 35, -10)."""
    rhs = lambda t, y: [cs * y[0] + ca * y[1] + cd * delta(t), -3 * delta(t)]
    sol = solve_ivp(rhs, (t_eval[0], t_eval[-1]), [Cs0, Ca0], method='Radau',
                    t_eval=t_eval, rtol=1e-11, atol=1e-13)
    assert sol.success
    return sol.y[0], sol.y[1]
