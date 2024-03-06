import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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


# Read performance data

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
deta.iloc[0, 3] = deta.iloc[0, 3] + 2.5
sets = match_p['set_no']
games = match_p['game_no']
match_points = match_p['point_no']

# --------画图设置-------------
d = 2
bifen = ['1-6', '7-6', '6-1', '3-6', '6-4']
set_labels = ['SET {}\n \n{}'.format(i, j) for i, j in zip(sets.unique(), bifen)]
boundary_acc = 0
set_boundaries = [boundary_acc]
for i in sets.unique():
    boundary_acc += (sets == i).sum() / d
    set_boundaries.append(boundary_acc)
text_effect = withStroke(linewidth=3, foreground='black')
font_style = {'family': 'sans-serif', 'size': 12, 'weight': 'bold', 'variant': 'normal', 'color': 'white',
              'path_effects': [text_effect]}
deta_g = deta.groupby(['set_no', 'game_no'])
# d_4 = deta_g['deta'].mean().values
x_label = []
a = deta_g.indices.keys()
for i, j in a:
    s = '{}-{}'.format(i, j)
    x_label.append(s)
x_position = (deta_g['point_no'].max() / d).values
# ---------------------------------
upper_num = 10

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
confi[2] = confi[2] * 0.02
# ----------------
# Sensitivity analysis for different 'a' values
a_values = [0.2,0.3,0.4, 0.5,0.6,0.7]  # Add more values as needed

plt.figure(figsize=(14, 7))
momentum_values = momentum_1(confi, int(num / d))
# Plot momentum curve
plt.plot(x_values, momentum_values, label=f'a=0.33',c='#D67BFF')
momentum_s = []
for a in a_values:
    momentum_s.append(momentum_1(confi, int(num / d), a=a))
momentum_s = np.array(momentum_s)
sense_min = np.min(momentum_s,axis=0)
sense_max = np.max(momentum_s,axis=0)
plt.fill_between(x_values, sense_min, sense_max, color='#D0BFFF', alpha=0.5, label='a:0.2~0.7')

plt.axhline(0, color='black', linestyle='--', linewidth=1)
# 绘制垂直虚线
for boundary, label in zip(set_boundaries[1:], set_labels):
    plt.axvline(boundary, color='gray', linestyle='--', linewidth=2)
    plt.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 0.27, label
             , verticalalignment='center', horizontalalignment='center', fontdict=font_style)
plt.xlim(x_values[0], x_values[-1])
plt.ylim(-0.2,0.35)
plt.xticks(x_position, x_label, rotation='vertical')
plt.title('Momentum Sensitivity Analysis', fontweight='bold')
plt.xlabel('games')
plt.ylabel('Momentum')
# 不显示 y 轴
plt.yticks([])
plt.grid(False)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

plt.show()
plt.close()
