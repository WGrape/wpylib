"""
@File: xjson.py
@Date: 2024/12/10 10:00
@Desc: JSON工具
"""
import json
import re


def _remove_markdown_of_json(raw_json: str):
    """
    去除markdown的JSON标签
    :param raw_json: 原JSON
    :return: 返回去除后的字符串
    """
    raw_json = raw_json.replace("```json", '')
    raw_json = raw_json.replace("```JSON", '')
    raw_json = raw_json.replace("```", '')
    return raw_json


def parse(raw_json: str, support_markdown: bool = True) -> (bool, dict):
    """
    解析数据为JSON
    :param raw_json: json字符串
    :param support_markdown: 是否支持markdown
    :return 返回是否解析成功以及解析后的JSON字典
    """
    # 如果支持markdown
    if support_markdown:
        raw_json = _remove_markdown_of_json(raw_json)

    # 直接尝试JSON解析
    try:
        data = json.loads(raw_json)
        return True, data
    except Exception as e:
        return False, None


def parse_raise(raw_json: str, support_markdown: bool = True) -> dict:
    """
    解析数据为JSON, 如果解析失败则直接抛出异常
    :param raw_json: json字符串
    :param support_markdown: 是否支持markdown
    :return 返回解析后的JSON字典
    """
    # 如果支持markdown
    if support_markdown:
        raw_json = _remove_markdown_of_json(raw_json)

    # 直接尝试JSON解析
    try:
        data = json.loads(raw_json)
        return data
    except Exception as e:
        raise RuntimeError(e)


def convert_to_jsonable(data):
    """
    强制转换为一定可以JSON编码的数据
    比如一个dict中如果有time、对象等原生类型, 那么是不可以被JSON编码的
    所以这个函数会递归遍历每一个属性, 只要不是JSON可以编码和解析的, 就会使用str强制转换
    :param data: 原数据
    :return: 返回处理后的数据
    """
    if isinstance(data, dict):
        return {k: convert_to_jsonable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_jsonable(item) for item in data]
    elif not isinstance(data, (int, float, str, bool, type(None))):
        # 对于非基本类型，尝试将其转换为字符串
        return str(data)
    else:
        return data


def stringify(data) -> str:
    """
    编码为JSON
    :param data: 被编码的数据
    :return string
    """
    return json.dumps(convert_to_jsonable(data), ensure_ascii=False)


def extract_first_json(text: str) -> dict:
    """
    提取字符串中的第一个```json```代码块内的JSON内容
    :param text: 原字符串
    :return: 返回解析后的JSON字典
    """
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)

    if match:
        json_content = match.group(1)
        return parse_raise(json_content)
    return {}
