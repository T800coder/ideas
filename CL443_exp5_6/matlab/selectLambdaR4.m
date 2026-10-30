function k = selectLambdaR4(err, stable)
%SELECTLAMBDAR4  Knee rule R4. err(i) is the validation error of model i,
%   models ordered from largest to smallest lambda. Unstable models
%   (stable(i) false) are removed first (step 4). Returns the index of the
%   model just after the largest drop in log10(error).
if nargin < 2, stable = true(size(err)); end
idx = find(stable);
e = log10(max(err(idx), realmin));
[~, j] = max(e(1:end-1) - e(2:end));
k = idx(j + 1);
end
