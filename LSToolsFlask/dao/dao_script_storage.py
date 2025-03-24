import time

from config import db_path
from utils.sqlite_tools import SQLiteTools


class DaoScriptStorage(object):
    @staticmethod
    def insert(pid, name, cmdline, user_phone) -> int:
        sql = """
        insert into script_storage (pid, name, cmdline,user_phone)
        values (?,?,?,?)
        """
        res = -1
        print("insert")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(sql, params=(pid, name, cmdline, user_phone))
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
    def select(name=None, user_phone=None, pid=None):
        sql = "SELECT * FROM script_storage"
        params = []  # 改为列表，避免元组拼接问题

        conditions = []
        if name is not None:
            conditions.append("name = ?")
            params.append(name)
        if user_phone is not None:
            conditions.append("user_phone = ?")
            params.append(user_phone)
        if pid is not None:
            conditions.append("pid = ?")
            params.append(pid)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        print("select")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_query(query=sql, params=tuple(params))
        sql_tools.close()
        if res:
            res = [dict(row) for row in res]
        return res
