"""
@File: chain.py
@Date: 2024/12/10 10:00
@desc: 第三方chain模块
"""
from langchain import LLMChain
from langfuse.callback import CallbackHandler
from wpylib.pkg.langchain.log_callback import LogCallback
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.language_models.base import BaseLanguageModel


def make_chain_callbacks(langfuse_config: dict, log_id: str = "") -> list:
    """
    获取回调函数
    :param langfuse_config: langfuse配置
    :param log_id: 日志追踪ID
    :return: 返回回答函数列表
    """
    if "secret_key" not in langfuse_config:
        langfuse_config["secret_key"] = ""
    if "public_key" not in langfuse_config:
        langfuse_config["public_key"] = ""
    if "host" not in langfuse_config:
        langfuse_config["host"] = ""
    if "trace_name" not in langfuse_config:
        langfuse_config["trace_name"] = ""
    if "tags" not in langfuse_config:
        langfuse_config["tags"] = []

    callbacks = [
        CallbackHandler(
            secret_key=langfuse_config["secret_key"],
            public_key=langfuse_config["public_key"],
            host=langfuse_config["host"],
            debug=False,
            session_id=log_id,
            trace_name=langfuse_config["trace_name"],
            tags=langfuse_config["tags"],
        )
    ]
    return callbacks


def create_chain(model: BaseLanguageModel, prompt: BasePromptTemplate, verbose: bool = False) -> LLMChain:
    """
    创建chain
    chain.invoke(*args, config={"callbacks": get_callbacks()}, **kwargs)
    chain.predict(*args, callbacks=get_callbacks(), **kwargs)
    chain.apredict(*args, callbacks=get_callbacks(), **kwargs)
    :param model: 模型
    :param prompt: 提示词
    :param verbose: 是否开启打印
    :return:
    """
    return LLMChain(
        llm=model,
        prompt=prompt,
        verbose=verbose,
        callbacks=[LogCallback()]
    )
