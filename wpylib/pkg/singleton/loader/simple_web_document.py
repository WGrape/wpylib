"""
@File: simple_web_document.py
@Date: 2024/2/27 00:07
@Desc: WEB文档结构
"""
from typing import Any
from langchain_core.documents import Document as LangChainDocument


class SimpleWebDocument(LangChainDocument):
    """
    Web文档对象
    """
    # 注意: 如果使用私有属性, 会提示没有此属性, 所以修改为公开属性
    title: str = ""
    url: str = ""
    description: str = ""
    content: str = ""

    def __init__(self, title: str = "", url: str = "", description: str = "", content: str = "", **kwargs: Any):
        super().__init__(content, **kwargs)
        self.title = title
        self.url = url
        self.description = description
        self.content = content

    def get_title(self) -> str:
        """
        获取title
        """
        return self.title

    def get_url(self) -> str:
        """
        获取url
        """
        return self.url

    def get_description(self) -> str:
        """
        获取description
        """
        return self.description

    def get_content(self) -> str:
        """
        获取content
        """
        return self.content
