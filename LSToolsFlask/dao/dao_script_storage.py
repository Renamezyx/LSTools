import time

from config import db_path
from utils.sqlite_tools import SQLiteTools


class DaoScriptStorage(object):
    @staticmethod
    def insert(values: list or tuple) -> int:
        sql = """
        insert into script_storage (pid, name, cmdline)
        values (?,?,?)
        """
        res = -1
        print("insert")
        sql_tools = SQLiteTools(db_path=db_path)
        if type(values) is tuple:
            res = sql_tools.execute_non_query(query=sql, params=values)
        if type(values) is list:
            res = sql_tools.execute_many(query=sql, params_list=values)
        sql_tools.close()
        return res

    @staticmethod
    def delete(pid=None):
        sql = "delete from script_storage"
        if pid is not None:
            sql += " WHERE pid <= ?"
            params = (pid,)
        else:
            params = ()  # 没有条件时，删除所有记录

        # 执行删除操作
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=params)  # 返回受影响的行数
        sql_tools.close()
        return res

    @staticmethod
    def select(name=None):
        sql = """
        select * from script_storage
        """
        params = ()  # 默认无参数

        # 如果提供了 `create_time`，加上 WHERE 条件
        if name is not None:
            sql += " WHERE name <= ?"
            params = (name,)

        # 执行查询
        print("select")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_query(query=sql, params=params)
        sql_tools.close()
        if res:
            res = [dict(row) for row in res]
        return res
