function [mat, padding_zeros] = vec2mat(x, mat_cols)

if size(x,1) ~= 1
    x=x.';
end

mat_rows = ceil(length(x)/mat_cols);
padding_zeros = mat_rows*mat_cols - length(x);	
x = [x, zeros(1, padding_zeros)];
mat = reshape(x, mat_cols, mat_rows).';
