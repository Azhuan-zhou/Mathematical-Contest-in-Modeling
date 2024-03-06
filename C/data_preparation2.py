import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.switch_backend('TKAgg')
path = 'checkpoint2'
data_raw = pd.read_csv(os.path.join(path,'Wimbledon_featured_matches_processed.csv'))
data_group_by_match = data_raw.groupby('match_id')
points = data_raw['point_no']
start = 1
end = len(data_raw)
# 1.ace
# 有异常值，存在一些选手在开局就拿到ace,使得该特征值为1
a = data_group_by_match['p1_ace'].cumsum()
b = data_group_by_match['p2_ace'].cumsum()
p1_ace = data_group_by_match['p1_ace'].cumsum()/points * 100
p2_ace = data_group_by_match['p2_ace'].cumsum()/points *100
p1_ace.name = 'p1_ace'
p2_ace.name = 'p2_ace'
plt.plot(range(end - start), p1_ace[start:end], label='p1')
plt.plot(range(end - start), p2_ace[start:end], label='p2')
plt.title('ace')
plt.legend()
plt.savefig('data/ace.png')
plt.close()
# 2. double faults
a = data_group_by_match['p1_double_fault'].cumsum()
b = data_group_by_match['p2_double_fault'].cumsum()
p1_double_faults = data_group_by_match['p1_double_fault'].cumsum()/points *100
p2_double_faults = data_group_by_match['p2_double_fault'].cumsum()/points * 100
p1_double_faults.name = 'p1_double_faults'
p2_double_faults.name = 'p2_double_faults'
plt.plot(range(end - start), p1_double_faults[start:end], label='p1')
plt.plot(range(end - start), p2_double_faults[start:end], label='p2')
plt.title('double faults')
plt.legend()
plt.savefig('data/double faults.png')
plt.close()

# 3.net points won

p1_net_points_cum = data_group_by_match['p1_net_pt'].cumsum()
p1_net_points_won_cum = data_group_by_match['p1_net_pt_won'].cumsum()
p1_net_points_won = p1_net_points_won_cum / (p1_net_points_cum + 0.000001) * 100
a = p1_net_points_won_cum
b = p1_net_points_cum
p2_net_points_cum = data_group_by_match['p2_net_pt'].cumsum()
p2_net_points_won_cum = data_group_by_match['p2_net_pt_won'].cumsum()
p2_net_points_won = p2_net_points_won_cum / (p2_net_points_cum + 0.000001) * 100
c = p2_net_points_won_cum
d = p2_net_points_cum
p1_net_points_won.name = 'p1_net_points_won'
p2_net_points_won.name = 'p2_net_points_won'
plt.plot(range(end - start), p1_net_points_won[start:end], label='p1')
plt.plot(range(end - start), p2_net_points_won[start:end], label='p2')
plt.title('net_points_won')
plt.legend()
plt.savefig('data/net points won.png')
plt.close()

# 4.break points won
p1_break_points_cum = data_group_by_match['p1_break_pt'].cumsum()
p1_break_points_won_cum = data_group_by_match['p1_break_pt_won'].cumsum()
p1_break_points_won = p1_break_points_won_cum / (p1_break_points_cum + 0.000001) *100
a = p1_break_points_won_cum
b = p1_break_points_cum
p2_break_points_cum = data_group_by_match['p2_break_pt'].cumsum()
p2_break_points_won_cum = data_group_by_match['p2_break_pt_won'].cumsum()
p2_break_points_won = p2_break_points_won_cum / (p2_break_points_cum + 0.000001) * 100
c = p2_break_points_won_cum
d = p2_break_points_cum
p1_break_points_won.name = 'p1_break_points_won'
p2_break_points_won.name = 'p2_break_points_won'

plt.plot(range(end - start), p1_break_points_won[start:end], label='p1')
plt.plot(range(end - start), p2_break_points_won[start:end], label='p2')
plt.title('break_points_won')
plt.legend()
plt.savefig('data/break points won.png')
plt.close()
# 5.winners
a = data_group_by_match['p1_winner'].cumsum()
b = data_group_by_match['p2_winner'].cumsum()
p1_winners = data_group_by_match['p1_winner'].cumsum()/points * 100
p2_winners = data_group_by_match['p2_winner'].cumsum()/points * 100

p1_winners.name = 'p1_winners'
p2_winners.name = 'p2_winners'

plt.plot(range(end - start), p1_winners[start:end], label='p1')
plt.plot(range(end - start), p2_winners[start:end], label='p2')
plt.title('winners count')
plt.legend()
plt.savefig('data/winners_count.png')
plt.close()

# 6.unforced records
a = data_group_by_match['p1_unf_err'].cumsum()
b = data_group_by_match['p2_unf_err'].cumsum()
p1_unforced_records = data_group_by_match['p1_unf_err'].cumsum()/points * 100
p2_unforced_records = data_group_by_match['p2_unf_err'].cumsum()/points * 100

p1_unforced_records.name = 'p1_unforced_records'
p2_unforced_records.name = 'p2_unforced_records'
plt.plot(range(end - start), p1_unforced_records[start:end], label='p1')
plt.plot(range(end - start), p2_unforced_records[start:end], label='p2')
plt.title('unforced records count')
plt.legend()
plt.savefig('data/unforced_records.png')
plt.close()

# 7.total points
a = data_raw['p1_points_won']
b= data_raw['p2_points_won']
p1_total_points = data_raw['p1_points_won']/points *100
p2_total_points = data_raw['p2_points_won']/points * 100

p1_total_points.name = 'p1_total_points'
p2_total_points.name = 'p2_total_points'

plt.plot(range(end - start), p1_total_points[start:end], label='p1')
plt.plot(range(end - start), p2_total_points[start:end], label='p2')
plt.title('total points')
plt.legend()
plt.savefig('data/total_points.png')
plt.close()

## 8.distance per rally
## 一个match中最大最小值归一化，可以使用DataFrame.apply(lamba)
# p1_distance_per_rally = (data_raw['p1_distance_run'])
# p2_distance_per_rally = (data_raw['p2_distance_run'])
#
# p1_distance_per_rally.name = 'p1_distance'
# p2_distance_per_rally.name = 'p2_distance'
#
# plt.plot(range(end - start), p1_distance_per_rally[start:end], label='p1')
# plt.plot(range(end - start), p2_distance_per_rally[start:end], label='p2')
# plt.title('distance per rally')
# plt.legend()
# plt.savefig('data/distance_per_rally.png')
# plt.close()

feature_raw = [p1_ace, p1_double_faults, p1_net_points_won, p1_break_points_won, p1_winners, p1_unforced_records,
               p1_total_points,  # p1_distance_per_rally,
               p2_ace, p2_double_faults, p2_net_points_won, p2_break_points_won, p2_winners, p2_unforced_records,
               p2_total_points,  # p2_distance_per_rally,
               data_raw['match_id'], data_raw['server'], data_raw['serve_no'], data_raw['p1_points_won'],
               data_raw['p2_points_won'], data_raw['speed_mph'], data_raw['point_victor'], data_raw['p1_double_fault']
    , data_raw['p2_double_fault'], pd.Series(np.ones_like(p1_ace), name='one')
               ]

feature_raw = pd.concat(feature_raw, axis=1)
# 1st serves
p1_st_serves = feature_raw[feature_raw['server'] == 1]  # player1 server

p1_st_serve1 = pd.concat([pd.Series(p1_st_serves['serve_no'] == 1, name='p1_st_serve1'),  # whether 1st
                          p1_st_serves['match_id'],  # for group by
                          p1_st_serves['point_victor']
                          ], axis=1)
p1_st_serves_g = p1_st_serves.groupby('match_id')
p1_st_serve1['p1_st_serve1'] = p1_st_serve1['p1_st_serve1'].astype(bool)
p1_st_serve1_g = p1_st_serve1.groupby('match_id')
p1_st_serve_in = p1_st_serve1_g['p1_st_serve1'].cumsum() / p1_st_serves_g['one'].cumsum()
a = p1_st_serve1_g['p1_st_serve1'].cumsum()
b = p1_st_serves_g['one'].cumsum()
p1_st_serve_in.name = 'p1_st_serve_in'

p2_st_serves = feature_raw[feature_raw['server'] == 2]
p2_st_serve1 = pd.concat([pd.Series(p2_st_serves['serve_no'] == 1, name='p2_st_serve1', dtype=bool),
                          p2_st_serves['match_id'],
                          p2_st_serves['point_victor']
                          ], axis=1)
p2_st_serves_g = p2_st_serves.groupby('match_id')
p2_st_serve1['p2_st_serve1'] = p2_st_serve1['p2_st_serve1'].astype(bool)
p2_st_serve1_g = p2_st_serve1.groupby('match_id')

p2_st_serve_in = p2_st_serve1_g['p2_st_serve1'].cumsum() / p2_st_serves_g['one'].cumsum()
p2_st_serve_in.name = 'p2_st_serve_in'
c = p2_st_serve1_g['p2_st_serve1'].cumsum()
d = p2_st_serves_g['one'].cumsum()
# 1st serve points won
p1_st_serve1_only = p1_st_serve1[p1_st_serve1['p1_st_serve1']]
p1_st_serve1_won = pd.concat(
    [p1_st_serve1['match_id'],
     pd.Series(p1_st_serve1_only['point_victor'] == 1, name='point_victor1', dtype=bool)
     ],
    axis=1
)
p1_st_serve1_won = p1_st_serve1_won.fillna(False)
p1_st_serve1_won_g = p1_st_serve1_won.groupby('match_id')
p1_st_serve1_g = p1_st_serve1.groupby('match_id')
p1_st_serve_points_won = p1_st_serve1_won_g['point_victor1'].cumsum() / (p1_st_serve1_g['p1_st_serve1'].cumsum())
p1_st_serve_points_won.name = 'p1_st_serve_points_won'
a = p1_st_serve1_won_g['point_victor1'].cumsum()
b = p1_st_serve1_g['p1_st_serve1'].cumsum()
p2_st_serve1_only = p2_st_serve1[p2_st_serve1['p2_st_serve1']]
p2_st_serve1_won = pd.concat(
    [p2_st_serve1['match_id'],
     pd.Series(p2_st_serve1_only['point_victor'] == 2, name='point_victor2', dtype=bool)
     ],
    axis=1
).groupby('match_id')
p2_st_serve1_won = p2_st_serve1_won.fillna(False)
p2_st_serve1_ = p2_st_serve1.groupby('match_id')
p2_st_serve_points_won = p2_st_serve1_won['point_victor2'].cumsum() / (p2_st_serve1['p2_st_serve1'].cumsum())
p2_st_serve_points_won.name = 'p2_st_serve_points_won'
c = p2_st_serve1_won['point_victor2'].cumsum()
d = p2_st_serve1['p2_st_serve1'].cumsum()
features_p1 = [p1_ace, p1_double_faults, p1_net_points_won, p1_break_points_won, p1_winners, p1_unforced_records,
               p1_total_points
               ]
features_p1 = pd.concat(features_p1, axis=1)
features_p1.columns = ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
                       'total_points']

features_p2 = [
    p2_ace, p2_double_faults, p2_net_points_won, p2_break_points_won, p2_winners, p2_unforced_records,
    p2_total_points
]
features_p2 = pd.concat(features_p2, axis=1)
features_p2.columns = ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
                       'total_points']

feature_p1_st_nd = pd.concat([p1_st_serve_in * p1_st_serve_points_won*100], axis=1)
feature_p1_st_nd.columns = ['st_serve']
feature_of_p1 = pd.concat([features_p1.copy(), feature_p1_st_nd], axis=1)

feature_p2_st_nd = pd.concat([p2_st_serve_in * p2_st_serve_points_won*100], axis=1)
feature_p2_st_nd.columns = ['st_serve']
feature_of_p2 = pd.concat([features_p2.copy(), feature_p2_st_nd], axis=1)

feature_all = pd.concat([data_raw[['match_id', 'point_no']], feature_of_p1, feature_of_p2, data_raw['server']], axis=1)
feature_all.columns = ['match_id', 'point_no',
                       'p1_ace', 'p1_double_faults', 'p1_net_points_won', 'p1_break_points_won',
                       'p1_winners',
                       'p1_unforced_records', 'p1_total_points', 'p1_st_serve',
                       'p2_ace', 'p2_double_faults', 'p2_net_points_won', 'p2_break_points_won', 'p2_winners',
                       'p2_unforced_records', 'p2_total_points', 'p2_st_serve',
                       'server'
                       ]
feature_all = feature_all.groupby('match_id').fillna(method='ffill')
feature_all = feature_all.fillna(0)
test_1 = feature_all[['p1_ace', 'p1_double_faults', 'p1_net_points_won', 'p1_break_points_won',
                      'p1_winners',
                      'p1_unforced_records', 'p1_total_points', 'p1_st_serve']].copy().reset_index(drop=True)
test_1.columns = ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
                  'total_points', 'st_serve']
test_2 = feature_all[['p2_ace', 'p2_double_faults', 'p2_net_points_won', 'p2_break_points_won', 'p2_winners',
                      'p2_unforced_records', 'p2_total_points', 'p2_st_serve']].copy().reset_index(drop=True)
test_2.columns = ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
                  'total_points', 'st_serve']
test = pd.concat([test_1, test_2], axis=0)
test.to_csv(os.path.join(path,'test.csv'))
feature_all.to_csv(os.path.join(path,'Wimbledon_featured_matches_all.csv'))
