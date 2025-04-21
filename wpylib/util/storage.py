"""
@File: storage.py
@Date: 2024/12/10 10:00
@desc: 本地存储工具
"""
import os


def is_file_exist(file) -> bool:
    """
    文件是否存在
    :param file: 文件路径
    :return 返回文件是否存在
    """
    return os.path.exists(file)


def is_directory_exist(directory: str) -> bool:
    """
    目录是否存在
    :param directory: 目录
    :return 返回目录是否存在
    """
    return os.path.exists(directory)


def create_directory(directory: str):
    """
    创建目录
    :param directory: 目录
    """
    os.mkdir(directory)
