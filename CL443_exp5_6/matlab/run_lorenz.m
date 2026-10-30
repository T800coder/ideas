function run_lorenz()
% RUN_LORENZ  Experiment 6, part 1: SINDy on the Lorenz system.
% Errors: rel_err per variable, averaged over x, y, z (and over the runs).
% Lambda chosen by R4 on E_dv; the chosen model is scored once on 3 test runs.
sig = 10; rho = 28; beta = 8/3; dt = 1e-3;
lor = @(t, s) [sig*(s(2) - s(1)); s(1)*(rho - s(3)) - s(2); s(1)*s(2) - beta*s(3)];
opts = odeset('RelTol', 1e-12, 'AbsTol', 1e-12);
sim = @(x0, T) deal((0:dt:T)', simOde(lor, x0, (0:dt:T)', opts));

% library: monomials up to order 5 (56 terms)
P = zeros(0, 3);
for n = 0:5
    for i = n:-1:0
        for j = (n - i):-1:0
            P(end+1, :) = [i, j, n - i - j]; %#ok<SAGROW>
        end
    end
end
theta = @(X) prod(bsxfun(@power, permute(X, [1 3 2]), permute(P, [3 1 2])), 3);
XiTrue = zeros(size(P, 1), 3);
row = @(p) find(ismember(P, p, 'rows'));
XiTrue(row([1 0 0]), 1) = -sig;  XiTrue(row([0 1 0]), 1) = sig;
XiTrue(row([1 0 0]), 2) = rho;   XiTrue(row([0 1 0]), 2) = -1;  XiTrue(row([1 0 1]), 2) = -1;
XiTrue(row([0 0 1]), 3) = -beta; XiTrue(row([1 1 0]), 3) = 1;

[t, X] = sim([-8 7 27], 100);
val = {[5 -5 20], [-3 4 30], [8 8 15]};
tst = {[1 -1 25], [-6 6 18], [10 3 32]};
for j = 1:3
    [~, val{j}] = sim(val{j}, 20);
    [~, tst{j}] = sim(tst{j}, 20);
end
lams = lambdaGrid(-12, 10^1.5);
cases = {'A', 'C2', 'C4'};
for c = 1:3
    [keep, dX] = deriv(X, dt, cases{c}, lor);
    Th = theta(X(keep, :));
    models = sweepLambda(Th, dX, lams);
    Edv = zeros(numel(models), 1); Esim1 = Edv;
    for k = 1:numel(models)
        [Edv(k), Esim1(k)] = scoreModel(models(k).Xi, val, theta, P, dt, cases{c}, lor);
    end
    sel = selectLambdaR4(Edv, isfinite(Esim1));
    Xi = models(sel).Xi;
    [EdvT, EsimT] = scoreModel(Xi, tst, theta, P, dt, cases{c}, lor);
    fprintf('\nCase %s\n  %-24s %5s %5s %10s %10s\n', cases{c}, 'lambda range', 'terms', 'wrong', 'E_dv', 'E_sim(1)');
    for k = 1:numel(models)
        s = models(k).Xi ~= 0;
        fprintf('  %9.2e - %9.2e %5d %5d %10.2e %10.2e\n', models(k).lamMin, models(k).lamMax, ...
            nnz(s), nnz(s & XiTrue == 0), Edv(k), Esim1(k));
    end
    fprintf('  selected: %d terms, lambda = %.3g, max coef. err. = %.2e\n', nnz(Xi), ...
        models(sel).lamMax, max(abs(Xi(:) - XiTrue(:))));
    fprintf('  test: E_dv = %.2e, E_sim(1) = %.2e\n', EdvT, EsimT);
end
end

function X = simOde(f, x0, t, opts)
[~, X] = ode45(f, t, x0, opts);
end

function [keep, dX] = deriv(X, dt, c, lor)
switch c
    case 'A'
        keep = 1:size(X, 1);
        dX = [10*(X(:,2) - X(:,1)), X(:,1).*(28 - X(:,3)) - X(:,2), X(:,1).*X(:,2) - 8/3*X(:,3)];
    case 'C2'
        keep = 2:size(X, 1) - 1;
        dX = (X(3:end, :) - X(1:end-2, :))/(2*dt);
    case 'C4'
        keep = 3:size(X, 1) - 2;
        dX = (-X(5:end, :) + 8*X(4:end-1, :) - 8*X(2:end-3, :) + X(1:end-4, :))/(12*dt);
end
end

function [Edv, Esim1] = scoreModel(Xi, runs, theta, P, dt, c, lor)
% E_dv: mean over runs of relErr(theta(X)*Xi, dX); E_sim(T=1): model solved from x0
active = any(Xi ~= 0, 2);
Pa = P(active, :); Ca = Xi(active, :);
rhs = @(t, s) (prod(bsxfun(@power, s(:)', Pa), 2)'*Ca)';
n = round(1/dt) + 1;
e1 = zeros(1, numel(runs)); e2 = e1;
for j = 1:numel(runs)
    X = runs{j};
    [keep, dX] = deriv(X, dt, c, lor);
    e1(j) = relErr(theta(X(keep, :))*Xi, dX);
    opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-10, 'Events', @(t, s) deal(1e4 - max(abs(s)), 1, 0));
    [tt, Xm] = ode45(rhs, (0:n-1)'*dt, X(1, :)', opts);
    if numel(tt) < n, e2(j) = Inf; else, e2(j) = relErr(Xm, X(1:n, :)); end
end
Edv = mean(e1); Esim1 = mean(e2);
end
