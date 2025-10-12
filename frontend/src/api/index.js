import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 創建 axios 實例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 添加認證令牌
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 響應攔截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // 嘗試刷新令牌
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/auth/refresh', {}, {
            headers: {
              Authorization: `Bearer ${refreshToken}`
            }
          })
          
          const newToken = response.data.access_token
          localStorage.setItem('access_token', newToken)
          
          // 重新發送原始請求
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return api(originalRequest)
          
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError)
          
          // 清除令牌並重定向到登入頁面
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          router.push('/login')
          
          return Promise.reject(refreshError)
        }
      } else {
        // 沒有刷新令牌，重定向到登入頁面
        router.push('/login')
      }
    }
    
    // 處理其他錯誤
    if (error.response?.status >= 500) {
      ElMessage.error('伺服器錯誤，請稍後再試')
    } else if (error.response?.status === 404) {
      ElMessage.error('請求的資源不存在')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('請求超時，請檢查網路連線')
    }
    
    return Promise.reject(error)
  }
)

export default api