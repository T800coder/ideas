function [Cs, Cavg, uEnd] = solvePDE(deltaFun, t, u0, f)
%SOLVEPDE  Spherical diffusion with surface flux, constant diffusivity f:
%   dC/dtau = f/r^2 d/dr(r^2 dC/dr),  f dC/dr(1) = -delta(tau),  dC/dr(0) = 0.
%   Uses pdepe when it exists (MATLAB); otherwise (e.g. Octave) a Chebyshev
%   collocation method of lines, even in r, integrated with ode15s.
%   u0: [] for C(r,0) = 1, or the uEnd of a previous call (same method).
if nargin < 4, f = 1; end
if nargin < 3, u0 = []; end
t = t(:);
if exist('pdepe', 'file') == 2
    r = [linspace(0, 0.9, 200), linspace(0.9, 1, 801)];
    r = unique(r);
    if isempty(u0), ic = @(x) 1; else, ic = @(x) interp1(r, u0, x); end
    pdefun = @(x, s, u, dudx) deal(1, f*dudx, 0);
    bcfun = @(xl, ul, xr, ur, s) deal(0, 1, deltaFun(s), 1);
    opts = odeset('RelTol', 1e-9, 'AbsTol', 1e-11);
    sol = pdepe(2, pdefun, ic, bcfun, r, t, opts);
    Cs = sol(:, end);
    Cavg = 3*trapz(r, sol .* r.^2, 2);
    uEnd = sol(end, :);
    return
end
persistent M L b p q w f0
N = 61;
if isempty(f0) || f0 ~= f
    [L, b, p, q, w, M] = chebOperator(N, f);
    f0 = f;
end
if isempty(u0), u0 = ones(M - 1, 1); end
opts = odeset('RelTol', 1e-9, 'AbsTol', 1e-11, 'Jacobian', @(s, u) L);
[~, U] = ode15s(@(s, u) L*u + b*deltaFun(s), t, u0, opts);
if numel(t) == 2, U = U([1 end], :); end
d = arrayfun(deltaFun, t);
u0col = U*p(:) + q*d;                 % surface value u(r = 1)
full = [u0col, U];
Cs = u0col;
Cavg = full*w(:);
uEnd = U(end, :)';
end

function [L, b, p, q, w, M] = chebOperator(N, f)
% Chebyshev grid x_j = cos(j pi/N), N odd; keep the M = (N+1)/2 points with
% x > 0 (r = x) and fold the matrices for an even solution.
x = cos(pi*(0:N)'/N);
c = [2; ones(N-1, 1); 2].*(-1).^(0:N)';
X = repmat(x, 1, N+1);
dX = X - X';
D = (c*(1./c)')./(dX + eye(N+1));
D = D - diag(sum(D, 2));
D2 = D*D;
M = (N + 1)/2;
fold = @(A) A(1:M, 1:M) + A(1:M, end:-1:end-M+1);
De = fold(D); D2e = fold(D2); r = x(1:M);
I = 2:M;
Op = f*(D2e + diag(2./r)*De);
p = -De(1, I)/De(1, 1);               % u(1) = p*uI + q*delta
q = -1/(f*De(1, 1));
L = Op(I, I) + Op(I, 1)*p;
b = Op(I, 1)*q;
% Clenshaw-Curtis weights on [-1, 1]; Cavg = 1.5 * int_{-1}^{1} u x^2 dx
theta = pi*(0:N)'/N;
wc = zeros(N+1, 1); v = ones(N-1, 1); ii = 2:N;
wc([1 N+1]) = 1/N^2;
for k = 1:(N-1)/2
    v = v - 2*cos(2*k*theta(ii))/(4*k^2 - 1);
end
wc(ii) = 2*v/N;
wc = wc.*x.^2;
w = 1.5*(wc(1:M) + wc(end:-1:end-M+1));
end
