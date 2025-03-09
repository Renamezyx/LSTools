import time

from config import db_path
from utils.sqlite_tools import SQLiteTools


class DaoTrendsStats(object):
    @staticmethod
    def insert(values: list or tuple) -> int:
        sql = """
        insert into trends_stats (pid, name, mem_usage, cmdline, create_time)
        values (?,?,?,?,?)
        """
        res = -1
        print("insert")
        sql_tools = SQLiteTools(db_path=db_path)
        if type(values) is tuple:
            values = (*values, int(time.time()))
            res = sql_tools.execute_non_query(query=sql, params=values)
        if type(values) is list:
            timestamp = int(time.time())
            values = [(*i, timestamp) for i in values]
            res = sql_tools.execute_many(query=sql, params_list=values)
        sql_tools.close()
        return res

    @staticmethod
    def delete(create_time=None):
        sql = "delete from trends_stats"
        if create_time is not None:
            sql += " WHERE create_time <= ?"
            params = (create_time,)
        else:
            params = ()  # 没有条件时，删除所有记录

        # 执行删除操作
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_non_query(query=sql, params=params)  # 返回受影响的行数
        sql_tools.close()
        return res

    @staticmethod
    def select(create_time=None):
        sql = """
            SELECT sum(mem_usage) as mem_usage, name, create_time
            FROM trends_stats
            GROUP BY name, create_time
            UNION ALL
            SELECT count(pid) as mem_usage, 'count_trends' as name, create_time
            FROM trends_stats
            GROUP BY create_time
            order by create_time
        """
        params = ()  # 默认无参数

        # 如果提供了 `create_time`，加上 WHERE 条件
        if create_time is not None:
            sql = """  
                SELECT sum(mem_usage) as mem_usage, name, create_time
                FROM trends_stats where create_time > ? 
                GROUP BY name, create_time
                UNION ALL
                SELECT count(pid) as mem_usage, 'count_trends' as name, create_time
                FROM trends_stats where create_time > ?
                GROUP BY create_time
                order by create_time
            """
            params = (create_time, create_time)

        # 执行查询
        print("select")
        sql_tools = SQLiteTools(db_path=db_path)
        res = sql_tools.execute_query(query=sql, params=params)
        sql_tools.close()
        if res:
            res = [dict(row) for row in res]
        return res
