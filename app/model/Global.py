import time
from datetime import datetime,timedelta
order_timeout_delta =  timedelta(hours = 12)  # 订单过时的期限
DbURL  = "postgresql://postgres:mwj1314520@localhost:5432/BookStore"
TokenTimeout = timedelta(hours=6)   # token 过期期限
PicturePath = "./../static/pictures/"

"""
下单:1
付款：2
发货：3
收货：4
订单失败：5
"""

      

