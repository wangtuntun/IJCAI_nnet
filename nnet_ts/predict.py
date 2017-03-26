#encoding=utf-8
from nnet_ts import *
import matplotlib.pyplot as plt

#生成模型并预测接下来42天的flow
def predict_flow(time_series):
    neural_net = TimeSeriesNnet(hidden_layers=[20, 15, 5],activation_functions=['sigmoid', 'sigmoid', 'sigmoid'])  # 隐藏层每层的神经元格式以及激活函数
    neural_net.fit(time_series, lag=40, epochs=10000)  # epochs代表迭代次数
    predictions=neural_net.predict_ahead(n_ahead = 42)#预测接下来30天的值,将结果以ndarray的格式返回
    pre_loss=neural_net.loss#返回的是损失函数类型，不是误差。估计要自己定义计算误差的函数。
    return neural_net,predictions,pre_loss

#图形化显示结果
def show_predicted_flow(neural_net,time_series):
    plt.plot(range(len(neural_net.timeseries)), neural_net.timeseries, '-r', label='Predictions', linewidth=1)
    plt.plot(range(len(time_series)), time_series, '-g',  label='Original series')
    plt.title("Box & Jenkins AirPassenger data")
    plt.xlabel("Observation ordered index")
    plt.ylabel("No. of passengers")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    time_series = np.array(pd.read_csv("AirPassengers.csv")["x"])  # #array list 都可以
    neural_net, predictions, pre_loss=predict_flow(time_series)
    show_predicted_flow(neural_net,time_series)