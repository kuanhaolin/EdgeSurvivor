# 3. 專案結構 (Project Structure)

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
