from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.use('TKAgg')


def draw_contour(X, Y, Z):
    # use plt.contourf to filing contours
    # 先设置等高图
    plt.figure(figsize=(8,10))
    plt.contourf(X, Y, Z, 10, alpha=0.75,
                 cmap=plt.cm.cool)  # 其中的8代表的是填充8个颜色,透明度。cmap:将每个数字对应在cmap图中有不同的颜色，有hot和cool两种
    # 再设置等高线
    C = plt.contour(X, Y, Z, 20, colors='black', linewidth=.5)
    # 设置线的参数，数字嵌套在内部，数字的label大小为10
    plt.clabel(C, inline=True, fontsize=10)

    plt.xlabel('横向坐标/NM（由西向东）', fontproperties='SimHei')
    plt.ylabel('纵向坐标/NM（由南向北）', fontproperties='SimHei')
    plt.show()


def draw_3D_contour(X, Y, Z):
    # 创建一个Matplotlib 3D图形对象
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 绘制三维等高线图
    contours = ax.contour(X, Y, Z, 50)
    ax.clabel(contours, inline=True, fontsize=8)
    # 添加颜色映射
    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.cool, alpha=0.5)
    # 添加颜色条
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    # 设置坐标轴标签
    ax.set_xlabel('横向坐标/NM（由西向东）', fontproperties='SimHei')
    ax.set_ylabel('纵向坐标/NM（由南向北）', fontproperties='SimHei')
    ax.set_zlabel('海水深度/m', fontproperties='SimHei')
    ax.invert_zaxis()
    ax.view_init(60, 35)
    plt.show()


if __name__ == '__main__':
    # 参数加载
    data = pd.read_csv("../axsis_data.csv", encoding='gbk', index_col=0)
    # 数据预处理
    x = data.columns.tolist()  # 西到东
    x = np.float_(x)
    y = data.index.tolist()  # 南到北
    y = np.float_(y)
    Z = data.values
    Z = np.array(Z)
    # 创建网格
    X, Y = np.meshgrid(x, y)
    draw_3D_contour(X, Y, Z)
    draw_contour(X, Y, Z)
