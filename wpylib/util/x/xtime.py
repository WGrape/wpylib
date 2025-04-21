"""
@File: xtime.py
@Date: 2024/12/10 10:00
@Desc: 时间工具
"""
from datetime import datetime
import pytz
import time

# 时间格式化串
FORMAT_STR_HUMAN: str = "%Y-%m-%d %H:%M:%S"
FORMAT_STR_COMPACT: str = "%Y%m%d%H%M%S"
SECOND = 1
MINUTE = 60 * SECOND


def now_time(time_str: str = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    获取当前的时间对象(北京时区)
    :param time_str: 当前时间字符串, 如2022-10-12 12:20:30
    :param format_str: 时间格式定义
    :return 时间对象
    """
    tz = pytz.timezone('Asia/Shanghai')
    if time_str:
        return datetime.strptime(time_str, format_str).astimezone(tz)
    return datetime.now(tz)


def now_time_str(time_str: str = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取现在的时间字符串
    :param time_str: 当前时间字符串, 如2022-10-12 12:20:30
    :param format_str: 时间格式定义
    :return 时间字符串
    """
    return now_time(time_str, format_str).strftime(format_str)


def now_timestamp(time_str: str = None) -> int:
    """
    获取现在的时间戳数字
    :param time_str: 当前时间字符串, 如2022-10-12 12:20:30
    :return 时间戳
    """
    return int(datetime.timestamp(now_time(time_str)))


def now_date_str(time_str: str = None, format_str: str = "%Y-%m-%d") -> str:
    """
    获取现在的日期字符串
    :param time_str: 当前时间字符串, 如2022-10-12 12:20:30
    :param format_str: 时间格式定义
    :return 时间字符串
    """
    return now_time(time_str).strftime(format_str)


def beijing_timetuple(sec, what) -> time.struct_time:
    """
    获取北京时间的时间元组
    :return 时间元组
    """
    return now_time().timetuple()
