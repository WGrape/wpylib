"""
@File: mysql.py
@Date: 2024/12/10 10:00
@Desc: 第三方mysql存储单例模块
"""
from wpylib.util.x.xtyping import is_not_none
from mysql.connector.pooling import MySQLConnectionPool
import logging

# 查询语句类型
QUERY_TYPE_RAW: str = "raw"
QUERY_TYPE_INSERT: str = "insert"
QUERY_TYPE_BATCH_INSERT: str = "batch_insert"
QUERY_TYPE_DELETE: str = "delete"
QUERY_TYPE_SELECT: str = "select"
QUERY_TYPE_UPDATE: str = "update"
QUERY_TYPE_INSERT_OR_UPDATE: str = "insert_or_update"


class Mysql:
    """
    Mysql数据库类
    """
    # 基础属性
    _pool: MySQLConnectionPool

    # 初始化需要的配置
    _mysql_config: dict

    # 单例类
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, mysql_config: dict):
        self._mysql_config = mysql_config
        self._connect()

    def _connect(self):
        """
        连接数据库
        1. buffered=True, fix error: raise InternalError("Unread result found")
           https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
        """
        for times in range(self._mysql_config["retry"]):
            try:
                self._pool = MySQLConnectionPool(pool_name="mysql_pool", **self._mysql_config["dsn"])
                self._log("connected to mysql successfully")
                break
            except Exception as e:
                self._log("connect to mysql retry", error=True, extra_info={"retry": times, "e": e})
                if times == self._mysql_config["retry"] - 1:
                    raise RuntimeError(e)

    def _re_connect(self):
        """
        连接失效后的重连
        """
        self._connect()

    def _execute(self, query_type: str, query: str, params: list = None):
        """
        执行语句
        :param query: 查询语句
        :param params: 参数列表
        :param query_type: Query类型
        :return: 返回结果
        """
        cnx = self._pool.get_connection()
        cursor = cnx.cursor(buffered=True)
        exception = None

        # 开始执行
        result = None
        try:
            # 执行Query
            for times in range(self._mysql_config["retry"]):
                try:
                    # 单条执行
                    if query_type != QUERY_TYPE_BATCH_INSERT:
                        cursor.execute(query, params)
                    # 多条执行
                    else:
                        cursor.executemany(query, params)
                    break
                except Exception as e:
                    # 记录日志
                    self._log(
                        "execute error",
                        error=True,
                        extra_info={"retry": times, "query": query, "params": params, "e": e}
                    )
                    # 超过最大重试次数则上抛错误
                    if times == self._mysql_config["retry"] - 1:
                        raise e

            # 提交Query
            # 调试的时候需要以这个为断点, 不然会一直报连接不上Mysql的问题
            cnx.commit()

            # 根据语句类型不同, 获取不同的返回值
            query_type = query_type.lower()
            if query_type == QUERY_TYPE_INSERT or query_type == QUERY_TYPE_BATCH_INSERT:
                # 无论单条插入还是批量插入, 都只返回最后一条插入记录ID
                result = cursor.lastrowid
            elif query_type == QUERY_TYPE_INSERT_OR_UPDATE:
                # 如果是insert_or_update, 只返回最后一条插入记录ID
                result = cursor.lastrowid
            elif query_type == QUERY_TYPE_DELETE:
                # 返回影响行数
                result = cursor.rowcount
            elif query_type == QUERY_TYPE_SELECT:
                # 返回查询结果
                # 无论是查询一条记录还是多条记录, 都返回一个数组, 需要上层自己处理
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in results]
            elif query_type == QUERY_TYPE_UPDATE:
                # 返回影响行数
                result = cursor.rowcount
            else:
                # RAW语句
                result = cursor.rowcount

            # 执行成功
            self._log("raw execute success", extra_info={"query": query, "params": params})
        except Exception as e:
            exception = e
            self._log("raw execute exception finally", error=True,
                      extra_info={"query": query, "params": params, "e": e})
        finally:
            # 关闭连接
            if cnx:
                cnx.close()
            # 关闭cursor
            if cursor:
                cursor.close()
            self._log("put connection to pool")

        # 处理执行结果
        if is_not_none(exception):
            raise exception
        return result

    def _log(self, message, error=False, extra_info=None):
        """
        辅助函数用于统一处理日志记录。
        :param message: 日志消息主体。
        :param error: 是否为错误信息，默认为False。
        :param extra_info: 额外信息字典，可选。
        """
        if extra_info:
            for key, value in extra_info.items():
                message += f" {key}: {value}"
        logger = logging.getLogger("wpylib_logger")
        if error:
            logger.error(message)
        else:
            logger.info(message)

    def execute_raw_query(self, query: str, params: list = None):
        """
        执行原生语句
        :param query: 语句
        :param params: 参数列表
        :return 返回类型不确定
        """
        return self._execute(QUERY_TYPE_RAW, query, params)

    def execute_insert_query(self, query: str, params: list = None) -> int:
        """
        执行insert语句
        :param query: 语句
        :param params: 参数列表
        :return 返回插入记录的ID
        """
        return self._execute(QUERY_TYPE_INSERT, query, params)

    def execute_insert_or_update_query(self, query: str, params: list = None) -> int:
        """
        执行insert_or_update语句
        :param query: 语句
        :param params: 参数列表
        :return 返回插入或更新的ID
        """
        return self._execute(QUERY_TYPE_INSERT_OR_UPDATE, query, params)

    def execute_batch_insert_query(self, query: str, params: list = None) -> int:
        """
        执行批量insert语句
        :param query: 语句
        :param params: 参数列表
        :return 返回插入的自增ID
        """
        return self._execute(QUERY_TYPE_BATCH_INSERT, query, params)

    def execute_delete_query(self, query: str, params: list = None) -> int:
        """
        执行delete语句
        :param query: 语句
        :param params: 参数列表
        :return 返回删除记录的ID
        """
        return self._execute(QUERY_TYPE_DELETE, query, params)

    def execute_select_query(self, query: str, params: list = None) -> list:
        """
        执行select语句
        :param query: 语句
        :param params: 参数列表
        :return 返回查到的列表
        """
        return self._execute(QUERY_TYPE_SELECT, query, params)

    def execute_update_query(self, query: str, params: list = None) -> int:
        """
        执行update语句
        :param query: 语句
        :param params: 参数列表
        :return 返回更新记录的ID
        """
        return self._execute(QUERY_TYPE_UPDATE, query, params)
