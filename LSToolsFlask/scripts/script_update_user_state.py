import json
import time

from common.request_base import request
from dao.dao_users import DaoUsers


def create_info(headers: dict):
    try:
        domain = headers.get('Host', None) or headers.get('host', None)
    except Exception as e:
        return -1, None
    url = f"https://{domain}/webcast/room/create_info/?aid=8311&version_code=0.80.0&language=zh-Hans&priority_region=tr"
    res = request("GET", url, headers=headers)

    return res.status_code, res


if __name__ == '__main__':
    while True:
        users = DaoUsers.select()
        for user in users:
            try:
                headers = json.loads(user["headers"])
            except Exception as e:
                DaoUsers.update_state(user["id"], -999)
                continue
            status_code, res = create_info(headers)
            if status_code == -1:
                DaoUsers.update_state(user["id"], -999)
                continue
            if status_code == 200:
                res_json = res.json()
                if res_json["status_code"] == 20003:
                    cookies_invalid = 1
                    DaoUsers.update_state(user["id"], -1)
                    continue
                live_status = res_json["data"]["live_status"]
                if live_status == 4:
                    DaoUsers.update_state(user["id"], 0)
                if live_status == 2 or live_status == 3:
                    DaoUsers.update_state(user["id"], 2)
        time.sleep(30)
