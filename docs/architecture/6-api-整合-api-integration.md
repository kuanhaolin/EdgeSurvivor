# 6. API 整合 (API Integration)

### 6.1 Axios 配置 (utils/axios.js)

```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

// 創建 Axios 實例
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
instance.interceptors.request.use(
  (config) => {
    // 添加 JWT Token
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }

    // 顯示載入動畫（可選）
    // ElLoading.service({ fullscreen: true })

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 響應攔截器
instance.interceptors.response.use(
  (response) => {
    // 隱藏載入動畫
    // ElLoading.service().close()

    return response
  },
  async (error) => {
    // 隱藏載入動畫
    // ElLoading.service().close()

    const authStore = useAuthStore()

    // 處理不同的錯誤狀態碼
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Token 過期或無效
          ElMessage.error('登入已過期，請重新登入')
          authStore.logout()
          router.push('/login')
          break

        case 403:
          // 權限不足
          ElMessage.error('您沒有權限執行此操作')
          break

        case 404:
          // 資源不存在
          ElMessage.error('請求的資源不存在')
          break

        case 422:
          // 表單驗證錯誤
          const errorMessage = data.errors 
            ? Object.values(data.errors).flat().join(', ')
            : data.message || '表單驗證失敗'
          ElMessage.error(errorMessage)
          break

        case 500:
          // 伺服器錯誤
          ElMessage.error('伺服器錯誤，請稍後再試')
          break

        default:
          ElMessage.error(data.message || '請求失敗')
      }
    } else if (error.request) {
      // 網路錯誤
      ElMessage.error('網路連線失敗，請檢查網路設定')
    } else {
      // 其他錯誤
      ElMessage.error('發生未知錯誤')
    }

    return Promise.reject(error)
  }
)

export default instance
```

### 6.2 API 服務模板 (api/activities.js)

```javascript
import axios from '@/utils/axios'

/**
 * 活動相關 API
 */

/**
 * 獲取活動列表
 * @param {Object} params - 查詢參數
 * @param {string} params.search - 搜尋關鍵字
 * @param {string} params.type - 活動類型
 * @param {string} params.status - 活動狀態
 * @param {number} params.page - 頁碼
 * @param {number} params.per_page - 每頁數量
 * @returns {Promise}
 */
export const getActivities = (params = {}) => {
  return axios.get('/activities', { params })
}

/**
 * 獲取活動詳情
 * @param {number} activityId - 活動 ID
 * @returns {Promise}
 */
export const getActivityDetail = (activityId) => {
  return axios.get(`/activities/${activityId}`)
}

/**
 * 創建活動
 * @param {Object} data - 活動資料
 * @returns {Promise}
 */
export const createActivity = (data) => {
  return axios.post('/activities', data)
}

/**
 * 更新活動
 * @param {number} activityId - 活動 ID
 * @param {Object} data - 更新資料
 * @returns {Promise}
 */
export const updateActivity = (activityId, data) => {
  return axios.put(`/activities/${activityId}`, data)
}

/**
 * 刪除活動
 * @param {number} activityId - 活動 ID
 * @returns {Promise}
 */
export const deleteActivity = (activityId) => {
  return axios.delete(`/activities/${activityId}`)
}

/**
 * 申請加入活動
 * @param {number} activityId - 活動 ID
 * @param {Object} data - 申請資料 { message }
 * @returns {Promise}
 */
export const joinActivity = (activityId, data = {}) => {
  return axios.post(`/activities/${activityId}/join`, data)
}

/**
 * 獲取參與者列表
 * @param {number} activityId - 活動 ID
 * @returns {Promise}
 */
export const getParticipants = (activityId) => {
  return axios.get(`/activities/${activityId}/participants`)
}

/**
 * 審核參與者申請
 * @param {number} activityId - 活動 ID
 * @param {number} userId - 用戶 ID
 * @param {string} status - 審核狀態 ('approved' | 'rejected')
 * @returns {Promise}
 */
export const reviewParticipant = (activityId, userId, status) => {
  return axios.post(`/activities/${activityId}/participants/${userId}/review`, {
    status
  })
}

/**
 * 上傳活動封面圖
 * @param {number} activityId - 活動 ID
 * @param {File} file - 圖片文件
 * @returns {Promise}
 */
export const uploadActivityCover = (activityId, file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return axios.post(`/activities/${activityId}/cover`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
```

### 6.3 API 使用範例

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { getActivities, joinActivity } from '@/api/activities'
import { ElMessage } from 'element-plus'

const activities = ref([])
const loading = ref(false)
const filters = ref({
  search: '',
  type: '',
  status: '招募中',
  page: 1,
  per_page: 12
})

// 獲取活動列表
const fetchActivities = async () => {
  try {
    loading.value = true
    const response = await getActivities(filters.value)
    activities.value = response.data.data
  } catch (error) {
    // 錯誤已在 Axios 攔截器處理
    console.error('獲取活動列表失敗:', error)
  } finally {
    loading.value = false
  }
}

// 申請加入活動
const handleJoinActivity = async (activityId) => {
  try {
    await joinActivity(activityId, {
      message: '您好，我對這個活動很感興趣！'
    })
    ElMessage.success('申請已送出，請等待組織者審核')
    // 重新獲取列表以更新狀態
    fetchActivities()
  } catch (error) {
    console.error('申請加入失敗:', error)
  }
}

onMounted(() => {
  fetchActivities()
})
</script>
```

---
