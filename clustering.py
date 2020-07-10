import numpy as np 
import pandas as pd 
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt


class Clustering(object):
    '''
        Cluster the scholars in the data set
    '''
    def __init__(self, file_path = "./results/cluster_features.csv"):
        self.data = pd.read_csv(file_path, index_col=0)
        #self.data.drop([31], inplace=True)
        self.data.drop([76], inplace=True)
        self.data.drop([47], inplace=True)
        self.data.iloc[:, 1] = 2020 - self.data.iloc[:, 1]
        self.data = self.data.rename({"earliest_year":"academic_age"}, axis="columns")
        self.full_features = scale(self.data.iloc[:, 1:])
        self.features_no_h = scale(self.data.iloc[:, [1,3,4,5]])
        self.features_no_j = scale(self.data.iloc[:, [1,2,3,4]])
        self.features_no_pj = scale(self.data.iloc[:, [1,2,3]])
        self.features_no_c = scale(self.data.iloc[:, [1,2,4,5]])
        self.features_no_ch = scale(self.data.iloc[:, [1,4,5]])

    def kmeans_clustering(self, data, n, save_data=False):
        model = KMeans(n_clusters=n).fit(data)
        mean_dist = sum(np.min(cdist(data, model.cluster_centers_, "euclidean"), axis=1))/data.shape[0]
        self.labels = model.labels_
        self.result = self.data
        self.result["labels"] = self.labels
        print(self.result)
        if save_data:
            self.result.to_csv("./results/cluster_orders.csv")
            print("data saved.")
        
        return mean_dist

    def select_opt_k(self, data):
        mean_dist = []
        for k in range(1, 6):
            temp = self.kmeans_clustering(data=data, n=k)
            mean_dist.append(temp)

        figure, ax = plt.subplots(1, 1)
        ax.plot(range(1, 6), mean_dist, "o-")
        ax.set_xticks(range(1, 6))
        ax.set_xlabel("k")
        ax.set_ylabel("SSE")
        plt.savefig("./results/figures/elb.png", dpi=800)
        plt.show()

    def draw_scatter_plots(self):
        data = self.result.iloc[:, [1,2,3,4,5,6]]
        type0 = data[data["labels"]==0]
        type1 = data[data["labels"]==1]
        type2 = data[data["labels"]==2]
        type3 = data[data["labels"]==3]
        
        figure, ax = plt.subplots(2, 2)
        ax[0,0].scatter(type0.iloc[:,0], type0.iloc[:, 4], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[0,0].scatter(type1.iloc[:,0], type1.iloc[:, 4], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[0,0].scatter(type2.iloc[:,0], type2.iloc[:, 4], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[0,0].scatter(type3.iloc[:,0], type3.iloc[:, 4], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[0,0].set_xlabel("Academic age")
        ax[0,0].set_ylabel("Number of citation")

        ax[0,1].scatter(type0.iloc[:,0], type0.iloc[:, 3], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[0,1].scatter(type1.iloc[:,0], type1.iloc[:, 3], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[0,1].scatter(type2.iloc[:,0], type2.iloc[:, 3], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[0,1].scatter(type3.iloc[:,0], type3.iloc[:, 3], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[0,1].set_xlabel("Academic age")
        ax[0,1].set_ylabel("Number of paper")

        ax[1,0].scatter(type0.iloc[:,0], type0.iloc[:, 1], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[1,0].scatter(type1.iloc[:,0], type1.iloc[:, 1], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[1,0].scatter(type2.iloc[:,0], type2.iloc[:, 1], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[1,0].scatter(type3.iloc[:,0], type3.iloc[:, 1], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[1,0].set_ylabel("H-index")
        ax[1,0].set_xlabel("Academic age")

        ax[1,1].scatter(type0.iloc[:,4], type0.iloc[:, 3], s=(type0.iloc[:, 1]/20.0)**2, c="red", label="type0")
        ax[1,1].scatter(type1.iloc[:,4], type1.iloc[:, 3], s=(type1.iloc[:, 1]/20.0)**2, c="blue", label="type1")
        ax[1,1].scatter(type2.iloc[:,4], type2.iloc[:, 3], s=(type2.iloc[:, 1]/20.0)**2, c="green", label="type2")
        ax[1,1].scatter(type3.iloc[:,4], type3.iloc[:, 3], s=(type3.iloc[:, 1]/20.0)**2, c="orange", label="type3")
        ax[1,1].set_ylabel("Number of paper")
        ax[1,1].set_xlabel("Number of citation")

        plt.subplots_adjust(wspace=0.45, hspace=0.45)

        ax[0,0].legend()
        ax[0,1].legend()
        ax[1,0].legend()
        ax[1,1].legend()
        plt.savefig("./results/figures/cluster_figure.png", dpi=800)
        plt.show()
        


def extract_cluster_features():
    data = pd.read_csv("./results/earliest_year.csv", index_col=0)
    data.index = range(0, data.shape[0])
    data = data.rename({"0":"name", "1":"earliest_year"}, axis="columns")
    #print(data.head())

    coauthor_data = pd.read_excel("./data/author_info/AuthorInfo.xlsx")
    coauthor_data = coauthor_data.iloc[:, 2:]
    #print(coauthor_data.head())

    num_data = pd.read_csv("./results/num_info.csv", index_col=0)
    num_data = num_data.iloc[:, 1:]
    #print(num_data.head())

    data = pd.concat([data, coauthor_data], axis=1)
    data = pd.concat([data, num_data], axis=1)
    #print(data.head())

    data.to_csv("./results/cluster_features.csv")
    print("data saved.")



if __name__ == "__main__":
    #extract_cluster_features()
    C = Clustering()
    data = C.features_no_c
    C.select_opt_k(data)
    C.kmeans_clustering(data=data, n=4, save_data=False)
    C.draw_scatter_plots()
    
    
    