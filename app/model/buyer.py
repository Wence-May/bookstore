# buyer 相关的功能
"""
* buyer
* 充值、下单、付款、提现、确认收货、转账到用户

"""
import app.model.Global as Global
import json 
from app.model.create_db import Users,Orders,Stores,UserToken,OrderBooks,StoreBooks,create_session
from app.model.user import UserMethod
import app.model.error as error
import logging
from datetime import datetime
from sqlalchemy import and_,update,create_engine
from sqlalchemy.orm import sessionmaker

class Buyer:
    def __init__(self):
        self.engine = create_engine(Global.DbURL)
        self.user_method = UserMethod()
    
    # 下单 
    def neworder(self,user_id,store_id,books:list,token):
        '''
        @params: user_id,store_id,books = [{"id": id_count_pair[0], "count": id_count_pair[1]},]
        @exceptions: password 错误,token错误，store_id 不存在，书不存在，库存不足，重复下单
        操作：（45是一个事务）
        4. 减少库存
        5. Order, OrderBooks表格中新建项(新建order的时间是"当前时间+timeout时间期限"
        '''
        timestr = datetime.now().strftime('%a-%b-%d-%H:%M:%S')
        order_id =store_id+user_id+timestr # order_id 的生成
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message,order_id
        try:
            session = create_session(self.engine)
            line = session.query(Stores).filter(Stores.StoreId==store_id).first()
            if line==None:
                return error.error_invalid_store_id(store_id),order_id
            if line.UserId != user_id:
                return error.error_invalid_store_id(store_id),order_id
            Amount = 0
            for book in books:
                book_id = book["id"]
                count = book["count"]
                bookline = session.query(StoreBooks).filter(StoreBooks.BookId==book_id).first()
                if bookline==None:
                    return error.error_non_exist_book_id(book_id),order_id
                elif bookline.StoreId != store_id or bookline.Stock < count:
                    return error.error_non_exist_book_id(book_id),order_id
                else:
                    Amount+=bookline.Price * count 
            #修改数据库 Orders 增加一条， OrderBooks，每个BookId 增加一条
            order = Orders(OrderId= order_id, StoreId =store_id,UserId = user_id,Status = "1", Amount= Amount,Deadline = datetime.now()+Global.order_timeout_delta)
            session.add(order)
            for book in books:
                book_id = book["id"]
                count = book["count"]
                orderbook = OrderBooks(OrderId=order_id,BookId = book_id,Count=count)
                session.add(orderbook)
            session.commit()
        except Exception as e:
            logging.error("app.model.buy.py line 64"+ e)
            session.rollback()
        finally:
            session.close()
        return error.success("neworder"),order_id


    # 付款
    def payment(self,user_id,order_id,password,token):
        '''
        @exceptions: 余额不足,token 对不上，order_id 无效，密码不对
        事务：
        4. 减少买家余额
        5. 修改order.status
        '''
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message
        try: 
            session = create_session(self.engine)
            orderline = session.query(Orders).filter(Orders.OrderId==order_id).first()
            userline = session.query(Users).filter(Users.UserId==user_id).first()
            if orderline == None :
                return error.error_invalid_order_id(order_id)
            elif orderline.OrderId != user_id or orderline.Status!="1":
                return error.error_invalid_order_id(order_id)
            elif userline.password != password:
                return error.error_authorization_fail()
            elif userline.Balance < orderline.Amount:
                return error.error_not_sufficient_funds(order_id)        
            else:   # 修改数据库
                orderline.Status = "2"
                userline.Balance-=orderline.Amount
                session.update({"Status":"2"})
                session.update({"Balance":userline.Balance})
                session.commit()
        except Exception as e:
            logging.error("app.model.Payment.py line 101"+e)
            session.rollback()
        finally:
            session.close()
        return error.success("Payment")


    # 充值
    def add_funds(self,user_id,password,add_value,token):
        '''
        @params: user_id , password, add_value
        exception: token,password,add_value>0?, 
        3. 修改用户金额
        '''
        logging.debug("topup has run")
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message
        try:
            session = create_engine(self.engine)
            line = session.query(Users).filter(Users.UserId==user_id).first()
            if line.Password==password:
                return error.error_authorization_fail()
            elif add_value<=0:
                return error.error_invalid_value(add_value)
        # 修改数据库
            line.update({"Balance":line.Balance+add_value})
            session.commit()
        except Exception as e:
            logging.error("app.model.Addfund.py line 130"+e)
            session.rollback()
        finally:
            session.close()
        return error.success("Addfund")


    # 下为扩展接口
    # 提现
    def withdraw(self,user_id, money, password, token):
        '''
        @exception: token?, password? 余额不足？
        @params: user_id, money, password, token
        减少用户balance
        '''
        logging.debug("withdraw has run")
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message
        try:
            session = create_engine(self.engine)
            line = session.query(Users).filter(Users.UserId==user_id).first()
            if line.Password==password:
                return error.error_authorization_fail()
            elif money<=0:
                return error.error_invalid_value(money)
            elif line.Balance<money:
                return error.error_not_sufficient_funds("about withdraw"+user_id)
        # 修改数据库
            line.update({"Balance":line.Balance-money})
            session.commit()
        except Exception as e:
            logging.error("app.model.withdraw.py line 161"+e)
            session.rollback()
        finally:
            session.close()       
        return error.success("withdraw")

    # 确认收货
    def comfirm_receiption(self,user_id,order_id,password,token):
        '''
        @exception: token? order_id 存在？ Orders.Status==3? password right?
        @params: order_id, user_id, password,token
        3. 增加商户金额
        4. 修改orders.status为已确认收货
        '''
        logging.debug("withdraw has run")
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message
        try:
            session = create_engine(self.engine)
            orderline = session.query(Orders).filter(Orders.OrderId==order_id).first()
            userline = session.query(Users).filter(Users.UserId==user_id).first()
            if orderline == None:
                return error.error_invalid_order_id(order_id)
            if orderline.UserId != order_id:
                return error.error_invalid_order_id(order_id)
            if userline==None:
                return error.error_exist_user_id(user_id)
            if userline.Password==password:
                return error.error_authorization_fail()
            store_id = orderline.StoreId
            storeline = session.query(Stores).filter(Stores.StoreId==store_id).first()
             # 修改数据库
            storeline.update({"Balance":storeline.Balance+orderline.Amount})
            orderline.update({"Status":"4"})
            session.commit()
        except Exception as e:
            logging.error("app.model.comfirm_receiption.py line 197"+e)
            session.rollback()
        finally:
            session.close()       
        return error.success("comfirm_receiption")       



    # 商户账户转账至拥有至拥有者账户
    def transfer_to_user(self,user_id,store_id,password,amount,token):
        '''
        @exception： token? store_id exist? password right? balance suffient?
        @params: user_id, password, amount, store_id
        事务：
        5. 修改store.balance
        6. 修改users.balance
        '''
        logging.debug("withdraw has run")
        code,message = self.user_method.check_token(user_id,token)
        if code!=200:
            return code,message
        try:
            session = create_engine(self.engine)
            userline = session.query(Users).filter(Users.UserId==user_id).first()
            storeline = session.query(Stores).filter(Stores.StoreId==store_id).first()
            if userline.Password==password:
                return error.error_authorization_fail()
            elif amount<=0:
                return error.error_invalid_value(amount)
            elif userline.Balance<amount:
                return error.error_not_sufficient_funds("about withdraw"+user_id)
            if storeline==None:
                return error.error_non_exist_store_id(store_id)
        # 修改数据库
            storeline.update({"Balance":storeline.Balance-amount})
            userline.update({"Balance":userline.Balance-amount})
            session.commit()
        except Exception as e:
            logging.error("app.model.transfer_to_user.py line 243"+e)
            session.rollback()
        finally:
            session.close()             
        return error.success("transfer_to_user")


            