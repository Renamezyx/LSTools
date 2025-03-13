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

sql_script_users ="""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headers TEXT,
    username TEXT, 
    phone TEXT UNIQUE,
    create_time INTEGER DEFAULT (strftime('%s', 'now')),  -- 记录创建时间
    update_time INTEGER DEFAULT (strftime('%s', 'now'))  -- 记录更新时间
)
"""
sql_script_users_trigger = """
CREATE TRIGGER IF NOT EXISTS update_users_trigger
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET update_time = strftime('%s', 'now') WHERE id = OLD.id;
END;

"""

if __name__ == '__main__':
    sqlite_tools = SQLiteTools(db_path="database.db")
    # sqlite_tools.execute_non_query(query=sql_trends_stats)
    sqlite_tools.execute_non_query(query=sql_script_users_trigger)
    sqlite_tools.close()
