import datetime
import time
import jwt
import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError

from app.model.create_db import Users, create_session
from app.model.Global import DbURL, SECRET_KEY
import app.model.error as error


class UsersMethod():
    def __init__(self):
        self.engine = create_engine(DbURL)

    def _encode_token(self, user_id: str, terminal: str):
        """
        生成认证Token
        :param user_id: 数据库中的if
        :param terminal: terminal_{登陆时间}
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 签发时间
                'iss': 'ken',  # 签发人
                'data': {
                    'id': user_id,
                    'terminal': terminal
                }
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            ).decode("utf-8")
        except Exception as e:
            logging.error(str(e))
            return e

    def _decode_token(self, token: str) -> (bool, object):
        """
        验证Token
        :param token
        :return: bool
        """
        data = {"user_id": "", "terminal": ""}
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            payload = jwt.decode(token, SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data'] and 'terminal' in payload['data']:
                logging.debug("in _decode_token: not in")
                data['user_id'] = payload['data']['id']
                data['terminal'] = payload['data']['terminal']
                return True, data
            else:
                logging.debug("1" + str(jwt.InvalidTokenError))
                return False, jwt.InvalidTokenError
        except jwt.ExpiredSignatureError as e:
            logging.debug("2" + str(e))
            return False, jwt.ExpiredSignatureError
        except jwt.InvalidTokenError as e:
            logging.debug("3" + str(e))
            return False, jwt.InvalidTokenError

    def register(self, user_id: str, password: str):
        try:
            session = create_session(self.engine)
            terminal = "terminal_{}".format(str(time.time()))
            new_user = Users(UserId=user_id, Password=password, UserName=user_id, HaveStore=False, Balance=0,
                             Terminal=terminal)
            session.add(new_user)
            session.commit()
            return 200, "ok"
        except DatabaseError:
            session.rollback()
            return error.error_exist_user_id(user_id)
        finally:
            session.close()

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = "invalid token"
        try:
            session = create_session(self.engine)
            # 检查密码和用户名是否匹配
            code, message = self.check_password(user_id, password)
            if code != 200:
                print("in login: after check_password ")
                return code, message, token

            token = self._encode_token(user_id, terminal)
            cursor = session.query(Users).filter(Users.UserId == user_id).filter(Users.Password == password).all()
            if len(cursor) == 0:
                print(" in login: found no user")
                return error.error_authorization_fail(), token

            # 登陆成功时将登陆时间写入数据库
            row = cursor[0]
            row.Terminal = terminal
            session.commit()
            return 200, "ok", token
            # return 200, "ok", "fake token"
        except DatabaseError:
            print("in login: exception")
            return error.error_authorization_fail(), token
        finally:
            session.close()

    def change_password(self, user_id: str, old_password: str, new_password: str) -> (int, str):
        try:
            session = create_session(self.engine)
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            cursor = session.query(Users).filter(Users.UserId == user_id).filter(Users.Password == old_password).all()
            if len(cursor) == 0:
                return error.error_authorization_fail()

            row = cursor[0]
            row.Password = new_password
            session.commit()
            return 200, "ok"
        except DatabaseError:
            return error.error_authorization_fail()
        finally:
            session.close()

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            session = create_session(self.engine)
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            rowcount = session.query(Users).filter(Users.UserId == user_id). \
                filter(Users.Password == password). \
                delete(synchronize_session=False)
            if rowcount != 1:
                return error.error_authorization_fail()
            session.commit()
            return 200, "ok"
        except DatabaseError:
            return error.error_authorization_fail()
        finally:
            session.close()

    def logout(self, user_id: str, token: str):
        # code, message = u.logout(user_id, token)
        try:
            code, message = self.check_token(token, user_id)
            if code != 200:
                print("logout: error check_token")
                return code, message
            session = create_session(self.engine)
            cursor = session.query(Users).filter(Users.UserId == user_id).all()
            cursor[0].Terminal = str(time.time())
            session.commit()
            return 200, "ok"
        except DatabaseError:
            print("logout: error database error")
            return error.error_authorization_fail()

    def check_token(self, token: str, user_id: str) -> (int, str):
        if token is None:
            return error.error_authorization_fail()

        ok, data = self._decode_token(token)
        if not ok:
            logging.debug("decode token error")
            return error.error_authorization_fail()

        if user_id != data['user_id']:
            logging.debug("user_id not match")
            return error.error_authorization_fail()

        session = create_session(self.engine)
        cursor = session.query(Users).filter(Users.UserId == user_id).filter(Users.Terminal == data['terminal']).all()
        if len(cursor) == 0:
            logging.debug("user not exist")
            return error.error_non_exist_user_id(user_id)
        session.close()
        return 200, "ok"

    def check_password(self, user_id, password):
        '''
        检查用户密码是否匹配
        :param user_id:
        :param password:
        :return: true/false
        '''
        session = create_session(self.engine)
        cursor = session.query(Users).filter(Users.UserId == user_id).all()  # query.all() returns a list
        if len(cursor) == 0:
            return error.error_non_exist_user_id(user_id)

        row = cursor[0]
        if row.Password != password:
            print("In check password")
            return error.error_authorization_fail()

        return 200, "ok"
