import sqlite3
from typing import Any, List, Tuple, Optional


class SQLiteTools:
    def __init__(self, db_path: str):
        """
        初始化 SQLite 工具类，连接数据库。
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # 支持以字典形式访问行数据
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[sqlite3.Row]:
        """
        执行 SELECT 查询并返回结果。
        :param query: SQL 查询语句
        :param params: 查询参数（可选）
        :return: 查询结果列表
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Query Error: {e}")
            return []

    def execute_non_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> int:
        """
        执行 INSERT/UPDATE/DELETE 等非查询语句，并返回受影响的行数。
        :param query: SQL 语句
        :param params: 参数（可选）
        :return: 受影响的行数（如果执行失败，返回 -1）
        """
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor.rowcount  # 返回受影响的行数
        except sqlite3.Error as e:
            print(f"Execution Error: {e}")
            return -1  # 返回 -1 表示执行失败

    def execute_many(self, query: str, params_list: List[Tuple[Any, ...]]) -> int:
        """
        批量执行多条 SQL 语句，并返回受影响的行数。
        :param query: SQL 语句
        :param params_list: 参数列表
        :return: 受影响的行数（如果执行失败，返回 -1）
        """
        try:
            self.cursor.executemany(query, params_list)
            self.conn.commit()
            return self.cursor.rowcount  # 返回受影响的行数
        except sqlite3.Error as e:
            print(f"Batch Execution Error: {e}")
            return -1  # 返回 -1 表示执行失败

    def close(self):
        """
        关闭数据库连接。
        """
        self.conn.close()
