import numpy as np 
import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import os

class NaiveRegModel(object):
    def __init__(self, file_name):
        self.data = pd.read_csv(file_name, index_col=0)
        self.N = self.data.shape[0]
        self.Y = self.data.iloc[:, 0]
        self.X = self.data.iloc[:, 1:]
        self.X.iloc[:, 2] = np.sqrt(self.X.iloc[:, 2])

        #self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=0)
        self.X_train = self.X.iloc[:int(0.8*self.N), :]
        self.X_test = self.X.iloc[int(0.8*self.N):, :]
        self.Y_train = self.Y.iloc[:int(0.8*self.N)]
        self.Y_test = self.Y.iloc[int(0.8*self.N):]

    def run_reg(self, draw=False):
        model = LinearRegression(normalize=True)
        model.fit(self.X_train, self.Y_train)
        self.pred = model.predict(self.X_test)
        self.pred_train = model.predict(self.X_train)
        self.coef_list = list(model.coef_)
        self.coef_list.insert(0, model.intercept_)
        #print(coef_list)
        self.R2 = model.score(self.X_test, self.Y_test)
        self.mse_pred = mean_squared_error(self.Y_test, self.pred)
        #print(mse_pred)

        # statsmodels
        X_train = sm.add_constant(self.X_train)
        est = sm.OLS(self.Y_train, X_train)
        est = est.fit()
        self.summary = est.summary()

        self.info = self.coef_list
        self.info.extend(list(est.pvalues))
        self.info.append(self.R2)
        self.info.append(self.mse_pred)
        if draw:
            self.draw_plots()

        return self.info


    def draw_plots(self):
        figure, ax = plt.subplots(1, 1)

        ax.plot(self.Y_train.index, self.Y_train)
        ax.plot(self.Y_train.index, self.pred_train)
        ax.plot(self.Y_test.index, self.Y_test)
        ax.plot(self.Y_test.index, self.pred, label="pred")

        plt.legend()
        plt.show()



def reg_all_data(file_path="./results/reg_data"):
    all_reg = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            reg_mod = NaiveRegModel(os.path.join(file_path, file_name))
            temp = reg_mod.run_reg()
            temp.insert(0, file_name[8:-4])
            temp = pd.DataFrame(temp).T
            all_reg = pd.concat([all_reg, temp], axis=0)
    print(all_reg)
    all_reg.index = list(range(0, all_reg.shape[0]))
    all_reg.to_csv("./results/reg_coef.csv")
    print("data saved. ")



if __name__ == "__main__":
    reg = NaiveRegModel("./results/reg_data/reg_for_Allen, Gabrielle D..csv")
    print(reg.run_reg(True))
    print(reg.summary)
    #reg_all_data()
