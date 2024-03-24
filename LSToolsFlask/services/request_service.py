import json
import os

from common.request_base import request
from config import get_project_root
from enums.studio_battle_enum import BattleStatusEnum
from services.local_service import catch_exceptions, studio
from utils.json_file_handler import JSONFileHandler


@catch_exceptions
def finish_pk():
    battle_status_dict = {member.value: member.name for member in BattleStatusEnum}
    end_pb_str = studio.link_mic_battle_pb_by_log[-1]
    end_pb = json.loads(end_pb_str)

    if end_pb["battle_settings"]["status"] == 1:
        channel_id = end_pb["battle_settings"]["channel_id"]
        battle_id = end_pb["battle_settings"]["battle_id"]
        other_party_left = "false" if len(end_pb["anchors_info"]) == 2 else "true"
        other_party_user_id = ",".join([anchor_info["key"] for anchor_info in end_pb["anchors_info"][1:]])
        params = {
            "aid": "8311",
            "app_name": "tiktok_live_studio",
            "device_id": "7299719749469767170",
            "install_id": "7345442360825202434",
            "channel": "studio",
            "version_code": "0.53.0",
            "device_platform": "windows",
            "timezone_name": "Asia/Shanghai",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Mozilla",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) TikTokLIVEStudio/0.53.0 Chrome/108.0.5359.215 Electron/22.3.18-tt.8.release.main.16 TTElectron/22.3.18-tt.8.release.main.16 Safari/537.36",
            "language": "zh-Hans",
            "app_language": "zh-Hans",
            "webcast_language": "zh-Hans",
            "priority_region": "us",
            "webcast_sdk_version": "530",
            "live_mode": "6",
            "channel_id": channel_id,
            "battle_id": battle_id,
            "cut_short": "false",
            "other_party_left": other_party_left,
            "other_party_user_id": other_party_user_id,
            "finish_source": "normal_finish",
            "finish_is_background": "0",
            "finish_network_quality": "1",
            "finish_cur_bitrate": "2800",
            "finish_is_sdk": "1"
        }
        header = JSONFileHandler.read_json_file(os.path.join(get_project_root(), "headers.json"))
        headers = header["battle"]
        res = request(method="POST", url=f"https://{headers["Host"]}/webcast/battle/finish/", params=params,
                      header=header)
        return res
    else:
        return battle_status_dict[end_pb["battle_settings"]["status"]]
