import logging
from flask import jsonify
from flask import Blueprint, request

bp_order = Blueprint("order", __name__, url_prefix="/order")

# 查询订单状态，查看历史订单，用户取消订单，自动取消订单
'''
注明
'''

@bp_order.route("/order_status")  # 用户查询历史订单状态
def order_status():
    '''
    0. check_token
    1. 查询订单是否存在，存在获取相关信息
    @request: order_id
    :return:
    '''
    logging.debug("ordersatus has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_order.route("/my_orders")  # 查询所有历史订单
def my_orders():
    '''
    0. check_token
    1. check_users检查用户是否存在
    2. 查找历史订单（频率比较低，不建立索引也可以）
    @request: user_id
    :return:
    '''
    logging.debug("ordersatus has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_order.route("/user_cancel_order")  # 用户取消订单
def user_cancel_order():
    '''
    0. check_token
    1. check_user
    2. 查询order对象，判断是否存在，存在再检查status，修改status为"失败订单"
    3. 查询OrderBooks:中订单对应的所有数据以及库存
    4. 修改StoreBooks中每本书对应的库存
    @request: order_id, user_id
    :return:
    '''
    logging.debug("user_cancel_order has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_order.route("/auto_cancel_order")  # 自动取消订单
def atuo_cancel_order():
    '''

    :return:
    '''
    logging.debug("auto_cancel_order has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


