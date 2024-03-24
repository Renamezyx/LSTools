import json
import os

from common.logger_base import logger


class JSONFileHandler:
    @staticmethod
    def read_json_file(file_path):
        """
        读取JSON文件并返回其内容
        :param file_path: JSON文件路径
        :return: JSON文件内容（字典）
        """
        try:

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"文件 '{file_path}' 不存在.")
            return None
        except json.JSONDecodeError:
            print(f"无法解析JSON文件 '{file_path}'.")
            return None

    @staticmethod
    def write_json_file(file_path, data):
        """
        将数据写入JSON文件
        :param file_path: JSON文件路径
        :param data: 要写入文件的数据（字典）
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                logger.info(f"数据已成功写入到文件 '{file_path}'.")
        except Exception as e:
            print(f"写入文件 '{file_path}' 时发生错误: {e}")
            raise Exception(f"写入文件 '{file_path}' 时发生错误: {e}")

    @staticmethod
    def update_json(file_path, key, value):
        """
        更新JSON文件中的数据
        :param file_path: JSON文件路径
        :param key: 要更新的键
        :param value: 要更新的值
        """
        if not os.path.exists(file_path):
            logger.error(f"{file_path} FileNotFoundError")
            raise FileNotFoundError
        data = JSONFileHandler.read_json_file(file_path)
        if data:
            data[key] = value
            JSONFileHandler.write_json_file(file_path, data)
        else:
            JSONFileHandler.write_json_file(file_path, {key: value})

    @staticmethod
    def delete_json_key(file_path, key):
        """
        从JSON文件中删除指定的键
        :param file_path: JSON文件路径
        :param key: 要删除的键名
        """
        if os.path.exists(file_path):
            data = JSONFileHandler.read_json_file(file_path)
            if data:
                if key in data:
                    del data[key]
                    JSONFileHandler.write_json_file(file_path, data)
                else:
                    print(f"键 '{key}' 不存在于JSON文件 '{file_path}' 中.")
