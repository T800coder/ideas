function Xi = stlsq(Theta, dX, lambda, nIter)
%STLSQ  Sequentially thresholded least squares (unnormalised library).
if nargin < 4, nIter = 10; end
Xi = Theta \ dX;
for it = 1:nIter
    small = abs(Xi) < lambda;
    Xi(small) = 0;
    for j = 1:size(dX, 2)
        big = ~small(:, j);
        if any(big)
            Xi(big, j) = Theta(:, big) \ dX(:, j);
        end
    end
end
end
