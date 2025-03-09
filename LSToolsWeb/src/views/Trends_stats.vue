<template>
  <div id="trends_echarts" style="width: 100%; height: 600px;"></div> <!-- ECharts 容器 -->
</template>

<script>
import * as echarts from 'echarts';
import { reactive, onMounted } from 'vue';
import { io } from "socket.io-client";

export default {
  name: 'Echarts',
  setup() {
    function formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString(); 
    }

    const option = reactive({
      title: { text: '实时数据监控' },
      tooltip: {
        trigger: 'axis',
        formatter: function (params) {
          let tooltipContent = params[0].name + '<br>';
          params.forEach(function (item) {
            tooltipContent += `<div style="width: 300px; display: flex; justify-content: space-between;">
                                <span>${item.seriesName}:</span> 
                                <span>${item.value} MB|个</span>
                              </div>`;
          });
          return tooltipContent;
        }
      },
      legend: {
        data: [],
        selected: {}
      },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      toolbox: { feature: { saveAsImage: {} } },
      xAxis: { type: 'category', boundaryGap: false, data: [] },
      yAxis: { type: 'value' },
      series: []
    });

    let myChart;

    onMounted(() => {
      const chartDom = document.getElementById('trends_echarts');
      myChart = echarts.init(chartDom);
      myChart.setOption(option);

      const socket = io("ws://localhost:8080", { transports: ["websocket"] });

      socket.on("connect", () => {
        console.log("Socket.IO 连接成功", socket.id);
        setInterval(() => {
          socket.emit("message", { func: "get_trends_stats" });
        }, 10000);
      });

      socket.on("server_response", (data) => {
        console.log("收到服务器消息:", data);
        if (data.type === "get_trends_stats") {
          const newLegend = data.data.legend;

          // **保留原来的 selected 状态**
          const updatedSelected = myChart.getOption().legend[0].selected || {};;
          // **新数据的图例默认显示，但不覆盖用户隐藏过的图例**
          newLegend.forEach(item => {
            if (!(item in updatedSelected)) {
              updatedSelected[item] = true;
            }
          });
          // **更新 ECharts 配置**
          myChart.setOption({
            legend: {
              data: newLegend,
              selected: updatedSelected
            },
            xAxis: { data: data.data.xAxis.map(formatTimestamp) },
            series: newLegend.map(item => ({
              name: item,
              type: 'line',
              smooth: true,
              data: data.data.chartData[item]
            }))
          });
        }
      });

      socket.on("disconnect", () => {
        console.log("Socket.IO 连接断开");
      });
    });

    return { option };
  }
};
</script>
