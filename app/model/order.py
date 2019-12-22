# order 相关的功能
import app.model.Global as Global
import json 
from app.model.create_db import Users,Orders,UserToken,OrderBooks,StoreBooks,create_session
from app.model.user import User
import app.model.error as error
import logging
from datetime import datetime
from sqlalchemy import and_,update,create_engine
from sqlalchemy.orm import sessionmaker
def to_dict(result:object,dropwords:list)->dict:
    dic = {}
    for att in dir(result):
        if att.startswith("_") or att in dropwords:
            continue
        value = getattr(result,att)
        dic[att] = value
    return dic

class Order():
    def __init__(self):
        self.engine = create_engine(Global.DbURL)
    def order_status(self,user_id:str,order_id:str,token:str)-> (str,str):
            '''
            0. check_token
            1. 查询订单是否存在，存在获取相关信息
            如果token 验证失败  code = 401,  message =  
            如果订单不存在 code =  518, message = 
            如果订单存在 返回订单信息和code =200
            '''
            # check token 
            code,message = User().check_token(user_id,token)
            if(code!="200"):
                return code,message
            # check order exist 
            session = create_session(self.engine)
            line  = session.query(Orders).filter(Orders.OrderId==order_id).first()
            session.close()
            if line == None:
                logging.error(error.error_invalid_order_id(order_id))
                return error.error_invalid_order_id(order_id)
            # order 存在， 查询OrderBooks
            dic = to_dict(line,[])
            line2  = session.query(OrderBooks).filter(Orders.OrderId==order_id).all()
            dic_list = line2.apply(lambda x: to_dict(x,["OrderId"]))
            keys = list(dic_list[0].keys())
            dic2 = dict()
            for i in range(len(dic_list)):
                for key in keys:
                    dic2[key+str(i)] = dic_list[i][key]
            dic_sum = dict(**dic,**dic2) # 合并字典
            logging.debug("dic_sum: " + message)
            message = json.dumps(dic_sum)
            return code,message

    def my_orders(self,user_id:str,token:str)-> (str,str):
        """
        0. check token 
        1. 找出所有订单
        2. 返回
        """
        code,message = User().check_token(user_id,token)
        if(code!="200"):
            return code,message
        session = create_session(self.engine)
        lines  = session.query(Orders,OrderBooks).filter(and_(Orders.UserId == user_id,Orders.OrderId==OrderBooks.OrderId)).all()
        session.close()
        if lines == None:
            logging.error("you dont't have any orders" )
            return "200","you dont't have any orders"   
        logging.debug(lines)   
        all_order = dict()
        for ord in lines:
            dic1 = to_dict(ord.Orders,dropwords=[])
            dic2 = to_dict(ord.OrderBooks,dropwords=["OrderId"])
            dic = dict(**dic1,**dic2)
            all_order[ord.Orders.OrderId] = dic
        return "200", json.dumps(all_order)

    def user_cancel_order(self,user_id,order_id,token):
        '''
        ### 步骤
        0. check_token
        1. check_user
        2. 查询order对象，判断是否存在，存在再检查status，修改status为"失败订单"
        3. 查询OrderBooks:中订单对应的所有数据以及库存
        4. 修改StoreBooks中每本书对应的库存

        ### 错误考虑：
        1. token 验证失败： code = 401, message = 
        2. user 不存在 code = 511, message = 
        3. order_id 不存在 code = 518 , message = 没有可以取消的订单
        4. status 不是已下单状态 code = 518, message = 
        @request: order_id, user_id,token
        :return:
        '''
        code,message = User().check_token(user_id,token)
        if(code!="200"):
            return code,message
        session = create_session(self.engine)
        line = session.query(Orders).filter(and_(Orders.OrderId==order_id)).first()
        if line == None:
            return error.error_invalid_order_id(order_id)
        if line.UserId!=user_id:
            return error.error_non_exist_user_id(user_id)
        if line.Status !="1":
            return error.error_order_can_not_be_cancelled(line.Status)
        
        # 修改Orders 
        session.execute(
                update(Orders).where(Orders.OrderId==order_id).values(
                {Orders.Status:"5"}))
        # Orders.Status = "5"
        logging.error("please examine here ------------------user_cancle_order")

        # 修改StoreBooks:
        store_id = line.StoreId
        booklist = session.query(StoreBooks,OrderBooks).filter(and_(StoreBooks.StoreId==store_id,StoreBooks.BookId==OrderBooks.BookId)).all() 
        for book in booklist:
            book.StoreBooks.Stock+=book.OrderBooks.Count
            session.execute(
                update(StoreBooks).where(StoreBooks.BookId==book.OrderBooks.BookId).values(
                {StoreBooks.Stock:book.StoreBooks.Stock}))
            # 可以这么玩吗》
            logging.error("please examine here ------------------user_cancle_order")
        session.commit()
        session.close()
        return error.success("cancle order")
    def auto_cancel_order(self):
        '''
        筛选所有的订单状态为1 且 时间>=deadtime 的orderid,然乎执行取消操作
        '''
        session = create_session(self.engine)
        localtime = datetime.now()
        Orderlist = session.query(Orders).filter(and_(Orders.Status==1, Orders.Deadline<localtime))
        if Orderlist ==[]:
            return error.success("no order is in state of 1")
        for line in Orderlist:
            order_id = line.OrderId
            # 修改Orders 
            session.execute(
                    update(Orders).where(Orders.OrderId==order_id).values(
                    {Orders.Status:"5"}))
            # Orders.Status = "5" # 可以这么玩吗》,可以注释掉execute吗？
            logging.error("please examine here ------------------user_cancle_order")

            # 修改StoreBooks:
            store_id = line.StoreId
            booklist = session.query(StoreBooks,OrderBooks).filter(and_(StoreBooks.StoreId==store_id,StoreBooks.BookId==OrderBooks.BookId)).all() 
            for book in booklist:
                book.StoreBooks.Stock+=book.OrderBooks.Count
                session.execute(
                    update(StoreBooks).where(StoreBooks.BookId==book.OrderBooks.BookId).values(
                    {StoreBooks.Stock:book.StoreBooks.Stock}))
                # 可以这么玩吗》,可以注释掉execute吗？
                logging.error("please examine here ------------------user_cancle_order")
                logging.debug("auto cancle orderId{}".format(book.StoreBooks.BookId))
            session.commit()
            session.close()
        return error.success("auto cancle order")


            
    


