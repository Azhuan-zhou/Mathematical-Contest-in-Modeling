import numpy as np
from problem_1 import calculate_w
from numpy import tan, cos, sin, arctan, arccos, pi


def calculate_gama(alpha, beta):
    """
    计算侧线平面和海域平面交线与水平面的夹角
    :param alpha:坡度(°)
    :param beta:测线方向与海底坡面的法向在水平面上投影的夹角（°）
    :return:侧线平面和海域平面交线与水平面的夹角
    """
    tan_gama = 0
    if 0 <= beta < 90 or 270 <= beta <= 360:
        tan_gama = sin((beta + 90) / 180 * pi) * tan(alpha / 180 * pi)
    elif 90 <= beta < 270:
        tan_gama = sin((beta - 90) / 180 * pi) * tan(alpha / 180 * pi)
    gama = arctan(tan_gama)
    gama = gama * 180 / pi
    return gama


def calculate_theta(alpha, beta):
    cos_degree = -tan(alpha / 180 * pi) * sin(beta / 180 * pi) / np.sqrt(1 + tan(alpha / 180 * pi) ** 2)
    degree = arccos(cos_degree)
    degree = degree * 180 / pi
    return degree


def calculate_width_in_inclination(deep, alpha, beta):
    """
    求出宽度
    :param deep:距离海平面高度
    :param alpha: 坡度(°)
    :param beta:测线方向与海底坡面的法向在水平面上投影的夹角（°）
    :return:覆盖宽度
    """
    degree = calculate_theta(alpha, beta)
    # 当beta大于180°
    if degree < 90:
        degree = 180 - degree
    b = 120 - degree
    c = 120 - (180 - degree)
    width = calculate_w(deep, b, c)
    return width


# 计算在某一个beta角度时的
def calculate_depths(depth_center, alpha, beta, d_distance):
    gama = calculate_gama(alpha, beta)
    d_depth = d_distance * sin(gama) / cos(gama)
    widths = [depth_center]
    width_current = depth_center
    for i in range(7):
        # 当船朝下走时
        if 0 <= beta <= 90 or 270 <= beta <= 360:
            width_current += d_depth
            widths.append(width_current)
        # 当船朝上走时
        else:
            width_current -= d_depth
            widths.append(width_current)
    return widths


# 计算所有beta角度的覆盖宽度
def calculate_widths(alpha, betas, depth_center, d_distance):
    widths_all = {}
    for beta in betas:
        # 算出某一个角度航线的所有深度
        deeps = calculate_depths(depth_center, alpha, beta, d_distance)
        widths = []
        for deep in deeps:
            width = calculate_width_in_inclination(deep, alpha, beta)
            widths.append(width)
        flag = '{}°'.format(beta)
        widths_all[flag] = widths
    return widths_all


if __name__ == '__main__':
    Alpha = 1.5
    center = 120
    sea_mile = 1852
    d_Distance = 0.3 * sea_mile
    beta_type = [0, 45, 90, 135, 180, 225, 270, 315]
    widths_in_all_betas = calculate_widths(Alpha, beta_type, center, d_Distance)
    keys = widths_in_all_betas.keys()
    for key in keys:
        a = []
        print('--------------------------{}---------------------'.format(key))
        for element in widths_in_all_betas[key]:
            print(element[0] + element[1])
        print('---------------------------------------------------')
