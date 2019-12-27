import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Order:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "order/")

    def user_cancel_order(self,user_id,order_id,token): # 取消订单
        json = {"user_id":user_id,"order_id":order_id}
        url = urljoin(self.url_prefix,"user_cancel_order")
        headers = {"token":token}
        r = requests.post(url,headers = headers,json = json)
        return r.satus_code 
    def order_status(self,user_id:str,order_id:str,token): # 根据订单号，查看单个订单
        json = {"user_id":user_id,"order_id":order_id}
        url = urljoin(self.url_prefix,"order_status")
        headers = {"token":token}
        r = requests.post(url,headers = headers,json = json)
        return r.satus_code
    def my_orders(self,user_id,token): # 查看我的所有订单
        json = {"user_id":user_id}
        url = urljoin(self.url_prefix,"my_orders")
        headers = {"headers":token}
        r = requests.post(url,headers = headers,json = json)
        return r.satus_code

    