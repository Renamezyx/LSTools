from scripts.trends_stats.dao_trends_stats import DaoTrendsStats


def get_trends_stats(start_time=None):
    res = {}
    dao = DaoTrendsStats.select(create_time=start_time)
    legend = set()
    xAxis = set()
    chartData = {}

    # 遍历数据库中的数据
    for i in dao:
        legend.add(i["name"])
        xAxis.add(i["create_time"])  # 收集 xAxis 的时间点

    # 将 xAxis 排序
    xAxis = sorted(xAxis)

    # 初始化 chartData，给每个 cmdline 一个空的列表
    for nickname in legend:
        chartData[nickname] = [0] * len(xAxis)

    # 填充 chartData
    for i in dao:
        nickname = i["name"]
        create_time = i["create_time"]
        mem_usage = i["mem_usage"]

        # 获取该 create_time 在 xAxis 中的索引位置
        index = xAxis.index(create_time)

        # 为该时间点填充对应的内存使用数据
        chartData[nickname][index] = int(mem_usage)

    res["legend"] = list(legend)
    res["xAxis"] = xAxis
    res["chartData"] = chartData
    return res
