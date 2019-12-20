"""
* auth
* 注册、登录、修改密码、登出、注销账号

"""
import logging
from flask import jsonify
from flask import Blueprint, request

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login")
def login():
    logging.debug("login has run")
    message = "messages from login funcion"
    code = 222
    token = "return from login function"
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/logout")
def logout():
    logging.debug("loginout has run")
    message = "messages from login funcion"
    code = 222
    token = "return from login function"
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/register")
def register():
    logging.debug("register has run")
    message = "messages from login funcion"
    code = 222
    token = "return from login function"
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    logging.debug("unregister has run")
    message = "messages from login funcion"
    code = 222
    token = "return from login function"
    #
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/password")
def change_password():
    logging.debug("changepassword has run")
    message = "messages from login funcion"
    code = 222
    token = "return from login function"
    return jsonify({"message": message, "token": token}), code
