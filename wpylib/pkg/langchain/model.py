"""
@File: model.py
@Date: 2024/12/10 10:00
@desc: 第三方model单例模块
"""
from typing import Any, Optional, Iterator
from langchain_openai import OpenAI, AzureOpenAI
from langchain_core.runnables.utils import Input, Output
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langchain_core.language_models.base import BaseLanguageModel
from langchain_community.chat_models import ChatZhipuAI, ChatBaichuan

# 角色
MODEL_ROLE_SYSTEM = "SYSTEM"
MODEL_ROLE_HUMAN = "HUMAN"
MODEL_ROLE_AI = "AI"

# MODEL类型
MODEL_TYPE = str
MODEL_TYPE_OPENAI_STRING: MODEL_TYPE = "model_type_openai_string"
MODEL_TYPE_OPENAI_CHAT: MODEL_TYPE = "model_type_openai_chat"
MODEL_TYPE_AZURE_STRING: MODEL_TYPE = "model_type_azure_string"
MODEL_TYPE_AZURE_CHAT: MODEL_TYPE = "model_type_azure_chat"
MODEL_TYPE_ZHIPU_CHAT: MODEL_TYPE = "model_type_zhipu_chat"
MODEL_TYPE_BAICHUAN_CHAT: MODEL_TYPE = "model_type_baichuan_chat"
MODEL_TYPE_DOUBAO_CHAT: MODEL_TYPE = "model_type_doubao_chat"
MODEL_TYPE_DEEPSEEK_CHAT: MODEL_TYPE = "model_type_deepseek_chat"

# Embedding类型
EMBEDDING_TYPE = str
EMBEDDING_TYPE_OPENAI: EMBEDDING_TYPE = "embedding_type_openai"
EMBEDDING_TYPE_AZURE: EMBEDDING_TYPE = "embedding_type_azure"
EMBEDDING_TYPE_HUGGING_FACE: EMBEDDING_TYPE = "embedding_type_hugging_face"


class Model:
    """
    Model模型
    """
    # 基础属性
    _model_type: MODEL_TYPE = MODEL_TYPE_AZURE_CHAT

    # 使用到的实例对象
    _raw_model: BaseLanguageModel

    def __init__(
            self,
            model_type: MODEL_TYPE = MODEL_TYPE_AZURE_CHAT,
            model_config: dict = None,
            temperature=0.5,
            cost_strict: bool = False,
            **kwargs
    ):
        # 判断是否开启cost_strict: 严格消费控制, 免得调用未经费用确认的model, 造成费用开销
        if cost_strict and model_type != MODEL_TYPE_DEEPSEEK_CHAT:
            raise RuntimeError(f"only support DEEPSEEK_CHAT model_type: {model_type}")
        self._model_type = model_type

        # 根据不同类型创建不同的Model
        if model_type == MODEL_TYPE_OPENAI_CHAT:
            self._raw_model = ChatOpenAI(
                temperature=temperature,
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_DOUBAO_CHAT:
            self._raw_model = ChatOpenAI(
                openai_api_key=model_config["api_key"],
                openai_api_base=model_config["api_base"],
                model_name=model_config["model"],
                temperature=temperature,
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_DEEPSEEK_CHAT:
            self._raw_model = ChatOpenAI(
                openai_api_key=model_config["api_key"],
                openai_api_base=model_config["api_base"],
                model_name=model_config["model"],
                temperature=temperature,
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_OPENAI_STRING:
            self._raw_model = OpenAI(
                temperature=temperature,
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_AZURE_CHAT:
            self._raw_model = AzureChatOpenAI(
                temperature=temperature,
                openai_api_key=model_config["api_key"],
                azure_endpoint=model_config["azure_endpoint"],
                openai_api_version=model_config["api_version"],
                model=model_config["model_version"],
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_AZURE_STRING:
            self._raw_model = AzureOpenAI(
                temperature=temperature,
                openai_api_key=model_config["api_key"],
                azure_endpoint=model_config["azure_endpoint"],
                openai_api_version=model_config["api_version"],
                model=model_config["model_version"],
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_BAICHUAN_CHAT:
            # 目前社区百川封装的模块, 暂不支持这种使用
            # 只能暂时先使用调接口的方式, 见BaichuanHTTPNode
            self._raw_model = ChatBaichuan(
                baichuan_api_key=model_config["api_key"],
                baichuan_api_base=model_config["api_base"],
                model=model_config["model"],
                temperature=temperature,
                max_retries=model_config["retry"],
                **kwargs
            )
        elif model_type == MODEL_TYPE_ZHIPU_CHAT:
            max_tokens = 1024
            if "max_tokens" in model_config:
                max_tokens = model_config["max_tokens"]
            self._raw_model = ChatZhipuAI(
                zhipuai_api_key=model_config["api_key"],
                zhipuai_api_base=model_config["api_base"],
                model=model_config["model"],
                temperature=temperature,
                max_retries=model_config["retry"],
                max_tokens=max_tokens,
                **kwargs
            )
        else:
            raise RuntimeError(f"unknown model_type: {model_type}")

    def stream(
            self,
            langchain_input: Input,
            config: Optional[RunnableConfig] = None,
            **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        """
        流式输出
        :param langchain_input:
        :param config:
        """
        return self._raw_model.stream(langchain_input, config, **kwargs)

    def get_raw_model(self) -> BaseLanguageModel:
        """
        返回实例model
        """
        return self._raw_model
