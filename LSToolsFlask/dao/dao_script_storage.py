import time

from config import db_path
from utils.sqlite_tools import SQLiteTools


class DaoScriptStorage(object):
    @staticmethod
    def insert(pid, name, cmdline) -> int:
        sql = """
        insert into script_storage (pid, name, cmdline)
        values (?,?,?)
        """
        res = -1
        print("insert")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(sql, params=(pid, name, cmdline))
        sql_tools.close()
        return res

    @staticmethod
    def delete(pid=None):
        print("delete")
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
