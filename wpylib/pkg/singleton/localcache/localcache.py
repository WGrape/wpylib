"""
@File: localcache.py
@Date: 2024/12/10 10:00
@Desc: 第三方本地缓存单例模块
"""
from typing import Any
from wpylib.util.x.xtyping import is_none
import threading


class Localcache:
    """
    Localcache本地缓存类
    """
    # 本地线程存储
    _thread_local: Any

    # 单例类
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self):
        self._thread_local = threading.local()

    def set_thread_local(self, key: Any, value: Any):
        """
        设置thread_local的Key-Value对
        :param key: 缓存的Key
        :param value: 缓存的值
        :return:
        """
        setattr(self._thread_local, key, value)

    def get_thread_local(self, key: Any) -> Any:
        """
        根据Key获取thread_local的Value
        :param key: 缓存的Key
        :return:
        """
        try:
            return getattr(self._thread_local, key)
        except Exception as e:
            return None

    def set_log_id(self, value: str):
        """
        设置log_id, log_id是程序运行过程中分配的唯一日志ID
        :param value: log_id的值
        :return:
        """
        key = "wpylib_threadkey_log_id"
        self.set_thread_local(key, value)

    def get_log_id(self) -> str:
        """
        获取log_idd的值
        :return:
        """
        key = "wpylib_threadkey_log_id"
        log_id = self.get_thread_local(key)
        if is_none(log_id):
            log_id = ""
        return log_id

    def set_user_id(self, value: int):
        """
        设置user_id
        :param value: user_id的值
        :return:
        """
        key = "wpylib_threadkey_user_id"
        self.set_thread_local(key, value)

    def get_user_id(self) -> int:
        """
        获取user_id
        :return: 返回user_id
        """
        key = "wpylib_threadkey_user_id"
        user_id = self.get_thread_local(key)
        if is_none(user_id):
            user_id = 0
        return user_id

