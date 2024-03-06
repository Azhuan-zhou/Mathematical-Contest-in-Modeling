import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

plt.switch_backend('TKAgg')


def corr_analysis(data):
    # 画热力图
    df_corr = data.corr()  # 计算相关系数矩阵
    fig, ax = plt.subplots(figsize=(6, 5))
    # mask
    mask = np.triu(np.ones_like(df_corr, dtype=bool))
    # adjust mask and df
    mask = mask[1:, :-1]
    corr = df_corr.iloc[1:, :-1].copy()
    # plot heatmap
    sns.heatmap(corr, mask=mask, annot=False, fmt=".2f",
                linewidths=5, cmap='viridis', vmin=-1, vmax=1,
                cbar_kws={"shrink": .8}, square=True)
    # ticks
    yticks = [i.upper() for i in corr.index]
    xticks = [i.upper() for i in corr.columns]
    plt.yticks(plt.yticks()[0], labels=yticks, rotation=0)
    plt.xticks(plt.xticks()[0], labels=xticks)
    # title
    title = 'CORRELATION MATRIX'
    plt.title(title, loc='left', fontsize=18)
    plt.savefig('picture/correlation.pdf')


if __name__ == '__main__':
    use = ['ACEP', 'DFP', 'NPW', 'BPW', 'WP', 'UEP', 'TPW', '$SR_1$']
    data_process = pd.read_csv('./checkpoint2/test.csv')[
        ['ace', 'double_faults', 'net_points_won', 'break_points_won', 'winners', 'unforced_records',
         'total_points', 'st_serve']]
    data_process.columns = use
    corr_analysis(data_process)
