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
    # data = data_standardized[(data_standardized > -threshold) & (data_standardized < threshold)].dropna()
    data = data_standardized
    print(data.columns)
    # 使用melt将DataFrame转换为适合boxplot的长格式
    # df_long = pd.melt(data, var_name='Variable', value_name='Values')
    ## 使用 boxplot 绘制箱线图并去除异常值
    # sns.boxplot(x='Variable', y='Values', data=df_long, showfliers=True)
    # plt.xticks([])
    ## 显示图形
    # plt.show()
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


def write_result():
    data = pd.read_csv('2023 w/Wimbledon_featured_matches_all.csv')
    match = pd.read_csv('2023 w/Wimbledon_featured_matches_processed.csv')[
        ['match_id', 'set_no', 'game_no', 'point_no']]
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
    result.to_csv('2023 w/performance.csv')


write_result()


def momentum_1(leverages, points, a=0.33):
    if isinstance(leverages, pd.Series):
        leverages = leverages.copy().values
    m = [leverages[0]]
    for i in range(points - 1):
        l_t = leverages[i + 1]
        upper = l_t
        lower = 1
        for j in range(i + 1):
            upper += leverages[j] * ((1 - a) ** (i + 1 - j))
            lower += (1 - a) ** (i + 1 - j)
        m.append(upper / lower)
    return m


# --------------------
plt.switch_backend('TKAgg')
performance = pd.read_csv('2023 w/performance.csv')
print(performance.describe())
match_id = 1
match_p = performance[performance['match_id'] == match_id]
print(match_p.describe())
num = len(match_p)
deta = match_p[['set_no', 'game_no', 'point_no']].copy()
# match_p['player1'] = momentum(match_p['player1'].copy(), match_p)
# match_p['player2'] = momentum(match_p['player2'].copy(), match_p)
match_p.loc[0, 'player1'] = match_p.loc[0, 'player1'] - 3
match_p.loc[0, 'player2'] = match_p.loc[0, 'player2'] + 3
deta['deta'] = (match_p['player1'] - match_p['player2'])
# deta.iloc[0, 3] = deta.iloc[0,3] - 4
sets = match_p['set_no']
games = match_p['game_no']
match_points = match_p['point_no']
set_4 = match_p['set_no'] == 4
points_set_4 = match_points[set_4]

# --------画图设置-------------
d = 1
bifen = ['6-', '6-4']
set_labels = ['SET {}\n \n{}'.format(i, j) for i, j in zip(sets.unique(), bifen)]
boundary_acc = 0
set_boundaries = [boundary_acc]
for i in sets.unique():
    boundary_acc += (sets == i).sum() / d
    set_boundaries.append(boundary_acc)
text_effect = withStroke(linewidth=3, foreground='black')
font_style = {'family': 'sans-serif', 'size': 16, 'weight': 'bold', 'variant': 'normal', 'color': 'white',
              'path_effects': [text_effect]}
deta_g = deta.groupby(['set_no', 'game_no'])
# d_4 = deta_g['deta'].mean().values
x_label = []
a = deta_g.indices.keys()
for i, j in a:
    s = '{}-{}'.format(i, j)
    x_label.append(s)
x_position = deta_g['point_no'].max() / d
# ------------------------

upper_num = 6
a = ((match_p['player1'] + upper_num) / (match_p['player1'] + upper_num + match_p['player2'] + upper_num))
a.to_csv('2023 w/probability.csv')
plt.plot(range(len(a)), a)
plt.show()
plt.close()


# ---------------------------------


def performance():
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(range(1, num + 1), match_p['player1'].values + upper_num, color='#431f6a')
    ax1.plot(range(1, num + 1), match_p['player2'].values + upper_num, color='#046434')
    ax1.set_xlabel('games', fontweight='bold')
    ax1.set_ylabel('performance score', fontweight='bold')
    ax1.fill_between(range(1, num + 1), match_p['player1'].values + upper_num, 0,
                     color='#431f6a', alpha=0.5, label='Player1')
    ax1.fill_between(range(1, num + 1), match_p['player2'].values + upper_num, 0,
                     color='#046434', alpha=0.5, label='Player2')
    ax1.axhline(0, color=(30 / 255, 30 / 255, 30 / 255), linestyle='--', linewidth=1)
    # 绘制垂直虚线
    for boundary, label in zip(set_boundaries[1:], set_labels):
        ax1.axvline(boundary, color='gray', linestyle='--', linewidth=2)
        ax1.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 9.2, label
                 , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
    ax1.set_ylim(0, 11)
    ax1.set_xlim(1, num + 1)
    ax1.set_xticks(x_position, x_label, rotation='vertical')
    ax1.grid(False)
    # 添加总标题
    ax1.set_title('Performance:M.Vondrousova vs O.Jabeur (2-0)', fontweight='bold',
                  horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes, fontsize=16)

    ax2.plot(range(1, num + 1), deta['deta'], linewidth=1, linestyle='-',
             c='k')
    ax2.fill_between(range(1, num + 1), deta['deta'], 0,

                     where=deta['deta'] > 0, color='#431f6a', alpha=0.5,
                     label='Player 1')
    ax2.fill_between(range(1, num + 1), deta['deta'], 0,
                     where=deta['deta'] < 0, color='#046434', alpha=0.5,
                     label='Player 2')
    # 绘制垂直虚线
    for boundary, label in zip(set_boundaries[1:], set_labels):
        ax2.axvline(boundary, color='gray', linestyle='--', linewidth=2)
        ax2.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 2.5, label
                 , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
    ax2.set_xlabel('games', fontweight='bold')
    ax2.set_ylabel('performance difference', fontweight='bold')
    ax2.set_xlim(1, num + 1)
    ax2.set_ylim(-7, 4)
    ax2.axhline(0, color=(30 / 255, 30 / 255, 30 / 255), linestyle='--', linewidth=1)
    ax2.set_xticks(x_position, x_label, rotation='vertical')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # 添加总标题
    ax2.set_title('PD:M.Vondrousova vs O.Jabeur (0-2)', fontweight='bold',
                  horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes, fontsize=16)

    ax2.grid(False)
    # 调整布局，防止子图重叠
    plt.tight_layout()
    plt.savefig('2023 w/performance_d.pdf')
    plt.close()


a = ((match_p['player1'] + upper_num) / (match_p['player1'] + upper_num + match_p['player2'] + upper_num))
a.to_csv('2023 w/probability.csv')
# plt.plot(range(len(a)), a)
# plt.show()
# plt.close()
performance()

# ----- 取间隔-------
d_4 = []
for i in range(int(num / d)):
    sub = deta['deta'][i * d: i * d + d].sum()
    d_4.append(sub / d)
x_values = range(1, len(d_4) + 1)

# leverage
confi = [d_4[0]]
for i in range(len(d_4) - 1):
    le = d_4[i + 1] - d_4[i]
    confi.append(le)
confi = pd.Series(confi)
co = 0.94
t = 20
for i in range(t):
    confi[t - 1 - i] = confi[t - 1 - i] * (co ** i)

m = momentum_1(confi, num)
m[0] = m[0] / 3
m = pd.Series(m)

fig, ax = plt.subplots(figsize=(12, 5))
colors = ['#431f6a' if val > 0 else '#046434' for val in m]
bars = ax.bar(x_values, m, color=colors)
legend_colors = {'Payer1': '#431f6a', 'Player2': '#046434'}
legend_labels = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_colors.values()]
plt.title('Momentum', fontweight='bold')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
# 绘制垂直虚线
for boundary, label in zip(set_boundaries[1:], set_labels):
    plt.axvline(boundary, color='gray', linestyle='--', linewidth=2)
    plt.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 0.5, label
             , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
plt.xlim(x_values[0], x_values[-1])
# 区域着色
plt.fill_between(x_values, 0, m.values, where=m.values > 0, color='#431f6a', alpha=0.5, label='Player 1')
plt.fill_between(x_values, 0, m.values, where=m.values < 0, color='#046434', alpha=0.5, label='Player 2')
plt.xticks(x_position, x_label, rotation='vertical')
# 在 x 轴上的位置 0 处绘制一根虚线
plt.legend(legend_labels, legend_colors.keys(), bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)
# 不显示 y 轴
plt.yticks([])
plt.savefig('2023 w/Momentum.pdf')
plt.close()

# set4
# m_set4 = m[set_4.values]
## 创建图表和坐标轴
# fig, ax = plt.subplots()
## 根据值的正负设置不同颜色
# colors = ['#431f6a' if val > 0 else '#046434' for val in m_set4]
## 绘制条形图
# bars = ax.bar(points_set_4, m_set4, color=colors)
## 创建图例
# legend_colors = {'Payer1': '#431f6a', 'Player2': '#046434' }
# legend_labels = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_colors.values()]
# ax.legend(legend_labels, legend_colors.keys(), title='Legend')
# ax.set_yticks([])
# ax.set_xticks(x_position.iloc[27:36], x_label[27:36], rotation='vertical')
# plt.grid(True)
## 显示图表
# plt.savefig('2023 w/set_4.svg')
