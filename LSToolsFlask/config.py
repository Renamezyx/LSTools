import os


def get_project_root():
    # 获取根目录 不受运行目录影响
    current_dir = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(current_dir, '.project_root')):
        current_dir = os.path.dirname(current_dir)
    return current_dir


def get_cookies(host):
    import sqlite3

    # 连接到SQLite数据库
    # 如果文件不存在，它将自动创建
    conn = sqlite3.connect(os.path.join(os.getenv('APPDATA'), "TikTok LIVE Studio", "Network", "Cookies"))

    # 创建一个cursor对象来执行SQL语句
    cursor = conn.cursor()

    # 执行查询，假设我们查询一个名为 'your_table_name' 的表
    cursor.execute(f"SELECT host_key,name,value FROM cookies where host_key = '{host}'")

    # 获取查询结果
    rows = cursor.fetchall()

    cookies = []
    for row in rows:
        cookies.append(f"{row[1]}={row[2]}")
    return ";".join(cookies).replace("\n", "").replace("\r", "")
    # 关闭游标和连接
    cursor.close()
    conn.close()


DEVICE_IDS = {"liveStudio_C": [], "liveStudio_D": ["423C3B0D-D6EA-4520-B11D-077A5477D914"], "liveStudio_A": ["283D927A-4680-498B-84C0-EE942187F6D7"]}
# 上传文件的保存路径
UPLOAD_ROOT = os.path.join(get_project_root(), "sources")
ALLOWED_EXTENSIONS = {'zip'}

ls_get_data_rules = {
    "liveStudio_C":
        {
            "CPU_electron进程": r"cpu_avg[\s\S]+?tiktok_live_studio: (.*)\n",
            "CPU_MediaSDK进程": r"cpu_avg[\s\S]+?mediasdk_server: (.*)\n",
            "CPU_整体": r"livestudio:[\s\S]+?CPU占用: (.*)%",
            "GPU3D_electron进程-A卡独显数据": r"",
            "GPU3D_MediaSDK进程-A卡独显数据": r"gpu_3d_avg[\s\S]+?mediasdk_server_AMD_Radeon_RX_6700M: (.*)\n",
            "GPU3D_整体": r"livestudio:[\s\S]+?GPU 3D 占用: [\s\S]+?AMD_Radeon_RX_6700M: (.*)%",
            "gpu_encode": r"",
            "内存占用(MB)_electron进程": r"memory_avg[\s\S]+?tiktok_live_studio: (.*)\n",
            "内存占用(MB)_sdk进程": r"memory_avg[\s\S]+?mediasdk_server: (.*)\n",
            "内存占用(MB)_整体": r"livestudio:[\s\S]+?内存占用： (.*)MB",
            "数据留存1": "",
            "编码帧率2": "主画布编码帧率： (.*)",
            "画布渲染帧率3": "渲染帧率： (.*)"
        },
    "liveStudio_D": {
        "CPU_electron进程": r"cpu_avg[\s\S]+?tiktok_live_studio: (.*)\n",
        "CPU_MediaSDK进程": r"cpu_avg[\s\S]+?mediasdk_server: (.*)\n",
        "CPU_整体": r"livestudio:[\s\S]+?CPU占用: (.*)%",
        "GPU3D_electron进程-A卡独显数据": r"",
        "GPU3D_MediaSDK进程-A卡独显数据": r"gpu_3d_avg[\s\S]+?mediasdk_server_NVIDIA_GeForce_GTX_1050_Ti: (.*)\n",
        "GPU3D_整体": r"livestudio:[\s\S]+?GPU 3D 占用: [\s\S]+?NVIDIA_GeForce_GTX_1050_Ti: (.*)%",
        "gpu_encode": r"",
        "内存占用(MB)_electron进程": r"memory_avg[\s\S]+?tiktok_live_studio: (.*)\n",
        "内存占用(MB)_sdk进程": r"memory_avg[\s\S]+?mediasdk_server: (.*)\n",
        "内存占用(MB)_整体": r"livestudio:[\s\S]+?内存占用： (.*)MB",
        "数据留存1": "",
        "编码帧率2": "主画布编码帧率： (.*)",
        "画布渲染帧率3": "渲染帧率： (.*)"
    },
    "liveStudio_E": {}
}

DEBUG = 1
