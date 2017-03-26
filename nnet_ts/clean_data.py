# encoding=utf-8
'''
原始的id_date_flow数据是由dataframe.sql(groupby user_id)完成，不能保证所有用户的所有天数据都有，所以进行一次清洗和填充
'''

from datetime import timedelta
import datetime

start_time_str = "2015-07-01"
end_time_str = "2016-10-30"
start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d')
end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d')

flow_dict = {}
for shop_id in range(1, 2001):
    for day in range(0, 487):
        next_day = start_time + timedelta(days=day)
        # print next_day.date()
        flow_dict[(shop_id, next_day)] = 0

f = open("/home/wangtuntun/IJCAI/Data/id_date_flow", "r+")
raw_data = f.readlines()
f.close()
for ele in raw_data:
    ele = ele.split(",")
    shop_id = int(ele[0])
    date_str = ele[1]
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    flow = int(ele[2])
    flow_dict[(shop_id, date)] = flow

#一次清洗
for ele in flow_dict:
    # print ele,flow_dict[ele]
    shop_id = ele[0]
    date = ele[1]

    date1 = date + timedelta(days=30)
    date2 = date + timedelta(days=21)
    date3 = date + timedelta(days=14)
    date4 = date + timedelta(days=7)

    date5 = date - timedelta(days=30)
    date6 = date - timedelta(days=21)
    date7 = date - timedelta(days=14)
    date8 = date - timedelta(days=7)

    if flow_dict[ele] == 0:
        # 如果该shop改天的flow为0,则用未来三天的
        if end_time - date > timedelta(days=30):  # 如果不是截止日期的最后三天
            if flow_dict[(shop_id, date1)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date1)]
                continue

        elif end_time - date > timedelta(days=21):
            if flow_dict[(shop_id, date2)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date2)]
                continue
        elif end_time - date > timedelta(days=14):
            if flow_dict[(shop_id, date3)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date3)]
                continue
        elif end_time - date > timedelta(days=7):
            if flow_dict[(shop_id, date4)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date4)]
                continue
        else:
            if flow_dict[(shop_id,date5)] != 0:
                flow_dict[ele]=flow_dict[(shop_id,date5)]
            elif flow_dict[(shop_id,date6)] != 0:
                flow_dict[ele]=flow_dict[(shop_id,date6)]
            elif flow_dict[(shop_id,date7)] != 0:
                flow_dict[ele]=flow_dict[(shop_id,date7)]
            elif flow_dict[(shop_id,date8)] != 0:
                flow_dict[ele]=flow_dict[(shop_id,date8)]


#二次清洗
for ele in flow_dict:
    # print ele,flow_dict[ele]
    shop_id = ele[0]
    date = ele[1]
    # print flow_dict[(shop_id,date)]
    date1 = date + timedelta(days=1)
    date2 = date + timedelta(days=2)
    date3 = date + timedelta(days=3)

    date4 = date - timedelta(days=1)
    date5 = date - timedelta(days=2)
    date6 = date - timedelta(days=3)

    if flow_dict[ele] == 0:
        # 如果该shop改天的flow为0,则用未来三天的
        if end_time - date > timedelta(days=3):  # 如果不是截止日期的最后三天
            if flow_dict[(shop_id, date1)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date1)]
                continue
            elif flow_dict[(shop_id, date2)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date2)]
                continue
            elif flow_dict[(shop_id, date3)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date3)]
                continue
        else:
            if flow_dict[(shop_id, date4)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date4)]
                continue
            elif flow_dict[(shop_id, date5)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date5)]
                continue
            elif flow_dict[(shop_id, date6)] != 0:
                flow_dict[ele] = flow_dict[(shop_id, date6)]
                continue
        # 如果未来连续三天都没有，则就下一个商家未来三天的信息
        if shop_id != 2000:  # 如果shop_id=2000，则+1就超出范围。
            if flow_dict[(shop_id + 1, date1)] != 0:
                flow_dict[ele] = flow_dict[(shop_id + 1, date1)]
                continue
            elif flow_dict[(shop_id + 1, date2)] != 0:
                flow_dict[ele] = flow_dict[shop_id + 1, date2]
                continue
            elif flow_dict[(shop_id + 1, date3)] != 0:
                flow_dict[ele] = flow_dict[(shop_id + 1, date3)]
                continue
        else:
            if flow_dict[(shop_id - 1, date1)] != 0:
                flow_dict[ele] = flow_dict[(shop_id - 1, date1)]
                continue
            elif flow_dict[(shop_id - 1, date2)] != 0:
                flow_dict[ele] = flow_dict[(shop_id - 1, date2)]
                continue
            elif flow_dict[(shop_id - 1, date3)] != 0:
                flow_dict[ele] = flow_dict[(shop_id - 1, date3)]
                continue



#三次清洗
for ele in flow_dict:
    # print ele,flow_dict[ele]
    shop_id = ele[0]
    date = ele[1]
    import random
    if flow_dict[ele] == 0:
        random_int=random.randint(5, 50)
        flow_dict[ele]=random_int


#将结果写入文件
f_write=open("/home/wangtuntun/IJCAI/Data/id_date_flow_cleaned","w+")
for ele in flow_dict:
    shop_id=str(ele[0])
    date=ele[1]
    date_str=str(date.date())
    flow=str(flow_dict[ele])
    f_write.write(shop_id)
    f_write.write(",")
    f_write.write(date_str)
    f_write.write(",")
    f_write.write(flow)
    f_write.write("\n")

f_write.close()