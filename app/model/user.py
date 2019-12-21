from app.model.create_db import DB_operations
from app.model.create_db import Users,Orders,UserToken
from datetime import datetime
from app.model import error 
from sqlalchemy import Column, String, Integer, Boolean,ForeignKey,Float,update, create_engine, PrimaryKeyConstraint, desc,delete,and_

class User():
    # 检查token
    def check_user(self, user_id):
        '''
        检查用户是否存在
        :param user_id:
        :return:true/false
        '''
        return True

    def check_password(self,user_id, password):
        '''
        检查用户密码是否匹配
        :param user_id:
        :param password:
        :return: true/false
        '''
        return True
    def check_token(self,user_id,token):
        session = DB_operations().connnet_db()
        localtime = datetime.now()
        line  = session.query(UserToken).filter(and_(UserToken.UserId==user_id,UserToken.DeadTime<=localtime)).first()
        session.close()
        if(line.Token == token):
            return error.success("Token Authorize")
        else:
            return error.error_authorization_fail()
