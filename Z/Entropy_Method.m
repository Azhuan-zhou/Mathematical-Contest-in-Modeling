function [W] = Entropy_Method(Z)
 [n,m] = size(Z);
    D = zeros(1,m);  % 初始化保存信息效用值的行向量
    for i = 1:m
        x = Z(:,i);  % 取出第i列的指标
        p = x / sum(x);
        e = -sum(p .* mylog(p)) / log(n); % 计算信息熵。mylog是自己定义的函数，当p==0,时lnp也返回0.
        D(i) = 1- e; % 计算信息效用值
    end
    W = D ./ sum(D);  % 将信息效用值归一化，得到权重    
end