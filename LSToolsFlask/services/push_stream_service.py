
from services.users_service import UsersService
from services.script_service import ScriptService


class PushStreamService:
    @staticmethod
    def push(phone: str, audio_path: str = r"C:\Users\Admin\Downloads\1-100音画同步.mp4"):
        # 获取userinfo
        users = UsersService.users_select(phone=phone)
        if isinstance(users, list):
            user = users[0]
            script_params = ["--headers", user["headers"], "--audio_path", audio_path]
            # 执行脚本
            return ScriptService.script_start(script_name="push_script", script_params=script_params, user_phone=phone)
        else:
            return {"code": -1, "error": "user not found"}


if __name__ == '__main__':
    res = PushStreamService.push("12342058060")
    for i in res:
        print(i)
