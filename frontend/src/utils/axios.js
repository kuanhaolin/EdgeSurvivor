import axios from 'axios'
import { ElMessage } from 'element-plus'

// 創建 axios 實例
const instance = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 請求攔截器 - 自動添加 Authorization header
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      // 確保 headers 對象存在
      if (!config.headers) {
        config.headers = {}
      }
      config.headers['Authorization'] = `Bearer ${token}`
      console.log('發送請求:', config.url, '帶 token:', token.substring(0, 20) + '...')
    } else {
      console.log('發送請求:', config.url, '無 token')
    }
    return config
  },
  error => {
    console.error('請求錯誤:', error)
    return Promise.reject(error)
  }
)

// 響應攔截器 - 統一處理錯誤
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 不要自動處理錯誤訊息，讓各個頁面自己決定如何處理
    console.error('API 錯誤:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export default instance
