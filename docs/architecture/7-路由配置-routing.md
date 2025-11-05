# 7. 路由配置 (Routing)

### 7.1 路由結構 (router/index.js)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/**
 * 路由定義
 */
const routes = [
  // 首頁重定向
  {
    path: '/',
    redirect: '/dashboard'
  },

  // 認證頁面（公開）
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '登入',
      requiresAuth: false,
      layout: 'auth'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: {
      title: '註冊',
      requiresAuth: false,
      layout: 'auth'
    }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/auth/ForgotPassword.vue'),
    meta: {
      title: '忘記密碼',
      requiresAuth: false,
      layout: 'auth'
    }
  },

  // 主應用頁面（需要認證）
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '控制台',
      requiresAuth: true,
      icon: 'House'
    }
  },

  // 個人資料
  {
    path: '/profile/:id?',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: {
      title: '個人資料',
      requiresAuth: true
    }
  },
  {
    path: '/profile/edit',
    name: 'ProfileEdit',
    component: () => import('@/views/ProfileEdit.vue'),
    meta: {
      title: '編輯個人資料',
      requiresAuth: true
    }
  },

  // 活動相關
  {
    path: '/activities',
    name: 'Activities',
    component: () => import('@/views/Activities.vue'),
    meta: {
      title: '活動管理',
      requiresAuth: true,
      icon: 'Calendar'
    }
  },
  {
    path: '/activities/create',
    name: 'CreateActivity',
    component: () => import('@/views/CreateActivity.vue'),
    meta: {
      title: '創建活動',
      requiresAuth: true
    }
  },
  {
    path: '/activities/:id',
    name: 'ActivityDetail',
    component: () => import('@/views/ActivityDetail.vue'),
    meta: {
      title: '活動詳情',
      requiresAuth: true
    },
    props: true
  },

  // 媒合
  {
    path: '/matches',
    name: 'Matches',
    component: () => import('@/views/Matches.vue'),
    meta: {
      title: '媒合管理',
      requiresAuth: true,
      icon: 'UserFilled'
    }
  },

  // 聊天
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: {
      title: '聊天室',
      requiresAuth: true,
      icon: 'ChatDotRound'
    }
  },
  {
    path: '/chat/:id',
    name: 'ChatRoom',
    component: () => import('@/views/Chat.vue'),
    meta: {
      title: '聊天室',
      requiresAuth: true
    },
    props: true
  },

  // 錯誤頁面
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '頁面不存在',
      requiresAuth: false
    }
  },
  {
    path: '/500',
    name: 'ServerError',
    component: () => import('@/views/ServerError.vue'),
    meta: {
      title: '伺服器錯誤',
      requiresAuth: false
    }
  },

  // 404 處理（必須放在最後）
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

/**
 * 創建路由實例
 */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

/**
 * 全域前置守衛 - 認證檢查
 */
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 設置頁面標題
  document.title = to.meta.title 
    ? `${to.meta.title} - EdgeSurvivor` 
    : 'EdgeSurvivor - 邊緣人神器'

  // 檢查是否需要認證
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth) {
    // 需要認證的頁面
    if (!authStore.isAuthenticated) {
      // 未登入，重定向到登入頁
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // 已登入，檢查是否需要獲取用戶資料
      if (!authStore.user) {
        try {
          await authStore.fetchCurrentUser()
          next()
        } catch (error) {
          // 獲取用戶資料失敗，清除認證並重定向
          authStore.logout()
          next('/login')
        }
      } else {
        next()
      }
    }
  } else {
    // 不需要認證的頁面
    if (authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
      // 已登入用戶訪問登入/註冊頁，重定向到控制台
      next('/dashboard')
    } else {
      next()
    }
  }
})

/**
 * 全域後置鉤子 - 追蹤頁面訪問（可選）
 */
router.afterEach((to, from) => {
  // 可以在這裡加入 Google Analytics 或其他追蹤
  // gtag('config', 'GA_MEASUREMENT_ID', {
  //   page_path: to.path
  // })
})

export default router
```

### 7.2 路由守衛使用場景

| 守衛類型 | 使用場景 | 範例 |
|---------|---------|------|
| **beforeEach** | 全域認證檢查、權限驗證 | 未登入用戶重定向到登入頁 |
| **beforeEnter** | 路由級別的權限控制 | 只有組織者可以編輯活動 |
| **beforeRouteEnter** | 組件級別的資料預載入 | 進入頁面前獲取資料 |
| **beforeRouteUpdate** | 參數變化時的處理 | 活動 ID 變化時重新載入 |
| **beforeRouteLeave** | 離開前的確認 | 表單未儲存時的提示 |

### 7.3 路由守衛範例

#### 7.3.1 組件級守衛 - 表單離開確認

```vue
<script setup>
import { ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const formData = ref({})
const isFormDirty = ref(false)

// 表單變更時設置 dirty 狀態
const handleFormChange = () => {
  isFormDirty.value = true
}

// 離開前確認
onBeforeRouteLeave(async (to, from) => {
  if (isFormDirty.value) {
    try {
      await ElMessageBox.confirm(
        '您有未儲存的變更，確定要離開嗎？',
        '提示',
        {
          confirmButtonText: '離開',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      return true
    } catch {
      return false
    }
  }
  return true
})
</script>
```

#### 7.3.2 路由級守衛 - 組織者權限檢查

```javascript
{
  path: '/activities/:id/edit',
  name: 'EditActivity',
  component: () => import('@/views/EditActivity.vue'),
  beforeEnter: async (to, from, next) => {
    const authStore = useAuthStore()
    const activityId = to.params.id
    
    try {
      // 檢查是否為活動組織者
      const response = await getActivityDetail(activityId)
      const activity = response.data
      
      if (activity.organizer_id === authStore.user.id) {
        next()
      } else {
        ElMessage.error('您沒有權限編輯此活動')
        next('/activities')
      }
    } catch (error) {
      next('/404')
    }
  }
}
```

---
