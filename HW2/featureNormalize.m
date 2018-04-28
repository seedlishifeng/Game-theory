function [X_norm, mu, sigma] = featureNormalize(X)

X_norm = X;
mu=mean(X);
sigma=std(X);
for i=1:size(mu,2)
    X_norm(:,i)=(X(:,i)-mu(i))./sigma(i);
  end
end

function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

feature_number=size(X,2);
temp=zeros(feature_number,1);

for iter = 1:num_iters
    for i=1:feature_number
        temp(i)=theta(i)-(alpha/m)*sum((X*theta-y).*X(:,i));
    end
    for j=1:feature_number
        theta(j)=temp(j);
    end
    J_history(iter) = computeCostMulti(X, y, theta);
end
end

function [X_norm, mu, sigma] = featureNormalize(X)

X_norm = X;
mu=mean(X);
sigma=std(X);
for i=1:size(mu,2)
    X_norm(:,i)=(X(:,i)-mu(i))./sigma(i);
end
end


load('detroit.mat','data');
re=zeros(7,1);
for i =2:7
 X = [data(:, 1),data(:, 8),data(:, i)];%change the third column to
 y = data(:, 10);
 m = length(y);

% Scale features and set them to zero mean
 [X,mu,sigma] = featureNormalize(X);

% Add intercept term to X
 X = [ones(m, 1) X];

% Choose some alpha value
 alpha = 0.01;
 num_iters = 5000;

% Init Theta and Run Gradient Descent 
 theta = zeros(4, 1);
 [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);

 % Plot the convergence graph

figure;
plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
xlabel('Number of iterations');
l=['Cost for No.' int2str(i) ' variable in dataset'];
ylabel(l);

% Display gradient descent's result
fprintf('Cost computed from gradient descent: \n');
fprintf(' %f \n', J_history(num_iters,1));
fprintf('\n');

re(i,1)=J_history(num_iters,1);
end

figure
x=2:7;
y=re(2:7,1);
bar(x,y)
set(gca,'xticklabel',{'UEMP','MAN','LIC','GR','NMAN','GOV','HE'})
xlabel('variable in dataset');
ylabel('Minmum cost for for each variable in dataset');
min=2;
for index=3:size(re,1)
    if re(min,1)>re(index,1)
        min=index;
    end
end
fprintf('The best input variable is the No.%d variable in dataset and the minimum cost is %f\n',min,re(min,1));
