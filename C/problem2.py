import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patheffects import withStroke

plt.switch_backend('TKAgg')



def draw_win_prob(data):
    points = len(data)
    data.columns = ['match', 'player1', 'player2', 'set_no', 'point_no', 'p1_prob', 'p2_prob']
    set = data['set_no'].unique()
    set_labels = ['SET {}'.format(i) for i in set]
    boundary_acc = 0
    set_boundaries = [boundary_acc]
    for i in set:
        boundary_acc += (data['set_no'] == i).sum()
        set_boundaries.append(boundary_acc)
    # 绘制曲线图
    plt.figure(figsize=(10, 6))
    # 绘制胜率曲线
    plt.plot(data['p1_prob'], linewidth=1, c='k')
    text_effect = withStroke(linewidth=3, foreground='black')
    font_style = {'family': 'sans-serif', 'size': 14, 'weight': 'bold', 'variant': 'normal', 'color': 'white',
                  'path_effects': [text_effect]}
    # 绘制垂直虚线
    for boundary, label in zip(set_boundaries[1:], set_labels):
        plt.axvline(boundary, color='gray', linestyle='--', linewidth=4)
        plt.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 0.9, label
                 , verticalalignment='center', horizontalalignment='center', fontdict=font_style)

    # 区域着色
    plt.fill_between(range(points), 0, data['p1_prob'], color='#D0A2F7', alpha=0.5, label='Player 1')
    plt.fill_between(range(points), data['p1_prob'], 1, color='#38E54D', alpha=0.5, label='Player 2')

    # 设置 x 轴和 y 轴的范围
    plt.xlim(1, points)
    plt.ylim(0, 1)
    player1 = data['player1'][0]
    player2 = data['player2'][0]
    # 设置标题和标签
    plt.title('{} VS {}'.format(player1, player2))
    plt.xlabel('Points')
    plt.ylabel('Win Probability')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()


def momentum(momentum_old, leverage, points, a=0.33):
    """
    :param momentum_old: t-1时刻的momentum
    :param leverage: 当前points的leverage
    :param points:
    :param a:
    :return:
    """
    lower = 1 - a
    for i in range(points - 1):
        lower = (1 - a) * lower + (1 - a)
    upper = momentum_old * (1 - a) + leverage
    return upper / lower


data_info = pd.read_csv('Wimbledon_featured_matches_processed.csv')[
    ['match_id', 'player1', 'player2', 'set_no', 'point_no']]
p1_pro = pd.DataFrame(np.linspace(0, 1, 334).T)
p2_pro = 1 - p1_pro
pro = pd.concat([p1_pro, p2_pro], axis=1)
match_31 = data_info[data_info['match_id'] == 31].copy().reset_index(drop=True)
data = pd.concat([match_31, pro], axis=1)
draw_win_prob(data)
