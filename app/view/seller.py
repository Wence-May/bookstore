"""
* seller
* 添加新的书籍信息、添加库存、新建商铺、发货
*
"""
import logging
from flask import jsonify
from flask import Blueprint, request

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store")  # 创建商铺
def create_store():
    '''
    0. check token
    1. check user是否存在
    2. 检查store id是否存在
    3. stores创建新的一行
    @request: store_id, seller_id(user_id)
    :return:
    '''
    logging.debug("create_store has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_seller.route("/add_book")  # 添加书籍信息
def add_bookinfo():
    '''
    0. check_token
    1. 检查store_id是否存在，对应的user_id是否匹配
    2。检查库存是否大于0

   !!谁写的话，用数据库自己测试一下，34额错误数据库返回信息是否相同，如果不同可以直接插入
    3. 检查不能为空的bookinfo是否为空
    4. 检查book_id是否存在

    5. 合并tag为字符串， 以#为分隔符
    6. 插入到StoreBooks # 图片保存参考：https://blog.csdn.net/mingyuli/article/details/82853812
    7. 插入到Pictures db
    @request: user_id, store_id, book_info, stock_level
    :return:
    '''
    logging.debug("add_book has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_seller.route("/add_stock_level")  # 添加库存
def add_stock():
    '''
    0. check_token
    1. 检查add_stock_level是否大于0
    2. Stores: 检查store_id是否存在，对应的user_id是否匹配
    3. 根据book_id查询书籍对象，看是否存在，存在就更新库存
    @request: user_id, store_id, book_id, add_stock_level
    :return:
    '''
    logging.debug("add_stock has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


# 扩展接口
@bp_seller.route("/delivery_books")  # 发货
def delivery_books():
    '''
    0. check_token
    1. 查询order对象，检查order是否存在，且status==已付款
    2. 修改status为已发货

    @request: order_id (user_id, store_id)
    :return:
    '''
    logging.debug("delivery_books has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code
