% TEST_QUICK  Fast checks of the MATLAB code against the Python results.
% 1) relErr on a known case; 2) PDE solver vs the Galerkin model (Table of
% Experiment 5, last period); 3) SINDy at w = 1 recovers -35.04, 35.04, -10.004.
assert(abs(relErr([1;2;3] + 0.1, [1;2;3]) - 0.05) < 1e-12)
A = 0.025;
for w = [0.5 200]
    P = 2*pi/w; t = linspace(0, 10*P, 2001)'; d = @(s) A*cos(w*s);
    [Cs, Ca] = solvePDE(d, t);
    G = galerkinModel([-35 35 -10], d, t, 1, 1);
    last = t >= 9*P - 1e-12;
    fprintf('w = %5g: band = %.4f, Rel last period = %.4g %%\n', w, ...
        max(Cs(last)) - min(Cs(last)), 100*relErr(G(last), Cs(last)));
end
o = run_pde_omega(1, A);
assert(max(abs(o.xi(:)' - [-35.039 35.039 -10.004])) < 2e-3)
disp('test_quick: all checks passed')
