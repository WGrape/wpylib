"""
@File: history.py
@Date: 2024/12/10 10:00
@desc: 第三方历史会话模块
"""
from wpylib.util.x.xtyping import is_none


def make_conversation_history(messages: list = None) -> str:
    """
    封装上下文
    :param messages: 消息记录
    :return:
    """
    conversation_history = ""
    if is_none(messages):
        messages = []
    for message in messages:
        conversation_history += f"\nUser: {message['query']}\nAssistant: {message['answer']}\n"
    return f"<ConversationHistory>{conversation_history}</ConversationHistory>"
