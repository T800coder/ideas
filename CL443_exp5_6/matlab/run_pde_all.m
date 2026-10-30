% RUN_PDE_ALL  Experiment 6, part 2: every training frequency, then the
% cross-test (each selected model on the cosine run at every w, last period,
% Rel of Cs and of the gap Cs - Cavg, in %).
A = 0.025;
omegas = [0.1 1 10 100];
names = {'Galerkin'}; XI = {[-35 35 -10]};
for w = omegas
    o = run_pde_omega(w, A);
    names{end+1} = sprintf('SINDy, trained at w = %g', w); %#ok<SAGROW>
    XI{end+1} = o.xi; %#ok<SAGROW>
end
fprintf('\nCross-test, Rel (%%), cosine flux, last period: Cs / gap\n');
fprintf('%-28s', 'model'); fprintf('   w = %-12g', omegas); fprintf('\n');
for m = 1:numel(XI)
    fprintf('%-28s', names{m});
    for w = omegas
        P = 2*pi/w; t = linspace(0, 10*P, 2001)';
        d = @(s) A*cos(w*s);
        [Cs, Ca] = solvePDE(d, t);
        [CsM, CaM] = galerkinModel(XI{m}, d, t, Cs(1), Ca(1));
        last = t >= 9*P - 1e-12;
        fprintf('  %8.3g / %-8.3g', 100*relErr(CsM(last), Cs(last)), ...
            100*relErr(CsM(last) - CaM(last), Cs(last) - Ca(last)));
    end
    fprintf('\n');
end
