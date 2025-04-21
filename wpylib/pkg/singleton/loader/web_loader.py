"""
@File: web_loader.py
@Date: 2024/2/27 00:07
@Desc: 第三方Web文档加载器
"""
from typing import List
from wpylib.util.http import requests_get
from wpylib.pkg.singleton.loader.simple_web_document import SimpleWebDocument

WEB_LOADER_ENGINE_JINA = "jina"


class WebLoader:
    """
    Web文档加载器
    """
    # 变量
    _engine: str = WEB_LOADER_ENGINE_JINA
    _jina_engine_config: dict = {
        "host": "https://r.jina.ai",
        "headers": {
            "Accept": "application/json",
        }
    }

    def __init__(self, engine: str = WEB_LOADER_ENGINE_JINA):
        self._engine = engine

    def load(self, resource_info_list: list[dict], proxies: dict = None, requests_kwargs: dict = None,
             headers: dict = None) -> List[SimpleWebDocument]:
        """
        加载网页
        """
        new_docs: List[SimpleWebDocument] = []

        # JINA爬虫引擎
        if self._engine == WEB_LOADER_ENGINE_JINA:
            new_docs = self._load_by_jina(
                resource_info_list=resource_info_list,
                proxies=proxies,
                requests_kwargs=requests_kwargs,
                headers=headers
            )
        return new_docs

    def _load_by_jina(self, resource_info_list: list[dict], proxies: dict = None, requests_kwargs: dict = None,
                      headers: dict = None) -> List[SimpleWebDocument]:
        """
        使用jina加载网页, jina控制参数都是在header中设置的
        """
        # 参数处理
        if requests_kwargs is None:
            requests_kwargs = {}
        if headers is None:
            headers = {}
        headers = dict(self._jina_engine_config["headers"], **headers)

        # 开始准备爬取网页
        new_docs: List[SimpleWebDocument] = []
        for url_info in resource_info_list:
            url = self._jina_engine_config["host"] + "/" + url_info["url"]
            resp = requests_get(url=url, headers=headers)
            new_docs.append(SimpleWebDocument(
                title=resp["data"]["title"],
                url=resp["data"]["url"],
                description=resp["data"]["description"],
                content=resp["data"]["content"],
            ))

        # 生成新的文档
        return new_docs
