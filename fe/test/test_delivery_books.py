import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from fe.access.seller import Seller
import uuid


class TestDeliveryBooks:
    seller_id: str
    store_id: str
    buyer_id: str
    password:str
    buy_book_info_list: [Book]
    total_price: int
    order_id: str
    buyer: Buyer
    seller: Seller

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200

        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code ==200
        # code = self.buyer.payment(self.order_id)
        # assert code ==200
        yield

    def test_ok(self):
        code = self.buyer.payment(self.order_id)
        assert code ==200
        code = self.seller.delivery_books(self.seller_id, self.order_id)
        assert code == 200

    def test_authorization_error(self): # token 和user_id 验证失败
        code = self.buyer.payment(self.order_id)
        assert code ==200
        seller_id = self.seller_id+"[[[[[]]]]]"
        code = self.seller.delivery_books(seller_id,self.order_id)
        assert code != 200
    def test_unpayed_order(self): # 未付款订单不能发货
        code = self.seller.delivery_books(self.seller_id,self.order_id)
        assert code != 200
    def test_no_this_order(self): # 不存在这个订单
        code = self.buyer.payment(self.order_id)
        assert code ==200
        order_id = self.order_id + "[[dkdkdk]]"
        code = self.seller.delivery_books(self.seller_id,order_id)
        assert code != 200
    def test_not_right_state(self): # 已完成订单不能发货
        code = self.buyer.payment(self.order_id)
        assert code ==200
        code = self.seller.delivery_books(self.seller_id,self.order_id)
        assert code == 200
        code = self.buyer.comfirm_reception(self.buyer_id,self.order_id,self.password)
        assert code == 200
        code = self.seller.delivery_books(self.seller_id,self.order_id)
        assert code != 200

    def test_repeat_delivery(self): # 已经发货订单不能发货
        code = self.buyer.payment(self.order_id)
        assert code ==200
        code = self.seller.delivery_books(self.seller_id,self.order_id)
        assert code == 200
        code = self.seller.delivery_books(self.seller_id,self.order_id)
        assert code != 200
