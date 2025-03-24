import argparse
import json
import subprocess
import time

from requests import Response

from common.request_base import request


def create(headers, domain) -> Response:
    data = {
        'title': 'Lets Go LIVE! ！！！！！',
        'live_studio': '1',
        'gen_replay': 'true',
        'chat_auth': '1',
        'cover_uri': 'tos-maliva-avt-0068/14a1d58897f84c360ac4c9994e9569f9',
        'close_room_when_close_stream': 'false',
        'hashtag_id': '42',
        'game_tag_id': '0',
        'screenshot_cover_status': '1',
        'live_sub_only': '0',
        'chat_sub_only_auth': '2',
        'multi_stream_scene': '0',
        'gift_auth': '1',
        'chat_l2': '1',
        'star_comment_switch': 'true',
        'multi_stream_source': '1',
        'is_group_live_session': 'false',
    }
    url = f'https://{domain}/webcast/room/create/?aid=8311&app_name=tiktok_live_studio&device_id=7304628306396431874&install_id=7475324946504730369&channel=studio&version_code=0.78.1&device_platform=windows&timezone_name=Asia%2FShanghai&screen_width=1707&screen_height=1067&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+TikTokLIVEStudio%2F0.78.1+Chrome%2F108.0.5359.215+Electron%2F22.3.18-tt.11.release.main.43+TTElectron%2F22.3.18-tt.11.release.main.43+Safari%2F537.36&language=zh-Hans&app_language=zh-Hans&webcast_language=zh-Hans&priority_region=tr&webcast_sdk_version=781&live_mode=6&carrier_region=JP&fake_region=JP'
    response = request(method="POST",
                       url=url,
                       headers=headers,
                       data=data,
                       )
    return response


def heat(headers, domain):
    url = f"https://{domain}/webcast/room/ping/anchor/?aid=8311&app_name=tiktok_live_studio&device_id=7304628306396431874&install_id=7475324946504730369&channel=studio&version_code=0.78.1&device_platform=windows&timezone_name=Asia%2FShanghai&screen_width=1707&screen_height=1067&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+TikTokLIVEStudio%2F0.78.1+Chrome%2F108.0.5359.215+Electron%2F22.3.18-tt.11.release.main.43+TTElectron%2F22.3.18-tt.11.release.main.43+Safari%2F537.36&language=zh-Hans&app_language=zh-Hans&webcast_language=zh-Hans&priority_region=tr&webcast_sdk_version=781&live_mode=6"
    data = {
        'status': '2',
        'room_id': room_id,
        'stream_id': stream_id,
    }
    res = request(method="POST", url=url, data=data, headers=headers)
    return None


def finish_stream(room_id, headers, domain):
    url = f"https://{domain}/webcast/game/basic/finish_info/?aid=8311&app_name=tiktok_live_studio&device_id=7304628306396431874&install_id=7475324946504730369&channel=studio&version_code=0.78.1&device_platform=windows&timezone_name=Asia%2FShanghai&screen_width=1707&screen_height=1067&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+TikTokLIVEStudio%2F0.78.1+Chrome%2F108.0.5359.215+Electron%2F22.3.18-tt.11.release.main.43+TTElectron%2F22.3.18-tt.11.release.main.43+Safari%2F537.36&language=zh-Hans&app_language=zh-Hans&webcast_language=zh-Hans&webcast_sdk_version=781&live_mode=6&room_id={room_id}&carrier_region=JP&fake_region=JP"
    res = request(method="GET", url=url, headers=headers)
    return res.status_code, res.json()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An example script with named arguments.")
    parser.add_argument('--headers', type=str)
    parser.add_argument('--audio_path', type=str)
    args = parser.parse_args()
    headers = json.loads(args.headers)
    audio_path = args.audio_path
    domain = headers["Host"]
    create_res = create(headers, domain)
    if create_res.status_code == 200:
        create_dict = create_res.json()
        if create_dict["status_code"] == 0:
            room_id = create_dict["data"]["living_room_attrs"]["room_id_str"]
            stream_id = create_dict["data"]["stream_id_str"]
            push_stream_url = create_dict["data"]["stream_url"]["rtmp_push_url"]
            try:
                ffmpeg_command = [
                    'ffmpeg',
                    '-re',
                    '-stream_loop', '-1',
                    '-i', audio_path,
                    '-vcodec', 'libx264',
                    '-acodec', 'aac',
                    '-f', 'flv',
                    push_stream_url
                ]
                process = subprocess.Popen(ffmpeg_command)
                while True:
                    time.sleep(3)
                    heat(headers, domain)
            except KeyboardInterrupt as e:
                print("Keyboard Interrupt")
                finish_stream(room_id, headers, domain)
            except Exception as e:
                print("Exception")
                finish_stream(room_id, headers, domain)
        if create_dict["status_code"] == 20003:
            raise Exception("登录态失效")
    else:
        raise Exception("请求异常")
