"""
@File: xtyping.py
@Date: 2024/12/10 10:00
@desc: 类型工具
"""


def is_none(data):
    """
    数据是否是None
    :param data: 数据
    :return 是否为None
    """
    if data is None:
        return True
    return False


def is_not_none(data):
    """
    数据是否不是None
    :param data: 数据
    :return 是否不为None
    """
    return is_none(data) is False
