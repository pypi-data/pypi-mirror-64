#Xdua Machine Learning 3 SDK

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import pearsonr
import math
import scipy
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
import joblib
import hashlib




class ml3:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True

    """
    data必须是dataframe,column_name是特征名字
    """
    def histplot(data,column_name):
        X = np.array(data[column_name])
        X_min = min(X)
        X_max = max(X)
        column_bins = np.arange(np.min(X), np.max(X), 0.1)
        column_mean = np.mean(X)
        column_std = np.std(X)
        plt.figure(figsize=(16, 8), dpi=100)
        plt.xlim(X_min-5 , X_max+5)
        sns.distplot(X, kde=True,norm_hist=True,bins=column_bins,color="black")
        plt.title(column_name + " mean=%.1f std=%.1f" % (float(column_mean), float(column_std)))
        plt.axvline(x=column_mean, color="r", linewidth=5)
        plt.axvline(x=column_mean - column_std, color="r", linewidth=2)
        plt.axvline(x=column_mean + column_std, color="r", linewidth=2)
        plt.axvline(x=column_mean - 2*column_std, color="r", linewidth=1)
        plt.axvline(x=column_mean + 2*column_std, color="r", linewidth=1)
        datetime_str = time.strftime("%Y%m%d%H%M%S",time.localtime())
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        plt.savefig(file_name + ".png", dpi=100)
        return True

def main():
    ml3.intro()

if __name__ == '__main__':
     main()

