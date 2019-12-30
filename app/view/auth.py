"""
* auth
* 注册、登录、修改密码、登出、注销账号

"""
import logging
from flask import jsonify
from flask import Blueprint, request
from app.model.user import UserMethod

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")
u = UserMethod()


@bp_auth.route("/register", methods=['POST'])
def register():
    '''
    @request:{
        "user_id":"$user name$",
        "password":"$user password$"
    }
    '''
    logging.debug("register has run")
    user_id = request.json['user_id']
    password = request.json['password']
    code, message = u.register(user_id, password)
    return jsonify({"message": message}), code


@bp_auth.route("/login", methods=["POST"])
def login():
    '''
    @request:{
        "user_id":"$user name$",
        "password":"$user password$",
        "terminal":"$terminal code$"
    }
    :return:
    '''
    logging.debug("login has run")
    logging.debug(request)
    user_id = request.json['user_id']
    password = request.json['password']
    terminal = request.json['terminal']
    code, message, token = u.login(user_id, password, terminal)
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/password", methods=['POST'])
def change_password():
    '''
    @request:{
        "user_id":"$user name$",
        "oldPassword":"$old password$",
        "newPassword":"$new password$"
    }
    '''
    logging.debug("login has run")
    user_id = request.json['user_id']
    old_password = request.json['oldPassword']
    new_password = request.json['newPassword']
    code, message = u.change_password(user_id, old_password, new_password)
    return jsonify({"message": message}), code


@bp_auth.route("/logout", methods=['POST'])
def logout():
    '''
    @request:
    {
        "user_id":"$user name$"
    }
    '''
    logging.debug("loginout has run")
    user_id = request.json['user_id']
    token = request.headers.get("token")
    code, message = u.logout(user_id, token)
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    '''
    @request:{
        "user_id":"$user name$",
        "password":"$user password$"
    }
    '''
    logging.debug("unregister has run")
    user_id = request.json['user_id']
    password = request.json['password']
    code, message = u.unregister(user_id, password)
    return jsonify({"message": message}), code



