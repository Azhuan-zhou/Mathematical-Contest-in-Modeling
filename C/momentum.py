import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke


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


#def momentum(leverages, points, a=0.6, t=10):
#    """
#   :param momentum_old: t-1时刻的momentum
#   :param leverage: 当前points的leverage
#   :param points:
#   :param a:
#   :return:
#   """
#    if isinstance(leverages, pd.Series):
#        leverages = leverages.copy().values
#    m = [leverages[0]]
#    for i in range(t - 1):
#        l_t = leverages[i + 1]
#        upper = l_t
#        lower = 1
#        for j in range(i + 1):
#            upper += leverages[j] * ((1 - a) ** (i + 1 - j))
#            lower += (1 - a) ** (i + 1 - j)
#        m.append(upper)
#    for i in range(points - t):
#        l_t = leverages[i + t]
#        upper = l_t
#        lower = 1
#        for j in range(t):
#            upper += leverages[i + j] * ((1 - a) ** (t - j))
#            lower += (1 - a) ** (t - i)
#        m.append(upper)
#    return m

#--------------------
plt.switch_backend('TKAgg')
performance = pd.read_csv('checkpoint2/performance.csv')
print(performance.describe())
match_id = 31
match_p = performance[performance['match_id'] == match_id]
print(match_p.describe())
num = len(match_p)
deta = match_p[['set_no', 'game_no', 'point_no']].copy()
# match_p['player1'] = momentum(match_p['player1'].copy(), match_p)
# match_p['player2'] = momentum(match_p['player2'].copy(), match_p)
deta['deta'] = (match_p['player1'] - match_p['player2'])
deta.iloc[0, 3] = deta.iloc[0,3] + 2.5
sets = match_p['set_no']
games = match_p['game_no']
match_points = match_p['point_no']
set_4 = match_p['set_no'] == 4
points_set_4 = match_points[set_4]
# --------画图设置-------------
d = 1
bifen = ['1-6', '7-6', '6-1', '3-6', '6-4']
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

# ---------------------------------


upper_num = 10


def performance():
    fig1, (ax1) = plt.subplots(1, 1, figsize=(14, 6))

    ax1.plot(range(1, num + 1), match_p['player1'].values + upper_num, color='#4e62ab')
    ax1.plot(range(1, num + 1), match_p['player2'].values + upper_num, color='#87cfa4')
    ax1.set_xlabel('games', fontweight='bold')
    ax1.set_ylabel('performance score', fontweight='bold')
    ax1.fill_between(range(1, num + 1), match_p['player1'].values + upper_num, 0,
                     color='#4e62ab', alpha=0.5,label='Player1')
    ax1.fill_between(range(1, num + 1), match_p['player2'].values + upper_num, 0,
                     color='#87cfa4', alpha=0.5,label='Player2')
    ax1.axhline(0, color=(30 / 255, 30 / 255, 30 / 255), linestyle='--', linewidth=1)
    # 绘制垂直虚线
    for boundary, label in zip(set_boundaries[1:], set_labels):
        ax1.axvline(boundary, color='gray', linestyle='--', linewidth=2)
        ax1.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 13.2, label
                 , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
    ax1.set_ylim(0, 15)
    ax1.set_xlim(1, num + 1)
    ax1.set_xticks(x_position, x_label, rotation='vertical')
    ax1.grid(False)
    # 添加总标题
    ax1.set_title('Performance:C.Alcaraz VS N.Djokovic (3-2)', fontweight='bold',
                  horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes, fontsize=16)
    # 调整布局，防止子图重叠
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.savefig('picture/performance.pdf')
    plt.close()

    fig2, (ax2) = plt.subplots(1, 1, figsize=(14, 6))
    ax2.plot(range(1, num + 1), deta['deta'], linewidth=1, linestyle='-',
             c='k')
    ax2.fill_between(range(1, num + 1), deta['deta'], 0,

                     where=deta['deta'] > 0, color='#4e62ab', alpha=0.5,
                     label='Player 1')
    ax2.fill_between(range(1, num + 1), deta['deta'], 0,
                     where=deta['deta'] < 0, color='#87cfa4', alpha=0.5,
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
    ax2.set_title('PD:C.Alcaraz VS N.Djokovic (3-2)', fontweight='bold',
                  horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes, fontsize=16)

    ax2.grid(False)
    # 调整布局，防止子图重叠
    plt.tight_layout()
    plt.savefig('picture/performance_d.pdf')
    plt.close()


a = ((match_p['player1'] + upper_num) / (match_p['player1'] + upper_num + match_p['player2'] + upper_num))
a.to_csv('checkpoint2/probability.csv')
plt.plot(range(len(a)), a)
plt.show()
plt.close()
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
co = 0.95
t = 50
for i in range(t):
    confi[t - 1 - i] = confi[t - 1 - i] * (co ** i)
confi[0] = confi[0] * 0.02
confi[1] = confi[1] * 0.02
confi[2] = confi[2] *0.02

m = momentum_1(confi, num)
m = pd.Series(m)
plt.figure(figsize=(12, 5))
plt.plot(x_values, m, drawstyle='steps-post', linewidth=1)
plt.title('Momentum',fontweight='bold')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
# 绘制垂直虚线
for boundary, label in zip(set_boundaries[1:], set_labels):
    plt.axvline(boundary, color='gray', linestyle='--', linewidth=2)
    plt.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 0.25, label
             , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
plt.xlim(x_values[0], x_values[-1])
# 区域着色
plt.fill_between(x_values, 0, m.values, where=m.values > 0, color='#4e62ab', alpha=0.5, label='Player 1')
plt.fill_between(x_values, 0, m.values, where=m.values < 0, color='#87cfa4', alpha=0.5, label='Player 2')
plt.xticks(x_position, x_label, rotation='vertical')
# 在 x 轴上的位置 0 处绘制一根虚线

plt.grid(True)
# 不显示 y 轴
plt.yticks([])
plt.savefig('picture/Momentum.svg')
plt.close()

# set4
m_set4 = m[set_4.values]
# 创建图表和坐标轴
fig, ax = plt.subplots()
# 根据值的正负设置不同颜色
colors = ['#4e62ab' if val > 0 else '#87cfa4' for val in m_set4]
# 绘制条形图
bars = ax.bar(points_set_4, m_set4, color=colors)
# 创建图例
legend_colors = {'Payer1': '#4e62ab', 'Player2': '#87cfa4' }
legend_labels = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_colors.values()]
ax.set_yticks([])
ax.set_xticks(x_position.iloc[27:36], x_label[27:36], rotation='vertical')
plt.grid(True)
# 显示图表
plt.savefig('picture/set_4.svg')
