function J = computeCostMulti(X, y, theta)
%COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
%   J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.
for j = 1 : m
    sum0 = 0;
    for i = 1 : size(X,2)
        sum0 = sum0 + theta(i)*X(j,i);
    end
   J = J + (sum0-y(j))*(sum0-y(j)); 
end
J = J/2/m;
% =========================================================================

end
