function out = run_pde_omega(w, A)
%RUN_PDE_OMEGA  Experiment 6, part 2, at one training frequency w.
%   Training: delta = A sin(w tau), 5 periods, dtau = P/200 (1001 points).
%   Library {Cs, Cavg, delta}; dCs/dtau by 2nd-order differences (gradient).
%   Validation (10 periods): cos, sin late, sin ph, cos ph -> E_sim (Rel of Cs,
%   whole run). Lambda by R4 on the stacked E_sim, unstable models removed.
%   Test (used once): random multisine, 10 periods.
if nargin < 2, A = 0.025; end
P = 2*pi/w; pts = 200; nTrain = 5; nVal = 10;
tTr = linspace(0, nTrain*P, nTrain*pts + 1)';
sinF = @(s) A*sin(w*s);
[Cs, Ca, uEnd] = solvePDE(sinF, tTr);
Theta = [Cs, Ca, sinF(tTr)];
dCs = gradient2(Cs, tTr);

tVal = linspace(0, nVal*P, nVal*pts + 1)';
val = {struct('name', 'cos',      'd', @(s) A*cos(w*s),        't', tVal, 'u0', []), ...
       struct('name', 'sin late', 'd', sinF,                   't', nTrain*P + tVal, 'u0', uEnd), ...
       struct('name', 'sin ph',   'd', @(s) A*sin(w*s + pi/4), 't', tVal, 'u0', []), ...
       struct('name', 'cos ph',   'd', @(s) A*cos(w*s + pi/4), 't', tVal, 'u0', [])};
for j = 1:numel(val)
    [val{j}.Cs, val{j}.Ca] = solvePDE(val{j}.d, val{j}.t, val{j}.u0);
end

models = sweepLambda(Theta, dCs, lambdaGrid(-6, 1e3));
nM = numel(models);
Esim = zeros(nM, numel(val));
for k = 1:nM
    for j = 1:numel(val)
        v = val{j};
        CsM = galerkinModel(models(k).Xi, v.d, v.t, v.Cs(1), v.Ca(1));
        Esim(k, j) = relErr(CsM, v.Cs);
    end
end
stacked = mean(Esim, 2);
stable = all(isfinite(Esim), 2);
k = selectLambdaR4(stacked, stable);
xi = models(k).Xi;

% test: random multisine (used once)
R = struct('w', {0.1, 1, 10, 100}, ...
    'a', {[0.82 0.74 0.75], [0.54 0.91 0.82], [0.91 0.53 0.69], [0.62 0.97 0.53]}, ...
    'ph', {[4.62 3.09 0.48], [1.24 3.70 5.63], [4.99 2.70 4.75], [1.31 0.81 2.65]});
r = R([R.w] == w);
wk = [w/2, w, 2*w];
raw = @(s) r.a(1)*sin(wk(1)*s + r.ph(1)) + r.a(2)*sin(wk(2)*s + r.ph(2)) + r.a(3)*sin(wk(3)*s + r.ph(3));
tt = linspace(0, nVal*4*pi/w, 200001);
scale = A/max(abs(raw(tt)));
rnd = @(s) scale*raw(s);
[CsT, CaT] = solvePDE(rnd, tVal);
EsimTest = relErr(galerkinModel(xi, rnd, tVal, CsT(1), CaT(1)), CsT);
EsimGal = relErr(galerkinModel([-35 35 -10], rnd, tVal, CsT(1), CaT(1)), CsT);

fprintf('\nomega = %g\n', w);
fprintf('  %-22s %9s %9s %9s %7s %10s\n', 'lambda range', 'Cs', 'Cavg', 'delta', 'stable', 'stacked %');
for m = 1:nM
    fprintf('  %9.2e - %9.2e %+9.3f %+9.3f %+9.3f %7d %10.3g\n', models(m).lamMin, ...
        models(m).lamMax, models(m).Xi, stable(m), 100*stacked(m));
end
fprintf('  selected: %d terms, lambda = %.3g, xi = [%.3f %.3f %.3f]\n', nnz(xi), models(k).lamMax, xi);
fprintf('  test (random): E_sim SINDy = %.3g %%, Galerkin = %.3g %%\n', 100*EsimTest, 100*EsimGal);
out = struct('w', w, 'xi', xi, 'lambda', models(k).lamMax, 'models', models, ...
    'Esim', Esim, 'stable', stable, 'EsimTest', EsimTest, 'EsimTestGalerkin', EsimGal);
end

function d = gradient2(y, t)
% 2nd-order differences at every point: central inside, one-sided at the ends
h = t(2) - t(1);
d = zeros(size(y));
d(2:end-1) = (y(3:end) - y(1:end-2))/(2*h);
d(1) = (-3*y(1) + 4*y(2) - y(3))/(2*h);
d(end) = (3*y(end) - 4*y(end-1) + y(end-2))/(2*h);
end
