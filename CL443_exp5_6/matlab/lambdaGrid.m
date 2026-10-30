function lams = lambdaGrid(loExp, hi, perDecade)
%LAMBDAGRID  lambda = 10^(k/perDecade) from 10^loExp up to hi, largest first.
if nargin < 3, perDecade = 4; end
k = loExp*perDecade : floor(log10(hi)*perDecade + 1e-9);
lams = 10.^(k / perDecade);
if lams(end) < hi*(1 - 1e-12), lams(end+1) = hi; end
lams = fliplr(lams);
end
