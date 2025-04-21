"""
@File: cmd.py
@Date: 2024/12/10 10:00
@desc: 命令行工具
"""
import sys


def args_to_dict():
    """
    将系统参数转为KV结构的kwargs
    """
    if len(sys.argv) <= 1:
        return []

    kwargs = {}
    for arg in sys.argv[0:]:
        chunks = arg.split("=")
        if len(chunks) < 2:
            continue

        pieces = chunks[0].split("--")
        if len(pieces) < 2:
            continue

        k = pieces[1]
        v = chunks[1]
        kwargs[k] = v
    return kwargs
