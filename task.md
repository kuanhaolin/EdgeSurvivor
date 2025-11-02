# 專案名稱

邊緣人神器 EdgeSurvivor

---

## 專案目標

建立一個專注於「旅伴與活動媒合」的中介平台，讓使用者能方便地找到合適的同行者。

主要目標：

1. 讓使用者能建立或搜尋旅伴活動。
2. 提供媒合與初步聯繫功能（內建聊天室）。
3. 提供活動紀錄與費用分攤功能，簡化行程後的結算。

---

## 軟體架構

- **架構模式**：MVC
- **前端框架**：Vue 3 (Composition API) + Element Plus
- **前端建構工具**：Vite
- **後端框架**：Python Flask (RESTful API)
- **資料庫**：MySQL / MariaDB
- **ORM**：SQLAlchemy 2.x
- **部署環境**：Docker / Nginx（後續可加）
- **驗證機制**：JWT (Flask-JWT-Extended)
- **即時通訊**：Socket.IO（聊天室）
- **檔案上傳**：Werkzeug FileStorage
- **開發代理**：Vite Proxy (API & 上傳檔案路由)

---

## 系統模組與 Use Cases

### 1. 使用者管理模組

- 註冊 / 登入 / 登出
- 個人資料管理（暱稱、性別、地區、興趣、頭像）
- 基本隱私設定（是否公開社群帳號）
- 個人統計儀表板（活動數、媒合數、旅行天數）

### 2. 旅伴媒合模組（核心功能）

- 活動建立（含主題、地點、日期、說明、封面圖）
- 活動搜尋與條件篩選（地點、日期、性別、活動類型）
- 活動參與申請（申請、審核、接受、拒絕）
- 媒合申請（申請、接受、拒絕）
- 聊天室初步聯繫（雙方媒合成功後可開啟聊天室）

### 3. 活動管理模組

- 瀏覽活動（全部 / 自己建立的 / 參與的）
- 活動詳細頁面（資訊、參與者、討論串、費用、相簿）
- 活動討論串（參與者即時交流）
- 活動相簿（上傳與瀏覽照片）
- 參與者管理（審核申請、移除成員）
- 歷史活動紀錄

### 4. 費用分攤模組

- 新增費用（含類別、金額、說明）
- 標記付款者
- 分攤計算（自動計算最佳結算方案）
- 顯示結算結果（誰付誰多少錢）
- 費用明細查看

### 5. 上傳服務模組

- 圖片上傳（支援頭像、活動封面、相簿照片）
- 檔案驗證（類型、大小限制）
- 靜態檔案服務

---

## 5. 延後功能（第二階段以後再考慮）

- 社群帳號綁定（IG / LINE / Facebook）
- 信任徽章 / 驗證標章
- 活動提醒通知（Email / 推播）
- 活動評價系統
- 推薦系統
- 多語系支援（zh-TW / en）

---

## 6. 資料庫需求

> **注意**: 所有欄位命名採用 snake_case (小寫加底線)

### users 表格

- `user_id`: 使用者唯一識別碼 (主鍵, 自動遞增)
- `name`: 使用者姓名 (字串, 非空)
- `email`: 使用者電子郵件 (字串, 唯一, 非空, 索引)
- `password_hash`: 密碼雜湊值 (字串, 非空)
- `privacy_setting`: 隱私設定 (字串, 預設 'public') - 可選值: public, partial, hidden
- `location`: 使用者位置 (字串)
- `profile_picture`: 使用者頭像圖片 URL (字串)
- `bio`: 個人簡介 (文字)
- `gender`: 性別 (字串)
- `age`: 年齡 (整數)
- `join_date`: 註冊日期 (日期時間, 預設當前時間)
- `is_verified`: 是否已驗證 (布林值, 預設 false)
- `is_active`: 帳號是否啟用 (布林值, 預設 true)
- `last_seen`: 最後上線時間 (日期時間)

### activities 表格

- `activity_id`: 活動唯一識別碼 (主鍵, 自動遞增)
- `title`: 活動標題 (字串, 非空)
- `date`: 活動日期 (日期)
- `start_time`: 活動開始時間 (字串)
- `location`: 活動地點 (字串)
- `description`: 活動描述 (文字)
- `category`: 活動分類 (字串) - 例如: 冒險、文化、休閒、運動、美食
- `max_participants`: 最大參與人數 (整數)
- `cost`: 活動費用 (數字)
- `duration_hours`: 活動時長(小時) (整數)
- `status`: 活動狀態 (字串, 預設 'open') - 可選值: open, ongoing, completed, cancelled
- `cover_image`: 活動封面圖片 URL (字串)
- `images`: 活動相簿圖片 JSON 陣列 (文字)
- `is_active`: 活動是否啟用 (布林值, 預設 true)
- `creator_id`: 活動創建者 (外鍵 → users.user_id, 非空)
- `created_at`: 建立時間 (日期時間, 預設當前時間)
- `updated_at`: 更新時間 (日期時間, 自動更新)

### activity_participants 表格 (新增)

- `participant_id`: 參與記錄唯一識別碼 (主鍵, 自動遞增)
- `activity_id`: 活動 ID (外鍵 → activities.activity_id, 非空)
- `user_id`: 使用者 ID (外鍵 → users.user_id, 非空)
- `status`: 參與狀態 (字串, 預設 'pending') - 可選值: pending, approved, joined, rejected, left, removed
- `role`: 角色 (字串, 預設 'participant') - 可選值: creator, participant
- `joined_at`: 加入時間 (日期時間, 預設當前時間)
- `approved_at`: 批准時間 (日期時間)
- `left_at`: 離開時間 (日期時間)
- `message`: 申請訊息 (文字)
- `rejection_reason`: 拒絕原因 (文字)
- **唯一約束**: (activity_id, user_id) - 一個使用者在同一活動中只能有一條記錄

### activity_discussions 表格 (新增)

- `discussion_id`: 討論訊息唯一識別碼 (主鍵, 自動遞增)
- `activity_id`: 活動 ID (外鍵 → activities.activity_id, 非空)
- `user_id`: 訊息發送者 ID (外鍵 → users.user_id, 非空)
- `message`: 訊息內容 (文字, 非空)
- `message_type`: 訊息類型 (字串, 預設 'text') - 可選值: text, image, announcement
- `created_at`: 建立時間 (日期時間, 預設當前時間)
- `updated_at`: 更新時間 (日期時間, 自動更新)
- `is_deleted`: 是否已刪除 (布林值, 預設 false)

### matches 表格

- `match_id`: 媒合唯一識別碼 (主鍵, 自動遞增)
- `activity_id`: 活動 ID (外鍵 → activities.activity_id)
- `user_a`: 使用者 A (外鍵 → users.user_id, 非空)
- `user_b`: 使用者 B (外鍵 → users.user_id, 非空)
- `status`: 媒合狀態 (字串, 預設 'pending') - 可選值: pending, accepted, confirmed, rejected, cancelled
- `match_date`: 媒合建立日期 (日期時間, 預設當前時間)
- `confirmed_date`: 媒合確認日期 (日期時間)
- `cancel_date`: 媒合取消日期 (日期時間)

### chat_messages 表格

- `message_id`: 訊息唯一識別碼 (主鍵, 自動遞增)
- `match_id`: 媒合 ID (外鍵 → matches.match_id, 非空)
- `sender_id`: 訊息發送者 ID (外鍵 → users.user_id, 非空)
- `content`: 訊息內容 (文字, 非空)
- `timestamp`: 訊息時間戳 (日期時間, 預設當前時間)
- `message_type`: 訊息類型 (字串, 預設 'text') - 可選值: text, image, file
- `status`: 訊息狀態 (字串, 預設 'sent') - 可選值: sent, delivered, read

### expenses 表格

- `expense_id`: 費用唯一識別碼 (主鍵, 自動遞增)
- `activity_id`: 活動 ID (外鍵 → activities.activity_id, 非空)
- `payer_id`: 付款者 ID (外鍵 → users.user_id, 非空)
- `amount`: 金額 (浮點數, 非空)
- `category`: 費用類別 (字串) - 可選值: transport, accommodation, food, ticket, other
- `expense_date`: 費用產生日期 (日期)
- `description`: 費用描述 (文字)
- `paid`: 是否已支付 (布林值, 預設 false)
- `created_at`: 建立時間 (日期時間, 預設當前時間)

### social_accounts 表格 (延後實作)

- `social_account_id`: 社群帳號唯一識別碼 (主鍵, 自動遞增)
- `user_id`: 使用者 ID (外鍵 → users.user_id, 非空)
- `provider`: 社群平台提供者 (字串) - 例如: Facebook, Google, Instagram
- `account_id`: 社群帳號 ID (字串)
- `access_token`: 授權令牌 (字串)
- `expiration_date`: 令牌過期時間 (日期時間)

### notifications 表格 (延後實作)

- `notification_id`: 通知唯一識別碼 (主鍵, 自動遞增)
- `user_id`: 使用者 ID (外鍵 → users.user_id, 非空)
- `message`: 通知內容 (文字, 非空)
- `type`: 通知類型 (字串) - 例如: match, expense, activity, system
- `status`: 通知狀態 (字串, 預設 'unread') - 可選值: unread, read
- `timestamp`: 通知時間 (日期時間, 預設當前時間)

---

## 7. 任務指引 (for Copilot Agent)

> 你是負責協助本系統開發的 Copilot Agent，請根據上述架構與 Use Case，協助：
>
> - Flask 後端 API 開發與維護（Blueprint + SQLAlchemy ORM）
> - Vue 3 前端頁面開發（Composition API + Element Plus）
> - RESTful API 設計與實作
> - 資料庫 schema 設計與遷移（MySQL/MariaDB）
> - 聊天室即時通訊功能（Socket.IO）
> - 檔案上傳與靜態資源服務
> - 系統功能測試與 Bug 修復

### 已實作的 API 端點

#### 認證 (auth_bp: /api/auth)

- POST `/register` - 使用者註冊
- POST `/login` - 使用者登入
- POST `/logout` - 使用者登出
- POST `/refresh` - 刷新 Token
- GET `/me` - 取得當前使用者資訊
- POST `/change-password` - 修改密碼

#### 使用者 (users_bp: /api/users)

- GET `/profile` - 取得個人資料
- PUT `/profile` - 更新個人資料
- GET `/stats` - 取得使用者統計資訊
- GET `/<user_id>` - 取得指定使用者資訊

#### 活動 (activities_bp: /api/activities)

- GET `/` - 取得活動列表 (支援篩選)
- POST `/` - 建立新活動
- GET `/<activity_id>` - 取得活動詳情
- PUT `/<activity_id>` - 更新活動資訊
- DELETE `/<activity_id>` - 刪除活動
- POST `/<activity_id>/join` - 申請加入活動
- GET `/<activity_id>/participants` - 取得參與者列表
- POST `/participants/<participant_id>/approve` - 批准參與申請
- POST `/participants/<participant_id>/reject` - 拒絕參與申請
- DELETE `/participants/<participant_id>` - 移除參與者

#### 媒合 (matches_bp: /api/matches)

- GET `/` - 取得媒合列表
- POST `/` - 建立媒合申請
- PUT `/<match_id>` - 更新媒合狀態
- DELETE `/<match_id>` - 刪除媒合

#### 聊天 (chat_bp: /api/chat)

- GET `/matches/<match_id>/messages` - 取得聊天訊息
- POST `/matches/<match_id>/messages` - 發送訊息

#### 討論串 (discussions_bp: /api)

- GET `/activities/<activity_id>/discussions` - 取得活動討論訊息
- POST `/activities/<activity_id>/discussions` - 發送討論訊息
- DELETE `/discussions/<discussion_id>` - 刪除討論訊息

#### 費用 (expenses_bp: /api)

- GET `/activities/<activity_id>/expenses` - 取得費用列表
- POST `/activities/<activity_id>/expenses` - 新增費用
- DELETE `/expenses/<expense_id>` - 刪除費用
- GET `/activities/<activity_id>/expenses/settlement` - 取得結算方案

#### 上傳 (upload_bp: /api/upload)

- POST `/image` - 上傳圖片 (支援頭像、封面、相簿)

#### 靜態檔案

- GET `/uploads/<filename>` - 存取已上傳的檔案

### 前端頁面結構

- `/` - 首頁
- `/login` - 登入頁面
- `/register` - 註冊頁面
- `/dashboard` - 個人儀表板
- `/activities` - 活動列表
- `/activities/:id` - 活動詳細頁面
- `/matches` - 媒合列表
- `/chat` - 聊天室
- `/profile` - 個人資料

---

## 完成定義 (MVP)

### 後端 (Backend)

- ✅ Flask 專案可成功啟動並連線 MySQL
- ✅ JWT 驗證機制運作正常
- ✅ RESTful API 完整實作 (auth, users, activities, matches, chat, discussions, expenses, upload)
- ✅ SQLAlchemy ORM 模型建立 (User, Activity, Match, ChatMessage, Expense, ActivityParticipant, ActivityDiscussion)
- ✅ 檔案上傳功能 (圖片驗證、大小限制、靜態檔案服務)

### 前端 (Frontend)

- ✅ Vue 3 前端可登入並顯示活動列表
- ✅ Dashboard 個人統計頁面
- ✅ 可建立活動 (含封面圖上傳)
- ✅ 可搜尋與篩選活動
- ✅ 活動詳細頁面 (資訊/參與者/討論串/費用/相簿)
- ✅ 參與活動申請與審核流程
- ✅ 活動討論串即時交流
- ✅ 活動相簿照片上傳與瀏覽
- ✅ 個人資料管理 (含頭像上傳)

### 媒合與聊天

- ✅ 媒合申請與管理 (申請、接受、拒絕)
- ✅ 媒合成功後可開啟聊天室
- ✅ Socket.IO 即時通訊 (已建立但需測試)

### 費用分攤

- ✅ 新增費用記錄 (含類別標籤)
- ✅ 分攤計算 (自動計算最佳結算方案)
- ✅ 結算結果顯示 (誰付誰多少錢)

### ~~待完成項目~~ 新增項目(含以上更新)

- ✅ Socket.IO 聊天室即時更新測試
- ✅ 討論串即時更新 (目前需手動重新整理)
- ✅ 未讀訊息數量計算
- ✅ ~~旅行天數精確計算~~ (改成評語數量)
- ✅ 兩步驟驗證功能 (使用驗證器)
- ✅ Email ~~通知功能~~ (忘記密碼使用 | 與測試同時存在 如果email沒有連線 就會直接顯示驗證碼 最後要關掉這個)
- ✅ 社群帳號連結與顯示
- ✅ 隱私設定公開/不公開 (社群)
- ✅ 第三方登入 (Google OAuth2)
- ✅ 變更密碼 (登入後與忘記密碼不同)
- ✅ 刪除帳號
- ✅ 新增陌生訊息
- ✅ 刪除好友
- ✅ 篩選功能 (活動, 交友)
- ✅ 活動互評 (評語)
- ✅ 個頁面的ㄧ些欄位新增

---

---
