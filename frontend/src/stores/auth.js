import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // 狀態
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const isLoading = ref(false)

  // 計算屬性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userInfo = computed(() => user.value)

  // 設置認證令牌
  const setToken = (accessToken, refreshTokenValue) => {
    token.value = accessToken
    refreshToken.value = refreshTokenValue
    
    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
    } else {
      localStorage.removeItem('access_token')
    }
    
    if (refreshTokenValue) {
      localStorage.setItem('refresh_token', refreshTokenValue)
    } else {
      localStorage.removeItem('refresh_token')
    }
  }

  // 設置用戶資訊
  const setUser = (userData) => {
    user.value = userData
  }

  // 登入
  const login = async (credentials) => {
    try {
      isLoading.value = true
      const response = await api.login(credentials)
      
      if (response.data.access_token) {
        setToken(response.data.access_token, response.data.refresh_token)
        setUser(response.data.user)
        
        ElMessage.success('登入成功！')
        
        // 重定向到控制台
        router.push('/dashboard')
        
        return response.data
      }
    } catch (error) {
      const message = error.response?.data?.error || '登入失敗，請稍後再試'
      ElMessage.error(message)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 註冊
  const register = async (userData) => {
    try {
      isLoading.value = true
      const response = await api.register(userData)
      
      if (response.data.access_token) {
        setToken(response.data.access_token, response.data.refresh_token)
        setUser(response.data.user)
        
        ElMessage.success('註冊成功！歡迎加入 EdgeSurvivor！')
        
        // 重定向到控制台
        router.push('/dashboard')
        
        return response.data
      }
    } catch (error) {
      const message = error.response?.data?.error || '註冊失敗，請稍後再試'
      ElMessage.error(message)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await api.logout()
    } catch (error) {
      console.error('Logout API call failed:', error)
    } finally {
      // 清除本地狀態
      setToken(null, null)
      setUser(null)
      
      ElMessage.info('已登出')
      
      // 重定向到首頁
      router.push('/')
    }
  }

  // 獲取當前用戶資訊
  const fetchCurrentUser = async () => {
    try {
      if (!token.value) {
        throw new Error('No token available')
      }
      
      const response = await api.getCurrentUser()
      setUser(response.data.user)
      
      return response.data.user
    } catch (error) {
      console.error('Failed to fetch current user:', error)
      
      // 如果令牌無效，清除認證狀態
      if (error.response?.status === 401) {
        setToken(null, null)
        setUser(null)
      }
      
      throw error
    }
  }

  // 刷新令牌
  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available')
      }
      
      const response = await api.refreshToken()
      setToken(response.data.access_token, refreshToken.value)
      
      return response.data.access_token
    } catch (error) {
      console.error('Failed to refresh token:', error)
      
      // 刷新失敗，清除認證狀態
      setToken(null, null)
      setUser(null)
      
      // 重定向到登入頁面
      router.push('/login')
      
      throw error
    }
  }

  // 更新用戶資訊
  const updateUser = (userData) => {
    if (user.value) {
      user.value = { ...user.value, ...userData }
    }
  }

  // 修改密碼
  const changePassword = async (passwords) => {
    try {
      isLoading.value = true
      const response = await api.changePassword(passwords)
      
      ElMessage.success('密碼修改成功！')
      
      return response.data
    } catch (error) {
      const message = error.response?.data?.error || '密碼修改失敗，請稍後再試'
      ElMessage.error(message)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 檢查認證狀態
  const checkAuthStatus = () => {
    return !!token.value && !!user.value
  }

  return {
    // 狀態
    user: userInfo,
    token,
    isLoading,
    
    // 計算屬性
    isAuthenticated,
    
    // 方法
    login,
    register,
    logout,
    fetchCurrentUser,
    refreshAccessToken,
    updateUser,
    changePassword,
    checkAuthStatus,
    setToken,
    setUser
  }
})