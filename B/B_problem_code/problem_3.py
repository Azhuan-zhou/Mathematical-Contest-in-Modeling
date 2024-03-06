import numpy as np
from numpy import tan, arctan, cos, pi, sin
import matplotlib.pyplot as plt
import matplotlib as mpl
from problem_2 import calculate_gama, calculate_width_in_inclination, calculate_theta
import time

mpl.use('TKAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def calculate_omiga(alpha, beta):
    if not (beta == 0 or beta == 180):
        tan_omiga = -1 / (cos(alpha / 180 * pi) * tan(beta / 180 * pi))
        w = arctan(tan_omiga)
        w = w * 180 / pi
    else:
        w = 90
    # 当β在[0,90],[180,270]时为负数，因为arctan的取值在[-90,90]之间,实际omiga是一个钝角
    if w < 0:
        w = 180 + w
    return w


def calculate_lower_bound_2(w_xi, theta_2, omiga, alpha):
    a = cos(omiga / 180 * pi) - sin(alpha / 180 * pi) * sin(60 / 180 * pi) / sin(theta_2 / 180 * pi)
    lower_bound = 0.80 * (w_xi[0] + w_xi[1]) / ( a
            )
    return lower_bound


def calculate_lower_bound_1(w_xi, theta_1, omiga, alpha):
    a =sin(alpha / 180 * pi) * sin(60 / 180 * pi) / sin(theta_1 / 180 * pi) + cos(omiga / 180 * pi)
    lower_bound = 0.80 * (w_xi[0] + w_xi[1]) / ( a
            )
    return lower_bound


def calculate_lower_bound_special(w_high, omiga):
    lower_bound = 0.80 * (w_high[0] + w_high[1]) / cos(omiga / 180 * pi)

    return lower_bound


def calculate_upper_bound_special(w_low, omiga):
    upper_bound = 1 * (w_low[0] + w_low[1]) / cos(omiga / 180 * pi)
    return upper_bound


def calculate_upper_bound(w_xi, theta_2, omiga, alpha):
    upper_bound = (1 * (w_xi[0] + w_xi[1])) / (
            cos(omiga / 180 * pi) - sin(alpha / 180 * pi) * sin(60 / 180 * pi) / sin(theta_2 / 180 * pi))
    return upper_bound


def calculate_parameter(D_high, D_low, alpha, beta):
    w_high = calculate_width_in_inclination(D_high, alpha, beta)  # 计算最低深度的宽度
    w_low = calculate_width_in_inclination(D_low, alpha, beta)
    omiga = calculate_omiga(alpha, beta)  # beta所对应的omiga
    theta = calculate_theta(alpha, beta)  # beta所对应的theta
    theta_1 = 120 - theta
    theta_2 = 120 - (180 - theta)
    return w_high, w_low, omiga, theta_1, theta_2


def calculate_lines(n_to_s, w_to_e, alpha):
    global best_beta, best_distance
    min_distance = float('inf')
    D_low = 110 - w_to_e * tan(alpha / 180 * pi) / 2  # 最低深度
    D_high = 110 + w_to_e * tan(alpha / 180 * pi) / 2  # 最大深度
    # 坐标限制
    x_lim = w_to_e / cos(1.5 / 180 * pi)  # 东西
    y_lim = n_to_s  # 南北
    best_x_right = []
    best_x_left = []
    best_y = []
    # 先使用range(270,360)查看有解的beta
    # 再使用np。linspace(270,272,2000)找到最优的解
    for beta in range(270, 360):
        # 计算参数
        w_high, w_low, omiga, theta_1, theta_2 = calculate_parameter(D_high, D_low, alpha, beta)
        distance = 0
        # 储存坐标
        x_right = [0]
        x_left = [n_to_s * tan(omiga / 180 * pi)]
        y_list_1 = []  # 宽度深的地方的y轴
        count = 0
        count_y_1 = 0
        flag = False  # 判断是否执行了一个if语句中的内容
        while x_right[count] <= x_lim:
            # 计算左边
            w_xi_left = calculate_width_in_inclination(x_left[count] * sin(alpha / 180 * pi) + D_low, alpha, beta)
            lower_bound = calculate_lower_bound_2(w_xi_left, theta_2, omiga, alpha)
            # 计算右边
            w_xi_right = calculate_width_in_inclination(x_right[count] * sin(alpha / 180 * pi) + D_low, alpha, beta)
            upper_bound = calculate_upper_bound(w_xi_right, theta_2, omiga, alpha)
            # 填补左上角
            if n_to_s * tan(omiga / 180 * pi) <= x_left[count] <= x_lim:
                x_left.append(x_left[count] + upper_bound)
                x_right.append(x_right[count] + upper_bound)
                count += 1
                distance += y_lim / cos(omiga / 180 * pi)
                flag = True
            else:
                # 当上面的计算完成后， 将超出界限的计算结果pop
                if flag:
                    x_left.pop()
                    x_right.pop()
                    count -= 1
                    distance -= y_lim / cos(omiga / 180 * pi)
                else:
                    count = 0
                # 计算左边
                lower_bound = calculate_lower_bound_special(w_high, omiga)
                y = y_lim - ((x_lim - (x_right[count] + upper_bound)) / tan(omiga / 180 * pi))
                x_left.append(x_lim)
                x_right.append(x_right[count] + upper_bound)
                y_list_1.append(y)
                count_y_1 += 1
                count += 1
                distance += (y_lim - y) / cos(omiga / 180 * pi)

            # 当发现下一条直线，不满足约束条件时，该方案pass
            if lower_bound > upper_bound or lower_bound < 0 or upper_bound < 0:
                x_left.pop()
                x_right.pop()
                count -= 1
                break
        if x_right[count] > x_lim:
            print(beta)
            if distance < min_distance:
                best_y = y_list_1
                best_x_left = x_left
                best_x_right = x_right
                best_beta = beta
                best_distance = distance
    return best_x_left, best_x_right, best_y, best_beta, best_distance


def supplement(best_x_left, best_x_right, best_beta, best_distance, n_to_s, w_to_e, alpha):
    global x_i_1
    D_low = 110 - w_to_e * tan(alpha / 180 * pi) / 2  # 最低深度
    D_high = 110 + w_to_e * tan(alpha / 180 * pi) / 2  # 最大深度
    y = []
    # 坐标限制
    x_lim = w_to_e / cos(1.5 / 180 * pi)  # 东西
    y_lim = n_to_s  # 南北
    w_high, w_low, omiga, theta_1, theta_2 = calculate_parameter(D_high, D_low, alpha, best_beta)
    y_i_1 = y_lim
    while best_x_left[0] >= 0:
        x_i = best_x_left[0]
        w_i = calculate_width_in_inclination(D_low + x_i * sin(alpha / 180 * pi), alpha, best_beta)
        lower_bound = calculate_lower_bound_1(w_i, theta_1, omiga, alpha)
        upper_bound = calculate_upper_bound_special(w_low, omiga)
        if upper_bound > lower_bound >= 0 and upper_bound >= 0:
            x_i_1 = x_i - upper_bound
            y_i_1 -= upper_bound / tan(omiga / 180 * pi)
            best_distance += x_i_1 / sin(omiga / 180 * pi)
            best_x_left.insert(0, x_i_1)
            best_x_right.insert(0, 0)
            y.insert(0, y_i_1)
    del best_x_left[0]
    del best_x_right[0]
    del y[0]
    best_distance -= x_i_1 / sin(omiga / 180 * pi)
    return best_x_left, best_x_right, y, best_distance


if __name__ == '__main__':
    west_to_east = 4 * 1852
    north_to_south = 2 * 1852
    x_lim = 4 * 1852
    y_lim = 2 * 1852
    alpha = 1.5
    # calculate_lines(width, high, 1.5)
    best_x_left, best_x_right, best_y_2, best_beta, best_distance = calculate_lines(north_to_south, west_to_east, 1.5)
    best_x_left, best_x_right, best_y_1, best_distance = supplement(best_x_left, best_x_right, best_beta, best_distance,
                                                                   north_to_south, west_to_east, alpha)
    for i, x in enumerate(best_x_left):
        best_x_left[i] = x * cos(alpha/180*pi)
    for i, x in enumerate(best_x_right):
        best_x_right[i] = x * cos(alpha / 180 * pi)
    omiga = calculate_omiga(alpha, best_beta)
    best_distance = best_distance*sin(omiga/180*pi)*cos(alpha/180*pi)/sin((best_beta-270)/180*pi)
    num = '{}°'.format(best_beta)
    plt.figure(figsize=(8, 16), num=num)
    l1 = len(best_y_1)
    l2 = len(best_y_2)
    for i in range(len(best_x_left)):
        if i + 1 <= l1:
            y_axis = np.linspace(x_lim - best_x_left[i], x_lim, 1000)
            x_axis = np.linspace(0, best_y_1[i], 1000)
            plt.plot(x_axis, y_axis, color='blue')
        elif l1 < i + 1 <= len(best_x_left) - l2:
            y_axis = np.linspace(x_lim - best_x_left[i], x_lim - best_x_right[i], 1000)
            x_axis = np.linspace(0, y_lim, 1000)
            plt.plot(x_axis, y_axis, color='blue')
        else:
            y_axis = np.linspace(x_lim, x_lim - best_x_right[i], 1000)
            x_axis = np.linspace(best_y_2[i - (len(best_x_left) - l2)], y_lim, 1000)
            plt.plot(x_axis, y_axis, color='blue')
    # 添加标题和标签
    print(len(best_x_left))
    plt.title('1.5坡面俯瞰图,侧线方向夹角：{}°,distance:{}'.format(best_beta, best_distance))
    plt.xlabel('北到南方向')
    plt.ylabel('西到东方向')
    # 限制横纵坐标距离
    plt.xlim(0, y_lim)
    plt.ylim(0, x_lim)
    # 显示图形
    plt.show()
    plt.close(num)
