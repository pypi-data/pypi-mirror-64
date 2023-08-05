#Xdua Machine Learning 3 SDK

import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
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
import seaborn as sns
from sklearn.metrics import silhouette_score

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
        print("这是地球号旗下数据分析绘图包")
        return True

    """
    data必须是dataframe,column_name是特征名字
    """
    def histplot(data,column_name,**kwargs):
        try:
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
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
        
        except Exception as err:
            print("An error occured!")
            print(err)
            return False
        
    def normal_distribution(mean, sigma):
        x = np.linspace(mean - 6*sigma, mean + 6*sigma, 100)
        return x,np.exp(-1*((x-mean)**2)/(2*(sigma**2)))/(math.sqrt(2*np.pi) * sigma)
    
    def gmmplot(data,feature_name,**kwargs):
        try:
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
            score_silhouette = silhouette_score(X_array, labels)
            plt.figure(figsize=(16, 8), dpi=100)
            plt.xlim(X_min , X_max)
            plt.title("GMM: K=%d score_silhouette=%.3f" % (N_COMPONENTS, score_silhouette))
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
                x,y = plot.normal_distribution(mean, std)
                plt.plot(x, y, color = "black")
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True

        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def kmeansplot(data,feature_name,**kwargs):
        try:
            N_CLUSTERS = int(kwargs['n_clusters'])     if 'n_clusters'    in kwargs else 2
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
            
            #调用kmeans类
            clf = KMeans(n_clusters=N_CLUSTERS)
            s = clf.fit(X_array)
        
        
            #9个中心
            #print(clf.cluster_centers_)
            
            #每个样本所属的簇
            #print(clf.labels_)
            
            #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
            #print(clf.inertia_)
            
            #进行预测
            labels = clf.predict(X_array)
            
            #保存模型
            #joblib.dump(clf , 'km.pkl')
            
            #载入保存的模型
            #clf = joblib.load('km.pkl')
            #print(gmm.get_params(True))

            score_silhouette = silhouette_score(X_array, labels)
            plt.figure(figsize=(16, 8), dpi=100)
            plt.xlim(X_min , X_max)
            plt.title("Kmeans: K=%d score_silhouette=%.3f inertia=%.3f" % (N_CLUSTERS, score_silhouette,clf.inertia_))
            for k in range(N_CLUSTERS):
                datask = []
                for i in range(len(labels)):
                    if labels[i] == k:
                        datask.append(X[i])
                datask_np = np.array(datask)
                cluster_mean = np.mean(datask_np)
                cluster_std  = np.std(datask_np)
                center = clf.cluster_centers_[k][0]
                label_str = "mean=%.2f std=%.2f center=%.2f"%(cluster_mean,cluster_std,center)
                sns.distplot(datask, bins=feature_bins,norm_hist=True,kde=True,kde_kws={ "label": label_str})
                x,y = plot.normal_distribution(cluster_mean, cluster_std)
                plt.plot(x, y, color = "black")
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True

        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def metrics(scores, n_clusters_range, **kwargs):
        try:
            X_LABEL = str(kwargs['x_label'])     if 'x_label'    in kwargs else "Number of clusters"
            Y_LABEL = str(kwargs['y_label'])     if 'y_label'    in kwargs else "Silhouette Score"

        
            range_space = n_clusters_range[1] - n_clusters_range[0]
            if range_space != len(scores):
                err = "The length of scores %d doesn't match the n_clusters_range %d." % (len(scores), range_space)
                raise Exception(err)

            plt.figure(figsize=(16, 8), dpi=100)

            plt.plot(range(n_clusters_range[0], n_clusters_range[1]), scores, marker='o')
            plt.xlabel(X_LABEL)
            plt.ylabel(Y_LABEL)

            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
            
        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def do_errorbar_1d(x, data, feature_name, kwargs):
        X_LABEL = str(kwargs['x_label'])     if 'x_label'    in kwargs else "time"
        Y_LABEL = str(kwargs['y_label'])     if 'y_label'    in kwargs else "value"
        TITLE = str(kwargs['title'])     if 'title'    in kwargs else "Errorbar plot"

        timeList = []
        for i in x:
            timeList.append(datetime.datetime.fromtimestamp(i))

        plt.figure(figsize=(24, 8), dpi=100)

        ax = plt.subplot()
        ax.errorbar(x=timeList, y=data[feature_name[0]], yerr=data[feature_name[1]], elinewidth=0.2, fmt=".", capsize=0.4)
        plt.title(TITLE)
        plt.xlabel(X_LABEL)
        plt.ylabel(Y_LABEL)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.01))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        file_name = file_name + ".png"
        print(file_name)
        plt.savefig(file_name, dpi=100)
        return True

    def do_errorbar_2d(x, data, feature_name, kwargs):
        X_LABEL = str(kwargs['x_label'])     if 'x_label'    in kwargs else "time"
        Y_LABEL = str(kwargs['y_label'])     if 'y_label'    in kwargs else "value"
        TITLE = str(kwargs['title']) if 'title' in kwargs else "Errorbar plot"

        timeList = []
        for i in x:
            timeList.append(datetime.datetime.fromtimestamp(i))

        plt.figure(figsize=(24, 8), dpi=100)

        ax1 = plt.subplot()
        ax2 = ax1.twinx()
        p1 = ax1.errorbar(x=timeList, y=data[feature_name[0][0]], yerr=data[feature_name[0][1]], elinewidth=0.2, fmt=".", capsize=0.4, color="blue")
        p2 = ax2.errorbar(x=timeList, y=data[feature_name[0][1]], yerr=data[feature_name[1][1]], elinewidth=0.2, fmt=".", capsize=0.4, color="red")
        plt.legend([p1, p2], ["Left", "Right"], loc='upper left')
        plt.title(TITLE)
        plt.xlabel(X_LABEL)
        plt.ylabel(Y_LABEL)

        ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.01))
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        file_name = file_name + ".png"
        print(file_name)
        plt.savefig(file_name, dpi=100)
        return True

    def errorbarplot(data, x, feature_name, **kwargs):
        try:
            pd.plotting.register_matplotlib_converters()
            if len(feature_name) != 2:
                err = "The length of feature_name is not 2."
                raise Exception(err)

            if isinstance(feature_name[0], str):
                return plot.do_errorbar_1d(x, data, feature_name, kwargs)
            elif isinstance(feature_name[0], list):
                return plot.do_errorbar_2d(x, data, feature_name, kwargs)
            else:
                print("feature_name Type error. feature_name should be [str, str] or [[str, str], [str, str]].")
                return False
        except Exception as err:
            print("An error occured!")
            print(err)
            return False



class seaborn:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True

    def boxplot():
        return

def main():
    ml3.intro()

if __name__ == '__main__':
     main()

