"""
@File: validate_post_params.py
@Date: 2024/1/13 14:07
@desc: 验证POST请求参数中间件
"""
from functools import wraps
from flask import request, g
from wpylib.util.http import resp_error, get_params


def validate_post_params_middleware(form_class):
    """
    验证参数
    """

    def decorator(func):
        """
        注解
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            wrapper
            """
            # 获取URL和请求参数
            url_params, post_params = get_params()
            form = form_class(meta={'csrf': False}, data=post_params)

            # 参数验证失败
            if not form.validate():
                # 返回错误信息
                return resp_error(msg="参数错误", code=4001)

            # 参数验证成功
            if "context_data" not in g:
                g.context_data = {}
            g.context_data["form_info"] = form.data
            return func(*args, **kwargs)

        return wrapper

    return decorator
