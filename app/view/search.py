"""
用户可以通过关键字搜索，参数化的搜索方式；==
如搜索范围包括，题目，标签,==目录==，内容；全站搜索或是当前店铺搜索。   ==检索类别==
如果显示结果较大，==需要分页==
(使用==全文索引==优化查找)
"""
import logging
from flask import jsonify
from flask import Blueprint, request

from app.model.search import SearchMethod

bp_search = Blueprint("search", __name__, url_prefix="/search")

s = SearchMethod()


@bp_search.route("/", methods=['POST'])
def search():
    logging.debug("ordersatus has run")
    message = "messages from funcion"
    code = 222
    token = "return from function"
    return jsonify({"message": message, "token": token}), code
