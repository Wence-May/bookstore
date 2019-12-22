import logging
from flask import jsonify
from flask import Blueprint, request
from app.model.order import Order
bp_order = Blueprint("order", __name__, url_prefix="/order")
order = Order()
# 查询订单状态，查看历史订单，用户取消订单，自动取消订单
'''
注明
'''
@bp_order.route("/order_status")  # 用户查询历史订单状态
def order_status():
    '''
    0. check_token
    1. 查询订单是否存在，存在获取相关信息
    如果token 验证失败  code = 401,  message =  
    如果订单不存在 code =  518, message = 
    @request: order_id, token ,user_id
    :return:
    '''
    logging.debug("ordersatus has run")
    order_id: str = request.json.get("order_id")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    code,message = order.order_status(user_id,order_id,token)
    return jsonify({"message": message}), code


@bp_order.route("/my_orders")  # 查询买家所有历史订单
def my_orders():
    '''
    0. check_token
    1. check_users检查用户是否存在
    2. 查找历史订单（频率比较低，不建立索引也可以）

    错误考虑：
    如果token 验证失败  code = 401,  message =  
    如果user_id 不存在 code = 401, message = 
    考虑分页显示
    @request: user_id
    :return:
    '''
    logging.debug("myorder has run")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    code,message = order.my_orders(user_id,token)
    return jsonify({"message": message}), code

@bp_order.route("/user_cancel_order")  # 用户取消订单
def user_cancel_order():
    '''
    0. check_token
    1. check_user
    2. 查询order对象，判断是否存在，存在再检查status，修改status为"失败订单"
    3. 查询OrderBooks:中订单对应的所有数据以及库存
    4. 修改StoreBooks中每本书对应的库存

    # c错误考虑：
    1. token 验证失败： code = 401, message = 
    2. user 不存在 code = 511, message = 
    3. order_id 不存在 code = 518 , message = 没有可以取消的订单
    4. status 不是已下单状态 code = 518, message = 
    @request: order_id, user_id,token
    :return:
    '''
    logging.debug("user_cancel_order has run")
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    token: str = request.headers.get("token")
    code,message = order.user_cancel_order(user_id,order_id,token)
    return jsonify({"message": message}), code


# @bp_order.route("/auto_cancel_order")  # 自动取消订单
def auto_cancel_order():
    '''
    实现过程是，每隔一段时间访问 Order表，选出已下单状态且已经到达可以取消订单时间的元组，对于每个元组调用取消改订单的函数
    :return:
    '''
    logging.debug("auto_cancel_order has run")
    code,message = order.auto_cancel_order()
    return code,message


