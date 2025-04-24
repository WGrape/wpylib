"""
@File: milvus.py
@Date: 2024/12/10 10:00
@Desc: milvus向量存储模块
"""
from pymilvus import MilvusClient
from wpylib.util.x.xtyping import is_none
from mem0.utils.factory import EmbedderFactory
from typing import Union, Dict, List, Optional


class Milvus:
    """
    milvus对象
    """
    # 初始化需要的配置
    _milvus_config: dict

    # 使用到的实例对象
    _instance_milvus: MilvusClient

    # 单例类
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, milvus_config: dict, model_config: dict):
        self._milvus_config = milvus_config

        # 初始化embedding模型
        self._embedding_model = EmbedderFactory.create(
            provider_name="ollama",
            config={
                "model": model_config["model"],  # 如text-embedding-ada-002
                "api_key": model_config["api_key"],  # 如3e6f8...
                "embedding_dims": model_config["embedding_dims"],  # 如1536
                "ollama_base_url": model_config["api_base"],  # 如http://localhost:11434
            }
        )

        # 初始化milvus客户端
        self._instance_milvus = MilvusClient(
            uri=milvus_config["uri"],
            # token=milvus_config["token"],
            db_name=milvus_config["db_name"],
            # ssl=False,
            # secure=False
        )
        for collection_name in milvus_config["collection"]:
            self._instance_milvus.load_collection(collection_name=collection_name)  # 加载collection, 否则可能会报错

        # 验证milvus客户端是否可用
        test_collection_name = milvus_config["collection"]["test"]
        search_res = self.search(
            collection_name=test_collection_name, query="test", output_fields=["*"]
        )

    def get_instance_milvus(self) -> MilvusClient:
        """
        获取实例
        :return:
        """
        return self._instance_milvus

    def embed(self, text: str) -> list[float]:
        """
        文本向量化
        :param text:
        :return:
        """
        embeddings = self._embedding_model.embed(text)
        return embeddings

    def query(
            self,
            collection_name: str,
            filter_str: str = "",
            output_fields: Optional[List[str]] = None,
            timeout: Optional[float] = None,
            ids: Optional[Union[List, str, int]] = None,
            partition_names: Optional[List[str]] = None
    ):
        """
        查询记录
        :param collection_name:
        :param filter_str:
        :param output_fields:
        :param timeout:
        :param ids:
        :param partition_names:
        :return:
        """
        query_res = self._instance_milvus.query(
            collection_name=collection_name,
            filter=filter_str,
            output_fields=output_fields,
            timeout=timeout,
            ids=ids,
            partition_names=partition_names
        )
        return query_res

    def insert(
            self,
            collection_name: str,
            data: Union[Dict, List[Dict]],
            timeout: Optional[float] = None,
            partition_name: Optional[str] = "",
    ) -> dict:
        """
        插入数据
        :param collection_name:
        :param data:
        :param timeout:
        :param partition_name:
        :return:
        """
        res = self._instance_milvus.insert(
            collection_name=collection_name,
            data=data,
            timeout=timeout,
            partition_name=partition_name
        )
        return res

    def upsert(
            self,
            collection_name: str,
            data: Union[Dict, List[Dict]],
            timeout: Optional[float] = None,
            partition_name: Optional[str] = "",
    ) -> dict:
        """
        插入或更新数据
        不是这样: 适用场景, 如果有update同一个question的需求, 是不是我先query出来(filter这个question字段), 拿出来ID后, 再使用upsert
        是这样: 如果是使用了auto_id的collection的话是不能用upsert的，您可以先delete然后再insert新的，因为auto_id是有唯一性的。实际上upsert的底层就是封装了delete和insert这两个操作，为的是代码方便
        :param collection_name:
        :param data:
        :param timeout:
        :param partition_name:
        :return:
        """
        res = self._instance_milvus.upsert(
            collection_name=collection_name,
            data=data,
            timeout=timeout,
            partition_name=partition_name
        )
        return res

    def search(
            self,
            collection_name: str,
            query: str,
            output_fields: list[str],
            search_params=None,
            filter_str: str = "",
            limit=3
    ):
        """
        搜索
        filter参数: https://milvus.io/docs/boolean.md
        search参数: https://docs.zilliz.com.cn/reference/python/python/Vector-search
        返回结构: data: ["[{'id': 452424477291365021, 'distance': 0.9999998211860657, 'entity': {}}]"]
        :param collection_name:
        :param query:
        :param output_fields:
        :param search_params:
        :param filter_str:
        :param limit:
        :return:
        """
        # 参数处理
        if is_none(search_params):
            search_params = {}
        default_search_params = {
            # 度量向量embedding间相似度的方法: 可选值为 IP、L2、COSINE。默认按已加载（load）的索引文件设定。
            "metric_type": "COSINE",
            # query failed: metric type not match: invalid parameter[expected=COSINE][actual=IP]
            "params": {}
        }
        default_search_params.update(search_params)

        # 向量化
        embeddings = self.embed(query)

        # 开始搜索
        search_list = self._instance_milvus.search(
            collection_name=collection_name,
            data=[embeddings],
            output_fields=output_fields,
            search_params=default_search_params,
            filter=filter_str,
            limit=limit
        )

        # 返回结果
        if len(search_list) > 0:
            return search_list[0]
        return []
