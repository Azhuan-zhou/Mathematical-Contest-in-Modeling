import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from tennisMatchProbability import matchProb

def momentum(leverages, points, a=0.8, t=3):
    """
   :param momentum_old: t-1时刻的momentum
   :param leverage: 当前points的leverage
   :param points:
   :param a:
   :return:
   """
    if isinstance(leverages,pd.Series):
        leverages = leverages.values
    m = [leverages[0]]
    for i in range(t - 1):
        l_t = leverages[i + 1]
        upper = l_t
        lower = 1
        for j in range(i + 1):
            upper += leverages[j] * ((1 - a) ** (i + 1 - j))
            lower += (1 - a) ** (i + 1 - j)
        m.append(upper)
    for i in range(points - t):
        l_t = leverages[i + t]
        upper = l_t
        lower = 1
        for j in range(t):
            upper += leverages[i + j] * ((1 - a) ** (t - j))
            lower += (1 - a) ** (t - i)
        m.append(upper)
    return m

def draw_win_prob(data,points,point_1):
    points_len = len(data)
    # /print(data['p1_prob'])
    data.columns = ['match','player1', 'player2', 'set_no', 'point_no', 'p1_prob']
    set = data['set_no'].unique()
    set_labels = ['SET {}'.format(i) for i in set]
    boundary_acc = 0
    set_boundaries = [boundary_acc]
    for i in set:
        boundary_acc += (data['set_no'] == i).sum()
        set_boundaries.append(boundary_acc-1)
    # 绘制曲线图
    plt.figure(figsize=(10, 6))
    # 绘制胜率曲线
    plt.plot(data['p1_prob'], linewidth=1, c='#12372A')
    text_effect = withStroke(linewidth=3, foreground='black')
    font_style = {'family': 'sans-serif', 'size': 14, 'weight': 'bold', 'variant': 'normal', 'color': 'white',
                  'path_effects': [text_effect]}
    # 绘制转折点
    for i in range(0,point_1):
        point = points[i]
        plt.scatter(point[0],point[1],color='b', label="Player 1's swing")
    for i in range(point_1,len(points)):
        point = points[i]
        plt.scatter(point[0],point[1],color='b', label="Player 2's swing")
    # 绘制垂直虚线
    for boundary, label in zip(set_boundaries[1:], set_labels):
        plt.axvline(boundary, color='gray', linestyle='--', linewidth=2)
        plt.text((boundary + set_boundaries[set_boundaries.index(boundary) - 1]) / 2, 0.9, label
                 , verticalalignment='center', horizontalalignment='center', fontdict=font_style)

    # 区域着色
    plt.fill_between(range(points_len), 0, data['p1_prob'], color='#7B66FF', alpha=0.5, label='Player 1')
    plt.fill_between(range(points_len), data['p1_prob'], 1, color='#F28585', alpha=0.5, label='Player 2')

    # 设置 x 轴和 y 轴的范围
    plt.xlim(0, points_len-0.8)
    plt.ylim(0, 1)
    player1 = data['player1'][0]
    player2 = data['player2'][0]
    # 设置标题和标签
    plt.title('{} VS {}'.format(player1, player2))
    plt.xlabel('Points')
    plt.ylabel('Win Probability')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.savefig('2.pdf')

data_raw = pd.read_csv('Wimbledon.csv')
data_raw['match_id'].unique()
data_raw['match_id'] = pd.factorize(data_raw['match_id'])[0]+1
replacement_dict = {'AD': 4, '15': 1, '30': 2, '40': 3,'0':0}
data_raw['p1_score'] = data_raw['p1_score'].replace(replacement_dict).astype(int)
data_raw['p2_score'] = data_raw['p2_score'].replace(replacement_dict).astype(int)
# 使用pd.get_dummies进行独热编码
one_hot_encoded_width = pd.get_dummies(data_raw['serve_width'], prefix='serve_width')

# 将独热编码的结果连接到原始DataFrame
data_raw = pd.concat([data_raw, one_hot_encoded_width], axis=1)
# 使用pd.Categorical将列转换为分类变量
data_raw['serve_depth'] = pd.Categorical(data_raw['serve_depth'], categories=['NCTL','CTL'], ordered=True)
# 添加一个新的列，表示分类变量的标签
data_raw['serve_depth_new'] = data_raw['serve_depth'].cat.codes
# data_raw = data_raw.loc[6950:7284]
# data_raw = data_raw.reset_index(drop=True)
win_score = 3
p1_serve = 0.0
p1_serve_win = 0.0
p2_serve = 0.0
p2_serve_win =0.0
p1_p=0
p2_p=0
p1=[]
p2=[]
win_rate=[]
for index, row in data_raw.iterrows():
    if row['server'] == 1:
        p1_serve += 1
        if row['point_victor'] == 1:
            p1_serve_win += 1
    else:
        p2_serve += 1
        if row['point_victor'] == 2:
            p2_serve_win += 1

p1_serve = 0.0
p1_serve_win = 0.0
p2_serve = 0.0
p2_serve_win =0.0

p1_p = 0.6
p2_p = 0.6
n = 200
performance =  pd.read_csv('pb.csv')
p_values = performance.mean()
print(p_values)
per = performance['0'].tolist()
# print(performance.iloc[333])
for index, row in data_raw.iterrows():
    if row['server'] == 1:
        p1_serve += 1
        if row['point_victor'] == 1:
            p1_serve_win += 1
    else:
        p2_serve += 1
        if row['point_victor'] == 2:
            p2_serve_win += 1
    # if p1_serve > 24 :
    p1_p=(n/(n+index+1))*0.6+(1-n/(n+index+1))*(per[index]-p_values+0.6)
    p2_p=(n/(n+index+1))*0.6+(1-n/(n+index+1))*((1-per[index])-p_values+0.6)
    # if p2_serve > 24 :
        # p2_p=p2_serve_win/p2_serve    
    # print(row['p1_score'],row['p2_score'],row['p1_games'],row['p2_games'],row['p1_sets'],row['p2_sets'])
    win_p = matchProb(p1_p,1-p2_p,row['p1_score'],row['p2_score'],row['p1_games'],row['p2_games'],row['p1_sets'],row['p2_sets'],win_score)
    win_rate.append(win_p.values[0])
columns = ['p1_prob']
df = pd.DataFrame(win_rate, columns=columns)
# print(df.head())
moving_average = df.rolling(window=3, min_periods=1, center=True).mean()

last_win_rate = 0.5
second_last_win = 0.5
l = []
for index, row in moving_average.iterrows():
    rate = row.values[0]
    l.append([index,rate + second_last_win - 2*last_win_rate])
    print(f"Point{index}: rate={rate},lev={rate + second_last_win - 2*last_win_rate}")
    second_last_win = last_win_rate
    last_win_increase = rate
l.sort(key=lambda x: x[1],reverse=True)
# for index in range(len(win_rate)):
#     rate = win_rate[index]
#     l.append([index,rate-last_win_rate-last_win_increase])
#     last_win_increase = rate-last_win_rate
# l.sort(key=lambda x: x[1],reverse=True)

sum_point = 0
top_5_points = []
for p in range(len(l)):
    if sum_point==5:
        break
    k=0
    for i in range(sum_point):
        if abs(l[p][0]-top_5_points[i][0])<15:
            k=1
            break
    if k==0:
        top_5_points.append(l[p])
        sum_point += 1
point_1 = sum_point
for p in range(len(l)-1,-1,-1):
    if sum_point==10:
        break
    k=0
    for i in range(point_1,sum_point):
        if abs(l[p][0]-top_5_points[i][0])<15:
            k=1
            break
    if k==0:
        top_5_points.append(l[p])
        sum_point += 1

data = pd.concat([data_raw[['match_id','player1', 'player2', 'set_no', 'point_no']],moving_average],axis=1)
data.columns = ['match','player1', 'player2', 'set_no', 'point_no', 'p1_prob']
for i in range(len(top_5_points)):
    filtered_row = data[data['point_no'] == top_5_points[i][0]+1 ]
    winning_rate = filtered_row['p1_prob'].values
    top_5_points[i][1] = winning_rate[0]
print(top_5_points)
print(data)
draw_win_prob(data,top_5_points,point_1)
