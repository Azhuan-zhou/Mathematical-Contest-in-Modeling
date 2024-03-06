import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
import numpy as np
import matplotlib as mpl
import os
from scipy.signal import savgol_filter
mpl.use('TKAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def fitting(y):
    data = pd.read_csv('D:\\wodedaima\\B\\axsis_data.csv', encoding='gbk', index_col=0)
    x_list = data.columns.tolist()
    x_list = np.float_(x_list)
    position = int(y / 0.02)
    y_list = data.index.tolist()
    y_in_list = y_list[position]
    deep = data.loc[y_in_list]
    deep = np.array(deep)
    deep = (197 - deep) / 1852
    coefficient = np.polyfit(x_list, deep, 2)
    return coefficient


def returnX():
    num = {}
    for z in np.arange(0, 5.02, 0.02):
        print("第", int(z / 0.02) + 1, "次循环开始")
        # dummy = []
        a, b, c = fitting(z)
        x, y = sp.symbols('x y')  # 变量
        f1 = a * x ** 2 + b * x + c - y
        x_flag = 0
        y_flag = c
        count = 1
        while 1:
            xi = (197 / 1852 - y_flag) * 1.73 + x_flag
            f2 = (-1.73 / 3) * (x - (197 / 1852 - y_flag) * 1.73 - x_flag) - y + 197 / 1852
            solution = sp.solve((f1, f2), (x, y))
            print("第", count, "次迭代")
            print(xi)

            if type(solution) == dict:
                x_flag = sp.re(solution[x])
                y_flag = sp.re(solution[y])
            else:
                temp = []
                for i in solution:
                    if sp.re(i[0]) > 0 and sp.re(i[1]) > 0:
                        temp.append([sp.re(i[0]), sp.re(i[1])])
                value_flagX = 100
                value_flagY = 100
                for j in temp:
                    if j[0] < value_flagX:
                        value_flagX = j[0]
                        value_flagY = j[1]
                x_flag = value_flagX
                y_flag = value_flagY
            if xi > 0 and xi <= 4:
                num.setdefault(count, []).append((xi, z))
            count += 1
            if xi >= 4 or xi < 0:
                # num.append(dummy)
                break
    return num


def draw_picture(num):
    keys = num.keys()
    plt.figure(figsize=(8, 10))
    for key in keys:
        axis = num[key]
        x = []
        y = []
        for element in axis:
            x.append(element[0])
            y.append(element[1])
        x_smooth = savgol_filter(x, 11, 3, mode='nearest')
        plt.plot(x_smooth, y, '-', color='blue', linewidth=1)
    plt.title('航线图')
    plt.xlabel('横向坐标/NM（由西向东）')
    plt.ylabel('纵向坐标/NM（由南向北）')
    plt.xlim([0, 4])
    plt.ylim([0, 5])
    plt.show()


def differential(a):
    i = 0
    b = []
    while i < len(a) - 1:
        b.append(a[i] - a[i + 1])
        i += 1
    return np.array(b)


def distance(x, y):
    x = np.float_(x)
    x = np.square(x)
    y = np.float_(y)
    y = np.square(y)
    z = x + y
    d_list = np.sqrt(z)
    return np.sum(d_list)


def calculate_distance(num):
    route_distance = 0
    for key in num.keys():
        x = []
        y = []
        for element in num[key]:
            x.append(element[0])
            y.append(element[1])
        x = differential(x)
        y = differential(y)
        d = distance(x, y)
        route_distance += d
    return route_distance


if __name__ == '__main__':
    path = 'data.npy'
    if os.path.exists(path):
        num = np.load(path, allow_pickle=True).item()
        draw_picture(num)
        d = calculate_distance(num)
        for key in num.keys():
            line = num[key]
            l = len(line)
            print(line[0])
    else:
        num = returnX()
        draw_picture(num)
        np.save(path, num)
        d = calculate_distance(num)
    print(d)
