"""
@File: http.py
@Date: 2024/12/10 10:00
@desc: HTTP请求工具
"""
from flask import request
from flask import jsonify
import requests

# HTTP请求方式
HTTP_METHOD_TYPE_GET: str = "get"
HTTP_METHOD_TYPE_POST: str = "post"

# 通用接口Code码
COMMON_HTTP_CODE_SUCCESS = 200
COMMON_HTTP_CODE_SYS_ERROR = 500
COMMON_HTTP_CODE_PARAMS_ERROR = 4001
COMMON_HTTP_CODE_LOGIN_AUTH_ERROR = 4002
COMMON_HTTP_CODE_MSG_MAP = {
    COMMON_HTTP_CODE_SUCCESS: "success",
    COMMON_HTTP_CODE_SYS_ERROR: "服务异常",
    COMMON_HTTP_CODE_PARAMS_ERROR: "参数校验失败",
    COMMON_HTTP_CODE_LOGIN_AUTH_ERROR: "用户未登录",
}


def get_params():
    """
    获取请求参数
    """
    post_params = {}
    url_params = request.args.to_dict()
    if request.method.lower() == HTTP_METHOD_TYPE_POST:
        if request.mimetype == "multipart/form-data":
            post_params = request.form
        elif request.mimetype == "application/json":
            post_params = request.json
    return url_params, post_params


def get_headers(header_name=""):
    """
    获取请求header
    """
    headers = request.headers
    if header_name != "":
        return headers[header_name] if header_name in headers else ""
    return headers


def requests_get(url: str, params=None, data=None, _json=None, parse_result=True, **kwargs):
    """
    使用requests库发起GET请求
    :param url: 请求地址
    :param params: 请求数据
    :param data: 请求数据, 类型为str
    :param _json: 请求数据, 类型为字典(即JSON), 即指的是一个可JSON序列化的Python对象
    :param parse_result: 是否解析结果
    :return: 返回请求结果
    """
    response = requests.get(url=url, params=params, data=data, json=_json, **kwargs)
    if response.status_code not in [0, 200]:
        raise RuntimeError(f"http code error: code={response.status_code} | response={response.text} | url={url}")

    if parse_result:
        try:
            res = response.json()
        except Exception as e:
            raise RuntimeError(f"requests_get exception: e={e}")
        return res
    return response.text


def resp_success(data):
    """
    响应成功
    :param data: 响应数据
    """
    res = {
        "code": 0,
        "data": data,
        "msg": "success",
    }
    return jsonify(res)


def resp_error(data=None, msg="操作失败", code=500):
    """
    响应错误
    """
    res = {
        "code": code,
        "data": data,
        "msg": msg,
    }
    return jsonify(res)


def resp_page_success(data_list, pg, pz, total):
    """
    返回分页数据
    :param data_list:
    :param pg:
    :param pz:
    :param total:
    :return:
    """
    return resp_success({
        'pg': pg,
        'pz': pz,
        'total': total,
        'list': data_list,
    })
