import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid
from fe.access.order import Order
from fe.access.auth import Auth
from fe import conf
class TestCancelOrder:
    seller_id: str
    store_id: str
    buyer_id: str
    password:str
    buy_book_info_list: [Book]
    total_price: int
    order_id: str
    token:str
    terminal:str
    buyer: Buyer
    order: Order
    auth: Auth
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.terminal = "terminal_" + self.buyer_id
        self.password = self.seller_id
        self.auth = Auth(conf.URL)
        self.order = Order(conf.URL)

        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.token = self.auth.login(self.buyer_id, self.password, self.terminal)
        assert code ==200
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield

    def test_ok(self):
        code = self.order.user_cancel_order(self.buyer_id,self.order_id,self.token)
        assert code == 200

    def test_authorization_error(self): # 授权失败，token 
        buyer_id = self.buyer_id+"dfdf"
        code = self.order.user_cancel_order(buyer_id,self.order_id,self.token)
        assert code != 200
        

    def test_not_valid_orderid(self): # 该订单不存在
        order_id = self.order_id+"dfdf"
        code = self.order.user_cancel_order(self.buyer_id,order_id,self.token)
        assert code != 200

    def test_repeat_cancel(self):# 重复取消
        code = self.order.user_cancel_order(self.buyer_id,self.order_id,self.token)
        assert code == 200
        code = self.order.user_cancel_order(self.buyer_id,self.order_id,self.token)
        assert code !=200
    def test_can_not_cancel(self):# 已付款订单，不可取消
        code = self.buyer.payment(order_id=self.order_id)
        assert code ==200
        code = self.order.user_cancel_order(self.buyer_id,self.order_id,self.token)
        assert code !=200
    

    
