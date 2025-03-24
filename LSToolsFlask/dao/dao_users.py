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
    def delete(id):
        sql = "delete from users where id=?"
        # 执行删除操作
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=(id,))  # 返回受影响的行数
        sql_tools.close()
        return res

    @staticmethod
    def select(phone=None):
        sql = """
            SELECT * FROM users
        """
        params = []

        conditions = []
        if phone is not None:
            conditions.append("phone = ?")
            params.append(phone)

        # 只有当有筛选条件时，才拼接 WHERE
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # 执行查询
        print("SQL:", sql)
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_query(query=sql, params=tuple(params))
        sql_tools.close()

        # 转换查询结果
        if res:
            res = [dict(row) for row in res]
        return res

    @staticmethod
    def update(headers, username, phone, id):
        sql = "update users set headers=?, username=?, phone=? where id = ?"
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=(headers, username, phone, id))
        sql_tools.close()
        return res

    @staticmethod
    def update_state(id, state):
        sql = "update users set state=? where id=?"
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(sql, params=(state, id))
        sql_tools.close()
        return res
