import json

from control.local_control import LocalControl
from enums.studio_battle_enum import BattleStatusEnum

studio = LocalControl()


def catch_exceptions(func):
    """
    函数装饰器
    捕获函数异常处理
    如遇到异常 进行捕获 返回异常信息字符串
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)  # 返回异常信息字符串

    return wrapper


@catch_exceptions
def open_language_dir():
    """
    打开本地 studio 多语言 文件夹
    :return:
    """
    if studio.version:
        studio.open_dir(
            '{0}\\{1}\\resources\\app\\locales\\Live_Studio'.format(studio.studio_file_path, studio.version))


@catch_exceptions
def generate_finsh_pk():
    """
    生成 studio PK完成 参数
    :return:
    """
    battle_status_dict = {member.value: member.name for member in BattleStatusEnum}
    end_pb_str = studio.link_mic_battle_pb_by_log[-1]
    end_pb = json.loads(end_pb_str)

    if end_pb["battle_settings"]["status"] == 1:
        channel_id = end_pb["battle_settings"]["channel_id"]
        battle_id = end_pb["battle_settings"]["battle_id"]
        other_party_left = "false" if len(end_pb["anchors_info"]) == 2 else "true"
        other_party_user_id = ",".join([anchor_info["key"] for anchor_info in end_pb["anchors_info"][1:]])
        params = f"""
        aid:8311
        app_name:tiktok_live_studio
        device_id:7299719749469767170
        install_id:7345442360825202434
        channel:studio
        version_code:0.53.0
        device_platform:windows
        timezone_name:Asia%2FShanghai
        screen_width:1920
        screen_height:1080
        browser_language:zh-CN
        browser_platform:Win32
        browser_name:Mozilla
        browser_version:5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+TikTokLIVEStudio%2F0.53.0+Chrome%2F108.0.5359.215+Electron%2F22.3.18-tt.8.release.main.16+TTElectron%2F22.3.18-tt.8.release.main.16+Safari%2F537.36
        language:zh-Hans
        app_language:zh-Hans
        webcast_language:zh-Hans
        priority_region:us
        webcast_sdk_version:530
        live_mode:6
        channel_id:{channel_id}
        battle_id:{battle_id}
        cut_short:false
        other_party_left:{other_party_left}
        other_party_user_id:{other_party_user_id}
        finish_source:normal_finish
        finish_is_background:0
        finish_network_quality:1
        finish_cur_bitrate:2800
        finish_is_sdk:1
        """.replace(" ", '')
        return params
    else:
        return battle_status_dict[end_pb["battle_settings"]["status"]]


def client_ab_list_listener(id=None, key=None) -> str:
    """
    监听客户端实验
    """
    # while num > 0:
    pass


if __name__ == '__main__':
    pass
