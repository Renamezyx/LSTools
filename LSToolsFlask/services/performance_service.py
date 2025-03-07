import os
import re
import shutil
import zipfile

from config import ls_get_data_rules, get_project_root
from utils.xls_tools import XlsTools

TEMPPATH = os.path.join(get_project_root(), "temp")


def pre_load_data(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        name = os.path.splitext(path)[0].split(os.sep)[-1]
        zip_ref.extractall(os.path.join(TEMPPATH, name))
        print(f"{path} 已成功解压到 {TEMPPATH}{os.sep}{name}")
    return os.path.join(TEMPPATH, name)


def get_data(content, rule):
    res = {}
    for key, value in rule.items():
        if value:
            res[key] = re.findall(value, content)[0]
        else:
            res[key] = ""
    return res


def format_ls_data(path, device):
    pre_load_data(path)
    datas = []
    for file_dirpath in os.listdir(TEMPPATH):
        file_path = os.path.join(TEMPPATH, file_dirpath, "data.txt")
        if os.path.exists(path=file_path):
            with open(file_path, mode="r", encoding="utf-8") as f:
                content = f.readlines()
                content = "".join(content)
                data = {"场景": file_dirpath}
                data.update(get_data(content, ls_get_data_rules[device]))
                datas.append(data)
    title = list(data.keys())
    xls_tools = XlsTools(os.path.join(get_project_root(), "data.xlsx"), title=title)
    print(datas)
    for index, item in enumerate(datas):
        xls_tools.write_row(item.values())
    xls_tools.save()
    xls_tools.close()
    shutil.rmtree(TEMPPATH)
    return datas


if __name__ == '__main__':
    format_ls_data(
        r"C:\Users\Admin\Desktop\LSTools\LSToolsFlask\temp\72_2025_01_07_19_36_44_screen_01", "liveStudio_C")
