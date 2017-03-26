#encoding=utf-8
import pandas as pd
# encoding=utf-8
from datetime import timedelta
import datetime
import random
start_time_str = "2015-07-01"
end_time_str = "2016-10-30"
start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d')
end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d')

list1=[ 214.08171082  ,242.06304932,  203.72013855  ,229.50350952  ,273.43499756
  ,273.45065308  ,291.86849976 , 202.27101135  ,240.02839661 , 216.33934021]
list_int=[]
for ele in list1:
    ele=str(int(ele))
    list_int.append(ele)
print(",".join(list_int))
