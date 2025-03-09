import sqlite3
from typing import Any, List, Tuple, Optional


class SQLiteTools:
    def __init__(self, db_path: str):
        """
        初始化 SQLite 工具类，连接数据库。
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # 结果集支持字典访问
            self.cursor = self.conn.cursor()
            print("数据库连接成功！")
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")

    def execute_query(
        self, query: str, params: Optional[Tuple[Any, ...]] = None, fetch_one: bool = False
    ) -> List[sqlite3.Row]:
        """
        执行 SELECT 查询并返回结果。
        :param query: SQL 查询语句
        :param params: 查询参数（可选）
        :param fetch_one: 是否只获取一条数据
        :return: 查询结果列表（或单个查询结果）
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone() if fetch_one else self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"查询失败: {e}\nSQL: {query}\n参数: {params}")
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
            print(f"执行失败: {e}\nSQL: {query}\n参数: {params}")
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
            print(f"批量执行失败: {e}\nSQL: {query}\n参数: {params_list}")
            return -1  # 返回 -1 表示执行失败

    def close(self):
        """
        关闭数据库连接。
        """
        try:
            self.conn.close()
            print("数据库连接已关闭。")
        except sqlite3.Error as e:
            print(f"关闭数据库失败: {e}")


# 示例用法
if __name__ == "__main__":
    db = SQLiteTools("test.db")

    # 创建表
    db.execute_non_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # 插入数据
    db.execute_non_query("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
    db.execute_many("INSERT INTO users (name, age) VALUES (?, ?)", [("Bob", 30), ("Charlie", 22)])

    # 查询数据
    users = db.execute_query("SELECT * FROM users")
    for user in users:
        print(dict(user))  # 以字典形式打印

    db.close()
