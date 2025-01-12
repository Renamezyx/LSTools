import os

from config import get_project_root
from utils.sqlite_tools import SQLiteTools


class SQLitePreferences:
    def __init__(self, db_path):
        self.sqlite_tools = SQLiteTools(db_path)

    def insert_task(self, task: dict):
        task_name = task.get("task_name")
        task_content = task.get("task_content")
        period_id = int(task.get("period_id"))
        sql = "insert into tasks (task_name,task_content,period_id) values (?, ?,?)"
        res = self.sqlite_tools.execute_non_query(sql, (task_name, task_content, period_id))
        return res

    def get_task_for_period(self, period_id: int):
        sql = "select * from tasks where period_id = ?"
        res = list(self.sqlite_tools.execute_query(sql, (period_id,)))
        return res


sqlite_preferences = SQLitePreferences(os.path.join(get_project_root(), 'performance.db'))
