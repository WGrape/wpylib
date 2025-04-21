"""
@File: logger.py
@Date: 2024/12/10 10:00
@Desc: 第三方logger单例模块
"""
from wpylib.util.x.xjson import convert_to_jsonable
from wpylib.util.storage import create_directory, is_directory_exist
from wpylib.util.x.xtime import now_timestamp, now_time_str, now_date_str, beijing_timetuple
import traceback
import threading
import logging
import inspect
import json
import sys


class Logger:
    """
    二次封装的Logger日志类
    """
    # 初始化需要的配置
    _logger_config: dict
    _global_config: dict

    # 原生logger实例
    _instance_logger: logging.Logger

    # Logger类的单例
    _singleton = None

    def __new__(cls, *args, **kwargs):
        # 在初始化Logger类的时候, 确保仅存在一个单例
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, logger_config: dict, global_config: dict):
        if "level" not in logger_config:
            logger_config["level"] = "info"
        if "log_format" not in logger_config:
            logger_config["log_format"] = '%(asctime)s - %(message)s'
        self._logger_config = logger_config

        if "global_base_dir" not in global_config:
            global_config["global_base_dir"] = "./"
        if "project" not in global_config:
            global_config["project"] = ""
        if "business" not in global_config:
            global_config["business"] = ""
        self._global_config = global_config

        self._init()

    def _init(self):
        """
        初始化Logger
        """
        # 日志初始配置
        date = now_date_str(None, "%Y%m%d")
        logging.Formatter.converter = beijing_timetuple

        # 设置全局日志级别, 日志优先级为 ERROR > INFO > DEBUG
        # 由于INFO日志优先级高于DEBUG，INFO级别的消息会被INFO和DEBUG处理器处理
        level = _get_level_num(self._logger_config["level"].upper())
        logging.basicConfig(
            level=level, stream=sys.stdout
        )

        # 创建主logger对象
        self._instance_logger = logging.getLogger('my_logger')
        self._instance_logger.propagate = False  # 禁止传播日志到根记录器, 必须有这个设置, 不然会有多个重复的打印

        # 获取langfuse日志对象
        langfuse_logger = logging.getLogger('langfuse')

        global_base_dir = self._global_config["global_base_dir"]
        log_dir = f"{global_base_dir}/logs"
        if not is_directory_exist(log_dir):
            create_directory(log_dir)

        # 创建不同日志级别的日志处理器和设置格式, 并添加到Logger对象
        for x_level in ["info", "error", "warning", "debug"]:
            log_file = f"{global_base_dir}/logs/{x_level}.{date}.log"
            handler = logging.FileHandler(log_file, encoding="utf-8")
            handler.setLevel(_get_level_num(x_level))
            handler.setFormatter(logging.Formatter(self._logger_config["log_format"]))
            self._instance_logger.addHandler(handler)
            langfuse_logger.addHandler(handler)

    def _log(self, level: int, msg: str, biz_data: dict, frame_data: dict):
        """
        内部底层写日志入口
        :param level: 日志级别
        :param msg: 消息内容
        :param biz_data: 业务数据
        :param frame_data: 框架数据
        """
        log_id = ""
        user_id = ""
        try:
            thread_local = threading.local()
            log_id = getattr(thread_local, "wpylib_threadkey_log_id")
            user_id = getattr(thread_local, "wpylib_threadkey_user_id")
        except Exception as e:
            ...

        # 日志模板
        template = convert_to_jsonable({
            # 业务信息
            "level": _get_level_text(level),
            "msg": msg,
            "log_id": log_id,
            "user_id": user_id,
            "data": biz_data,
            "project": self._global_config["project"],
            "business": self._global_config["business"],
            # 框架信息
            "thread_id": threading.current_thread().ident,
            "module": frame_data["module"] if "module" in frame_data else None,
            "caller": frame_data["caller"] if "caller" in frame_data else None,
            "client_ip": frame_data["client_ip"] if "client_ip" in frame_data else "127.0.0.1",
            "sysarg": sys.argv,
            # 时间信息
            "timestamp": now_timestamp(),
            "datetime": now_time_str(),
        })

        # 根据日志级别处理
        if level == logging.ERROR:
            # 封装日志模板信息
            template["traceback_info"] = traceback.format_exc()
            if template["traceback_info"] == "NoneType: None\n":
                template["traceback_info"] = ""
            template_string = f"ERROR: {json.dumps(template, ensure_ascii=False)}"

            # 记录ERROR记录
            self._instance_logger.error(template_string)

            # 自动在INFO日志中也冗余一份, 方便查询
            self._instance_logger.info(template_string)
        elif level == logging.INFO:
            # 封装日志模板信息
            template_string = f"INFO: {json.dumps(template, ensure_ascii=False)}"

            # 记录INFo日志
            self._instance_logger.info(template_string)
        else:
            raise RuntimeError(f"unknown log level")

        # 同步在输出缓存区
        print(template_string)

    def log_info(self, msg: str, biz_data: dict = None, frame_data: dict = None):
        """
        直接打印INFo级别日志
        :param msg: 消息内容
        :param biz_data: 业务数据字典结构
        :param frame_data: 框架数据
        """
        if biz_data is None:
            biz_data = {}
        if frame_data is None:
            frame_data = {}
        frame_data["module"] = _get_module(inspect.currentframe())
        frame_data["caller"] = _get_caller(inspect.stack())
        self._log(logging.INFO, f"[log_info]: {msg}", biz_data, frame_data)

    def log_error(self, msg: str, biz_data: dict = None, frame_data: dict = None):
        """
        直接打印ERROR级别日志
        :param msg: 消息内容
        :param biz_data: 业务数据字典结构
        :param frame_data: 框架数据
        """
        if biz_data is None:
            biz_data = {}
        if frame_data is None:
            frame_data = {}
        frame_data["module"] = _get_module(inspect.currentframe())
        frame_data["caller"] = _get_caller(inspect.stack())
        self._log(logging.ERROR, f"[log_error]: {msg}", biz_data, frame_data)


def _get_module(currentframe) -> str:
    """
    获取当前的module模块名
    :param currentframe: 当前帧
    :return: 返回模块名
    """
    try:
        return inspect.getmodule(currentframe).__name__
    except Exception as e:
        # 可能获取不到, 返回空即可, 不需要抛出异常
        return ""


def _get_caller(stack_list: list) -> str:
    """
    获取调用栈
    :param stack_list: 调用栈
    :return: 返回调用栈信息字符串
    """
    if len(stack_list) <= 1:
        return ""

    stack_2th = stack_list[1]
    if len(stack_2th) <= 3:
        return ""

    file = stack_2th[1]
    line = stack_2th[2]
    func = stack_2th[3]
    return f"{file}=>{line}=>{func}"


def _get_level_text(level: int) -> str:
    """
    获取日志级别(数字)所对应的字符串
    :param level: 日志级别(数字)
    :return: 返回日志级别(数字)所对应的字符串
    """
    level_text_map: dict = {
        logging.ERROR: "ERROR",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.DEBUG: "DEBUG",
    }
    return level_text_map[level]


def _get_level_num(text: str) -> int:
    """
    获取日志级别(字符串)所对应的数字值
    :param text: 日志级别(字符串)
    :return: 返回日志级别(字符串)所对应的数字值
    """
    level_num_map: dict = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "DEBUG": logging.DEBUG,
    }
    return level_num_map[text.upper()]
