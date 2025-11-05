# 5. 狀態管理 (State Management)

### 5.1 Pinia Store 結構

```plaintext
stores/
├── index.js              # Store 匯總（可選）
├── auth.js               # 認證狀態
├── app.js                # 應用全域狀態
├── activities.js         # 活動狀態
├── chat.js               # 聊天狀態
└── matches.js            # 媒合狀態
```

### 5.2 Store 模板範例

#### 5.2.1 認證 Store (auth.js)

```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginApi, logoutApi, getCurrentUser } from '@/api/auth'
import Cookies from 'js-cookie'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const accessToken = ref(Cookies.get('access_token') || null)
  const refreshToken = ref(Cookies.get('refresh_token') || null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const userRole = computed(() => user.value?.role || 'guest')
  const userName = computed(() => user.value?.name || '')
  const userAvatar = computed(() => user.value?.avatar || '/default-avatar.png')

  // Actions
  /**
   * 登入
   * @param {Object} credentials - { email, password }
   */
  const login = async (credentials) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await loginApi(credentials)
      const { access_token, refresh_token, user: userData } = response.data

      // 儲存 Token
      accessToken.value = access_token
      refreshToken.value = refresh_token
      Cookies.set('access_token', access_token, { expires: 7 })
      Cookies.set('refresh_token', refresh_token, { expires: 30 })

      // 儲存用戶資料
      user.value = userData

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '登入失敗'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 登出
   */
  const logout = async () => {
    try {
      await logoutApi()
    } catch (err) {
      console.error('登出 API 失敗:', err)
    } finally {
      // 清除狀態
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      Cookies.remove('access_token')
      Cookies.remove('refresh_token')

      // 跳轉到登入頁
      router.push('/login')
    }
  }

  /**
   * 獲取當前用戶資料
   */
  const fetchCurrentUser = async () => {
    if (!accessToken.value) return

    try {
      isLoading.value = true
      const response = await getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('獲取用戶資料失敗:', err)
      // Token 可能過期，清除認證狀態
      logout()
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 更新用戶資料
   */
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
  }

  /**
   * 重置錯誤
   */
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    userRole,
    userName,
    userAvatar,
    // Actions
    login,
    logout,
    fetchCurrentUser,
    updateUser,
    clearError
  }
})
```

#### 5.2.2 應用全域 Store (app.js)

```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const sidebarCollapsed = ref(false)
  const theme = ref(localStorage.getItem('theme') || 'light')
  const notifications = ref([])
  const unreadCount = ref(0)

  // Actions
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  const addNotification = (notification) => {
    notifications.value.unshift({
      id: Date.now(),
      timestamp: new Date(),
      read: false,
      ...notification
    })
    unreadCount.value++
  }

  const markAsRead = (notificationId) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification && !notification.read) {
      notification.read = true
      unreadCount.value--
    }
  }

  const markAllAsRead = () => {
    notifications.value.forEach(n => n.read = true)
    unreadCount.value = 0
  }

  const clearNotifications = () => {
    notifications.value = []
    unreadCount.value = 0
  }

  return {
    // State
    sidebarCollapsed,
    theme,
    notifications,
    unreadCount,
    // Actions
    toggleSidebar,
    setTheme,
    addNotification,
    markAsRead,
    markAllAsRead,
    clearNotifications
  }
})
```

### 5.3 Store 使用範例

```vue
<script setup>
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

// 使用 Store
const authStore = useAuthStore()
const appStore = useAppStore()

// 解構響應式狀態（必須使用 storeToRefs）
const { user, isAuthenticated } = storeToRefs(authStore)
const { theme, unreadCount } = storeToRefs(appStore)

// 直接使用 Actions（不需要 storeToRefs）
const { login, logout } = authStore
const { setTheme, addNotification } = appStore

// 使用範例
const handleLogin = async () => {
  const result = await login({ email: 'test@example.com', password: '123456' })
  if (result.success) {
    addNotification({ type: 'success', message: '登入成功！' })
  }
}
</script>
```

---
