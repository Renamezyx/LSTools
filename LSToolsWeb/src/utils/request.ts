import axios from 'axios'
import { ElLoading } from 'element-plus'

// 定义 loading 变量和请求计数器
let loadingInstance: any = null
let requestCount = 0 // 计数器

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:8080', // API 地址
  timeout: 5000, // 超时时间
  withCredentials: false
})

// 显示 loading（只在第一个请求时触发）
const showLoading = () => {
  if (requestCount === 0) {
    loadingInstance = ElLoading.service({
      lock: true,
      text: 'Loading...',
      background: 'rgba(0, 0, 0, 0.7)',
    })
  }
  requestCount++
}

// 关闭 loading（仅当所有请求都完成时关闭）
const hideLoading = () => {
  requestCount--
  if (requestCount === 0) {
    loadingInstance?.close()
  }
}

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    showLoading()
    return config
  },
  (error) => {
    hideLoading()
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    hideLoading()
    return response.data
  },
  (error) => {
    hideLoading()
    console.error('Request error:', error) // 记录错误信息
    return Promise.reject(error)
  }
)

export default service
