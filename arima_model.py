import numpy as np 
import pandas as pd 
import pmdarima as pm 


class ARIMAModel(object):
    def __init__(self, file_path="./results/h_index_data.csv"):
        self.data = pd.read_csv(file_path, index_col=0)
        self.e_year = pd.read_csv("./results/earliest_year.csv", index_col=0)

    def run_arima(self, i=0):
        temp_year = self.e_year.iloc[i, 1]
        if temp_year >= 1970:
            data_list = self.data.iloc[temp_year-1970+1:, i]
        else:
            data_list = self.data.iloc[:, i]
        
        model = pm.auto_arima(data_list, stepwise=True, seasonal=False)
        order = list(model.get_params()["order"])
        return order


def get_all_order():
    mod = ARIMAModel()
    order_list = pd.DataFrame([])
    for i in range(0, mod.data.shape[1]):
        temp = mod.run_arima(i)
        temp = pd.DataFrame(temp).T
        order_list = pd.concat([order_list, temp], axis=0)
    print(order_list)
    order_list.to_csv("./results/arima_orders.csv")
    print("data saved.")




if __name__ == "__main__":
    get_all_order()


