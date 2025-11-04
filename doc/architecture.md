# EdgeSurvivor 前端技術架構文件
# 邊緣人神器 - 旅伴媒合平台前端架構

**Version:** 1.0  
**Status:** Active  
**Date:** 2025-11-03  
**Owner:** Winston (Architect)

---

## 變更日誌 (Change Log)

| 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|
| 2025-11-03 | 1.0 | 初始前端架構文件，基於 PRD v1.0 和 UI/UX 規格 v1.0 | Winston (Architect) |

---

## 1. 簡介 (Introduction)

本文件定義 EdgeSurvivor（邊緣人神器）的前端技術架構，包含技術棧選擇、專案結構、編碼標準、狀態管理、API 整合、路由設計、樣式指南、測試策略等。

### 1.1 架構目標

1. **開發效率**：使用現代化的開發工具鏈，提供快速的熱重載和開發體驗
2. **可維護性**：清晰的專案結構、一致的編碼規範、模組化的組件設計
3. **效能優化**：達成 UX 規格定義的效能目標（LCP < 2.5s, FID < 100ms, CLS < 0.1）
4. **可擴展性**：支援未來功能擴展，易於新增頁面和組件
5. **開發者體驗**：提供完善的 TypeScript 支援、程式碼提示、自動化測試
6. **無障礙性**：符合 WCAG 2.1 Level AA 標準

### 1.2 技術決策原則

- **成熟穩定**：選擇經過生產環境驗證的技術棧
- **社群活躍**：優先選擇有活躍社群支援的框架和函式庫
- **文件完善**：技術選型需有完整的官方文件和豐富的教學資源
- **性能優先**：關注首屏載入速度和執行時效能
- **開發體驗**：提供良好的 DX（Developer Experience）

---

## 2. 前端技術棧 (Frontend Tech Stack)

### 2.1 技術棧總覽表

| 類別 | 技術 | 版本 | 用途 | 選擇理由 |
|------|------|------|------|---------|
| **核心框架** | Vue.js | 3.3.8+ | 前端 UI 框架 | 漸進式框架、Composition API、優秀的效能、豐富的生態系統 |
| **UI 組件庫** | Element Plus | 2.4.2+ | 企業級 UI 組件庫 | 完整的組件集、優秀的設計、活躍的社群、良好的 Vue 3 支援 |
| **狀態管理** | Pinia | 2.1.7+ | 應用狀態管理 | Vue 3 官方推薦、TypeScript 友善、模組化設計、DevTools 支援 |
| **路由** | Vue Router | 4.2.5+ | 單頁應用路由 | Vue 官方路由、支援嵌套路由、路由守衛、懶載入 |
| **建構工具** | Vite | 4.5.3+ | 開發伺服器與打包工具 | 極快的冷啟動、HMR、原生 ESM、優化的打包輸出 |
| **HTTP 客戶端** | Axios | 1.6.0+ | HTTP 請求函式庫 | 攔截器支援、Promise API、廣泛使用、易於測試 |
| **即時通訊** | Socket.IO Client | 4.7.4+ | WebSocket 客戶端 | 自動重連、房間機制、與後端 Flask-SocketIO 完美配合 |
| **樣式方案** | SCSS + CSS Variables | - | CSS 預處理器與主題系統 | 支援嵌套、變數、混合；CSS Variables 支援動態主題 |
| **日期處理** | Day.js | 1.11.10+ | 日期格式化與處理 | 輕量（僅 2KB）、Moment.js 替代方案、豐富的 API |
| **圖示庫** | Element Plus Icons | 2.1.0+ | 圖示組件 | 與 Element Plus 集成、SVG 圖示、Tree-shakable |
| **Cookie 管理** | js-cookie | 3.0.5+ | Cookie 操作 | 輕量、簡單的 API、跨瀏覽器相容 |
| **程式碼規範** | ESLint + Prettier | 8.54.0+ | 程式碼檢查與格式化 | 統一程式碼風格、自動修復、Vue 3 支援 |
| **測試框架** | Vitest (建議) | - | 單元測試 | Vite 原生整合、快速執行、與 Jest API 相容 |
| **E2E 測試** | Playwright (建議) | - | 端到端測試 | 跨瀏覽器、自動等待、強大的選擇器 |

### 2.2 瀏覽器支援

根據 PRD 的 NFR3.1 要求：

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Browserslist 配置**：
```
> 1%
last 2 versions
not dead
not ie 11
```

---

## 3. 專案結構 (Project Structure)

### 3.1 目錄結構

```plaintext
frontend/
├── public/                          # 靜態資源（不經過 Webpack 處理）
│   ├── favicon.ico                  # 網站圖示
│   ├── main.js                      # 公共 JS（如果需要）
│   └── images/                      # 靜態圖片
├── src/                             # 源代碼目錄
│   ├── main.js                      # 應用入口
│   ├── App.vue                      # 根組件
│   │
│   ├── api/                         # API 服務層
│   │   ├── index.js                 # API 客戶端配置與實例
│   │   ├── auth.js                  # 認證相關 API
│   │   ├── activities.js            # 活動相關 API
│   │   ├── matches.js               # 媒合相關 API
│   │   ├── chat.js                  # 聊天相關 API
│   │   ├── expenses.js              # 費用相關 API
│   │   ├── reviews.js               # 評價相關 API
│   │   ├── users.js                 # 用戶相關 API
│   │   └── upload.js                # 檔案上傳 API
│   │
│   ├── components/                  # 可重用組件
│   │   ├── common/                  # 通用組件
│   │   │   ├── LoadingSpinner.vue   # 載入動畫
│   │   │   ├── EmptyState.vue       # 空狀態
│   │   │   ├── ErrorMessage.vue     # 錯誤訊息
│   │   │   ├── ConfirmDialog.vue    # 確認對話框
│   │   │   └── Pagination.vue       # 分頁器
│   │   │
│   │   ├── layout/                  # 佈局組件
│   │   │   ├── NavBar.vue           # 導航欄
│   │   │   ├── SideBar.vue          # 側邊欄
│   │   │   ├── Footer.vue           # 頁腳
│   │   │   └── AppLayout.vue        # 應用佈局容器
│   │   │
│   │   ├── chat/                    # 聊天相關組件
│   │   │   ├── ChatList.vue         # 聊天列表
│   │   │   ├── ChatWindow.vue       # 聊天視窗
│   │   │   ├── MessageBubble.vue    # 訊息氣泡
│   │   │   └── MessageInput.vue     # 訊息輸入框
│   │   │
│   │   ├── activity/                # 活動相關組件
│   │   │   ├── ActivityCard.vue     # 活動卡片
│   │   │   ├── ActivityForm.vue     # 活動表單
│   │   │   ├── ActivityFilters.vue  # 活動篩選器
│   │   │   └── ParticipantList.vue  # 參與者列表
│   │   │
│   │   ├── ActivityDiscussion.vue   # 活動討論串
│   │   ├── ActivityReviews.vue      # 活動評價
│   │   ├── ExpenseManager.vue       # 費用管理器
│   │   └── ImageUploader.vue        # 圖片上傳器
│   │
│   ├── views/                       # 頁面視圖（路由對應）
│   │   ├── auth/                    # 認證頁面
│   │   │   ├── Login.vue            # 登入頁
│   │   │   ├── Register.vue         # 註冊頁
│   │   │   └── ForgotPassword.vue   # 忘記密碼頁
│   │   │
│   │   ├── Dashboard.vue            # 控制台
│   │   ├── Profile.vue              # 個人資料頁
│   │   ├── ProfileEdit.vue          # 編輯個人資料
│   │   │
│   │   ├── Activities.vue           # 活動列表頁
│   │   ├── ActivityDetail.vue       # 活動詳情頁
│   │   ├── CreateActivity.vue       # 建立活動頁
│   │   │
│   │   ├── Matches.vue              # 媒合列表頁
│   │   ├── Chat.vue                 # 聊天頁
│   │   │
│   │   ├── NotFound.vue             # 404 頁面
│   │   └── ServerError.vue          # 500 錯誤頁
│   │
│   ├── router/                      # 路由配置
│   │   └── index.js                 # 路由定義與守衛
│   │
│   ├── stores/                      # Pinia 狀態管理
│   │   ├── auth.js                  # 認證狀態
│   │   ├── app.js                   # 應用全域狀態
│   │   ├── activities.js            # 活動狀態
│   │   ├── chat.js                  # 聊天狀態
│   │   └── index.js                 # Store 匯總（如需要）
│   │
│   ├── services/                    # 業務邏輯服務
│   │   ├── socket.js                # Socket.IO 服務
│   │   ├── notification.js          # 通知服務
│   │   └── storage.js               # LocalStorage 服務
│   │
│   ├── utils/                       # 工具函數
│   │   ├── axios.js                 # Axios 實例與攔截器
│   │   ├── validators.js            # 表單驗證器
│   │   ├── formatters.js            # 格式化工具
│   │   ├── helpers.js               # 通用輔助函數
│   │   └── constants.js             # 常數定義
│   │
│   ├── styles/                      # 全域樣式
│   │   ├── theme.css                # 主題變數（CSS Variables）
│   │   ├── global.scss              # 全域樣式
│   │   ├── mixins.scss              # SCSS Mixins
│   │   ├── animations.scss          # 動畫定義
│   │   └── utilities.scss           # 工具類
│   │
│   ├── composables/                 # Vue 3 組合式函數
│   │   ├── useAuth.js               # 認證邏輯
│   │   ├── useSocket.js             # Socket 連接邏輯
│   │   ├── useForm.js               # 表單處理邏輯
│   │   └── useInfiniteScroll.js     # 無限滾動邏輯
│   │
│   ├── directives/                  # 自定義指令
│   │   ├── v-lazy.js                # 圖片懶載入
│   │   └── v-permission.js          # 權限控制
│   │
│   ├── types/                       # TypeScript 類型定義（如使用 TS）
│   │   ├── api.d.ts                 # API 回應類型
│   │   ├── models.d.ts              # 資料模型類型
│   │   └── index.d.ts               # 類型匯總
│   │
│   └── assets/                      # 資源文件（經過 Webpack 處理）
│       ├── images/                  # 圖片資源
│       ├── fonts/                   # 字型文件
│       └── icons/                   # SVG 圖示
│
├── tests/                           # 測試文件
│   ├── unit/                        # 單元測試
│   │   ├── components/              # 組件測試
│   │   └── utils/                   # 工具函數測試
│   ├── integration/                 # 整合測試
│   └── e2e/                         # 端到端測試
│
├── .env.development                 # 開發環境變數
├── .env.production                  # 生產環境變數
├── .env.test                        # 測試環境變數
├── .eslintrc.js                     # ESLint 配置
├── .prettierrc                      # Prettier 配置
├── vite.config.js                   # Vite 配置
├── package.json                     # 專案依賴與腳本
└── README.md                        # 專案說明
```

### 3.2 目錄職責說明

| 目錄 | 職責 | 範例 |
|------|------|------|
| **api/** | 封裝所有後端 API 請求 | `api/activities.js` 包含 `getActivities()`, `createActivity()` |
| **components/** | 可重用的 UI 組件 | `ActivityCard.vue`, `ChatWindow.vue` |
| **views/** | 路由對應的頁面組件 | `Dashboard.vue`, `ActivityDetail.vue` |
| **stores/** | Pinia 狀態管理 | `auth.js` 管理認證狀態 |
| **services/** | 業務邏輯服務（非 API） | `socket.js` 管理 Socket.IO 連接 |
| **utils/** | 純工具函數 | `formatters.js` 提供日期、金額格式化 |
| **composables/** | Vue 3 可重用邏輯 | `useAuth.js` 提供認證相關的響應式邏輯 |
| **router/** | Vue Router 配置 | 路由定義、守衛、懶載入 |
| **styles/** | 全域樣式與主題 | `theme.css` 定義 CSS Variables |

---

## 4. 組件標準 (Component Standards)

### 4.1 組件命名規範

#### 4.1.1 文件命名

- **PascalCase**：所有 Vue 組件文件使用 PascalCase 命名
- **語意化**：名稱應清楚描述組件用途

```
✅ 正確：
  - ActivityCard.vue
  - ChatWindow.vue
  - ImageUploader.vue

❌ 錯誤：
  - activityCard.vue
  - chat-window.vue
  - img-uploader.vue
```

#### 4.1.2 組件名稱規則

| 類型 | 規則 | 範例 |
|------|------|------|
| **基礎組件** | 以 `Base` 開頭 | `BaseButton.vue`, `BaseInput.vue` |
| **單一實例組件** | 以 `The` 開頭 | `TheNavBar.vue`, `TheSidebar.vue` |
| **緊密耦合組件** | 以父組件名稱開頭 | `ActivityCard.vue` → `ActivityCardActions.vue` |
| **頁面組件** | 描述性名稱 | `Dashboard.vue`, `ActivityDetail.vue` |

#### 4.1.3 組件註冊

```javascript
// ✅ 全域註冊（main.js）- 僅用於基礎組件
import BaseButton from '@/components/common/BaseButton.vue'
app.component('BaseButton', BaseButton)

// ✅ 局部註冊（推薦）
import ActivityCard from '@/components/activity/ActivityCard.vue'
export default {
  components: { ActivityCard }
}

// ✅ 使用時採用 PascalCase
<ActivityCard :activity="activity" />
```

### 4.2 組件模板範例

#### 4.2.1 基礎組件模板（Composition API）

```vue
<template>
  <div class="activity-card" :class="cardClasses">
    <!-- 封面圖 -->
    <div v-if="activity.cover_image" class="activity-card__cover">
      <img :src="activity.cover_image" :alt="activity.title" loading="lazy" />
    </div>

    <!-- 內容區 -->
    <div class="activity-card__content">
      <div class="activity-card__header">
        <h3 class="activity-card__title">{{ activity.title }}</h3>
        <el-tag :type="statusTagType" size="small">
          {{ activity.status }}
        </el-tag>
      </div>

      <div class="activity-card__info">
        <div class="info-item">
          <el-icon><Calendar /></el-icon>
          <span>{{ formattedDate }}</span>
        </div>
        <div class="info-item">
          <el-icon><Location /></el-icon>
          <span>{{ activity.location }}</span>
        </div>
        <div class="info-item">
          <el-icon><User /></el-icon>
          <span>{{ participantsText }}</span>
        </div>
      </div>

      <p class="activity-card__description">
        {{ truncatedDescription }}
      </p>
    </div>

    <!-- 操作區 -->
    <div class="activity-card__actions">
      <el-button type="primary" @click="handleViewDetail">
        查看詳情
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Calendar, Location, User } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

// Props
const props = defineProps({
  activity: {
    type: Object,
    required: true,
    validator: (value) => {
      return value.id && value.title && value.status
    }
  },
  truncateLength: {
    type: Number,
    default: 100
  }
})

// Emits
const emit = defineEmits(['view-detail'])

// Router
const router = useRouter()

// Computed
const formattedDate = computed(() => {
  return dayjs(props.activity.start_date).format('YYYY-MM-DD')
})

const participantsText = computed(() => {
  const current = props.activity.current_participants || 0
  const max = props.activity.max_participants || 0
  return `${current}/${max} 人`
})

const truncatedDescription = computed(() => {
  const desc = props.activity.description || ''
  if (desc.length <= props.truncateLength) {
    return desc
  }
  return desc.substring(0, props.truncateLength) + '...'
})

const statusTagType = computed(() => {
  const statusMap = {
    '招募中': 'success',
    '進行中': 'warning',
    '已完成': 'info',
    '已取消': 'danger'
  }
  return statusMap[props.activity.status] || 'info'
})

const cardClasses = computed(() => ({
  'activity-card--clickable': true,
  'activity-card--featured': props.activity.is_featured
}))

// Methods
const handleViewDetail = () => {
  emit('view-detail', props.activity.id)
  router.push(`/activities/${props.activity.id}`)
}
</script>

<style lang="scss" scoped>
.activity-card {
  background: var(--el-bg-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--el-box-shadow-light);
  overflow: hidden;
  transition: all 0.3s var(--el-transition-function);

  &--clickable {
    cursor: pointer;

    &:hover {
      transform: translateY(-4px);
      box-shadow: var(--el-box-shadow-dark);
    }
  }

  &__cover {
    width: 100%;
    height: 200px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: var(--spacing-md);
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-sm);
  }

  &__title {
    font-size: var(--font-size-h4);
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin: 0;
    flex: 1;
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-sm);

    .info-item {
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
      font-size: var(--font-size-small);
      color: var(--el-text-color-secondary);

      .el-icon {
        font-size: 16px;
      }
    }
  }

  &__description {
    font-size: var(--font-size-body);
    color: var(--el-text-color-regular);
    line-height: 1.6;
    margin: 0;
  }

  &__actions {
    padding: var(--spacing-md);
    border-top: 1px solid var(--el-border-color-lighter);
  }
}

// 響應式
@media (max-width: 640px) {
  .activity-card {
    &__cover {
      height: 150px;
    }
  }
}
</style>
```

### 4.3 組件編寫最佳實踐

#### 4.3.1 組件結構順序

```vue
<template>
  <!-- 模板內容 -->
</template>

<script setup>
// 1. 導入
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 2. Props
const props = defineProps({...})

// 3. Emits
const emit = defineEmits(['event-name'])

// 4. 響應式數據
const data = ref(null)

// 5. Computed
const computed = computed(() => {...})

// 6. Methods
const handleClick = () => {...}

// 7. 生命週期
onMounted(() => {...})
</script>

<style lang="scss" scoped>
/* 樣式內容 */
</style>
```

#### 4.3.2 Props 定義規範

```javascript
// ✅ 完整的 Props 定義
const props = defineProps({
  // 基本類型
  title: {
    type: String,
    required: true
  },
  
  // 帶預設值
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  
  // 對象類型（提供預設值工廠函數）
  user: {
    type: Object,
    default: () => ({})
  },
  
  // 數組類型
  items: {
    type: Array,
    default: () => []
  },
  
  // 多種類型
  value: {
    type: [String, Number],
    default: ''
  }
})

// ❌ 避免：缺少類型定義
const props = defineProps(['title', 'size'])
```

#### 4.3.3 Emits 定義規範

```javascript
// ✅ 定義並驗證 Emits
const emit = defineEmits({
  // 帶驗證
  submit: (payload) => {
    return payload && typeof payload.id === 'number'
  },
  
  // 不帶驗證
  cancel: null,
  
  // 事件名稱使用 kebab-case
  'update:modelValue': (value) => typeof value === 'string'
})

// 使用
emit('submit', { id: 1, name: 'Test' })
emit('update:modelValue', 'new value')

// ❌ 避免：直接 emit 未定義的事件
this.$emit('unknownEvent')
```

---

## 5. 狀態管理 (State Management)

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

## 6. API 整合 (API Integration)

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

## 7. 路由配置 (Routing)

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

## 8. 樣式指南 (Styling Guidelines)

### 8.1 CSS 變數系統 (styles/theme.css)

```css
/**
 * EdgeSurvivor 主題變數系統
 * 基於 UX 規格的設計系統
 */

:root {
  /* ========== 色彩系統 ========== */
  
  /* 主色調 */
  --color-primary: #667eea;
  --color-primary-light: #818cf8;
  --color-primary-dark: #5b63d3;
  --color-secondary: #764ba2;
  --color-secondary-light: #9d6cc1;
  --color-secondary-dark: #5e3a7f;

  /* 功能色 */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #3b82f6;

  /* 中性色 - Light Mode */
  --color-text-primary: #1f2937;
  --color-text-secondary: #6b7280;
  --color-text-disabled: #9ca3af;
  --color-border: #e5e7eb;
  --color-divider: #f3f4f6;
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;

  /* 漸變色 */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-success: linear-gradient(135deg, #4ade80 0%, #10b981 100%);
  --gradient-info: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);

  /* ========== 間距系統 ========== */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* ========== 字體系統 ========== */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
                 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 
                 'Helvetica Neue', 'Microsoft YaHei', '微软雅黑', sans-serif;
  --font-family-mono: 'Courier New', Courier, monospace;

  /* 字級 */
  --font-size-h1: 32px;
  --font-size-h2: 24px;
  --font-size-h3: 20px;
  --font-size-h4: 18px;
  --font-size-body: 16px;
  --font-size-small: 14px;
  --font-size-caption: 12px;

  /* 字重 */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* 行高 */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;

  /* ========== 圓角系統 ========== */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  --border-radius-2xl: 24px;
  --border-radius-full: 9999px;

  /* ========== 陰影系統 ========== */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

  /* ========== 過渡系統 ========== */
  --transition-fast: 150ms;
  --transition-base: 250ms;
  --transition-slow: 350ms;
  --transition-function: cubic-bezier(0.4, 0, 0.2, 1);

  /* ========== Z-Index 系統 ========== */
  --z-index-dropdown: 1000;
  --z-index-sticky: 1020;
  --z-index-fixed: 1030;
  --z-index-modal-backdrop: 1040;
  --z-index-modal: 1050;
  --z-index-popover: 1060;
  --z-index-tooltip: 1070;
}

/* ========== Dark Mode ========== */
[data-theme='dark'] {
  /* 中性色 - Dark Mode */
  --color-text-primary: #f9fafb;
  --color-text-secondary: #d1d5db;
  --color-text-disabled: #6b7280;
  --color-border: #374151;
  --color-divider: #1f2937;
  --color-bg-primary: #111827;
  --color-bg-secondary: #1f2937;
  --color-bg-tertiary: #374151;
}

/* ========== 響應式字級調整 ========== */
@media (max-width: 640px) {
  :root {
    --font-size-h1: 28px;
    --font-size-h2: 22px;
    --font-size-h3: 18px;
    --font-size-h4: 16px;
    --font-size-body: 14px;
    --font-size-small: 12px;
    --font-size-caption: 11px;
  }
}
```

### 8.2 全域樣式 (styles/global.scss)

```scss
/**
 * 全域樣式
 */

// 導入變數
@import './mixins.scss';

// 重置與基礎樣式
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  line-height: var(--line-height-normal);
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  min-height: 100vh;
}

// 標題樣式
h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-md);
}

h2 {
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-sm);
}

h3 {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-sm);
}

h4 {
  font-size: var(--font-size-h4);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-xs);
}

// 連結樣式
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast) var(--transition-function);

  &:hover {
    color: var(--color-primary-light);
  }
}

// 按鈕重置
button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

// 輸入框重置
input,
textarea,
select {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

// 列表重置
ul,
ol {
  list-style: none;
}

// 圖片
img {
  max-width: 100%;
  height: auto;
  display: block;
}

// 滾動條樣式（Webkit）
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg-tertiary);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--border-radius-full);

  &:hover {
    background: var(--color-text-disabled);
  }
}

// 選擇文字顏色
::selection {
  background-color: var(--color-primary-light);
  color: white;
}

// 玻璃擬態效果
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

[data-theme='dark'] .glass-effect {
  background: rgba(31, 41, 55, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### 8.3 SCSS Mixins (styles/mixins.scss)

```scss
/**
 * SCSS Mixins
 */

// 響應式斷點
$breakpoints: (
  'mobile': 640px,
  'tablet': 1024px,
  'desktop': 1440px,
);

// 響應式 Mixin
@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (max-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Breakpoint #{$breakpoint} not found.";
  }
}

// Flexbox 居中
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

// Flexbox 列
@mixin flex-column {
  display: flex;
  flex-direction: column;
}

// 文字省略
@mixin text-ellipsis($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

// 清除浮動
@mixin clearfix {
  &::after {
    content: '';
    display: table;
    clear: both;
  }
}

// 絕對定位居中
@mixin absolute-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

// 卡片樣式
@mixin card {
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-md);
}

// 按鈕樣式
@mixin button-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base) var(--transition-function);
  cursor: pointer;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

// 漸變背景
@mixin gradient-bg($gradient) {
  background: $gradient;
  background-size: 200% 200%;
  transition: background-position var(--transition-base) var(--transition-function);

  &:hover {
    background-position: right center;
  }
}

// 使用範例
// .my-card {
//   @include card;
//   @include respond-to('mobile') {
//     padding: var(--spacing-sm);
//   }
// }
```

### 8.4 動畫定義 (styles/animations.scss)

```scss
/**
 * 動畫定義
 */

// 淡入
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// 從下滑入
@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

// 從上滑入
@keyframes slideInDown {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

// 縮放進入
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

// 脈衝
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

// 旋轉
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

// 彈跳
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

// 搖晃
@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-5px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(5px);
  }
}

// 工具類
.fade-in {
  animation: fadeIn var(--transition-base) var(--transition-function);
}

.slide-in-up {
  animation: slideInUp var(--transition-base) var(--transition-function);
}

.slide-in-down {
  animation: slideInDown var(--transition-base) var(--transition-function);
}

.scale-in {
  animation: scaleIn var(--transition-base) var(--transition-function);
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

.rotate {
  animation: rotate 1s linear infinite;
}

.bounce {
  animation: bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.shake {
  animation: shake 0.5s ease-in-out;
}
```

---

## 9. Socket.IO 整合 (services/socket.js)

```javascript
import { io } from 'socket.io-client'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { ElNotification } from 'element-plus'

class SocketService {
  constructor() {
    this.socket = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
  }

  /**
   * 連接到 Socket.IO 伺服器
   */
  connect() {
    const authStore = useAuthStore()
    
    if (!authStore.accessToken) {
      console.warn('無法連接 Socket: 缺少認證 Token')
      return
    }

    const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'

    this.socket = io(socketUrl, {
      auth: {
        token: authStore.accessToken
      },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: this.maxReconnectAttempts
    })

    this.setupEventHandlers()
  }

  /**
   * 設置事件處理器
   */
  setupEventHandlers() {
    const appStore = useAppStore()

    // 連接成功
    this.socket.on('connect', () => {
      console.log('Socket 已連接:', this.socket.id)
      this.reconnectAttempts = 0
    })

    // 連接錯誤
    this.socket.on('connect_error', (error) => {
      console.error('Socket 連接錯誤:', error)
      this.reconnectAttempts++

      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        ElNotification({
          title: '連線失敗',
          message: '無法連接到伺服器，請稍後再試',
          type: 'error'
        })
      }
    })

    // 斷開連接
    this.socket.on('disconnect', (reason) => {
      console.log('Socket 已斷開:', reason)
      
      if (reason === 'io server disconnect') {
        // 伺服器主動斷開，需要手動重連
        this.socket.connect()
      }
    })

    // 重連
    this.socket.on('reconnect', (attemptNumber) => {
      console.log('Socket 重連成功:', attemptNumber)
      ElNotification({
        title: '連線恢復',
        message: '已重新連接到伺服器',
        type: 'success'
      })
    })

    // 新訊息通知
    this.socket.on('new_message', (data) => {
      console.log('收到新訊息:', data)
      appStore.addNotification({
        type: 'message',
        title: '新訊息',
        message: `${data.sender_name}: ${data.message}`,
        data: data
      })
    })

    // 活動更新通知
    this.socket.on('activity_update', (data) => {
      console.log('活動更新:', data)
      appStore.addNotification({
        type: 'activity',
        title: '活動更新',
        message: data.message,
        data: data
      })
    })
  }

  /**
   * 加入聊天室
   */
  joinRoom(roomId) {
    if (!this.socket) {
      console.warn('Socket 未連接')
      return
    }

    this.socket.emit('join', { room: roomId })
    console.log('加入聊天室:', roomId)
  }

  /**
   * 離開聊天室
   */
  leaveRoom(roomId) {
    if (!this.socket) return

    this.socket.emit('leave', { room: roomId })
    console.log('離開聊天室:', roomId)
  }

  /**
   * 發送訊息
   */
  sendMessage(roomId, message) {
    if (!this.socket) {
      console.warn('Socket 未連接')
      return
    }

    return new Promise((resolve, reject) => {
      this.socket.emit('send_message', {
        room: roomId,
        message: message
      }, (response) => {
        if (response.success) {
          resolve(response)
        } else {
          reject(new Error(response.error || '發送失敗'))
        }
      })
    })
  }

  /**
   * 監聽事件
   */
  on(event, callback) {
    if (!this.socket) return

    this.socket.on(event, callback)
  }

  /**
   * 移除事件監聽
   */
  off(event, callback) {
    if (!this.socket) return

    this.socket.off(event, callback)
  }

  /**
   * 斷開連接
   */
  disconnect() {
    if (!this.socket) return

    this.socket.disconnect()
    this.socket = null
    console.log('Socket 已手動斷開')
  }

  /**
   * 檢查連接狀態
   */
  isConnected() {
    return this.socket && this.socket.connected
  }
}

// 導出單例
export default new SocketService()
```

---

## 10. 環境配置 (Environment Configuration)

### 10.1 環境變數定義

EdgeSurvivor 使用 Vite 的環境變數系統。所有環境變數必須以 `VITE_` 開頭才能在客戶端代碼中訪問。

#### 10.1.1 開發環境 (.env.development)

```bash
# API 配置
VITE_API_BASE_URL=http://localhost:5000/api
VITE_API_TARGET=http://localhost:5000
VITE_SOCKET_URL=http://localhost:5000

# 上傳配置
VITE_UPLOAD_URL=http://localhost:5000/uploads
VITE_MAX_FILE_SIZE=16777216

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your-google-client-id-here

# 功能開關
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# 其他
NODE_ENV=development
```

#### 10.1.2 生產環境 (.env.production)

```bash
# API 配置
VITE_API_BASE_URL=https://api.edgesurvivor.com/api
VITE_API_TARGET=https://api.edgesurvivor.com
VITE_SOCKET_URL=https://api.edgesurvivor.com

# 上傳配置
VITE_UPLOAD_URL=https://api.edgesurvivor.com/uploads
VITE_MAX_FILE_SIZE=16777216

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your-production-google-client-id

# 功能開關
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false

# 其他
NODE_ENV=production
```

#### 10.1.3 測試環境 (.env.test)

```bash
# API 配置
VITE_API_BASE_URL=http://localhost:5000/api
VITE_SOCKET_URL=http://localhost:5000

# 功能開關
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# 其他
NODE_ENV=test
```

### 10.2 環境變數使用範例

```javascript
// ✅ 在代碼中訪問環境變數
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
const mode = import.meta.env.MODE

// ✅ 使用範例
if (import.meta.env.VITE_ENABLE_DEBUG) {
  console.log('Debug mode enabled')
}

// ❌ 避免：未以 VITE_ 開頭的變數無法訪問
const secret = import.meta.env.SECRET_KEY // undefined
```

### 10.3 TypeScript 類型定義（可選）

創建 `src/vite-env.d.ts`：

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TARGET: string
  readonly VITE_SOCKET_URL: string
  readonly VITE_UPLOAD_URL: string
  readonly VITE_MAX_FILE_SIZE: string
  readonly VITE_GOOGLE_CLIENT_ID: string
  readonly VITE_ENABLE_ANALYTICS: string
  readonly VITE_ENABLE_DEBUG: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

---

## 11. 測試策略 (Testing Requirements)

### 11.1 測試金字塔

```
         /\
        /  \  E2E Tests (5%)
       /____\
      /      \
     / Integration Tests (15%)
    /________\
   /          \
  / Unit Tests (80%)
 /____________\
```

### 11.2 單元測試設置

#### 11.2.1 安裝 Vitest

```bash
npm install -D vitest @vue/test-utils jsdom @vitest/ui
```

#### 11.2.2 Vitest 配置 (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.spec.js',
        '**/*.test.js'
      ]
    }
  }
})
```

#### 11.2.3 組件測試模板

```javascript
// tests/unit/components/ActivityCard.spec.js
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ActivityCard from '@/components/activity/ActivityCard.vue'
import ElementPlus from 'element-plus'

describe('ActivityCard.vue', () => {
  // Setup
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  // 測試案例 1: 正確渲染
  it('renders activity information correctly', () => {
    const activity = {
      id: 1,
      title: '陽明山登山之旅',
      status: '招募中',
      start_date: '2025-11-10',
      location: '陽明山',
      current_participants: 3,
      max_participants: 10,
      description: '一起去爬山吧！'
    }

    const wrapper = mount(ActivityCard, {
      props: { activity },
      global: {
        plugins: [ElementPlus]
      }
    })

    expect(wrapper.text()).toContain('陽明山登山之旅')
    expect(wrapper.text()).toContain('招募中')
    expect(wrapper.text()).toContain('陽明山')
    expect(wrapper.text()).toContain('3/10 人')
  })

  // 測試案例 2: 點擊事件
  it('emits view-detail event when button clicked', async () => {
    const activity = {
      id: 1,
      title: 'Test Activity',
      status: '招募中'
    }

    const wrapper = mount(ActivityCard, {
      props: { activity },
      global: {
        plugins: [ElementPlus]
      }
    })

    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('view-detail')).toBeTruthy()
    expect(wrapper.emitted('view-detail')[0]).toEqual([1])
  })

  // 測試案例 3: 描述截斷
  it('truncates long description', () => {
    const longDescription = 'A'.repeat(150)
    const activity = {
      id: 1,
      title: 'Test',
      status: '招募中',
      description: longDescription
    }

    const wrapper = mount(ActivityCard, {
      props: { 
        activity,
        truncateLength: 100
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    const description = wrapper.find('.activity-card__description').text()
    expect(description.length).toBeLessThanOrEqual(103) // 100 + '...'
    expect(description).toContain('...')
  })
})
```

#### 11.2.4 工具函數測試模板

```javascript
// tests/unit/utils/formatters.spec.js
import { describe, it, expect } from 'vitest'
import { formatDate, formatCurrency, truncateText } from '@/utils/formatters'

describe('formatters.js', () => {
  describe('formatDate', () => {
    it('formats date correctly', () => {
      const date = '2025-11-03'
      expect(formatDate(date)).toBe('2025-11-03')
      expect(formatDate(date, 'YYYY/MM/DD')).toBe('2025/11/03')
    })

    it('handles invalid date', () => {
      expect(formatDate(null)).toBe('')
      expect(formatDate('invalid')).toBe('')
    })
  })

  describe('formatCurrency', () => {
    it('formats currency correctly', () => {
      expect(formatCurrency(1000)).toBe('NT$ 1,000')
      expect(formatCurrency(1500.5)).toBe('NT$ 1,501')
    })

    it('handles zero and negative values', () => {
      expect(formatCurrency(0)).toBe('NT$ 0')
      expect(formatCurrency(-500)).toBe('NT$ -500')
    })
  })

  describe('truncateText', () => {
    it('truncates text correctly', () => {
      const text = 'This is a long text'
      expect(truncateText(text, 10)).toBe('This is a...')
    })

    it('does not truncate short text', () => {
      const text = 'Short'
      expect(truncateText(text, 10)).toBe('Short')
    })
  })
})
```

### 11.3 E2E 測試設置（使用 Playwright）

#### 11.3.1 安裝 Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

#### 11.3.2 Playwright 配置 (playwright.config.js)

```javascript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
})
```

#### 11.3.3 E2E 測試範例

```javascript
// tests/e2e/login.spec.js
import { test, expect } from '@playwright/test'

test.describe('Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    // 訪問登入頁
    await page.goto('/login')

    // 填寫表單
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')

    // 點擊登入按鈕
    await page.click('button[type="submit"]')

    // 等待跳轉到控制台
    await page.waitForURL('/dashboard')

    // 驗證頁面元素
    await expect(page.locator('h1')).toContainText('控制台')
    await expect(page.locator('.user-info')).toBeVisible()
  })

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'wrong@example.com')
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // 驗證錯誤訊息
    await expect(page.locator('.el-message--error')).toBeVisible()
    await expect(page.locator('.el-message--error')).toContainText('登入失敗')

    // 確認仍在登入頁
    await expect(page).toHaveURL('/login')
  })
})
```

### 11.4 測試最佳實踐

| 原則 | 說明 | 範例 |
|-----|------|------|
| **單元測試** | 測試單一組件或函數的邏輯 | 測試 `ActivityCard` 組件的渲染邏輯 |
| **整合測試** | 測試多個組件的互動 | 測試表單提交流程 |
| **E2E 測試** | 測試完整的使用者流程 | 測試登入到建立活動的完整流程 |
| **測試結構** | 使用 Arrange-Act-Assert 模式 | 1. 設置 2. 執行 3. 驗證 |
| **Mock 外部依賴** | API 呼叫、路由、Store | 使用 `vi.mock()` |
| **覆蓋率目標** | 80% 以上 | 使用 `vitest --coverage` 檢查 |

### 11.5 測試腳本 (package.json)

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

---

## 12. 前端開發者標準 (Frontend Developer Standards)

### 12.1 關鍵編碼規則

#### 12.1.1 Vue 3 Composition API 規則

```javascript
// ✅ 正確：使用 Composition API
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

onMounted(() => {
  console.log('Component mounted')
})
</script>

// ❌ 錯誤：不要混用 Options API
<script>
export default {
  data() {
    return { count: 0 }
  }
}
</script>
```

#### 12.1.2 響應式數據規則

```javascript
// ✅ 正確：使用 ref 和 reactive
import { ref, reactive } from 'vue'

const count = ref(0)
const user = reactive({ name: 'John', age: 30 })

// 訪問值
console.log(count.value)
console.log(user.name)

// ❌ 錯誤：直接賦值給 reactive 對象
user = { name: 'Jane' } // 會失去響應式

// ✅ 正確：使用 Object.assign 或展開運算符
Object.assign(user, { name: 'Jane' })
```

#### 12.1.3 組件通信規則

```vue
<!-- ✅ 正確：父傳子使用 Props -->
<template>
  <ChildComponent :user="user" :count="count" />
</template>

<!-- ✅ 正確：子傳父使用 Emits -->
<script setup>
const emit = defineEmits(['update', 'delete'])

const handleUpdate = () => {
  emit('update', { id: 1 })
}
</script>

<!-- ❌ 錯誤：不要直接修改 Props -->
<script setup>
const props = defineProps(['count'])
props.count++ // 錯誤！
</script>
```

#### 12.1.4 異步處理規則

```javascript
// ✅ 正確：使用 async/await
const fetchData = async () => {
  try {
    loading.value = true
    const response = await getActivities()
    activities.value = response.data
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

// ❌ 錯誤：未處理錯誤
const fetchData = async () => {
  const response = await getActivities()
  activities.value = response.data
}
```

#### 12.1.5 性能優化規則

```vue
<!-- ✅ 正確：使用 v-show 用於頻繁切換 -->
<div v-show="isVisible">Content</div>

<!-- ✅ 正確：使用 v-if 用於條件渲染 -->
<div v-if="isLoggedIn">Welcome</div>

<!-- ✅ 正確：使用 :key 在 v-for 中 -->
<div v-for="item in items" :key="item.id">
  {{ item.name }}
</div>

<!-- ❌ 錯誤：不要使用 index 作為 key -->
<div v-for="(item, index) in items" :key="index">
  {{ item.name }}
</div>

<!-- ✅ 正確：使用 computed 緩存計算結果 -->
<script setup>
const expensiveComputation = computed(() => {
  return items.value.filter(...).map(...)
})
</script>

<!-- ❌ 錯誤：在模板中進行複雜計算 -->
<template>
  <div>{{ items.filter(...).map(...) }}</div>
</template>
```

### 12.2 程式碼風格規範

#### 12.2.1 ESLint 配置 (.eslintrc.js)

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    '@vue/eslint-config-prettier'
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module'
  },
  rules: {
    // Vue 相關
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'error',
    'vue/require-prop-types': 'error',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/html-self-closing': ['error', {
      html: {
        void: 'always',
        normal: 'never',
        component: 'always'
      }
    }],

    // JavaScript 相關
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'prefer-const': 'error',
    'no-var': 'error',

    // 程式碼風格
    'quotes': ['error', 'single'],
    'semi': ['error', 'never'],
    'comma-dangle': ['error', 'never'],
    'arrow-parens': ['error', 'always'],
    'space-before-function-paren': ['error', 'never']
  }
}
```

#### 12.2.2 Prettier 配置 (.prettierrc)

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "none",
  "arrowParens": "always",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "endOfLine": "lf",
  "vueIndentScriptAndStyle": false
}
```

### 12.3 Git 提交規範

#### 12.3.1 提交訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 12.3.2 Type 類型

| Type | 說明 | 範例 |
|------|------|------|
| **feat** | 新功能 | `feat(activities): add activity filter` |
| **fix** | 修復 Bug | `fix(chat): resolve message ordering issue` |
| **docs** | 文件更新 | `docs(readme): update setup instructions` |
| **style** | 程式碼格式（不影響邏輯） | `style(auth): format login component` |
| **refactor** | 重構 | `refactor(api): simplify axios interceptor` |
| **perf** | 性能優化 | `perf(list): implement virtual scrolling` |
| **test** | 測試相關 | `test(utils): add formatters unit tests` |
| **chore** | 建置/工具變更 | `chore(deps): update dependencies` |

#### 12.3.3 提交範例

```bash
# 好的提交訊息
git commit -m "feat(activities): add activity search and filter functionality"
git commit -m "fix(chat): resolve WebSocket reconnection issue on network error"
git commit -m "refactor(stores): migrate from Vuex to Pinia"

# 不好的提交訊息
git commit -m "update"
git commit -m "fix bug"
git commit -m "WIP"
```

### 12.4 快速參考指南

#### 12.4.1 常用命令

```bash
# 開發伺服器
npm run dev

# 生產建置
npm run build

# 預覽生產建置
npm run preview

# 程式碼檢查
npm run lint

# 程式碼格式化
npm run format

# 單元測試
npm run test:unit

# 覆蓋率測試
npm run test:coverage

# E2E 測試
npm run test:e2e
```

#### 12.4.2 關鍵導入模式

```javascript
// Vue 核心
import { ref, reactive, computed, watch, onMounted } from 'vue'

// Router
import { useRouter, useRoute } from 'vue-router'

// Store
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

// Element Plus
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

// API
import { getActivities, createActivity } from '@/api/activities'

// Utils
import { formatDate, formatCurrency } from '@/utils/formatters'

// Composables
import { useAuth } from '@/composables/useAuth'
```

#### 12.4.3 常用程式碼片段

```javascript
// 基礎響應式狀態
const data = ref(null)
const loading = ref(false)
const error = ref(null)

// API 請求模式
const fetchData = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await getData()
    data.value = response.data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// 表單驗證
const rules = {
  email: [
    { required: true, message: '請輸入 Email', trigger: 'blur' },
    { type: 'email', message: '請輸入有效的 Email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
    { min: 8, message: '密碼至少 8 個字元', trigger: 'blur' }
  ]
}

// Computed 屬性
const filteredItems = computed(() => {
  return items.value.filter((item) => {
    return item.status === 'active'
  })
})

// Watch 監聽
watch(searchTerm, (newValue, oldValue) => {
  console.log(`Search changed from ${oldValue} to ${newValue}`)
  fetchSearchResults(newValue)
})

// Store 使用
const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)
const { login, logout } = authStore
```

---

## 13. 效能優化檢查清單 (Performance Optimization Checklist)

### 13.1 建置優化

- [x] **程式碼分割**：使用路由懶載入，減少初始載入包大小
- [x] **Tree Shaking**：移除未使用的程式碼
- [x] **Chunk 分割**：將第三方庫分離到 vendor chunk
- [x] **壓縮與醜化**：生產環境自動壓縮 JS 和 CSS
- [ ] **Gzip 壓縮**：伺服器端啟用 Gzip 壓縮
- [ ] **Source Map**：生產環境禁用或上傳到錯誤追蹤服務

### 13.2 資源優化

- [x] **圖片懶載入**：使用 `loading="lazy"` 屬性
- [ ] **圖片格式**：使用 WebP 格式，降級到 JPEG/PNG
- [ ] **響應式圖片**：使用 `srcset` 提供不同尺寸
- [x] **圖示優化**：使用 SVG 圖示，支援 Tree-shaking
- [ ] **字型優化**：使用系統字型或 font-display: swap

### 13.3 渲染優化

- [x] **虛擬滾動**：長列表使用虛擬滾動（如活動列表）
- [x] **骨架屏**：使用骨架屏替代 Loading Spinner
- [x] **防抖與節流**：搜尋、滾動事件使用防抖/節流
- [x] **Computed 緩存**：使用 computed 替代 methods 進行計算
- [x] **v-show vs v-if**：頻繁切換使用 v-show，條件渲染使用 v-if

### 13.4 網路優化

- [x] **API 快取**：適當使用 HTTP 快取頭
- [x] **請求合併**：避免重複請求，使用快取
- [ ] **CDN**：靜態資源使用 CDN
- [x] **預載入**：關鍵資源使用 `<link rel="preload">`
- [ ] **Service Worker**：使用 PWA 快取策略

---

## 14. 無障礙性檢查清單 (Accessibility Checklist)

### 14.1 WCAG 2.1 Level AA 合規

- [ ] **色彩對比**：文字對比度至少 4.5:1（正文）、3:1（大字）
- [ ] **焦點指示器**：所有可互動元素有明顯焦點框
- [ ] **鍵盤導航**：所有功能可用鍵盤操作（Tab、Enter、Esc）
- [ ] **螢幕閱讀器**：語意化 HTML + ARIA 屬性
- [ ] **替代文字**：所有圖片有 alt 描述
- [ ] **表單標籤**：所有輸入框有對應 label
- [ ] **錯誤訊息**：使用 aria-live 通知錯誤
- [ ] **標題結構**：H1-H6 層級正確

### 14.2 測試工具

- **Lighthouse**：自動化無障礙性掃描
- **axe DevTools**：瀏覽器擴充，即時檢查
- **NVDA / VoiceOver**：螢幕閱讀器測試

---

## 15. 部署與 CI/CD (Deployment)

### 15.1 建置流程

```bash
# 安裝依賴
npm ci

# 執行測試
npm run test:unit
npm run test:e2e

# 程式碼檢查
npm run lint

# 生產建置
npm run build

# 建置輸出在 dist/ 目錄
```

### 15.2 Docker 部署

前端已包含在專案根目錄的 `docker-compose.yml` 中：

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "8080:80"
  environment:
    - VITE_API_TARGET=http://backend:5000
  depends_on:
    - backend
```

### 15.3 CI/CD Pipeline 建議（GitHub Actions）

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test:unit
      - run: cd frontend && npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # 部署腳本
```

---

## 16. 故障排除 (Troubleshooting)

### 16.1 常見問題

#### 問題 1：Vite 開發伺服器無法啟動

**症狀**：執行 `npm run dev` 失敗

**解決方案**：
1. 檢查端口 8080 是否被占用
2. 刪除 `node_modules` 和 `package-lock.json`，重新安裝
3. 檢查 Node.js 版本（需 16+）

```bash
# 檢查端口
netstat -ano | findstr :8080

# 重新安裝
rm -rf node_modules package-lock.json
npm install
```

#### 問題 2：API 請求失敗（CORS 錯誤）

**症狀**：瀏覽器控制台顯示 CORS 錯誤

**解決方案**：
1. 檢查後端 CORS 配置
2. 確認 Vite proxy 配置正確
3. 使用正確的 API URL

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

#### 問題 3：Socket.IO 連接失敗

**症狀**：即時聊天無法使用

**解決方案**：
1. 檢查後端 Socket.IO 是否啟動
2. 確認 WebSocket proxy 配置
3. 檢查防火牆設定

```javascript
// vite.config.js
'/socket.io': {
  target: 'http://localhost:5000',
  changeOrigin: true,
  ws: true
}
```

#### 問題 4：建置失敗（記憶體不足）

**症狀**：`npm run build` 出現 JavaScript heap out of memory

**解決方案**：
```bash
# 增加 Node.js 記憶體限制
set NODE_OPTIONS=--max_old_space_size=4096
npm run build
```

---

## 17. 未來改進建議 (Future Improvements)

### 17.1 Phase 2 功能

- [ ] **TypeScript 遷移**：漸進式遷移到 TypeScript
- [ ] **PWA 支援**：實現離線功能與推送通知
- [ ] **國際化 (i18n)**：支援多語言
- [ ] **暗黑模式**：完整的深色主題支援
- [ ] **性能監控**：整合 Sentry 或 LogRocket
- [ ] **A/B 測試**：實現功能開關與實驗

### 17.2 技術升級

- [ ] **Vite 5**：升級到最新版本
- [ ] **Vue 3.4+**：使用最新 Vue 特性
- [ ] **Composition API 工具**：使用 VueUse
- [ ] **狀態持久化**：Pinia Plugin Persistedstate
- [ ] **表單管理**：整合 VeeValidate 或 Formkit

---

## 18. 參考資源 (References)

### 18.1 官方文件

- **Vue 3**: https://vuejs.org
- **Vite**: https://vitejs.dev
- **Vue Router**: https://router.vuejs.org
- **Pinia**: https://pinia.vuejs.org
- **Element Plus**: https://element-plus.org

### 18.2 最佳實踐

- **Vue 3 風格指南**: https://vuejs.org/style-guide/
- **Vite 效能優化**: https://vitejs.dev/guide/performance.html
- **Web Vitals**: https://web.dev/vitals/

### 18.3 測試資源

- **Vitest**: https://vitest.dev
- **Vue Test Utils**: https://test-utils.vuejs.org
- **Playwright**: https://playwright.dev

---

## 附錄 A：專案檔案對應表

| 功能 | 相關檔案 | 說明 |
|-----|---------|------|
| **應用入口** | `src/main.js` | Vue 應用初始化 |
| **路由配置** | `src/router/index.js` | 所有路由定義 |
| **認證狀態** | `src/stores/auth.js` | 用戶認證管理 |
| **API 客戶端** | `src/utils/axios.js` | Axios 配置與攔截器 |
| **Socket 服務** | `src/services/socket.js` | Socket.IO 整合 |
| **主題系統** | `src/styles/theme.css` | CSS 變數定義 |
| **環境配置** | `.env.development`, `.env.production` | 環境變數 |
| **建置配置** | `vite.config.js` | Vite 配置 |

---

## 附錄 B：API 端點映射表

| 功能模組 | API 服務檔案 | 後端端點 |
|---------|-------------|---------|
| **認證** | `api/auth.js` | `/api/auth/*` |
| **活動** | `api/activities.js` | `/api/activities/*` |
| **媒合** | `api/matches.js` | `/api/matches/*` |
| **聊天** | `api/chat.js` | `/api/chat/*` |
| **費用** | `api/expenses.js` | `/api/expenses/*` |
| **評價** | `api/reviews.js` | `/api/reviews/*` |
| **用戶** | `api/users.js` | `/api/users/*` |
| **上傳** | `api/upload.js` | `/api/upload/*` |

---

## 附錄 C：組件層級結構

```
App.vue
├── NavBar.vue (布局)
├── Router View
    ├── Dashboard.vue (頁面)
    │   ├── StatCard.vue (組件)
    │   ├── ActivityCard.vue (組件)
    │   └── MatchCard.vue (組件)
    ├── Activities.vue (頁面)
    │   ├── ActivityFilters.vue (組件)
    │   └── ActivityCard.vue (組件)
    ├── ActivityDetail.vue (頁面)
    │   ├── ParticipantList.vue (組件)
    │   ├── ActivityDiscussion.vue (組件)
    │   ├── ExpenseManager.vue (組件)
    │   └── ActivityReviews.vue (組件)
    └── Chat.vue (頁面)
        ├── ChatList.vue (組件)
        └── ChatWindow.vue (組件)
            ├── MessageBubble.vue (組件)
            └── MessageInput.vue (組件)
```

---

**文檔結尾**

此前端技術架構文件由 Winston (Architect) 建立，基於 EdgeSurvivor PRD v1.0 和 UI/UX 規格 v1.0。如有任何問題或建議，請聯繫專案團隊。

**版本**：1.0  
**最後更新**：2025-11-03  
**狀態**：Active

---

**下一步行動**：

1. **前端開發團隊**：檢閱此架構文件，確認技術選型與實現方案
2. **DevOps 團隊**：根據部署章節設置 CI/CD Pipeline
3. **QA 團隊**：根據測試策略章節準備測試計畫
4. **PM 團隊**：驗證架構是否滿足 PRD 中的所有需求

**相關文件**：
- [產品需求文件 (PRD)](./prd.md)
- [UI/UX 規格文檔](./front-end-spec.md)
- [後端架構文檔](./backend-architecture.md) *(待建立)*


由於文件較長，我將分批繼續生成。接下來會包含路由配置、樣式指南、環境配置等內容。

