# 对数据库初始化的操作
# 数据库连接时候的地址需要修改
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, DateTime, create_engine, PrimaryKeyConstraint, desc, \
    Sequence,and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, DataError
import random
import app.model.Global as Global
Base = declarative_base()

def create_session(engine):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


class Users(Base):
    __tablename__ = 'Users'
    UserId = Column(String(100), Sequence('user_id_seq'), primary_key=True)
    UserName = Column(String(10))
    HaveStore = Column(Boolean, nullable=False)
    Balance = Column(Float(precision=10, decimal_return_scale=2))
    Password = Column(String(10))
    Terminal = Column(String(10))
    Token = Column(String(100))
 


class Stores(Base):
    __tablename__ = "Stores"
    StoreId = Column(String(100), Sequence('Stores_id_seq'), primary_key=True)
    # StoreName = Column(String(10))
    UserId = Column(ForeignKey("Users.UserId"))
    Balance = Column(Float(precision=10, decimal_return_scale=2))


class StoreBooks(Base):
    #
    __tablename__ = 'StoreBooks'
    __table_args__ = (
        PrimaryKeyConstraint('BookId'),
    )
    StoreId = Column(String(100), ForeignKey("Stores.StoreId"))
    Stock = Column(Integer)
    # book info
    BookId = Column(String(100), Sequence('book_id_seq'))
    Title = Column(String(10), nullable=False)
    Author = Column(String(10))
    Publisher = Column(String(10))
    OriginalTitle = Column(String(10))
    Translator = Column(String(10))
    PubYear = Column(String(10))
    Pages = Column(Integer)
    Price = Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    Binding = Column(String(10))
    Isbn = Column(String(10))
    AuthorIntro = Column(String(10))
    BookIntro = Column(String(10))
    Content = Column(String(10))
    Tags = Column(String(500))
    PictureId = Column(String(500), ForeignKey("BookPictures.PictureId"))


class BookPictures(Base):
    __tablename__ = 'BookPictures'
    __table_args__ = (
        PrimaryKeyConstraint('PictureId'),
    )
    PictureId = Column(String(500), primary_key=True)
    BookId = Column(String(100), ForeignKey("StoreBooks.BookId"))
    Address = Column(String(100)) # 图片命名：userId + 上传时间戳
    # 图片保存参考：https://blog.csdn.net/mingyuli/article/details/82853812


class Orders(Base):
    __tablename__ = 'Orders'
    OrderId = Column(String(100), Sequence('order_id_seq'), primary_key=True)
    StoreId = Column(String(100), ForeignKey("Stores.StoreId"), nullable=False)
    UserId = Column(String(100), ForeignKey("Users.UserId"), nullable=False)
    Status = Column(String(50), nullable=False)
    Amount = Column(Integer, nullable=False)
    Deadline = Column(DateTime, nullable=False)
      
class OrderBooks(Base):
    __tablename__ = 'OrderBooks'
    __table_args__ = (
        PrimaryKeyConstraint('OrderId', "BookId"),
    )
    OrderId = Column(String(100), ForeignKey("Orders.OrderId"), primary_key=True)
    BookId = Column(String(100), ForeignKey("StoreBooks.BookId"), primary_key=True)
    Count = Column(Integer, nullable=False)
    
class UserToken(Base):
    __tablename__ = 'UserToken'
    UserId = Column(ForeignKey("Users.UserId"),primary_key = True)
    Token = Column(String(100),nullable = False )
    DeadTime = Column(DateTime,nullable = False)

if __name__ == '__main__':
    engine = create_engine(Global.DbURL)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)  # 创建所有表格
    # insert_batch(session)
    session.close()
