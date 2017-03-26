#encoding=utf-8
from nnet_ts import *
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta


start_time_str = "2015-07-01"
end_time_str = "2016-10-30"
start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d')
end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d')

#清洗数据
def clean_data(data_path):
    #已经在clean_data.py文件中完成，并已经存入文件id_date_flow_cleaned
    pass

#传入shop_id返回所有天的flow（天数连续且完整）
def get_shop_flows(shop_id,flow_dict):
    return_list = []
    for day in range(0, 488):  # 训练集一共有488天
        next_day = start_time + timedelta(days=day)
        # print(shop_id,next_day.date(),flow_dict[(shop_id,next_day)])
        return_list.append(flow_dict[(shop_id, next_day)])
    return return_list

#将浮点list转换为一个int型的字符串
def float_list2str(float_list):
    list_int = []
    for ele in float_list:
        ele = str(int(ele))
        list_int.append(ele)

    return ",".join(list_int)

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
    # time_series = list(np.array(pd.read_csv("AirPassengers.csv")["x"]))#array list 都可以
    # neural_net, predictions, pre_loss=predict_flow(time_series)
    # show_predicted_flow(neural_net,time_series)
    cleaned_data_path="/home/wangtuntun/IJCAI/Data/id_date_flow_cleaned"
    f_open = open(cleaned_data_path, "r+")
    raw_data = f_open.readlines()
    f_open.close()
    flow_dict = {}
    for ele in raw_data:
        ele = ele.split(",")
        shop_id = int(ele[0])
        time_str = ele[1]
        date = datetime.datetime.strptime(time_str, '%Y-%m-%d')
        flow = int(ele[2])
        flow_dict[(shop_id, date)] = flow
    result_path="/home/wangtuntun/IJCAI/Data/nnets_predicted_flow"
    f_write=open(result_path,"w+")
    # show_predicted_flow(neural_net,time_series)
    for i in range(1,2001):
        shop_flow_list = get_shop_flows(i, flow_dict)
        time_series = shop_flow_list
        neural_net, predictions, pre_loss = predict_flow(time_series)
        predictions_str=float_list2str(predictions)
        f_write.write(str(i))
        f_write.write(",")
        f_write.write(predictions_str)
        f_write.write("\n")
    f_write.close()