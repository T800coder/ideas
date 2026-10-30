function models = sweepLambda(Theta, dX, lams)
%SWEEPLAMBDA  STLSQ for every lambda (give lams from largest to smallest);
%   lambda values giving the same set of terms are merged into one model.
%   models(k).Xi, .lamMax, .lamMin
models = struct('Xi', {}, 'lamMax', {}, 'lamMin', {});
for lam = lams(:)'
    Xi = stlsq(Theta, dX, lam);
    if ~isempty(models) && isequal(models(end).Xi ~= 0, Xi ~= 0)
        models(end).lamMin = lam;
    else
        models(end+1) = struct('Xi', Xi, 'lamMax', lam, 'lamMin', lam); %#ok<AGROW>
    end
end
end
