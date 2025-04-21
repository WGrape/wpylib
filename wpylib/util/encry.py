"""
@File: encry.py
@Date: 2024/12/10 10:00
@desc: 编码加密工具
"""
import uuid
import hashlib


def sha1(input_string: str) -> str:
    """
    sha1加密
    :param input_string: 输入的字符串
    :return: 返回使用sha1算法计算后的加密字符串
    """
    # 创建sha1哈希函数对象
    sha1_hash_func = hashlib.sha1()

    # 计算输入字符串的哈希值
    sha1_hash_func.update(input_string.encode('utf-8'))

    # 获取哈希值的十六进制值
    hashed_string = sha1_hash_func.hexdigest()

    # 返回十六进制的哈希值作为计算后的加密字符串
    return hashed_string


def gen_random_md5(node=0x87654321) -> str:
    """
    生成随机md5字符串
    :param node: 使用uuid1生成唯一ID时的节点信息
    :return: 返回生成的md5字符串
    """
    log_id = uuid.uuid1(node)
    return log_id.hex.replace('-', '')
