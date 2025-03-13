import time

from config import db_path
from utils.sqlite_tools import SQLiteTools


class DaoUsers(object):
    @staticmethod
    def insert(values: list or tuple) -> int:
        sql = """
        insert into users (headers, username, phone)
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
    def delete(phone):
        sql = "delete from users where phone=?"
        # 执行删除操作
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=(phone,))  # 返回受影响的行数
        sql_tools.close()
        return res

    @staticmethod
    def select(phone=None):
        sql = """
            select * from users
        """
        params = ()  # 默认无参数
        if phone is not None:
            sql = sql + " where phone=?"
            params = (phone,)
        # 执行查询
        print("select")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_query(query=sql, params=params)
        sql_tools.close()
        if res:
            res = [dict(row) for row in res]
        return res

    @staticmethod
    def update(headers, username, phone):
        params = ()
        if headers and username:
            sql = "update users set headers=?, username=? where phone=?"
            params = (headers, username, phone)
        elif headers:
            sql = "update users set headers=? where phone =?"
            params = (headers, phone)
        elif username:
            sql = "update users set username=? where phone =?"
            params = (username, phone)
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=params)
        sql_tools.close()
        return res
