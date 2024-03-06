clc;clear;
load 'Year.mat'
load 'GDP.mat'
figure(1)
ydata_log=log(ydata);%通过图形判断曲线类型
plot(xdata,ydata_log,'b+');%通过求解对数，简化曲线
xlabel("Year");
ylabel('ln(GDP)');
title('The relation between ln(GDP) and Year');
legend('ln(GDP)');

a=polyfit(xdata,ydata_log,4);%拟合多项式曲线,得出系数
t_1=input('请输入GDP开始核算年份:');
t_2=input('请输入GDP结束核算年份：');
xdata_constant=t_1:0.1:t_2;
ydata_log_costant= polyval(a, xdata_constant);%利用求解出的系数求出多项式方程的因变量
figure(2)
plot(xdata,ydata_log,'k+',xdata_constant,ydata_log_costant,'r'); 
x0=[a(1),a(2),a(3),a(4),a(5)];
fun=@(x,xdata)exp(x(1)*xdata.^4+x(2)*xdata.^3+x(3)*xdata.^2+x(4)*xdata+x(5));
x = lsqcurvefit(fun,x0,xdata,ydata);%非线性拟合
figure(3)
xdata_constant_2=t_1:0.1:1984;
y=exp(x(1)*xdata_constant_2.^4+x(2)*xdata_constant_2.^3+x(3)*xdata_constant_2.^2+x(4)*xdata_constant_2+x(5));

plot(xdata,ydata,'k+',xdata_constant_2,y,'b-');
legend('GDP','Fitted curve');
title('GDP growth');

figure(4)
plot(xdata,ydata,'+');
xlabel("Year");
ylabel('GDP');
title('GDP growth');
legend('GDP');
