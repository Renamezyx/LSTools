import axios from 'axios'
import { ElLoading, ElMessage } from 'element-plus'

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
    if (response.status !== 200 && String(response.status)[0] !== '2' && String(response.status)[0] !== '3') {
      ElMessage({
        message: 'server error',
        type: 'error',
        plain: true,
      })
    } else if (response.data.code !== 0) {
      ElMessage({
        message: response.data.message,
        type: 'error',
        plain: true,
      })
    } else {
      ElMessage({
        message: response.data.message,
        type: 'success',
        plain: true,
      })
    }
    return response
  },
  (error) => {
    hideLoading()
    ElMessage({
      message: String(error),
      type: 'error',
      plain: true,
    });
    return Promise.reject(error)
  }
)

export default service
