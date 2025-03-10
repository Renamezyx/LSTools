from utils.sqlite_tools import SQLiteTools

# 进程状态表
sql_trends_stats = """
 CREATE TABLE IF NOT EXISTS trends_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER NOT NULL,
            name TEXT NOT NULL,
            mem_usage FLOAT NOT NULL,
            cmdline TEXT,
            create_time INTEGER DEFAULT (strftime('%s', 'now')))
"""

sql_script_storage = """
 CREATE TABLE IF NOT EXISTS script_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER NOT NULL,
            name TEXT NOT NULL,
            cmdline TEXT,
            create_time INTEGER DEFAULT (strftime('%s', 'now')))
"""

if __name__ == '__main__':
    sqlite_tools = SQLiteTools(db_path="database.db")
    # sqlite_tools.execute_non_query(query=sql_trends_stats)
    sqlite_tools.execute_non_query(query=sql_script_storage)
    sqlite_tools.close()
