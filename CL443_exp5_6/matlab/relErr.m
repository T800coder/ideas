function e = relErr(pred, ref)
%RELERR  Agreed error: per column, RMS(pred - ref) / (max(ref) - min(ref)),
%   both over the rows given (the window), then the mean over columns.
%   Returned as a fraction; multiply by 100 for %. Non-finite pred gives Inf.
if any(~isfinite(pred(:)))
    e = Inf;
    return
end
rmsErr = sqrt(mean((pred - ref).^2, 1));
band = max(ref, [], 1) - min(ref, [], 1);
e = mean(rmsErr ./ band);
end
