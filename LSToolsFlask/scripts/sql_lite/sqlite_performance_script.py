import os.path
import sqlite3
from config import get_project_root
from utils.xls_tools import XlsTools
from scripts.sql_lite.sql_preformance import sqlite_preferences


def db_init():
    db_path = os.path.join(get_project_root(), 'performance.db')
    if os.path.exists(db_path):
        # 使用上下文管理器自动管理资源
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,  
                task_name TEXT,               
                task_content TEXT,
                period_id INTEGER,
                install_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS task_detail (
                id INTEGER PRIMARY KEY,  
                task_id INTEGER,               
                cpu_Electron REAL,
                cpu_MediaSDK REAL,
                cpu_LiveStudio REAL,
                gpu_Integrated REAL,
                gpu_LiveStudio REAL,
                memory_Electron REAL,
                memory_MediaSDK REAL,
                memory_LiveStudio REAL,  
                streamFPS_Encode REAL,
                streamFPS_Rander REAL,
                cameraFPS_Rander REAL,
                install_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            # 提交事务已经在上下文管理器退出时自动完成


def gene_performance_tasks(period_id: int):
    xls_tools = XlsTools(os.path.join(get_project_root(), "data", "performance_task.xlsx"))
    rows = xls_tools.read_all_rows()
    tasks = []
    for row in rows:
        task = dict()
        task["period_id"] = period_id
        task["task_name"] = "".join(row[1].split("\n"))
        task["task_content"] = "".join(row[2].split("\n"))
        tasks.append(task)
    res = sqlite_preferences.get_task_for_period(period_id)
    res = list(map(lambda x: dict(x), res))
    for task in tasks:
        if task["task_name"] in [row["task_name"] for row in res]:
            print(f"{task['task_name']} already exists")
        else:
            sqlite_preferences.insert_task(task)
    return res


if __name__ == '__main__':
    db_init()

    # 生成和插入性能任务
    tasks = gene_performance_tasks(1)
