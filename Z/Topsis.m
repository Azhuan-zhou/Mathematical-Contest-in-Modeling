clc;clear
load summer_analysis.mat
[n,m] = size(X);
disp(['共有' num2str(n) '个评价对象, ' num2str(m) '个评价指标']) 
Judge = input(['这' num2str(m) '个指标是否需要经过正向化处理，需要请输入1 ，不需要输入0：  ']);
%正向化
if Judge == 1
    Position = input('请输入需要正向化处理的指标所在的列，例如第2、3、6三列需要处理，那么你需要输入[2,3,6]： ');
    disp('请输入需要处理的这些列的指标类型（1：极小型， 2：中间型， 3：区间型） ')
    Type = input('例如：第2列是极小型，第3列是区间型，第6列是中间型，就输入[1,3,2]：  '); 
    for i = 1 : size(Position,2)  
        X(:,Position(i)) = Positivization(X(:,Position(i)),Type(i),Position(i));
    end
    disp('正向化后的矩阵 X =  ')
    disp(X)
end
%标准化
t=0;
for j=1:m
    for i=1:n
        if X(i,j)>0
            Z(i,j) = X(i,j)./ sum(X(:,j).^2);
        else
            t=j;
            Z(i,j)=(X(i,t)-min(X(:,t)))/(max(X(:,t))-min(X(:,t)));
        end
    end
end
disp('标准化矩阵 Z = ')
disp(Z)
%增加权重
disp("请输入是否需要增加权重向量，需要输入1，不需要输入0")
Judge = input('请输入是否需要增加权重： ');
if Judge == 1
    Judge = input('使用熵权法确定权重请输入1，否则输入0： ');
    if Judge == 1
        if sum(sum(Z<0)) >0  
            disp('原来标准化得到的Z矩阵中存在负数，所以需要对X重新标准化')
            for i = 1:n
                for j = 1:m
                    Z(i,j) = [X(i,j) - min(X(:,j))] / [max(X(:,j)) - min(X(:,j))];
                end
            end
            disp('X重新进行标准化得到的标准化矩阵Z为:  ')
            disp(Z)
        end
        weight = Entropy_Method(Z);
        disp('熵权法确定的权重为：')
        disp(weight)
    else
        disp('如果你有3个指标，你就需要输入3个权重，例如它们分别为0.25,0.25,0.5, 则你需要输入[0.25,0.25,0.5]');
        weight = input(['你需要输入' num2str(m) '个权数。' '请以行向量的形式输入这' num2str(m) '个权重: ']);
        OK = 0; 
        while OK == 0 
            if abs(sum(weight) -1)<0.000001 && size(weight,1) == 1 && size(weight,2) == m 
                OK =1;
            else
                weight = input('你输入的有误，请重新输入权重行向量: ');
            end
        end
    end
else
    weight = ones(1,m) ./ m ; 
end
%利用权重计算评分
D_P = sum(((Z - repmat(max(Z),n,1)) .^ 2 ) .* repmat(weight,n,1) ,2) .^ 0.5;  
D_N = sum(((Z - repmat(min(Z),n,1)) .^ 2 ) .* repmat(weight,n,1) ,2) .^ 0.5;  
S = D_N ./ (D_P+D_N);    
disp('最后的得分为：')
stand_S = S / sum(S)
[sorted_S,index] = sort(stand_S ,'descend')

