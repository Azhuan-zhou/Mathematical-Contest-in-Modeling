from matplotlib.colors import LinearSegmentedColormap

from PCA import PCA_method
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from matplotlib.patheffects import withStroke
from matplotlib import cm
import seaborn as sns

text_effect = withStroke(linewidth=3, foreground='black')
plt.switch_backend('TKAgg')

use_p1 = ['p1_ace', 'p1_double_faults', 'p1_net_points_won', 'p1_break_points_won',
          'p1_winners',
          'p1_unforced_records', 'p1_total_points', 'p1_st_serve']
use_p2 = ['p2_ace', 'p2_double_faults', 'p2_net_points_won', 'p2_break_points_won', 'p2_winners',
          'p2_unforced_records', 'p2_total_points', 'p2_st_serve']
use = ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
       'total_points', 'st_serve']


def w(path, threshold=4):
    data = pd.read_csv(path)
    data = data.drop(data.columns[0], axis=1)
    data = data[use]
    print('-------------------------------------')
    print("原始数据形状：", data.shape)
    mean = data.mean(axis=0)
    std = data.std(axis=0)
    data_standardized = (data - mean) / std
    #data = data_standardized[(data_standardized > -threshold) & (data_standardized < threshold)].dropna()
    data =data_standardized
    print(data.columns)
    # 使用melt将DataFrame转换为适合boxplot的长格式
    df_long = pd.melt(data, var_name='Variable', value_name='Values')
    # 使用 boxplot 绘制箱线图并去除异常值
    sns.boxplot(x='Variable', y='Values', data=df_long, showfliers=True)
    plt.xticks([])
    # 显示图形
    plt.show()
    # 初始化PCA模型，指定主成分的数量（这里设定为2）
    pca = PCA(n_components=1)
    # 对数据进行PCA转换
    transformed_data = pca.fit_transform(data)
    # 输出原始数据形状和转换后的数据形状

    print("转换后的数据形状：", transformed_data.shape)
    # 输出主成分的方差解释比例
    print("主成分的方差解释比例：", pca.explained_variance_ratio_)
    # 输出主成分的特征向量
    print("主成分的特征向量：", pca.components_)
    PCA_method(data.cov())
    return pca.components_, mean, std


w, mean, std = w('checkpoint2/test.csv')


def competition(start, end):
    data = pd.read_csv('checkpoint2/Wimbledon_featured_matches_all.csv')
    data = data.iloc[start:end, :]
    data_p1 = data[
        use_p1].copy()
    data_p2 = data[
        use_p2].copy()
    player1 = []
    player2 = []
    for i in range(len(data)):
        p1 = np.dot((data_p1.iloc[i, :] - mean.values) / std.values, w[0])
        p2 = np.dot((data_p2.iloc[i, :] - mean.values) / std.values, w[0])
        player1.append(p1)
        player2.append(p2)
    player1 = pd.Series(player1)
    player2 = pd.Series(player2)
    plt.figure()
    plt.plot(range(1, end - start + 1), player1, label='player1')
    plt.plot(range(1, end - start + 1), player2, label='player2')
    plt.legend()
    plt.show()
    return player1, player2


p1, p2 = competition(6950, 7284)


def write_result():
    data = pd.read_csv('checkpoint2/Wimbledon_featured_matches_all.csv')
    match = pd.read_csv('Wimbledon_featured_matches_processed.csv')[['match_id', 'set_no', 'game_no', 'point_no']]
    data = data
    data_p1 = data[
        use_p1].copy()
    data_p2 = data[
        use_p2].copy()
    player1 = []
    player2 = []
    for i in range(len(data)):
        p1 = np.dot((data_p1.iloc[i, :] - mean.values) / std.values, w[0])
        p2 = np.dot((data_p2.iloc[i, :] - mean.values) / std.values, w[0])
        player1.append(p1)
        player2.append(p2)
    result = {
        'match_id': match['match_id'],
        'set_no': match['set_no'],
        'game_no': match['game_no'],
        'point_no': match['point_no'],
        'player1': player1,
        'player2': player2,
    }
    result = pd.DataFrame(result)
    result.to_csv('checkpoint2/performance.csv')


write_result()


def scree_plot():
    a = np.array(
        [2.32996297, 0.5817509, 0.1971167, 0.06017425, 0.23332831, 0.26399242,
         0.29561177, 0.33806268])
    a = np.sort(a)[::-1]

    fig, (ax1) = plt.subplots(1, 1, figsize=(6, 4))

    # 计算百分比
    percentage = a / a.sum()
    print(percentage)
    text = ['{:.1f}%'.format(i * 100) for i in percentage]
    print(text)
    # 绘制折线图
    ax1.plot(range(1, len(a) + 1), a, marker='o', linestyle='-', color='#610C9F')
    ax1.set_xlim(0.5, len(a) + 1)
    ax1.set_ylim(0, 3)
    ax1.set_title('Scree Plot')
    ax1.set_xlabel('Component')
    ax1.set_ylabel('Eigenvalue')
    ax1.grid(True)
    plt.savefig('picture/scree.pdf')


scree_plot()


def plot_weighted_scatter(a):
    # 创建一个渐变色的颜色映射
    cmap = LinearSegmentedColormap.from_list("my_colormap", ['#4e62ab', '#469eb4', '#87cfa4', '#cbe99d'])

    # 设置条形的数量和高度
    categories = ['ACEP', 'DFP', 'NPW', 'BPW', 'WP', 'UEP', 'TPW', '$SR_1$']

    # 创建一个包含渐变色的条形图
    fig, ax = plt.subplots()

    # 使用ScalarMappable实现颜色随着高度变化
    norm = plt.Normalize(-0.5, 0.5)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # 绘制条形，并根据高度设置颜色
    bars = ax.barh(categories, a, color=cmap(norm(a)), edgecolor='none')

    # 添加颜色条
    cbar = plt.colorbar(sm, ax=ax)

    # 在每个条形的右侧添加数值标签
    for bar, val in zip(bars, a):
        if val > 0:
            xpos = bar.get_x() + bar.get_width() + 0.02  # 调整x位置
            ypos = bar.get_y() + bar.get_height() / 2.0  # 设置y位置在条形中央
            ax.text(xpos, ypos, f'{val:.2f}', ha='left', va='center', color='black'
                    , fontdict={'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 10}
                    )
        else:
            xpos = bar.get_x() + bar.get_width() - 0.1  # 调整x位置
            ypos = bar.get_y() + bar.get_height() / 2.0  # 设置y位置在条形中央
            ax.text(xpos, ypos, f'{val:.2f}', ha='left', va='center', color='black'
                    , fontdict={'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 10})

    # 设置图表标题和轴标签
    plt.axvline(0, color='black', linestyle='--', linewidth=1)
    plt.title('Weight')
    plt.xlim(-0.5, 0.5)
    plt.ylabel('Feature')

    # 隐藏坐标轴刻度
    ax.tick_params(left=False, right=False)

    # 隐藏图表边框
    ax.set_frame_on(False)

    # 显示图表
    plt.savefig('picture/weight.pdf')


