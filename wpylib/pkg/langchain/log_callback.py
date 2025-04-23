"""
@File: log_callback.py
@Date: 2024/12/10 10:00
@desc: 第三方日志回调模块
"""
from wpylib.util.x.xjson import stringify
from typing import Dict, Any, List, Union
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
import logging


class LogCallback(BaseCallbackHandler):
    """
    日志回调
    接Langchain的回调: https://python.langchain.com/docs/modules/callbacks/
    """
    # 基础属性
    _name: str = ""
    _class: str = ""
    _logger: logging.Logger

    def __init__(self, name: str = "langchain日志回调"):
        self._name = name
        self._class = "LogCallback"
        self._logger = logging.getLogger("wpylib_logger")

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        result_snapshot = {"serialized": serialized, "prompts": prompts}
        logger = logging.getLogger("wpylib_logger")
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_llm_start" + stringify(result_snapshot))

    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""
        result_snapshot = {"serialized": serialized, "messages": messages}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_chat_model_start" + stringify(result_snapshot))

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        result_snapshot = {"token": token}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_llm_new_token" + stringify(result_snapshot))

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        result_snapshot = {"response": response}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_llm_end" + stringify(result_snapshot))

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        result_snapshot = {"error": error}
        self._logger.error("ERROR: langchain -> callback -> log_callback -> on_llm_error" + stringify(result_snapshot))

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        result_snapshot = {"serialized": serialized, "inputs": inputs}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_chain_start" + stringify(result_snapshot))

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        result_snapshot = {"outputs": outputs}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_chain_end" + stringify(result_snapshot))

    def on_chain_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors."""
        result_snapshot = {"error": error}
        self._logger.error("ERROR: langchain -> callback -> log_callback -> on_chain_error" + stringify(result_snapshot))

    def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        result_snapshot = {"serialized": serialized, "input_str": input_str}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_tool_start" + stringify(result_snapshot))

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        result_snapshot = {"output": output}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_tool_end" + stringify(result_snapshot))

    def on_tool_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""
        result_snapshot = {"error": error}
        self._logger.error("ERROR: langchain -> callback -> log_callback -> on_tool_error" + stringify(result_snapshot))

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""
        result_snapshot = {"text": text}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_text" + stringify(result_snapshot))

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        result_snapshot = {"action": action}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_agent_action" + stringify(result_snapshot))

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        result_snapshot = {"finish": finish}
        self._logger.info("INFO: langchain -> callback -> log_callback -> on_agent_finish" + stringify(result_snapshot))
