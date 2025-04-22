"""
@File: access.py
@Date: 2024/1/13 14:07
@desc: access中间件
"""
from functools import wraps
from flask import request, g
from wpylib.util.x.xjson import stringify
from wpylib.util.encry import gen_random_md5
from wpylib.util.http import get_params, get_headers
import threading
import logging


def access_middleware(func):
    """
    access_middleware中间件
    :param func: 被装饰的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        注解wrapper
        """
        # 请求参数处理
        url_params, post_params = get_params()

        # 生成Log_id
        # Log_id由上层服务生成, 比如网关为每个请求附加一个唯一的log_id
        log_id = get_headers("x-logid")
        if log_id == "":
            log_id = gen_random_md5()
        setattr(threading.local(), "wpylib_threadkey_log_id", log_id)

        # 记录日志
        logger = logging.getLogger("wpylib_logger")
        logger.info("INFO: " + stringify({
            "data": {
                "msg": "access_middleware",
                "post_params": post_params,
                "url_params": url_params,
                "url": request.url,
                "headers": request.headers,
                "log_id": log_id,
            }
        }))

        # 获取启动信息
        if "context_data" not in g:
            g.context_data = {}
        g.context_data["start_info"] = {
            "log_id": log_id
        }
        return func(*args, **kwargs)

    return wrapper
