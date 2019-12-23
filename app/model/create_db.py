from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, DateTime, create_engine, \
    PrimaryKeyConstraint, desc, \
    Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.model.Global import DbURL

Base = declarative_base()


def create_session(engine):
    '''
    在传入的数据库engine上建立新的session
    :param engine:
    :return: new_session
    '''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


class Users(Base):
    __tablename__ = 'Users'

    UserId = Column(String(100), Sequence('user_id_seq'), primary_key=True, autoincrement=False)
    UserName = Column(String(100))
    HaveStore = Column(Boolean, nullable=False)
    Balance = Column(Float(precision=10, decimal_return_scale=2), default=0)
    Password = Column(String(100), nullable=False)
    Terminal = Column(String(100))

    def __init__(self, UserId: str, UserName: str, HaveStore: bool, Balance: float, Password: str, Terminal: str):
        self.UserId = UserId
        self.UserName = UserName
        self.HaveStore = HaveStore
        self.Balance = Balance
        self.Password = Password
        self.Terminal = Terminal


class Stores(Base):
    __tablename__ = "Stores"

    StoreId = Column(String(100), Sequence('user_id_seq'), primary_key=True)
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
    PictureId = Column(String(500))  # 删除了外键盘


class BookPictures(Base):
    __tablename__ = 'BookPictures'
    __table_args__ = (
        PrimaryKeyConstraint('PictureId', 'BookId'),
    )
    PictureId = Column(String(500), primary_key=True)
    BookId = Column(String(100), ForeignKey("StoreBooks.BookId"), primary_key=True)
    Address = Column(String(100))  # 图片命名：userId + 上传时间戳
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


if __name__ == '__main__':
    engine = create_engine(DbURL)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)  # 创建所有表格
    # insert_batch(session)
    session.close()
