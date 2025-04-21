"""
@File: binding.py
@Date: 2024/12/10 10:00
@desc: sql工具
"""


def get_insert_sql(table: str, data: dict) -> (str, list):
    """
    获取insert语句
    :param table: 表名
    :param data: insert语句的数据
    :return: 返回插入SQL, 和绑定参数
    """
    # 参数检查
    if len(data) == 0:
        return "", []

    # 构建 COLUMN 子句
    column_clause_str = ', '.join(data.keys())

    # 构建 VALUES 子句
    values_clause_str = ', '.join(['%s'] * len(data.values()))

    query = f"INSERT INTO {table} ({column_clause_str}) VALUES ({values_clause_str})"
    params = list(data.values())
    return query, params


def get_insert_or_update_sql(table: str, data: dict, update_data: dict) -> (str, list):
    """
    获取insert或update语句
    :param table: 表名
    :param data: insert语句的数据
    :param update_data: 需要更新的列名和值的字典
    :return: 返回插入或更新SQL, 和绑定参数
    """
    # 参数检查
    if len(data) == 0:
        return "", []

    # 构建 COLUMN 子句
    column_clause_str = ', '.join(data.keys())

    # 构建 VALUES 子句
    values_clause_str = ', '.join(['%s'] * len(data.values()))

    # 构建 ON DUPLICATE KEY UPDATE 子句
    update_clause_list = []
    update_params = []
    for key, value in update_data.items():
        if isinstance(value, str) and '+' in key:  # 自增表达式检查
            key = key.replace("+", "")
            update_clause_list.append(f"{key} = {key} + {value}")
        elif isinstance(value, str) and '-' in key:  # 自减表达式检查
            key = key.replace("-", "")
            update_clause_list.append(f"{key} = {key} - {value}")
        else:
            update_clause_list.append(f"{key} = %s")
            update_params.append(value)

    update_clause_str = ', '.join(update_clause_list)

    query = f"INSERT INTO {table} ({column_clause_str}) VALUES ({values_clause_str}) ON DUPLICATE KEY UPDATE {update_clause_str}"
    params = list(data.values()) + update_params
    return query, params


def get_update_sql(table: str, data: dict, where: dict) -> (str, list):
    """
    获取update语句
    :param table: 表名
    :param data: update语句的数据
    :param where: update语句的where条件
    :return: 返回更新SQL, 和绑定参数
    """
    # 参数检查
    if len(data) == 0 or len(where) == 0:
        return "", []
    params = []

    # 构建 SET 子句
    set_clause_parts = []
    for key, value in data.items():
        params.append(value)
        set_clause_parts.append(f"{key} = %s")
    set_clause_str = ', '.join(set_clause_parts)

    # 构建 WHERE 子句
    condition_clause_parts = []
    for key, value in where.items():
        comparator = "="
        for comp in ['>=', '<=', '>', '<', '!=', '<>']:
            if comp in key:
                comparator = comp
                key = key.replace(comparator, '')
                break

        if isinstance(value, list):
            # 如果值是数组，使用 IN 语句
            params.extend(value)
            condition_clause_parts.append(f"{key} IN ({', '.join(['%s'] * len(value))})")
        else:
            params.append(value)
            condition_clause_parts.append(f"{key} {comparator} %s")
    condition_clause_str = " AND ".join(condition_clause_parts)

    query = f"UPDATE {table} SET {set_clause_str} WHERE {condition_clause_str}"
    return query, params


def get_select_by_where_sql(
        table: str,
        column_list: list[str],
        where: dict,
        order_by: str = "",
        limit: int = 10000) -> (str, list):
    """
    根据条件获取SELECT查询语句
    :param table: 表名
    :param column_list: 列名
    :param where: WHERE子句字典，包含字段和对应的值
    :param order_by: 排序
    :param limit: 上限
    :return: 返回查询SQL, 和绑定参数
    """
    # 参数检查
    if len(column_list) == 0 or len(where) == 0:
        return "", []
    params = []

    # 构建 COLUMN 子句
    column_clause_str = ", ".join(column_list)

    # 构建 WHERE 子句
    condition_clause_parts = []
    for key, value in where.items():
        comparator = "="
        for comp in ['>=', '<=', '>', '<', '!=', '<>', 'LIKE', 'like']:
            if comp in key:
                comparator = comp
                key = key.replace(comparator, '').strip()
                break

        if isinstance(value, list):
            # 如果值是数组，使用 IN 语句
            params.extend(value)
            condition_clause_parts.append(f"{key} IN ({', '.join(['%s'] * len(value))})")
        else:
            params.append(value)
            condition_clause_parts.append(f"{key} {comparator} %s")
    condition_clause_str = " AND ".join(condition_clause_parts)

    # 构建 ORDER 子句
    order_by_clause_str = ""
    if order_by:
        order_by_clause_str = f"ORDER BY {order_by}"

    # 构建 SELECT 查询语句
    query = f"SELECT {column_clause_str} FROM {table} WHERE {condition_clause_str} {order_by_clause_str} LIMIT {limit};"
    return query, params
