"""
@File: prompt.py
@Date: 2024/12/10 10:00
@Desc: OpenAI提供了chat和非chat的两种API, chat:/chat/completions, 非chat: /completions
@Desc: 所以区别chat还是非chat, 判断URL接口中是否有/chat/completions, 有则是Chat的API, 否则是非Chat的API
"""
from langchain.prompts import PromptTemplate
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts.chat import SystemMessage, HumanMessagePromptTemplate

# PROMPT类型
PROMPT_TYPE = str
PROMPT_TYPE_STRING: PROMPT_TYPE = "string_prompt"
PROMPT_TYPE_CHAT: PROMPT_TYPE = "chat_prompt"


def create_string_prompt(template: str = "", **kwargs) -> BasePromptTemplate:
    """
    创建文本类Prompt
    :param template: 提示词模板
    :param kwargs:
    :return:
    """
    return PromptTemplate.from_template(template, **kwargs)


def create_chat_prompt_by_messages(messages: list = None, **kwargs) -> BasePromptTemplate:
    """
    使用消息列表, 创建聊天类Prompt
    :param messages: 消息列表
    :param kwargs:
    :return:
    """
    return ChatPromptTemplate.from_messages(
        messages,
        **kwargs
    )


def create_chat_prompt_by_system_content(prompt_system_content: str, **kwargs) -> BasePromptTemplate:
    """
    使用系统提示词, 创建聊天类prompt
    :param prompt_system_content: 系统提示词部分内容
    :param kwargs:
    :return:
    """
    # (1) 拼装messages
    messages = [
        SystemMessage(prompt_system_content),
        HumanMessagePromptTemplate.from_template("{user_input_placeholder}")
    ]
    # (2) 创建prompt实例
    return ChatPromptTemplate.from_messages(messages, **kwargs)
