"""
* buyer
* 充值、下单、付款、提现、确认收货、转账到用户

"""
import logging
from flask import jsonify
from flask import Blueprint, request
from app.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")


@bp_buyer.route("/neworder")  # 下单
def neworder():
    '''
    @params: user_id,password store_id,bookdict = {"book_id":count,"book_id2":count}
    @exceptions: 余额不足，库存不足(助教给的案例没有考虑这种情况)，password 错误,user_id 未授权，store_id 未授权
    '''
    '''
    0. 检查token
    1. 检查用户是否存在
    2. 检查商店是否存在
    3. 检查书是否存在，库存是否充足，顺便计算总金额
    （45是一个事务）
    4. 减少库存
    5. Order, OrderBooks表格中新建项(新建order的时间是"当前时间+timeout时间期限"
    '''
    logging.debug("neworder has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_buyer.route("/payment")  # 付款
def payment():
    '''
    @params: user_id, money,store_id
    @exceptions: 余额不足
    '''
    '''
    0. 检查token
    1. 检查order表：看user_id、order_id是否存在且匹配； 401
    2. 检查密码
    3. 检查余额
    事务：
    4. 减少买家余额
    5. 修改order.status
    '''
    logging.debug("payment has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_buyer.route("/topup")  # 充值
def topup():
    '''
    @params: user_id , password, add_value
    '''
    '''
    1. check_password()
    2. 检查充值金额是否是整数且大于0
    3. 修改用户金额
    '''
    logging.debug("topup has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


# 下为扩展接口
@bp_buyer.route("/withdraw")  # 提现
def withdraw():
    '''
    0. check_token
    1. check_password
    2. 余额不足
    3. 减少用户balance
    @params: user_id, money, password, token
    @exceptions: 余额不足，user_id 未授权, password 不对
    '''
    logging.debug("withdraw has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code


@bp_buyer.route("/comfirm_receiption")  # 确认收货
def comfirm_receiption():
    '''
    0. check_token
    1. check order_id
    2. check_password
    3. 增加商户金额
    4. 修改orders.status为已确认收货
    @params: order_id, user_id, password
    '''
    order_id: int = 1
    logging.debug("comfirm_receiption has run")
    order_id: str = request.json.get("order_id")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    password: str = request.json.get("password")
    code,message = Buyer().comfirm_reception(user_id,order_id,token,password)
    return jsonify({"message": message}), code


@bp_buyer.route("/transfer_to_user") # 商户账户转账至拥有至拥有者账户
def transfer_to_user():
    '''
    0. check token
    1. check store_id
    2. check_password()
    3. 转账金额大于0
    4. 检查余额是否充足
    事务：
    5. 修改store.balance
    6. 修改users.balance
    @params: user_id, password, amount, store_id
    :return:
    '''

