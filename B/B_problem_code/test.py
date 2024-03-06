import numpy as np
from numpy import tan, pi, sqrt
tan(1.5/180*pi)
def calculate(x):
    result = (207 - (9*tan(1.5/180*pi)/10 - sqrt(3)*9/30)*(207+sqrt(3)*x)/(tan(1.5/180*pi)+sqrt(3)/3))/(sqrt(3)/3)
    return result

if __name__ == '__main__':
    x_0 = 207 * np.sqrt(3)
    x = [x_0]
    y = [207]
    count = 0
    while x[count] < 4*1852:
        x_i = calculate(x[count])
        count += 1
        x.append(x_i)
    print(len(x))
