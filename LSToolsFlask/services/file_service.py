import os
from werkzeug.utils import secure_filename
from config import get_project_root

# 上传文件的保存路径
UPLOAD_FOLDER = os.path.join(get_project_root(), "temp")
ALLOWED_EXTENSIONS = {'zip'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 检查文件类型是否被允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file):
    if not file or not allowed_file(file.filename):
        return {"error": "File type not allowed or no file provided."}

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # 保存文件
    file.save(file_path)
    return {"message": "File successfully uploaded", "filename": filename, "path": file_path}
