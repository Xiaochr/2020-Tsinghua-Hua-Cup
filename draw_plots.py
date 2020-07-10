import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


def draw_all_plots(data, title="", save=False):
    figure, ax = plt.subplots(1, 1)
    ax.plot(data)
    ax.set_title(title)
    ax.set_xlabel("Academic age")
    ax.set_ylabel("H-index")
    if save:
        plt.savefig("./results/figures/%s.png"%title, dpi=800)
        print("figure saved.")

    plt.show()

def plot_all_h():
    data = pd.read_csv("./results/h_index_data.csv", index_col=0)
    label = pd.read_csv("./results/cluster_orders.csv", index_col=0)["labels"]
    data = data.T
    data.index = range(0, data.shape[0])
    data = pd.concat([data, label], axis=1)
    data_0 = data[data["labels"] == 0]
    data_0 = data_0.iloc[:, :-3]
    data_1 = data[data["labels"] == 1]
    data_1 = data_1.iloc[:, :-3]
    data_2 = data[data["labels"] == 2]
    data_2 = data_2.iloc[:, :-3]
    data_3 = data[data["labels"] == 3]
    data_3 = data_3.iloc[:, :-3]
    
    draw_all_plots(data_0.T, "data_0")
    draw_all_plots(data_1.T, "data_1")
    draw_all_plots(data_2.T, "data_2")
    draw_all_plots(data_3.T, "data_3")


def plot_20_h():
    data = pd.read_csv("./results/first_20_year.csv", index_col=0)
    label = pd.read_csv("./results/cluster_orders.csv", index_col=0)["labels"]
    data = pd.concat([data, label], axis=1)
    data = data.iloc[:, 1:]
    data_0 = data[data["labels"] == 0]
    data_0 = data_0.iloc[:, :-1]
    data_1 = data[data["labels"] == 1]
    data_1 = data_1.iloc[:, :-1]
    data_2 = data[data["labels"] == 2]
    data_2 = data_2.iloc[:, :-1]
    data_3 = data[data["labels"] == 3]
    data_3 = data_3.iloc[:, :-1]
    
    draw_all_plots(data_0.T, "data_0")
    draw_all_plots(data_1.T, "data_1")
    draw_all_plots(data_2.T, "data_2")
    draw_all_plots(data_3.T, "data_3")
    

def double_plot(title="Yoshua Bengio"):
    data = pd.read_csv("./results/h_index_data.csv", index_col=0)
    data = data.iloc[:-2, 6]
    #draw_all_plots(data.iloc[:-2, 36], title=title, save=True)
    figure, ax = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].plot(data)
    ax[0].set_title(title)
    ax[0].set_xlabel("Academic age")
    ax[0].set_ylabel("H-index")

    data_0 = pd.read_csv("./results/h_index_data.csv", index_col=0)
    label = pd.read_csv("./results/cluster_orders.csv", index_col=0)["labels"]
    data_0 = data_0.T
    data_0.index = range(0, data_0.shape[0])
    data_0 = pd.concat([data_0, label], axis=1)
    data_0 = data_0[data_0["labels"] == 1]
    data_0 = data_0.iloc[:, :-3]

    ax[1].plot(data_0.T, c="blue")
    ax[1].set_title("All type1")
    ax[1].set_xlabel("Academic age")
    ax[1].set_ylabel("H-index")

    plt.savefig("./results/figures/%s.png"%title, dpi=800)
    print("figure saved.")

    plt.show()


def double_plot2(title="type2_3"):
    figure, ax = plt.subplots(1, 2, figsize=(8, 4))
    data = pd.read_csv("./results/h_index_data.csv", index_col=0)
    label = pd.read_csv("./results/cluster_orders.csv", index_col=0)["labels"]
    data = data.T
    data.index = range(0, data.shape[0])
    data = pd.concat([data, label], axis=1)
    data_2 = data[data["labels"] == 2]
    data_2 = data_2.iloc[:, :-3]
    data_3 = data[data["labels"] == 3]
    data_3 = data_3.iloc[:, :-3]


    ax[0].plot(data_2.T, c="red")
    ax[0].set_title("All type2")
    ax[0].set_xlabel("Academic age")
    ax[0].set_ylabel("H-index")

    ax[1].plot(data_3.T, c="blue")
    ax[1].set_title("All type3")
    ax[1].set_xlabel("Academic age")
    ax[1].set_ylabel("H-index")

    plt.savefig("./results/figures/%s.png"%title, dpi=800)
    print("figure saved.")

    plt.show()


def yao():
    data = [0, 0, 1, 1, 1, 2, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 30, 32, 33, 33, 33, 34, 34, 35, 36, 36, 37, 38, 39, 39]
    draw_all_plots(data)



if __name__ == "__main__":
    data = pd.read_csv("./results/h_index_data.csv", index_col=0)
    draw_all_plots(data.iloc[:-2, 9], title="", save=False)
    #plot_all_h()
    #double_plot2()
    #yao()

