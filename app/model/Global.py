import time
from datetime import datetime,timedelta
timeout_delta =  timedelta(hours = 12)  # 订单过时的期限
DbURL  = "postgresql://postgres:mwj1314520@localhost:5432/BookStore"
TokenTimeout = timedelta(hours=6)   # token 过期期限

"""
下单:1
付款：2
发货：3
收货：4
订单失败：5

Token 的时间用 datetime.datetime 的方式
"""
# print(datetime.now()>datetime.now()+TokenTimeout)
dic1= {"a":1}
dic2 = {"c":2}
dic = dict(**dic1,**dic2)
import json 
print(type(json.dumps(dic)))
a = [1,2,3]
print(*dic1)