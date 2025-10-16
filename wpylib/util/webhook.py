"""
@File: webhook.py
@Date: 2024/1/13 14:07
"""
from wpylib.util.http import post


def send_to_group_robot(msg: str, key: str, at_user_list: list = None, msg_type: str = "text", channel: str = "feishu"):
    """
    通过群机器人将消息发送到飞书群
    :param msg: 消息内容
    :param key: key 是群机器人 webhook 地址
    :param at_user_list: @的人员列表, 飞书使用用户的 openid
    :param msg_type: 消息类型, 支持text, 飞书markdown格式支持较少，也不支持颜色，比较难用，这里不推荐使用, 颜色可以考虑使用emoji来代替
    :param channel: 通道
    doc: https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
    """
    if msg_type != "text":
        print(f"send_to_feishu_group_robot failed: error msg_type({msg_type})")
        return False

    if at_user_list is None:
        at_user_list = []  # ["7246358855863599106"]
    if key.startswith("http"):
        url = key
    else:
        url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"

    for au in at_user_list:
        msg += f" <at user_id=\"{au}\"></at>"

    # TODO 添加重试功能
    try:
        data = {
            "msg_type": "text",
            "content": {
                "text": f"[AI-ARCH] {msg}",
            }
        }
        return post(url, data)
    except Exception as e:
        print(f"send_to_group_robot error: {e!r}")
        return False
