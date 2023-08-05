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
import time
import random
import datetime

class ml3:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True



class plot:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True

    """
    data必须是dataframe,column_name是特征名字
    """
    def histplot(data,column_name,**kwargs):
        X = np.array(data[column_name])
        X_min = min(X)
        X_max = max(X)
        X_range = X_max - X_min;
        X_min     = int(kwargs['xmin'])     if 'xmin'    in kwargs else min(X) - X_range *0.05
        X_max     = int(kwargs['xmax'])     if 'xmax'    in kwargs else max(X) + X_range *0.05
        column_bins = np.arange(np.min(X), np.max(X), 0.1)
        column_mean = np.mean(X)
        column_std = np.std(X)
        plt.figure(figsize=(16, 8), dpi=100)
        plt.xlim(X_min, X_max)
        sns.distplot(X, kde=True,norm_hist=True,bins=column_bins,color="black")
        plt.title(column_name + " mean=%.1f std=%.1f" % (float(column_mean), float(column_std)))
        plt.axvline(x=column_mean, color="r", linewidth=5)
        plt.axvline(x=column_mean - column_std, color="r", linewidth=2)
        plt.axvline(x=column_mean + column_std, color="r", linewidth=2)
        plt.axvline(x=column_mean - 2*column_std, color="r", linewidth=1)
        plt.axvline(x=column_mean + 2*column_std, color="r", linewidth=1)
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        plt.savefig(file_name + ".png", dpi=100)
        return True
    def normal_distribution(mean, sigma):
        x = np.linspace(mean - 6*sigma, mean + 6*sigma, 100)
        return x,np.exp(-1*((x-mean)**2)/(2*(sigma**2)))/(math.sqrt(2*np.pi) * sigma)
    
    def gmmplot(data,feature_name,**kwargs):
        N_COMPONENTS = int(kwargs['n_components'])     if 'n_components'    in kwargs else 2
        X = np.array(data[feature_name])

        X_min = min(X)
        X_max = max(X)
        X_range = X_max - X_min;
        X_min     = int(kwargs['xmin'])     if 'xmin'    in kwargs else min(X) - X_range *0.05
        X_max     = int(kwargs['xmax'])     if 'xmax'    in kwargs else max(X) + X_range *0.05
        feature_bins = np.arange(np.min(X), np.max(X), 0.1)
        
        feature_mean = np.mean(X)
        feature_std = np.std(X)
        
        X_array = X.reshape(len(X),1)
        gmm = GaussianMixture(n_components=N_COMPONENTS).fit(X_array)
        #print(gmm.get_params(True))
        
        #打印5个分布的权重
        #print(gmm.weights_)
        
        #打印5个分布的期望
        #print(gmm.means_)
        
        #打印5各分布的协方差,因为高斯混合模型是面向多维的，所以
        #print(gmm.covariances_)
        
        labels = gmm.predict(X_array)
        
        plt.figure(figsize=(16, 8), dpi=100)
        plt.xlim(X_min , X_max)
        plt.title("score=%.2f" % ( float(gmm.score(X_array))))
        for k in range(N_COMPONENTS):
            datask = []
            for i in range(len(labels)):
                if labels[i] == k:
                    datask.append(X[i])
            weight = gmm.weights_[k]
            mean = gmm.means_[k][0]
            std = math.sqrt(gmm.covariances_[k][0][0])
            label_str = "mean=%.2f std=%.2f weight=%.2f"%(mean,std,weight)
            #sns.distplot(datask, bins=100,norm_hist=True,kde=True,fit=scipy.stats.norm,kde_kws={ "label": label_str})
            sns.distplot(datask, bins=feature_bins,norm_hist=True,kde=True,kde_kws={ "label": label_str})
            x,y = self.normal_distribution(mean, std)
            plt.plot(x, y, color = "black")
        plt.show()


def main():
    ml3.intro()

if __name__ == '__main__':
     main()

