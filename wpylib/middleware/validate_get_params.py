"""
@File: validate_get_params.py
@Date: 2024/1/13 14:07
@desc: 验证GET请求参数中间件
"""
from functools import wraps
from flask import request, g
from wpylib.util.http import resp_error


def validate_get_params_middleware(form_class):
    """
    验证GET请求参数中间件
    """

    def decorator(func):
        """
        Decorator to wrap the function with validation logic.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function to handle validation and context data injection.
            """
            form = form_class(meta={'csrf': False}, data=request.args)

            # 参数验证失败
            if not form.validate():
                # 返回错误信息
                return resp_error(msg="参数错误", code=4001)

            # 参数验证成功
            if "context_data" not in g:
                g.context_data = {}
            g.context_data["arg_info"] = form.data
            return func(*args, **kwargs)

        return wrapper

    return decorator
