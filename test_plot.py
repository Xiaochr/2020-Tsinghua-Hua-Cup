import numpy as np 
import pandas as pd 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm



def yao_reg():
    '''
        Draw an h-index plot for Prof. Yao
    '''
    data = [0, 0, 1, 1, 1, 2, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 30, 32, 33, 33, 33, 34, 34, 35, 36, 36, 37, 38, 39]
    data = np.array(data).reshape(-1, 1)
    train_y = data[:-10]
    test_y = data[-10:]

    t = range(0, len(data))
    t = np.array(t).reshape(-1, 1)
    train_t = t[:-10]
    test_t = t[-10:]
    model = LinearRegression(normalize=True)
    model.fit(train_t, train_y)
    pred = model.predict(test_t)
    pred_train = model.predict(train_t)
    print(model.coef_)
    print(model.intercept_)

    R2 = model.score(test_t, test_y)
    print(R2)
    mse_pred = mean_squared_error(test_y, pred)
    print(mse_pred)

    # statsmodels
    X_train = sm.add_constant(train_t)
    est = sm.OLS(train_y, X_train)
    est = est.fit()
    summary = est.summary()
    print(summary)

    figure, ax = plt.subplots(1, 1)

    ax.plot(train_t, train_y, c="blue")
    ax.plot(train_t, pred_train, c="orange")
    ax.plot(test_t, test_y, c="blue")
    ax.plot(test_t, pred, c="orange", label="pred")

    ax.set_xlabel("Academic age")
    ax.set_ylabel("H-index")

    plt.legend()
    plt.savefig("./results/figures/yao.png", dpi=800)
    plt.show()



if __name__ == "__main__":
    yao_reg()




