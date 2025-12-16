# EdgeSurvivor Brownfield 架構文檔

## 簡介

本文檔記錄 **EdgeSurvivor（邊緣人神器）** 專案的**實際架構狀態**，這是一個旅伴媒合與活動管理平台。文檔反映真實的技術實作、已知限制、技術債務，以及系統的運作方式。

### 文檔範圍

**全面系統文檔** - 涵蓋整個 EdgeSurvivor 平台的架構、實作細節與開發指南

### 變更記錄

| 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|
| 2025-12-15 | 1.0 | 初始 Brownfield 分析文檔 | Mary (Business Analyst) |

---

## 快速參考 - 關鍵檔案與進入點

### 後端關鍵檔案

- **主要進入點**: `backend/app.py` - Flask 應用程式工廠
- **配置檔案**: `backend/config.py` - 環境配置與資料庫設定
- **Socket.IO 事件**: `backend/socketio_events.py` - 即時通訊事件處理
- **資料庫初始化**: `backend/init_db.py` - 資料庫初始化腳本
- **Models 目錄**: `backend/models/` - SQLAlchemy 資料模型
- **Blueprints 目錄**: `backend/blueprints/` - Flask 路由藍圖
- **測試目錄**: `backend/test/` - Pytest 測試套件

### 前端關鍵檔案

- **主要進入點**: `frontend/src/main.js` - Vue 3 應用程式進入點
- **路由定義**: `frontend/src/router/index.js` - Vue Router 配置
- **API 客戶端**: `frontend/src/utils/axios.js` - Axios 實例與攔截器
- **狀態管理**: `frontend/src/stores/` - Pinia stores
- **Views 目錄**: `frontend/src/views/` - Vue 頁面組件
- **Components 目錄**: `frontend/src/components/` - 可重用組件

### 部署與設定檔案

- **環境變數範例**: `.env.example` - 環境變數模板
- **Docker Compose**: `docker-compose.yml` - 容器編排配置
- **部署指南**: `DEPLOYMENT_GUIDE.md` - 完整部署文檔
- **專案簡介**: `docs/project-brief.md` - 專案需求與規格

---

## 高階架構

### 技術摘要

EdgeSurvivor 是一個**三層式 Web 應用程式**：
- **前端**: Vue 3 + Element Plus + Socket.IO Client
- **後端**: Flask + Flask-SocketIO + SQLAlchemy
- **資料庫**: MariaDB 10.11

系統採用 **RESTful API + WebSocket** 雙通道通訊：
- REST API 用於一般 CRUD 操作
- WebSocket (Socket.IO) 用於即時聊天與通知

### 實際技術堆疊

#### 後端技術堆疊

| 類別 | 技術 | 版本 | 用途與備註 |
|------|------|------|-----------|
| **運行環境** | Python | 3.9+ | 後端主要語言 |
| **Web 框架** | Flask | 2.3.3 | 輕量級 Web 框架 |
| **ORM** | Flask-SQLAlchemy | 3.0.5 | 資料庫 ORM，使用 SQLAlchemy 2.x 語法 |
| **認證** | Flask-JWT-Extended | 4.5.3 | JWT Token 認證 |
| **即時通訊** | Flask-SocketIO | 5.3.6 | WebSocket 支援 |
| **CORS** | Flask-CORS | 4.0.0 | 跨域資源共享 |
| **資料庫遷移** | Flask-Migrate | 4.0.5 | Alembic 資料庫遷移工具 |
| **資料庫驅動** | PyMySQL | 1.1.0 | MySQL/MariaDB 連接器 |
| **密碼加密** | Werkzeug | 2.3.7 | 內建密碼雜湊功能 |
| **序列化** | Marshmallow | 3.20.1 | 資料序列化與驗證 |
| **非同步處理** | gevent | 24.2.1 | 生產環境使用的 WSGI 伺服器 |
| **2FA** | pyotp | 2.9.0 | 兩步驟驗證 |
| **生產伺服器** | gunicorn | 21.2.0 | WSGI HTTP 伺服器 |

#### 前端技術堆疊

| 類別 | 技術 | 版本 | 用途與備註 |
|------|------|------|-----------|
| **框架** | Vue | 3.3.8 | 前端主框架（Composition API） |
| **UI 庫** | Element Plus | 2.4.2 | UI 組件庫 |
| **狀態管理** | Pinia | 2.1.7 | 官方推薦的狀態管理 |
| **路由** | Vue Router | 4.2.5 | 前端路由管理 |
| **HTTP 客戶端** | Axios | 1.6.0 | API 請求處理 |
| **即時通訊** | socket.io-client | 4.7.4 | WebSocket 客戶端 |
| **日期處理** | dayjs | 1.11.10 | 輕量級日期工具 |
| **Cookie 管理** | js-cookie | 3.0.5 | Cookie 操作工具 |
| **建置工具** | Vite | 4.5.3 | 快速開發伺服器與建置工具 |
| **測試框架** | Vitest | 4.0.15 | Vue 測試工具 |

#### 基礎設施

| 類別 | 技術 | 版本 | 備註 |
|------|------|------|------|
| **資料庫** | MariaDB | 10.11 | 主要資料庫 |
| **容器化** | Docker | 20.10+ | 容器運行環境 |
| **編排** | Docker Compose | 2.0+ | 多容器編排 |

### Repository 結構現狀

```
EdgeSurvivor/
 backend/                    # Python Flask 後端
    app.py                 # 主應用程式（工廠模式）
    config.py              # 環境配置
    socketio_events.py     # Socket.IO 事件處理
    init_db.py             # 資料庫初始化
    requirements.txt       # Python 依賴
    Dockerfile             # 後端容器配置
    models/                # SQLAlchemy 資料模型
       __init__.py       # 資料庫實例初始化
       user.py           # 使用者模型
       activity.py       # 活動模型
       match.py          # 媒合記錄模型
       chat_message.py   # 聊天訊息模型
       expense.py        # 費用分攤模型
       activity_*.py     # 活動相關模型
    blueprints/            # Flask 路由藍圖
       auth.py           # 認證相關 API
       users.py          # 使用者管理 API
       activities.py     # 活動管理 API
       matches.py        # 媒合管理 API
       chat.py           # 聊天 API
       discussions.py    # 討論區 API
       expenses.py       # 費用管理 API
       reviews.py        # 評價系統 API
       upload.py         # 檔案上傳 API
    test/                  # Pytest 測試套件
       conftest.py       # 測試配置與 fixtures
       TC_*.py           # 測試案例（170+ 個）
    migrations/            # 資料庫遷移腳本
    uploads/               # 上傳檔案儲存目錄

 frontend/                   # Vue 3 前端
    src/
       main.js           # Vue 應用程式進入點
       App.vue           # 根組件
       router/           # 路由配置
          index.js      # 路由定義
       views/            # 頁面組件
          Home.vue      # 首頁
          Login.vue     # 登入頁
          Register.vue  # 註冊頁
          Dashboard.vue # 儀表板
          Activities.vue # 活動列表
          Chat.vue      # 聊天室
          ...           # 其他頁面
       components/       # 可重用組件
       stores/           # Pinia 狀態管理
          app.js        # 應用程式狀態
          auth.js       # 認證狀態
       utils/            # 工具函數
          axios.js      # Axios 實例配置
       api/              # API 呼叫函數
    package.json          # 前端依賴
    vite.config.js        # Vite 建置配置
    Dockerfile            # 前端容器配置

 db/                         # 資料庫初始化腳本
    init.sql              # Docker 初始化 SQL
    init-complete.sql     # 完整初始化 SQL

 docs/                       # 專案文檔
    project-brief.md      # 專案簡介與需求（853 行）
    case_doc/             # 軟體工程文檔
    Dirgrams/             # 系統圖表

 .env.example               # 環境變數模板
 docker-compose.yml         # 容器編排配置
 docker-compose.test.yml    # 測試環境配置
 pytest.ini                 # Pytest 配置
 README.md                  # 專案說明
 DEPLOYMENT_GUIDE.md        # 部署指南（457 行）
 SETUP.md                   # 開發環境設定

**重要**: 本專案為 **Monorepo** 結構，前後端分離但共存於同一 repository
```

### 專案架構模式

- **類型**: Monorepo (前後端分離但在同一 repository)
- **套件管理**: 
  - 後端: pip (requirements.txt)
  - 前端: npm (package.json)
- **特殊之處**: 
  - 採用 Docker Compose 進行容器化部署
  - 前後端透過 Nginx 反向代理整合（生產環境）
  - 開發環境直接跨域通訊

---

## 原始碼樹與模組組織

### 後端模組結構

#### 應用程式工廠模式 (app.py)

```python
# backend/app.py 使用工廠模式建立 Flask 應用程式
def create_app(config_name=None):
    """
    應用程式工廠函數
    - 支援多環境配置 (development, production, testing)
    - 初始化所有擴充套件 (db, jwt, socketio, cors, migrate)
    - 註冊所有 Blueprint
    - 設定 CORS 允許來源
    """
```

**關鍵特性**:
- 環境由 `FLASK_ENV` 環境變數控制
- Socket.IO 異步模式：生產環境使用 `gevent`，開發環境使用 `threading`
- CORS 配置允許多個來源（localhost:3000, localhost:8080, 生產域名）

#### Blueprint 架構

所有 API 路由都組織在獨立的 Blueprint 中：

| Blueprint | URL 前綴 | 檔案位置 | 功能 |
|-----------|---------|---------|------|
| **auth_bp** | `/api/auth` | `blueprints/auth.py` | 註冊、登入、JWT 刷新、2FA |
| **users_bp** | `/api/users` | `blueprints/users.py` | 使用者資料管理、隱私設定 |
| **activities_bp** | `/api/activities` | `blueprints/activities.py` | 活動 CRUD、參與者管理 |
| **matches_bp** | `/api/matches` | `blueprints/matches.py` | 媒合申請、確認、拒絕 |
| **chat_bp** | `/api/chat` | `blueprints/chat.py` | 聊天訊息歷史查詢 |
| **discussions_bp** | `/api` | `blueprints/discussions.py` | 活動討論區 |
| **expenses_bp** | `/api` | `blueprints/expenses.py` | 費用記錄與分攤計算 |
| **reviews_bp** | `/api` | `blueprints/reviews.py` | 活動評價系統 |
| **upload_bp** | `/api/upload` | `blueprints/upload.py` | 圖片上傳處理 |

**注意**: 部分 Blueprint 使用 `/api` 作為前綴（discussions, expenses, reviews），需要完整路徑才能呼叫

#### 資料庫連接配置

```python
# config.py 中的連接池配置
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,          # 連接池大小
    'max_overflow': 40,       # 超過 pool_size 後最多再建立的連接數
    'pool_timeout': 30,       # 獲取連接的超時時間
    'pool_recycle': 3600,     # 連接回收時間（秒）
    'pool_pre_ping': True     # 使用前先測試連接是否有效
}
```

**重要**: SQLAlchemy 2.x 語法變更，需使用 `text()` 包裝原生 SQL

### 前端模組結構

#### Vue 3 Composition API

專案使用 Vue 3 的 **Composition API**（不是 Options API），所有組件都採用 `<script setup>` 語法。

#### 路由結構

```javascript
// frontend/src/router/index.js
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/activities', name: 'Activities', component: Activities, meta: { requiresAuth: true } },
  { path: '/activity/:id', name: 'ActivityDetail', component: ActivityDetail, meta: { requiresAuth: true } },
  { path: '/matches', name: 'Matches', component: Matches, meta: { requiresAuth: true } },
  { path: '/chat', name: 'Chat', component: Chat, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  // ... 更多路由
]
```

**路由守衛**: 使用 `meta.requiresAuth` 標記需要認證的頁面，在導航守衛中檢查 token

#### Axios 攔截器配置

```javascript
// frontend/src/utils/axios.js
// 請求攔截器 - 自動添加 JWT Token
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

// 響應攔截器 - 錯誤處理
instance.interceptors.response.use(
  response => response,
  error => {
    console.error('API 錯誤:', error.response?.status)
    return Promise.reject(error)
  }
)
```

**重要**: Token 儲存在 `localStorage`，沒有自動過期處理（需手動檢查）

#### Pinia 狀態管理

```javascript
// stores/auth.js - 認證狀態
// stores/app.js - 應用程式全域狀態
```

**注意**: 目前使用較少，大部分組件直接使用 localStorage 存取 token

---

## 資料模型與 API

### 核心資料模型

#### 1. User 模型

**檔案位置**: `backend/models/user.py`

**關鍵欄位**:
```python
- user_id: 主鍵
- email: 唯一識別（有索引）
- password_hash: Werkzeug 加密密碼
- name, location, bio, gender, age
- interests: JSON 字串格式儲存興趣標籤
- privacy_setting: 'public', 'partial', 'hidden'
- social_privacy: 'public', 'friends_only'
- profile_picture: 大頭照 URL
- is_verified, is_active: 帳號狀態
- two_factor_enabled, two_factor_secret: 2FA 支援
- rating_count, average_rating: 評價統計
```

**關聯關係**:
- `created_activities`: 創建的活動 (一對多)
- `matches_as_user_a/b`: 媒合記錄（雙向）
- `sent_messages`: 發送的聊天訊息
- `activity_participations`: 參與的活動

**重要方法**:
- `set_password(password)`: 設定密碼雜湊
- `check_password(password)`: 驗證密碼
- `to_dict(include_private=False, is_friend=False)`: 序列化，支援隱私控制

#### 2. Activity 模型

**檔案位置**: `backend/models/activity.py`

**關鍵欄位**:
```python
- activity_id: 主鍵
- title, description, category
- date: 舊欄位（向後兼容），現為開始日期
- start_date, end_date: 活動日期範圍（新增）
- start_time, end_time: 活動時間（新增）
- location, meeting_point: 地點資訊
- max_participants, cost: 參與限制與費用
- status: 'active', 'completed', 'cancelled'
- creator_id: 創建者（外鍵到 User）
- difficulty_level: 'easy', 'medium', 'hard'
- gender_preference, age_min, age_max: 參與者條件
- cover_image, images: 圖片（JSON 格式）
```

**重要**: 有 `date` 和 `start_date` 兩個欄位是因為後期新增時間範圍功能，保留舊欄位向後兼容

#### 3. Match 模型

**檔案位置**: `backend/models/match.py`

**關鍵欄位**:
```python
- match_id: 主鍵
- activity_id: 關聯活動（可為 NULL - 支援直接媒合使用者）
- user_a: 申請者（外鍵到 User）
- user_b: 活動創建者或被申請者
- status: 'pending', 'confirmed', 'rejected', 'cancelled'
- match_date, confirmed_date, cancel_date: 狀態時間戳
- message: 申請訊息
- rejection_reason: 拒絕原因
```

**重要特性**:
- `activity_id` 可為 NULL，支援不透過活動的直接使用者媒合
- `user_a` 和 `user_b` 有各自的反向關聯 (`user_a_ref`, `user_b_ref`)

#### 4. Expense 模型

**檔案位置**: `backend/models/expense.py`

**關鍵欄位**:
```python
- expense_id: 主鍵
- activity_id: 關聯活動
- payer_id: 代墊者（外鍵到 User）
- amount: 金額 (Decimal)
- description, category: 費用描述與分類
- split_type: 'all'(全體), 'selected'(部分), 'borrow'(借款)
- split_method: 'equal'(平均), 'custom'(自訂)
- split_participants: JSON 格式參與者列表
- borrower_id: 借款人（僅 split_type='borrow' 時使用）
```

**費用分攤邏輯**:
- 支援三種分攤類型：全體分攤、指定部分人、1對1借款
- 計算由後端 API 處理，前端顯示結果

#### 5. ChatMessage 模型

**檔案位置**: `backend/models/chat_message.py`

**關鍵欄位**:
```python
- message_id: 主鍵
- match_id: 關聯媒合記錄（決定聊天室）
- sender_id: 發送者
- content: 訊息內容
- timestamp: 發送時間
- is_read: 已讀狀態
```

**即時通訊**: 訊息透過 Socket.IO 即時傳送，同時存入資料庫供歷史查詢

#### 6. ActivityParticipant 模型

**檔案位置**: `backend/models/activity_participant.py`

管理活動參與者狀態：
- `status`: 'pending', 'approved', 'rejected', 'joined', 'cancelled'
- `role`: 'creator', 'participant'

#### 7. ActivityDiscussion & ActivityReview

**討論區**: `backend/models/activity_discussion.py` - 活動討論串  
**評價系統**: `backend/models/activity_review.py` - 活動結束後的評價

### API 端點規格

完整 API 規格請參考各 Blueprint 檔案。以下是核心端點概覽：

#### 認證 API (`/api/auth`)

| 端點 | 方法 | 功能 | 需認證 |
|------|------|------|--------|
| `/register` | POST | 使用者註冊 |  |
| `/login` | POST | 使用者登入（返回 JWT） |  |
| `/refresh` | POST | 刷新 JWT Token |  |
| `/logout` | POST | 登出（目前僅清除客戶端） |  |
| `/2fa/setup` | POST | 設定雙因素認證 |  |
| `/2fa/verify` | POST | 驗證 2FA 代碼 |  |

#### 活動 API (`/api/activities`)

| 端點 | 方法 | 功能 | 需認證 |
|------|------|------|--------|
| `/` | GET | 取得活動列表（支援 type 參數） |  |
| `/` | POST | 建立新活動 |  |
| `/<id>` | GET | 取得活動詳情 |  |
| `/<id>` | PUT | 更新活動 |  (限創建者) |
| `/<id>` | DELETE | 刪除活動 |  (限創建者) |
| `/<id>/join` | POST | 申請加入活動 |  |
| `/<id>/participants` | GET | 取得參與者列表 |  |
| `/<id>/participants/<user_id>` | PUT | 審核參與者 |  (限創建者) |

**查詢參數**:
- `type=created`: 我創建的活動
- `type=joined`: 我參加的活動
- 無參數: 所有活動

#### 媒合 API (`/api/matches`)

| 端點 | 方法 | 功能 | 需認證 |
|------|------|------|--------|
| `/` | GET | 取得媒合列表 |  |
| `/` | POST | 建立媒合申請 |  |
| `/<id>` | GET | 取得媒合詳情 |  |
| `/<id>/confirm` | PUT | 確認媒合 |  |
| `/<id>/reject` | PUT | 拒絕媒合 |  |
| `/<id>/cancel` | PUT | 取消媒合 |  |

#### 聊天 API (`/api/chat` + Socket.IO)

**REST API**:
| 端點 | 方法 | 功能 | 需認證 |
|------|------|------|--------|
| `/messages` | GET | 取得聊天歷史 |  |
| `/messages` | POST | 發送訊息（備用） |  |

**Socket.IO 事件**:
| 事件 | 方向 | 功能 |
|------|------|------|
| `connect` | ClientServer | 連線（需傳 auth.token） |
| `user_ready` | ClientServer | 通知伺服器已就緒 |
| `join_chat` | ClientServer | 加入聊天室 |
| `send_message` | ClientServer | 發送訊息 |
| `new_message` | ServerClient | 接收新訊息 |
| `user_online` | ServerClient | 使用者上線通知 |
| `user_offline` | ServerClient | 使用者離線通知 |

**重要**: Socket.IO 連線需在 auth 參數中傳遞 JWT token

#### 費用 API (`/api/expenses` 或 `/api/activities/<id>/expenses`)

| 端點 | 方法 | 功能 | 需認證 |
|------|------|------|--------|
| `/activities/<id>/expenses` | GET | 取得活動費用列表 |  |
| `/activities/<id>/expenses` | POST | 新增費用記錄 |  |
| `/expenses/<id>` | PUT | 更新費用 |  |
| `/expenses/<id>` | DELETE | 刪除費用 |  |
| `/activities/<id>/expenses/summary` | GET | 取得費用分攤摘要 |  |

**費用分攤摘要** 包含：
- 每人應付金額
- 代墊統計
- 結算建議（誰應該付給誰多少錢）

---

## 技術債務與已知問題

### 關鍵技術債務

#### 1. Socket.IO 連線管理 

**問題**: `socketio_events.py` 中的 `online_users` 是記憶體內字典，不支援多實例部署

```python
# 目前實作 - 僅適用於單實例
online_users = {}  # {user_id: sid}
```

**影響**: 
- 水平擴展時，不同伺服器實例無法共享線上使用者資訊
- 伺服器重啟會丟失所有連線狀態

**解決方案建議**: 使用 Redis 儲存線上使用者狀態

#### 2. Token 過期處理不完整 

**問題**: 前端 Axios 攔截器不會自動刷新過期的 JWT Token

**影響**: Token 過期後，使用者需要重新登入

**解決方案建議**: 在 401 響應時自動呼叫 `/api/auth/refresh` 端點

#### 3. 資料庫遷移未統一 

**問題**: 
- `backend/migrations/` 目錄下有手動 Python 腳本（`add_activity_time_fields.py` 等）
- 沒有使用 Flask-Migrate 的標準遷移流程

**影響**: 
- 難以追蹤資料庫 schema 變更歷史
- 部署時需要手動執行遷移腳本

#### 4. Activity 模型的日期欄位混亂 

**問題**: 同時存在 `date` 和 `start_date` 欄位

```python
date = db.Column(db.Date, nullable=False)  # 舊欄位
start_date = db.Column(db.Date)             # 新欄位
end_date = db.Column(db.Date)               # 新欄位
```

**原因**: 後期新增多天活動支援，但保留舊欄位向後兼容

**影響**: 需在 `to_dict()` 中特別處理，邏輯複雜

#### 5. 測試覆蓋率配置過於嚴格

**問題**: `pytest.ini` 設定 `--cov-fail-under=70`，但實際可能未達標

**建議**: 調整至實際覆蓋率或逐步提升

### 已知限制與注意事項

#### 1. CORS 配置硬編碼

```python
# app.py 中的 CORS 設定
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000", 
            "http://localhost:8080",
            "https://edgesurvivor.ddns.net",
            "http://edgesurvivor.ddns.net"
        ]
    }
})
```

**注意**: 新增部署域名需修改程式碼

#### 2. 上傳檔案儲存在本地

**位置**: `backend/uploads/`

**限制**: 
- 不支援 CDN 或雲端儲存
- 容器重啟會丟失上傳檔案（除非使用 Volume）

#### 3. Socket.IO 不支援身份驗證中間件

**問題**: 連線時透過 `auth` 參數傳遞 token，但沒有統一的認證中間件

**影響**: 每個 Socket.IO 事件處理函數需自行驗證使用者身份

#### 4. 環境變數依賴 .env 檔案

**注意**: 
- Docker 環境需確保 `.env` 檔案存在
- `docker-compose.yml` 使用 `env_file: .env` 載入環境變數
- 開發環境由 `python-dotenv` 載入

### 效能瓶頸

#### 1. N+1 查詢問題

部分 API 端點在序列化關聯資料時可能觸發 N+1 查詢，例如：

```python
# activities.py - get_activities
for activity in activities:
    activity_dict = activity.to_dict(include_creator_info=True)
    # 每次迭代都會查詢 creator
```

**建議**: 使用 `joinedload` 預載入關聯資料

#### 2. 費用分攤計算在請求時進行

費用摘要計算邏輯在每次 API 請求時重新計算，未快取結果

---

## 整合點與外部依賴

### 內部整合點

#### 前後端通訊

**REST API**:
- **Base URL**: `/api`（透過 Vite proxy 或 Nginx 轉發）
- **認證**: JWT Token 放在 `Authorization: Bearer <token>` header
- **資料格式**: JSON

**WebSocket**:
- **協議**: Socket.IO over WebSocket
- **命名空間**: 預設 `/`
- **認證**: 連線時在 `auth.token` 中傳遞 JWT

#### 容器間通訊

```yaml
# docker-compose.yml 中的網路配置
services:
  frontend:
    depends_on: [backend]
  backend:
    depends_on: [db]
  db:
    healthcheck: ...  # 確保 DB 準備好才啟動 backend
```

**DNS 解析**: 容器名稱可直接作為主機名（如 `db:3306`）

### 外部依賴服務

#### 1. 社群帳號綁定（預留功能）

User 模型中有以下欄位：
```python
instagram_url = db.Column(db.String(255))
facebook_url = db.Column(db.String(255))
line_id = db.Column(db.String(100))
twitter_url = db.Column(db.String(255))
```

**狀態**: 資料庫欄位已建立，但尚未實作 OAuth 整合

#### 2. 圖片上傳與儲存

**目前實作**: 本地檔案系統 (`backend/uploads/`)  
**URL 格式**: `/api/upload/<filename>`

**未來擴展方向**: 
- AWS S3 / Azure Blob Storage
- CDN 加速

#### 3. Email 通知（未實作）

專案中有 `EMAIL-SETUP.md` 文檔，但尚未整合 Email 服務

### 第三方套件依賴風險

| 套件 | 風險等級 | 備註 |
|------|---------|------|
| **gevent** | 中 | 生產環境依賴，需確保與其他套件相容 |
| **Flask-SocketIO** | 中 | 版本升級需注意 breaking changes |
| **Element Plus** | 低 | UI 庫相對穩定 |
| **PyMySQL** | 低 | 成熟的資料庫驅動 |

---

## 開發與部署

### 本地開發環境設定

#### 方法一：原生執行

**後端**:
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example ../.env  # 編輯 .env 設定資料庫
python init_db.py            # 初始化資料庫
python app.py                # 啟動開發伺服器（port 5000）
```

**前端**:
```bash
cd frontend
npm install
npm run dev  # 啟動 Vite 開發伺服器（port 3000）
```

**資料庫**:
需自行安裝 MariaDB/MySQL，或使用 Docker:
```bash
docker run -d -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=edgesurvivor \
  mariadb:10.11
```

#### 方法二：Docker Compose（推薦）

```bash
cp .env.example .env  # 編輯 .env
docker-compose up --build
```

**服務存取**:
- 前端: http://localhost:8080
- 後端: http://localhost:5001
- 資料庫: localhost:3307

### 建置與部署流程

#### Docker 容器建置

**後端 Dockerfile**:
- 基於 `python:3.9`
- 安裝依賴後使用 `gunicorn` 啟動
- 環境變數由 `.env` 注入

**前端 Dockerfile**:
- 建置階段：使用 `node:18` 執行 `npm run build`
- 執行階段：使用 `nginx:alpine` 提供靜態檔案
- Nginx 配置反向代理 `/api` 到後端

#### 部署環境

**環境配置**:
- **開發環境** (`FLASK_ENV=development`): 
  - Debug 模式
  - 詳細日誌
  - SQLite 或本地 MySQL
  
- **生產環境** (`FLASK_ENV=production`):
  - 關閉 Debug
  - 使用 gevent worker
  - MariaDB 資料庫
  - Gunicorn + Nginx

**部署步驟** (參考 `DEPLOYMENT_GUIDE.md`):
1. 設定 `.env` 環境變數（**必須修改 SECRET_KEY**）
2. 執行 `docker-compose up -d`
3. 檢查容器狀態 `docker-compose ps`
4. 初始化資料庫（首次部署）
5. 驗證服務健康檢查

#### 資料庫遷移

**目前方式**: 手動執行 Python 腳本

```bash
cd backend/migrations
python add_activity_time_fields.py   # 範例遷移腳本
```

**建議方式**: 使用 Flask-Migrate

```bash
flask db init       # 初始化（僅首次）
flask db migrate -m "description"  # 生成遷移檔案
flask db upgrade    # 應用遷移
```

### 常用指令與腳本

#### 開發指令

```bash
# 後端
python backend/app.py                    # 啟動 Flask 開發伺服器
python backend/init_db.py                # 初始化資料庫
python backend/init_db.py test           # 測試資料庫連線
pytest backend/test                      # 執行測試

# 前端
npm run dev              # 啟動 Vite 開發伺服器
npm run build            # 建置生產版本
npm run preview          # 預覽建置結果
npm run lint             # ESLint 檢查

# Docker
docker-compose up        # 啟動所有服務
docker-compose down      # 停止所有服務
docker-compose logs -f backend  # 查看後端日誌
docker-compose restart backend  # 重啟後端服務
```

#### 資料庫管理

```bash
# 連線到 Docker 內的資料庫
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 匯出資料庫
docker exec edgesurvivor_db mysqldump -u user -ppassword edgesurvivor > backup.sql

# 匯入資料庫
docker exec -i edgesurvivor_db mysql -u user -ppassword edgesurvivor < backup.sql
```

#### 測試相關

```bash
# 執行所有測試
pytest backend/test

# 執行特定測試檔案
pytest backend/test/TC_1_1.py

# 產生測試報告
pytest --html=report.html

# 測試覆蓋率
pytest --cov=backend --cov-report=html
```

### 偵錯與疑難排解

#### 常見問題

**1. 資料庫連線失敗**

檢查項目：
- `.env` 中的資料庫配置是否正確
- Docker 容器中使用 `DB_HOST=db`（服務名稱）
- 資料庫容器是否已啟動並 healthy

```bash
# 檢查資料庫容器狀態
docker-compose ps db

# 查看資料庫日誌
docker-compose logs db
```

**2. Socket.IO 連線失敗**

常見原因：
- Token 未正確傳遞
- CORS 配置不包含前端域名
- WebSocket 被防火牆阻擋

檢查方式：
```javascript
// 前端瀏覽器 Console
socket.on('connect_error', (error) => {
  console.error('Socket.IO 連線錯誤:', error)
})
```

**3. 前端無法呼叫 API**

檢查項目：
- Vite proxy 配置 (`vite.config.js`)
- CORS 設定 (`backend/app.py`)
- Token 是否存在於 localStorage
- 瀏覽器 Network 面板查看錯誤訊息

**4. Docker 容器啟動失敗**

```bash
# 查看詳細錯誤
docker-compose logs backend

# 重新建置映像檔
docker-compose up --build

# 清除舊容器與映像
docker-compose down -v
docker system prune -a
```

#### 日誌位置

- **Flask 應用程式**: 標準輸出（`docker-compose logs backend`）
- **Nginx**: `/var/log/nginx/` (在容器內)
- **測試報告**: `backend/test/report.html`
- **覆蓋率報告**: `htmlcov/index.html`

#### 效能監控

**資料庫查詢日誌**:
```python
# config.py 中啟用 SQL 日誌
app.config['SQLALCHEMY_ECHO'] = True  # 開發環境
```

**Socket.IO 日誌**:
```python
# app.py 中的 Socket.IO 配置
socketio.init_app(app, logger=True, engineio_logger=True)
```

---

## 測試現狀

### 測試架構

**測試框架**: Pytest  
**測試套件位置**: `backend/test/`  
**測試配置**: `pytest.ini`

### 測試覆蓋範圍

專案包含 **170+ 個測試檔案**，涵蓋：

| 測試類別 | 檔案範例 | 數量 |
|---------|---------|------|
| **使用者認證** | TC_1_1_*.py | 7+ |
| **使用者管理** | TC_1_2_*.py | 7+ |
| **活動管理** | TC_2_*.py | 30+ |
| **媒合系統** | TC_3_*.py | 20+ |
| **聊天功能** | TC_4_*.py | 30+ |

### 執行測試

```bash
# 執行所有測試
pytest backend/test

# 執行特定模組
pytest backend/test/TC_1_1.py

# 產生 HTML 報告
pytest --html=report.html

# 測試覆蓋率
pytest --cov=backend --cov-report=html
```

### 測試標記 (Markers)

```python
@pytest.mark.auth       # 認證測試
@pytest.mark.activity   # 活動測試
@pytest.mark.slow       # 慢速測試
```

使用方式：
```bash
pytest -m auth          # 只執行認證測試
pytest -m "not slow"    # 跳過慢速測試
```

### Fixtures

**主要 Fixtures** (`conftest.py`):
- `test_app`: 測試用 Flask 應用程式（SQLite in-memory）
- `client`: HTTP 測試客戶端
- `socketio_client`: Socket.IO 測試客戶端

### 測試覆蓋率目標

```ini
# pytest.ini
--cov-fail-under=70  # 最低覆蓋率 70%
```

**目前狀態**: 需執行測試確認實際覆蓋率

### 測試資料管理

- 使用 **SQLite in-memory** 資料庫
- 每個測試獨立的資料庫實例
- 測試結束後自動清理

---

## 附錄 - 實用命令與腳本

### 快速啟動腳本

**Windows** (`start-docker.bat`):
```batch
docker-compose up -d
```

**Windows** (`restart-docker.bat`):
```batch
docker-compose restart
```

### 環境變數生成

**生成安全密鑰**:
```python
# scripts/generate_secrets.py
import secrets
print(secrets.token_urlsafe(32))
```

### 資料庫初始化

**自動化腳本** (`setup_database.py`):
- 讀取 `.env` 配置
- 建立資料庫與使用者
- 設定權限
- 測試連線

### 疑難排解快速指令

```bash
# 檢查所有容器狀態
docker-compose ps

# 重新啟動有問題的服務
docker-compose restart backend

# 查看即時日誌
docker-compose logs -f

# 進入容器 shell
docker exec -it edgesurvivor_backend bash

# 檢查資料庫連線
python backend/init_db.py test

# 清除所有 Docker 快取並重建
docker-compose down -v
docker system prune -a
docker-compose up --build
```

---

## 總結與建議

### 系統優勢

 **架構清晰**: 前後端分離，模組化設計  
 **技術現代**: Vue 3, Flask, Docker 都是成熟且流行的技術  
 **測試完整**: 170+ 測試案例覆蓋核心功能  
 **文檔齊全**: 包含專案簡介、部署指南、API 文檔  
 **容器化**: Docker Compose 簡化部署流程

### 優先改進建議

1. **統一資料庫遷移流程** - 使用 Flask-Migrate 標準流程
2. **完善 Token 自動刷新** - 前端自動處理 JWT 過期
3. **Socket.IO 狀態外部化** - 使用 Redis 支援水平擴展
4. **新增 E2E 測試** - 補充端對端測試覆蓋
5. **實作 API 文檔** - 使用 Swagger/OpenAPI 自動生成 API 文檔

### 適合的開發任務類型

-  **功能新增**: 模組化架構易於擴展
-  **Bug 修復**: 測試覆蓋率高，容易驗證
-  **效能優化**: 可針對特定模組優化
-  **UI/UX 改進**: Element Plus 提供豐富組件
-  **大規模重構**: 需注意向後兼容（如 Activity.date 欄位）

---

## 附加資源

### 重要文檔連結

- **專案簡介**: [docs/project-brief.md](docs/project-brief.md) - 詳細的產品需求與市場分析（853 行）
- **部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 完整部署步驟（457 行）
- **設定指南**: [SETUP.md](SETUP.md) - 開發環境設定
- **Docker 指南**: [DOCKER-SETUP.md](DOCKER-SETUP.md) - Docker 環境說明

### 技術文檔

- **Flask 官方文檔**: https://flask.palletsprojects.com/
- **Vue 3 官方文檔**: https://vuejs.org/
- **Socket.IO 文檔**: https://socket.io/docs/
- **Element Plus**: https://element-plus.org/
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/

### 聯絡與支援

如有問題或需要協助，請參考：
- 專案 README: [README.md](README.md)
- 測試報告: `backend/test/report.html`
- Issue Tracker: （如有 GitHub/GitLab repository）

---

**文檔版本**: 1.0  
**最後更新**: 2025-12-15  
**維護者**: EdgeSurvivor 開發團隊

---

*本文檔由 Mary (Business Analyst) 根據實際程式碼庫分析生成，反映專案的真實狀態。*
