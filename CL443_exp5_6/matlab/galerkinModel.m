function [Cs, Cavg] = galerkinModel(xi, deltaFun, t, Cs0, Cavg0)
%GALERKINMODEL  Solve dCs/dtau = xi(1)*Cs + xi(2)*Cavg + xi(3)*delta together
%   with the exact mass balance dCavg/dtau = -3*delta.
%   Galerkin model: xi = [-35 35 -10]. A SINDy model uses its own xi.
%   Returns Cs = Inf if the solution grows without bound (|Cs| > 10).
t = t(:);
rhs = @(s, y) [xi(1)*y(1) + xi(2)*y(2) + xi(3)*deltaFun(s); -3*deltaFun(s)];
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-12, 'Events', @blowUp);
[tt, Y] = ode45(rhs, t, [Cs0; Cavg0], opts);
if numel(tt) ~= numel(t) || any(abs(Y(:, 1)) > 10)
    Cs = Inf(size(t)); Cavg = Inf(size(t));
else
    Cs = Y(:, 1); Cavg = Y(:, 2);
end
end

function [value, isterminal, direction] = blowUp(~, y)
value = 10 - abs(y(1)); isterminal = 1; direction = 0;
end
