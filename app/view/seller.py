"""
* seller
* 添加新的书籍信息、添加库存、新建商铺、发货
*
"""
import logging
from flask import jsonify
from flask import Blueprint, request
from app.model.seller import Seller
bp_seller = Blueprint("seller", __name__, url_prefix="/seller")
seller = Seller()

@bp_seller.route("/create_store", methods=["POST"])  # 创建商铺
def create_store():
    store_id = request.json.get("store_id")
    user_id  = request.json.get("user_id")
    token = request.headers.get("token")
    code,message = seller.create_store( user_id,store_id,token)
    return jsonify({"message": message}), code

@bp_seller.route("/add_book", methods=["POST"])  # 添加书籍信息
def add_bookinfo():
    logging.debug("add_book has run")
    store_id = request.json.get("store_id")
    user_id  = request.json.get("user_id")
    book_info  = request.json.get("book_info")
    stock_level = request.json.get("stock_level")
    token = request.headers.get("token")
    code,message = seller.add_bookinfo(user_id, store_id,book_info,stock_level,token)
    return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=["POST"])  # 添加库存
def add_stock():
    logging.debug("add_stock has run")
    store_id = request.json.get("store_id")
    user_id  = request.json.get("user_id")
    book_id  = request.json.get("book_id")
    add_stock_level = request.json.get("add_stock_level")
    token = request.headers.get("token")
    code,message = seller.add_stock(user_id,store_id,book_id,add_stock_level,token)
    return jsonify({"message": message}), code



# 扩展接口
@bp_seller.route("/delivery_books", methods=["POST"])  # 发货
def delivery_books():
    '''
    0. check_token， 授权失败
    1. 该订单不存在，该订单还未付款，该订单已被取消，该订单已经发货，
    2. 修改status为已发货

    @request: order_id (user_id, store_id)
    :return:
    '''
    logging.debug("delivery_books has run")
    order_id: str = request.json.get("order_id")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    code,message = seller.delivery_books(user_id,order_id,token)
    return jsonify({"message": message}), code
