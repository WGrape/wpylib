"""
@File: flask.py
@Date: 2024/12/10 10:00
@desc: 第三方flask单例模块
"""
from flask_cors import CORS
from flask.app import Flask as OfficialFlaskApp


class Flask:
    """
    二次封装的Flask类
    """
    # flask的app实例
    _instance_app: OfficialFlaskApp

    # Flask类的单例
    _singleton = None

    def __new__(cls, *args, **kwargs):
        # 在初始化Flask类的时候, 确保仅存在一个单例
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, app_name: str):
        self._instance_app = OfficialFlaskApp(app_name)
        # 启用CORS，允许所有来源的跨域请求
        CORS(self._instance_app, supports_credentials=True)

    def get_instance_app(self):
        """
        返回flask的app实例
        :return:
        """
        return self._instance_app
