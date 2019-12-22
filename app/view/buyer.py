"""
* buyer
* 充值、下单、付款、提现、确认收货、转账到用户

"""
import logging
from flask import jsonify
from flask import Blueprint, request
from app.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")

buy = Buyer()
@bp_buyer.route("/neworder")  # 下单
def neworder():
    logging.debug("neworder has run")
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    token: str = request.headers.get("token")
    books = request.json.get("books")
    code,message,order_id = buy.neworder(user_id,order_id,books,token)
    return jsonify({"message": message, "order_id":order_id}), code


@bp_buyer.route("/payment")  # 付款
def payment():
    logging.debug("payment has run")
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    token: str = request.headers.get("token")
    code,message = buy.payment(user_id,order_id,password,token)
    return jsonify({"message": message}), code


@bp_buyer.route("/topup")  # 充值
def add_funds():
    user_id: str = request.json.get("user_id")
    password: str = request.json.get("password")
    add_value: str = request.json.get("add_value")
    token: str = request.headers.get("token")
    code,message = buy.add_funds(user_id,password,add_value,token)
    return jsonify({"message": message}), code


# 下为扩展接口
@bp_buyer.route("/withdraw")  # 提现
def withdraw():
    user_id: str = request.json.get("user_id")
    password: str = request.json.get("password")
    money: str = request.json.get("money")
    token: str = request.headers.get("token")
    code,message = buy.withdraw(user_id, money, password, token)
    return jsonify({"message": message}), code


@bp_buyer.route("/comfirm_receiption")  # 确认收货
def comfirm_receiption():
    logging.debug("comfirm_receiption has run")
    order_id: str = request.json.get("order_id")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    password: str = request.json.get("password")
    code,message =buy.comfirm_receiption(user_id,order_id,password,token)
    return code,message


@bp_buyer.route("/transfer_to_user") # 商户账户转账至拥有至拥有者账户
def transfer_to_user():
    logging.debug("comfirm_receiption has run")
    store_id: str = request.json.get("store_id")
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    password: str = request.json.get("password")
    amount: str = request.json.get("amount")
    code,message =buy.transfer_to_user(user_id,store_id,password,amount,token)
    return code,message

