import time

import psutil


def get_process_memory_usage(cmdline_filter=None):
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'cmdline']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            mem_usage = proc.info['memory_info'].rss / 1024 / 1024  # 转换为MB
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""
            if cmdline_filter.replace(" ", "").lower() in cmdline.replace(" ", "").lower():
                processes.append({
                    "pid": pid,
                    "name": name,
                    "mem_usage": mem_usage,
                    "cmdline": cmdline
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # 按内存使用量降序排序
    processes.sort(key=lambda x: x["mem_usage"], reverse=True)

    print(f"{'PID':<10}{'进程名':<30}{'内存占用 (MB)':<15}{'命令行参数'}")
    print("=" * 80)
    for process in processes:
        print(f"{process['pid']:<10}{process['name']:<30}{process['mem_usage']:.2f} MB     {process['cmdline']}")
    return processes


if __name__ == "__main__":
    from .dao_trends_stats import DaoTrendsStats

    res = DaoTrendsStats.delete()
    print(res)
    while True:
        processes = get_process_memory_usage(cmdline_filter="TikTok Live Studio")
        res = DaoTrendsStats.insert([tuple(i.values()) for i in processes])
        print(res)
        time.sleep(3)
    # res = DaoTrendsStats.select()
    # print(res)
