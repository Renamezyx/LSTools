import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from config import get_project_root, DEVICE_IDS, UPLOAD_ROOT, ALLOWED_EXTENSIONS
from services.performance_service import format_ls_data


# 检查文件类型是否被允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file, device_id):
    upload_folder = UPLOAD_ROOT
    if not file or not allowed_file(file.filename):
        return {"error": "File type not allowed or no file provided."}
    print(device_id)
    device = "liveStudio_D"
    if device_id:
        for k, v in DEVICE_IDS.items():
            if device_id in v:
                upload_folder = os.path.join(UPLOAD_ROOT, k)
                device = k
                break
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    str_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_path = os.path.join(upload_folder, str(uuid.uuid4())[:2] + "_" + str_time + "_" + filename)

    # 保存文件
    file.save(file_path)

    #
    data = format_ls_data(file_path, device)
    return {"message": "File successfully uploaded", "filename": filename, "path": file_path, "data": data}


if __name__ == '__main__':
    format_ls_data(r"C:\Users\Admin\Desktop\LSTools\LSToolsFlask\temp\2d_2025_01_07_17_04_44_screen_03_1",
                   "liveStudio_C")
