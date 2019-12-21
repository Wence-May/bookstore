# order 相关的功能
import app.model.Global as Global
import json 
from app.model.create_db import DB_operations,Users,Orders,UserToken,OrderBooks,StoreBooks
from app.model.user import User
import app.model.error as error
import logging
from datetime import datetime
from sqlalchemy import and_,update

class Seller():
    def delivery_books(self,seller_id:str,order_id:str,token: str)->(str,str):
        # check token
        code,message = User().check_token(seller_id,token)
        if(code!=200):
            return code,message
        session = DB_operations().connnet_db()
        # 该订单不存在
        order = session.query(Orders).filter(Orders.OrderId==order_id).first()
        if order == None:
            return error.error_invalid_order_id(order_id)
        # 订单非已付款的状态
        if order.Status==3:
            return error.error_repeated_operation("delivery books")
        if order.Status==1:
            return error.error_order_steate_not_right("Unpayed order")
        if order.Status==5:
            return error.error_order_steate_not_right("Fail order")
        if order.Status==4:
            return error.error_order_steate_not_right("finished order")
        # 修改订单状态：  
        session.execute(
                    update(Orders).where(Orders.OrderId==order_id).values(
                    {Orders.Status:"3"}))
        session.commit()
        session.close()
        return error.success("Dlivery books")