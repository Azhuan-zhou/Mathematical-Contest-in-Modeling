import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('TKAgg')


def PCA_method(corr):
    # data (n,p)
    eigValues, eig = np.linalg.eig(corr)
    eigValues_sum = np.sum(eigValues)
    lambda_ = eigValues[0] / eigValues_sum * 100  # 计算累计贡献率
    w1 = eig[:, 0]
    print('选取的第一个特征值为：{}，特征向量为：{}'.format(eigValues[0], w1))
    print('累计贡献率为： {}%'.format(lambda_))
    print('所有特征值：',eigValues)
