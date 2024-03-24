import os
import re
from utils.json_file_handler import JSONFileHandler


class LocalControl(object):
    """
    本地控制类
    操作本地文件
    """

    def __init__(self):
        self.studio_file_path = "C:\\Program Files\\TikTok LIVE Studio"
        self.studio_data_path = os.path.join(os.path.expandvars('%appdata%'), "TikTok LIVE Studio")

    @property
    def version(self) -> str:
        """
        获取studio安装目录下文件最大的版本号
        :return: str
        """
        folders = [os.path.join(self.studio_file_path, name) for name in
                   os.listdir(self.studio_file_path) if
                   os.path.isdir(os.path.join(self.studio_file_path, name))]
        curr_version_path = max(folders, key=self.get_folder_size)
        return curr_version_path.split('\\')[-1]

    @property
    def branch(self) -> str:
        """
        获取studio的分支信息
        :return: str
        """
        package = JSONFileHandler.read_json_file(
            file_path=os.path.join(self.studio_file_path, self.version, 'resources\\app\\package.json'))
        branch = package['branch']
        return branch

    def open_dir(self, path: str) -> None:
        """
        打开指定目录
        :param path: str
        :return: None
        """
        os.system('start "" "{0}"'.format(path))

    def get_folder_size(self, folder_path: str) -> int:
        """
        获取指定目录下各文件夹的大小
        :param folder_path: str
        :return: int
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size

    @property
    def link_mic_battle_pb_by_log(self) -> list:
        """
        获取本地log文件打印的关于 battle db 数据
        :return: list
        """
        with open(os.path.join(self.studio_data_path, "logs", "renderer.log"), "r", encoding="utf-8") as log_file:
            pb_list = []
            result = []
            pb_re_str = r'LinkMicBattlePB (.*)'
            for line in log_file.readlines():
                res = re.search(pb_re_str, line)
                if res:
                    pb_list.append(res.group(1))
            for i in pb_list:
                i = re.sub(r'(\w+): ', r'"\1":', i)
                i = i.replace("'", '"')
                result.append(i)
        return result
