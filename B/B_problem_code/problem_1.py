import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TKAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def calculate_w(deep, theta_1, theta_2):
    """
    求解宽度
    :param deep:深度
    :param theta_1:朝斜面外
    :param theta_2:朝斜面内
    :return:
    """
    theta = np.sin(60 / 180 * np.pi)
    # 外侧
    sin_theta_1 = np.sin(theta_1 / 180 * np.pi)
    # 内测
    sin_theta_2 = np.sin(theta_2 / 180 * np.pi)
    w_1 = deep * theta / sin_theta_1
    w_2 = deep * theta / sin_theta_2
    return w_1, w_2


def calculate_overlap(width):
    a = np.cos(1.5 / 180 * np.pi)
    distance = 200 * a
    overlapping_ratios = []
    for i in range(8):
        # 前一个覆盖宽度(x1,x2),x1表示侧线左侧的宽度，x2表示侧线右侧的宽度
        w_1 = width[i]
        # 当前覆盖宽度(x1,x2),x1表示侧线左侧的宽度，x2表示侧线右侧的宽度
        w_2 = width[i + 1]
        # 计算各个侧线的宽度
        w_3 = w_1[0] + w_2[1] + distance
        w_1 = w_1[0] + w_1[1]
        w_2 = w_2[0] + w_2[1]
        # 计算重叠面积
        overlap = w_1 + w_2 - w_3
        overlapping_ratio = overlap / w_1
        overlapping_ratios.append(overlapping_ratio)
    return overlapping_ratios


def depth():
    depth_center = 70
    slope = np.tan(1.5 / 180 * np.pi)
    d_distance = 200
    d_depth = d_distance * slope
    d = [depth_center]
    # 计算中心点前的侧线深度
    depth_current = 70
    for i in range(4):
        depth_current += d_depth
        d.insert(0, depth_current)
    # 计算中心点后的侧线深度
    depth_current = 70
    for i in range(4):
        depth_current -= d_depth
        d.append(depth_current)
    return np.array(d)


def draw_picture(widths):
    a = np.cos(1.5 / 180 * np.pi)
    distance = 200 * a
    x = widths[0][0]
    # 创建一个图形
    plt.figure(figsize=(8, 4))
    for i, width in enumerate(widths):
        color2 = 'black'
        color1 = 'royalblue'

        # 定义x坐标范围
        x_axis = np.linspace(0, 2000, 2000)  # 根据你的需求设置x范围

        # 定义左边界和右边界
        left_boundary = x - width[0]
        right_boundary = x + width[1]

        # 使用fill_between函数绘制并着色区域
        plt.fill_between(x_axis, 0, 1, where=(x_axis > left_boundary) & (x_axis < right_boundary), color=color1,
                         alpha=0.5)

        # 添加垂直线
        plt.axvline(x=x, color=color2, linestyle='-')
        x = x + distance

    # 添加标题和标签
    plt.title("坡度1.5的法向重叠俯瞰图")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # 显示图形
    plt.show()


if __name__ == '__main__':
    depths = depth()
    width = []
    print("海水深度")
    for d in depths:
        w = calculate_w(d, 28.5, 31.5)
        width.append(w)
        print("{}m".format(d))
    draw_picture(width)
    print('覆盖宽度')
    axis = 0
    a = np.cos(1.5 / 180 * np.pi)
    distance = 200 * a
    for i, w in enumerate(width):
        if i == 0:
            axis = w[0]
        print("{}/{}, {}".format(w[0], w[1], axis))
        axis += distance
    overlappingRatios = calculate_overlap(width)
    print('与前一条测线的重叠率')
    for overlappingRatio in overlappingRatios:
        print("{}%".format(100 * overlappingRatio))
