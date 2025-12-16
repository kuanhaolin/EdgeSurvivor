# EdgeSurvivor Brownfield 產品需求文檔（PRD）

**邊緣人神器 - 旅伴媒合與活動管理平台完整系統規格**

---

## 文檔資訊

| 項目 | 內容 |
|------|------|
| **文檔類型** | Brownfield 系統逆向工程 PRD |
| **專案名稱** | EdgeSurvivor（邊緣人神器） |
| **文檔版本** | 1.0 |
| **建立日期** | 2025-12-15 |
| **作者** | John (Product Manager) |
| **狀態** | 已完成 MVP，本文檔記錄現有系統 |

---

## 目錄

1. [專案分析與背景](#1-專案分析與背景)
2. [需求規格](#2-需求規格)
   - 2.1 [功能需求](#功能需求)
   - 2.2 [非功能需求](#非功能需求)
   - 2.3 [兼容性需求](#兼容性需求)
3. [技術約束](#3-技術約束)
4. [Epic 結構](#4-epic-結構)
   - [Epic 1: 用戶認證與授權系統](#epic-1-用戶認證與授權系統-user-authentication--authorization)
   - [Epic 2: 活動管理系統](#epic-2-活動管理系統-activity-management)
   - [Epic 3: 旅伴媒合系統](#epic-3-旅伴媒合系統-travel-companion-matching)
   - [Epic 4: 即時聊天系統](#epic-4-即時聊天系統-real-time-chat-system)
   - [Epic 5: 費用管理與分帳系統](#epic-5-費用管理與分帳系統-expense-management)
   - [Epic 6: 社交互動與評價系統](#epic-6-社交互動與評價系統-social-interaction)
   - [Epic 7: 檔案上傳與管理](#epic-7-檔案上傳與管理-file-upload)
5. [總結](#5-總結)

---

## 1. 專案分析與背景

### 分析來源

 **使用現有 document-project 輸出**
- 路徑：`c:\EdgeSurvivor\docs\brownfield-architecture.md`
- 建立日期：2025-12-15
- 版本：1.0
- 作者：Mary (Business Analyst)

### 當前專案狀態

**EdgeSurvivor（邊緣人神器）** 是一個完整的旅伴媒合與活動管理平台 MVP，已完成開發並具備以下核心能力：

**技術架構**：
- 三層式 Web 應用程式（Vue 3 前端 + Flask 後端 + MariaDB 資料庫）
- RESTful API + WebSocket 雙通道通訊
- Docker Compose 容器化部署
- 170+ 測試案例覆蓋核心功能

**核心功能模組**：
1. 用戶認證系統（含 2FA）
2. 活動創建與管理
3. 智能旅伴媒合系統
4. 即時聊天通訊（Socket.IO）
5. 活動討論區
6. 費用分攤計算
7. 評價與信譽系統
8. 圖片上傳管理

### 可用文檔分析

 **使用 document-project 分析輸出**

已有完整技術文檔：
-  技術堆疊文檔（後端/前端完整版本清單）
-  源代碼樹與架構
-  編碼標準（Flask Blueprint 架構、Vue 3 Composition API）
-  API 文檔（9 個 Blueprint，所有端點已記錄）
-  外部 API 文檔（Socket.IO 事件規格）
-  技術債務文檔（5 個關鍵技術債務項）

### 增強範圍定義

**增強類型**：
-  **完整系統記錄（逆向工程 PRD）**

此 PRD 的目的是為現有的 EdgeSurvivor MVP 系統創建完整的產品需求文檔，記錄所有已實現的功能、技術約束和系統能力，以便：
1. 為 AI 開發代理提供完整的系統規格參考
2. 記錄系統的「應有狀態」作為未來增強的基準
3. 識別現有技術債務並規劃改進路徑
4. 為團隊協作提供統一的功能與技術規格文檔

**影響評估**：
-  **文檔工作** - 這是記錄性文檔，不涉及程式碼變更
-  **範圍** - 覆蓋整個 EdgeSurvivor 平台的所有現有功能

### 目標與背景

**目標**：
- 為現有 MVP 創建完整的產品需求文檔
- 記錄所有已實現的功能模組及其交互
- 文檔化技術約束、已知問題和改進機會
- 建立未來增強的參考基準

**背景**：
EdgeSurvivor 平台已完成 MVP 開發，所有核心功能（用戶管理、活動創建、旅伴媒合、即時聊天、費用分攤、評價系統）均已實現並經過測試。現需要創建完整的 PRD 文檔，記錄系統的實際狀態，為未來的功能增強和程式碼維護提供可靠的參考規格。

該平台解決獨自旅行者尋找志同道合旅伴的痛點，提供從活動發布、智能配對、安全溝通到費用管理的完整流程支援。

### 變更日誌

| 變更 | 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|------|
| 初始建立 | 2025-12-15 | 1.0 | 基於現有 MVP 創建逆向工程 PRD | John (PM) |

---
## 2. 需求規格

基於現有系統的完整分析，以下是 EdgeSurvivor 平台的功能需求、非功能需求和兼容性要求。

### 功能需求

#### 用戶認證與管理

- **FR1**: 系統應支援用戶透過 email 和密碼註冊帳號，密碼使用 Werkzeug 進行雜湊加密儲存
- **FR2**: 系統應支援用戶登入並返回 JWT token（access token 和 refresh token）
- **FR3**: 系統應支援雙因素認證（2FA），使用 TOTP 協定（pyotp 實現）
- **FR4**: 系統應支援 JWT token 刷新機制，透過 `/api/auth/refresh` 端點
- **FR5**: 用戶資料應支援隱私等級設定（public/partial/hidden）和社交隱私設定（public/friends_only）
- **FR6**: 用戶個人資料應包含：姓名、地點、簡介、性別、年齡、興趣標籤（JSON 格式）、頭像 URL
- **FR7**: 系統應支援用戶評價統計（rating_count, average_rating）

#### 活動管理

- **FR8**: 用戶應能創建活動，包含：標題、描述、類別、日期範圍（start_date, end_date）、時間（start_time, end_time）、地點、集合點、最大參與人數、費用
- **FR9**: 活動應支援難度等級（easy/medium/hard）和參與者條件（性別偏好、年齡範圍）
- **FR10**: 活動創建者應能上傳封面圖和多張活動圖片（JSON 格式儲存 URL）
- **FR11**: 用戶應能查詢活動列表，支援篩選：我創建的活動（type=created）、我參加的活動（type=joined）、所有活動
- **FR12**: 活動創建者應能更新和刪除自己創建的活動
- **FR13**: 用戶應能申請加入活動（透過 `/api/activities/<id>/join`）
- **FR14**: 活動創建者應能審核參與者申請（批准/拒絕），透過 `/api/activities/<id>/participants/<user_id>`
- **FR15**: 活動應支援狀態管理（active/completed/cancelled）
- **FR16**: 系統應保留 `date` 欄位以實現向後兼容，同時支援新的 `start_date/end_date` 欄位

#### 旅伴媒合系統

- **FR17**: 用戶應能發起媒合申請，可選擇關聯活動或直接向其他用戶發起（activity_id 可為 NULL）
- **FR18**: 媒合申請應包含申請訊息（message 欄位）
- **FR19**: 媒合記錄應支援狀態流轉：pending  confirmed/rejected/cancelled
- **FR20**: 被申請用戶應能確認或拒絕媒合申請
- **FR21**: 拒絕媒合時應能提供拒絕原因（rejection_reason）
- **FR22**: 系統應記錄媒合的時間戳：申請時間（match_date）、確認時間（confirmed_date）、取消時間（cancel_date）
- **FR23**: 媒合確認後應自動創建聊天室（基於 match_id）

#### 即時聊天系統

- **FR24**: 系統應支援基於 Socket.IO 的 WebSocket 即時通訊
- **FR25**: 用戶連線時應在 `auth.token` 參數中傳遞 JWT 進行身分驗證
- **FR26**: 用戶應能加入特定聊天室（基於 match_id）
- **FR27**: 用戶應能發送和接收即時訊息
- **FR28**: 聊天訊息應同時儲存到資料庫（ChatMessage 模型）供歷史查詢
- **FR29**: 系統應支援訊息已讀狀態（is_read 欄位）
- **FR30**: 系統應廣播用戶上線/離線狀態（user_online/user_offline 事件）
- **FR31**: 系統應維護線上用戶清單（當前使用記憶體字典 online_users）

#### 活動討論區

- **FR32**: 每個活動應有獨立的討論區（ActivityDiscussion 模型）
- **FR33**: 參與者應能在活動討論區發布和查看討論內容

#### 費用分攤管理

- **FR34**: 用戶應能為活動創建費用記錄，包含：金額、描述、類別、代墊者
- **FR35**: 系統應支援三種費用分攤類型：全體分攤（all）、指定部分參與者（selected）、一對一借款（borrow）
- **FR36**: 系統應支援兩種分攤方式：平均分攤（equal）、自訂金額（custom）
- **FR37**: 費用分攤參與者資訊應以 JSON 格式儲存（split_participants）
- **FR38**: 系統應提供費用分攤摘要計算，包含：每人應付金額、代墊統計、結算建議
- **FR39**: 用戶應能更新和刪除自己創建的費用記錄

#### 評價系統

- **FR40**: 活動結束後，參與者應能對活動進行評價（ActivityReview 模型）
- **FR41**: 評價應關聯到用戶的評價統計（rating_count, average_rating）

#### 文件上傳

- **FR42**: 系統應支援圖片上傳功能（`/api/upload`）
- **FR43**: 上傳的檔案應儲存在本地檔案系統（`backend/uploads/`）
- **FR44**: 系統應返回上傳檔案的存取 URL

---
### 非功能需求

#### 效能

- **NFR1**: 系統應使用資料庫連線池（pool_size=20, max_overflow=40）以支援並行存取
- **NFR2**: 生產環境應使用 gevent 非同步模式以提高 WebSocket 連線效能
- **NFR3**: 系統應在生產環境使用 gunicorn + gevent worker 部署
- **NFR4**: API 回應時間應保持在合理範圍內（需注意 N+1 查詢問題）

#### 安全性

- **NFR5**: 所有密碼應使用 Werkzeug 進行雜湊加密，不得明文儲存
- **NFR6**: 系統應使用 JWT（Flask-JWT-Extended）進行 API 認證
- **NFR7**: 系統應支援可選的雙因素認證（2FA）增強安全性
- **NFR8**: CORS 應限制為明確允許的來源（localhost:3000, localhost:8080, 生產網域）
- **NFR9**: Socket.IO 連線應透過 JWT token 驗證用戶身分

#### 可靠性

- **NFR10**: 資料庫連線應設定 pool_pre_ping=True 以確保連線有效性
- **NFR11**: 資料庫連線應設定 pool_recycle=3600 以防止長時間連線失效
- **NFR12**: 系統應包含 170+ 測試用例覆蓋核心功能
- **NFR13**: 測試應使用獨立的 SQLite in-memory 資料庫避免污染生產資料

#### 可維護性

- **NFR14**: 後端應採用 Flask Blueprint 架構實現模組化
- **NFR15**: 前端應採用 Vue 3 Composition API（`<script setup>` 語法）
- **NFR16**: 程式碼應遵循 SQLAlchemy 2.x 語法規範
- **NFR17**: 系統應提供完整的技術文檔（brownfield-architecture.md）

#### 可擴展性

- **NFR18**: 系統架構應支援前後端獨立部署
- **NFR19**: Docker Compose 設定應支援容器化部署
- **NFR20**: 注意：當前 Socket.IO 線上用戶清單使用記憶體儲存，不支援水平擴展（已知技術債務）

#### 兼容性

- **NFR21**: 前端應支援現代瀏覽器（Chrome, Firefox, Safari, Edge）
- **NFR22**: 系統應支援 WebSocket 協定（Socket.IO）
- **NFR23**: 後端應兼容 Python 3.9+
- **NFR24**: 資料庫應使用 MariaDB 10.11

### 兼容性需求

- **CR1: 資料模型兼容性** - Activity 模型必須同時維護 `date` 和 `start_date` 欄位以支援舊版本資料和新的日期範圍功能
- **CR2: API 端點兼容性** - 所有現有 API 端點必須保持 URL 路徑、請求/回應格式不變，確保前端和整合系統正常運作
- **CR3: JWT Token 兼容性** - 認證機制必須繼續使用 JWT token，token 格式和驗證流程保持一致
- **CR4: Socket.IO 協定兼容性** - WebSocket 通訊必須繼續使用 Socket.IO 協定，事件名稱和資料格式保持不變
- **CR5: 資料庫 Schema 兼容性** - 資料庫表格結構變更必須透過遷移腳本實現，不得破壞現有資料
- **CR6: 環境設定兼容性** - 必須繼續支援透過 `.env` 檔案進行環境設定，環境變數命名保持一致
- **CR7: Docker 部署兼容性** - 必須繼續支援 Docker Compose 部署方式，容器名稱和網路設定保持穩定

---
## 3. 技術約束

### 現有技術棧

| 層級 | 技術 | 版本 | 說明 |
|------|------|------|------|
| **前端** | Vue.js | 3.3.8 | 採用 Composition API (`<script setup>`) |
| | Vue Router | 4.2.5 | 單頁應用路由 |
| | Axios | 1.6.2 | HTTP 客戶端 |
| | Socket.IO Client | 4.5.4 | WebSocket 通訊 |
| | Vite | 5.0.0 | 建置工具 |
| | Vitest | 1.0.4 | 測試框架 |
| **後端** | Python | 3.9+ | 主要程式語言 |
| | Flask | 2.3.3 | Web 框架 |
| | Flask-SocketIO | 5.3.5 | WebSocket 支援 |
| | Flask-JWT-Extended | 4.5.3 | JWT 認證 |
| | Flask-CORS | 4.0.0 | 跨域資源共享 |
| | SQLAlchemy | 2.0.23 | ORM 框架 |
| | PyMySQL | 1.1.0 | MySQL 驅動 |
| | Werkzeug | 3.0.1 | 工具庫（密碼雜湊等） |
| **資料庫** | MariaDB | 10.11 | 主資料庫 |
| | SQLite | 3.x | 測試用記憶體資料庫 |
| **部署** | Docker | Latest | 容器化 |
| | Docker Compose | Latest | 多容器編排 |
| | Gunicorn | 21.2.0 | WSGI 伺服器 |
| | Gevent | 23.9.1 | 非同步工作模式 |

### 整合策略

#### 資料庫整合
- **保持現有資料模型設計**：7個核心資料表（User, Activity, Match, ChatMessage, Expense, ActivityReview, ActivityDiscussion）
- **維持資料庫連線配置**：`pool_size=20, max_overflow=40, pool_pre_ping=True, pool_recycle=3600`
- **遵循 SQLAlchemy 2.x 語法**：使用 `select()`, `Session.scalar()` 等新 API
- **處理日期欄位遷移**：Activity 同時保留 `date` 和 `start_date`/`end_date` 欄位

#### API 整合
- **維持現有 REST API 端點**：9 個 Blueprint 模組（auth, users, activities, matches, chat, discussions, expenses, reviews, upload）
- **保持 JWT 認證流程**：使用 `@jwt_required()` 裝飾器
- **維護 Socket.IO 事件協定**：現有事件名稱和資料格式不變
- **遵循 Flask Blueprint 架構**：保持模組化設計

#### 前端整合
- **採用 Vue 3 Composition API**：使用 `<script setup>` 語法
- **維持 Vue Router 路由配置**：現有路由路徑不變
- **使用 Axios + Socket.IO 客戶端**：保持與後端通訊方式
- **保留現有 UI 組件結構**：避免大規模重構

#### WebSocket 整合
- **維持 Flask-SocketIO 架構**：保持現有事件處理邏輯
- **JWT Token 驗證**：從 query 參數或 auth 資料中提取 token
- **注意記憶體狀態限制**：線上用戶清單不支援分散式部署（已知技術債務）

#### 測試策略
- **保持 pytest 測試框架**：170+ 測試用例
- **使用 SQLite in-memory 資料庫**：測試隔離
- **維護現有測試覆蓋範圍**：包含單元測試和整合測試

### 程式碼組織標準

- **後端模組化**：按 Blueprint 分離（auth, activities, chat 等）
- **前端元件化**：Views（頁面）+ Components（可重用元件）
- **模型定義集中**：`backend/models/` 目錄統一管理
- **工具函數分離**：`backend/utils/` 目錄存放輔助功能
- **測試程式獨立**：`backend/test/` 目錄組織測試用例

### 部署環境適應

- **Docker Compose 編排**：3 個服務（frontend, backend, db）
- **環境變數管理**：使用 `.env` 檔案
- **生產環境優化**：gunicorn + gevent worker
- **容器網路隔離**：`edgesurvivor-network` 專用網路

### 風險評估

| 風險 | 影響 | 可能性 | 緩解措施 |
|------|------|--------|----------|
| Socket.IO 記憶體狀態不支援分散式部署 | 高 | 中 | 優先級 P2 - 改用 Redis 或資料庫儲存 |
| N+1 查詢效能問題 | 中 | 高 | 優先級 P1 - 使用 `joinedload()` 優化查詢 |
| 日期欄位命名不一致（date vs start_date） | 低 | 低 | 已緩解 - 同時保留兩組欄位 |
| 缺乏 API 文件 | 中 | 已發生 | 優先級 P2 - 生成 API 規格文件 |
| 測試覆蓋率未量化 | 低 | 已發生 | 優先級 P3 - 加入 pytest-cov 工具 |

---
## 4. Epic 結構

### Epic 1: 用戶認證與授權系統 (User Authentication & Authorization)

#### 用戶故事

##### Story 1.1: 用戶註冊
**身份**：新用戶  
**目的**：建立個人帳號以使用平台服務  
**場景**：我是新用戶，想要註冊一個帳號開始使用 EdgeSurvivor 平台

**驗收標準**：
- 可以透過 email 和密碼註冊
- Email 格式驗證（必須是有效的 email 格式）
- 密碼強度驗證（至少 8 字元，包含英文和數字）
- 密碼自動進行 Werkzeug 雜湊加密儲存
- 不允許重複的 email 註冊
- 註冊成功後自動登入並返回 JWT token
- 顯示註冊成功訊息

**整合驗證點**：
- 系統應呼叫 `POST /api/auth/register` 端點
- 請求 payload 應包含：email, password, name（選填）
- 後端應檢查 email 唯一性（查詢 users 表）
- 密碼應使用 `werkzeug.security.generate_password_hash()` 加密
- 成功後返回 access_token 和 refresh_token（Flask-JWT-Extended）
- 前端應將 token 儲存到 localStorage 或 sessionStorage

##### Story 1.2: 用戶登入
**身份**：已註冊用戶  
**目的**：使用 email 和密碼登入帳號  
**場景**：我是已註冊用戶，想要登入以存取我的個人資料和活動

**驗收標準**：
- 可以輸入 email 和密碼登入
- 驗證 email 和密碼是否正確
- 登入成功後返回 JWT token（access 和 refresh）
- 登入失敗顯示錯誤訊息（如：帳號或密碼錯誤）
- 支援「記住我」功能（選填）
- Token 過期時自動導向登入頁

**整合驗證點**：
- 系統應呼叫 `POST /api/auth/login` 端點
- 後端應使用 `werkzeug.security.check_password_hash()` 驗證密碼
- 成功後使用 `create_access_token()` 和 `create_refresh_token()` 生成 JWT
- 前端應在後續 API 請求的 Authorization header 中帶上 Bearer token
- 密碼錯誤應返回 401 Unauthorized 狀態碼

##### Story 1.3: JWT Token 刷新
**身份**：已登入用戶  
**目的**：在 access token 過期時自動刷新以保持登入狀態  
**場景**：我正在使用平台，access token 即將過期，系統應自動刷新而不需要我重新登入

**驗收標準**：
- Access token 過期時可使用 refresh token 取得新的 access token
- 刷新過程對用戶透明（不中斷操作）
- Refresh token 也有過期時間（較長）
- Refresh token 過期後需重新登入
- 每次刷新應返回新的 access token

**整合驗證點**：
- 系統應呼叫 `POST /api/auth/refresh` 端點
- 請求 header 應包含 `Authorization: Bearer <refresh_token>`
- 端點應使用 `@jwt_required(refresh=True)` 裝飾器
- 後端應使用 `create_access_token()` 生成新 token
- 前端應實作攔截器（Axios interceptor）自動處理 401 錯誤並刷新 token

##### Story 1.4: 啟用雙因素認證 (2FA)
**身份**：註重安全的用戶  
**目的**：啟用 2FA 以增強帳號安全性  
**場景**：我想要為我的帳號增加額外的安全保護，啟用雙因素認證

**驗收標準**：
- 可以在帳號設定中啟用 2FA
- 系統生成 TOTP secret 並顯示 QR code
- 用戶使用 Google Authenticator 等應用掃描 QR code
- 輸入 6 位數驗證碼確認啟用
- 啟用後登入時需要輸入 2FA 驗證碼
- 可以生成備用碼（未來功能）

**整合驗證點**：
- 系統應呼叫 `POST /api/auth/2fa/enable` 端點
- 後端使用 `pyotp.random_base32()` 生成 secret
- Secret 儲存到 User 模型的 `totp_secret` 欄位
- QR code 使用 `pyotp.totp.TOTP(secret).provisioning_uri()` 生成
- 前端顯示 QR code 供用戶掃描

##### Story 1.5: 使用 2FA 登入
**身份**：已啟用 2FA 的用戶  
**目的**：使用 2FA 驗證碼完成安全登入  
**場景**：我已啟用 2FA，登入時需要輸入驗證碼

**驗收標準**：
- 輸入 email 和密碼後，顯示 2FA 驗證碼輸入框
- 輸入 6 位數 TOTP 驗證碼
- 驗證碼正確後完成登入
- 驗證碼錯誤顯示錯誤訊息
- 驗證碼有時間限制（30 秒輪換）
- 提供「信任此裝置」選項（未來功能）

**整合驗證點**：
- 系統應呼叫 `POST /api/auth/login` 端點，包含 totp_code 參數
- 後端使用 `pyotp.TOTP(user.totp_secret).verify(code)` 驗證
- User 模型的 `is_2fa_enabled` 欄位應為 True
- 驗證失敗返回 401 並附帶錯誤訊息

##### Story 1.6: 編輯用戶個人資料
**身份**：已登入用戶  
**目的**：更新個人資料和偏好設定  
**場景**：我想更新我的個人資訊，讓其他用戶更了解我

**驗收標準**：
- 可以編輯姓名、地點、簡介、性別、年齡
- 可以新增或編輯興趣標籤（JSON 格式儲存）
- 可以設定隱私等級（public/partial/hidden）
- 可以設定社交隱私（public/friends_only）
- 可以上傳或更換頭像
- 修改後即時儲存並顯示更新成功訊息

**整合驗證點**：
- 系統應呼叫 `PUT /api/users/<user_id>` 端點
- 端點應使用 `@jwt_required()` 驗證身分
- 後端應驗證當前用戶只能編輯自己的資料（user_id 匹配）
- 興趣標籤應以 JSON 格式儲存到 `interests` 欄位
- 頭像 URL 儲存到 `avatar_url` 欄位

##### Story 1.7: 查看用戶個人資料
**身份**：所有用戶  
**目的**：查看其他用戶的公開資料以了解旅伴背景  
**場景**：我想查看某位用戶的個人資料，確認是否適合一起旅行

**驗收標準**：
- 可以查看用戶的公開資料（依照隱私設定）
- 顯示用戶姓名、頭像、地點、簡介、興趣
- 顯示用戶的評價統計（rating_count, average_rating）
- 隱私設定為 hidden 的用戶資料不可見
- 隱私設定為 partial 的用戶部分資料不可見（如年齡、性別）
- 顯示用戶參與過的活動數量

**整合驗證點**：
- 系統應呼叫 `GET /api/users/<user_id>` 端點
- 後端應根據 `privacy_level` 欄位過濾回應資料
- 前端應優雅處理不同隱私等級的顯示

---

### Epic 2: 活動管理系統 (Activity Management)

#### 用戶故事

##### Story 2.1: 創建活動
**身份**：已登入用戶  
**目的**：發布一個新的旅遊或活動邀請  
**場景**：我計劃了一趟旅行，想找志同道合的旅伴一起參加

**驗收標準**：
- 可以輸入活動標題和詳細描述
- 可以選擇活動類別（hiking, camping, travel, sports 等）
- 可以設定活動日期範圍（start_date, end_date）和時間（start_time, end_time）
- 可以設定活動地點和集合點
- 可以設定最大參與人數（max_participants）
- 可以設定活動費用和難度等級（easy/medium/hard）
- 可以設定參與者條件（性別偏好、年齡範圍）
- 可以上傳封面圖和活動圖片
- 創建成功後顯示活動詳情頁

**整合驗證點**：
- 系統應呼叫 `POST /api/activities` 端點
- 端點應使用 `@jwt_required()` 驗證身分
- 創建者自動設為 `creator_id`（從 JWT 取得）
- 活動狀態預設為 `active`
- 封面圖先透過 `POST /api/upload` 上傳取得 URL，再儲存到 `cover_image_url`
- 同時設定 `date` 欄位（向後兼容）和 `start_date` 欄位

##### Story 2.2: 瀏覽活動列表
**身份**：所有用戶（包含未登入）  
**目的**：瀏覽平台上的活動以找到感興趣的活動  
**場景**：我想找一些有趣的活動參加

**驗收標準**：
- 可以查看所有公開活動的列表
- 顯示活動標題、封面圖、日期、地點、參與人數
- 可以依類別篩選（hiking, travel 等）
- 可以依日期範圍篩選
- 可以依地點搜尋
- 可以依難度等級篩選
- 支援分頁載入
- 點擊活動卡片可進入詳情頁

**整合驗證點**：
- 系統應呼叫 `GET /api/activities` 端點
- 支援 query 參數：category, start_date, end_date, location, difficulty
- 預設只返回 status=active 的活動
- 回應應包含創建者基本資訊（name, avatar_url）
- 前端應顯示「剩餘名額」計算（max_participants - 當前參與人數）

##### Story 2.3: 查看活動詳情
**身份**：所有用戶  
**目的**：查看活動的完整資訊以決定是否參加  
**場景**：我對某個活動感興趣，想了解更多細節

**驗收標準**：
- 顯示活動的完整描述、日期時間、地點、費用
- 顯示創建者資料（姓名、頭像、評價）
- 顯示當前參與者列表
- 顯示活動圖片集
- 顯示活動討論區
- 顯示「立即參加」或「申請參加」按鈕
- 如果已額滿顯示「候補」選項（未來功能）
- 顯示活動狀態（進行中/已結束/已取消）

**整合驗證點**：
- 系統應呼叫 `GET /api/activities/<activity_id>` 端點
- 查詢應使用 `joinedload()` 預載參與者和創建者資料（避免 N+1）
- 回應應包含：activity 資料、creator 資料、participants 列表
- 前端應根據 status 欄位顯示不同的互動按鈕

##### Story 2.4: 申請加入活動
**身份**：已登入用戶  
**目的**：申請參加感興趣的活動  
**場景**：我找到一個喜歡的活動，想要申請加入

**驗收標準**：
- 點擊「申請參加」按鈕發送申請
- 可以選擇是否附上申請訊息（未來功能）
- 申請成功後顯示「等待審核」狀態
- 不能重複申請同一個活動
- 自己創建的活動自動成為參與者
- 活動已額滿時不能申請

**整合驗證點**：
- 系統應呼叫 `POST /api/activities/<activity_id>/join` 端點
- 端點應使用 `@jwt_required()` 驗證身分
- 後端應檢查：用戶是否已是參與者、活動是否已額滿
- 創建 ActivityParticipant 記錄，預設 status=pending
- 創建者應收到通知（未來整合推播）

##### Story 2.5: 審核參與申請（創建者）
**身份**：活動創建者  
**目的**：審核用戶的參與申請並決定是否批准  
**場景**：有用戶申請加入我的活動，我想審核他們的資料

**驗收標準**：
- 可以查看所有待審核的申請
- 顯示申請者的個人資料（姓名、頭像、簡介、評價）
- 可以批准或拒絕申請
- 批准後申請者成為正式參與者
- 拒絕後申請者收到通知
- 活動額滿時自動停止接受新申請

**整合驗證點**：
- 系統應呼叫 `PUT /api/activities/<activity_id>/participants/<user_id>` 端點
- 端點應驗證當前用戶是活動創建者
- 請求 payload 包含：status (approved/rejected)
- 後端應更新 ActivityParticipant 的 status 欄位
- 批准時應檢查是否超過 max_participants

##### Story 2.6: 查看我的活動
**身份**：已登入用戶  
**目的**：查看我創建或參加的所有活動  
**場景**：我想查看我參與的所有活動

**驗收標準**：
- 可以切換「我創建的」和「我參加的」分頁
- 顯示活動狀態（進行中/已結束）
- 可以查看活動的參與者資訊
- 創建者可以看到待審核申請的數量
- 可以快速進入活動詳情頁

**整合驗證點**：
- 系統應呼叫 `GET /api/activities?type=created` 或 `?type=joined`
- `type=created` 應過濾 creator_id=當前用戶
- `type=joined` 應查詢 ActivityParticipant 表並過濾 user_id=當前用戶 且 status=approved
- 使用 `@jwt_required()` 取得當前用戶 ID

##### Story 2.7: 編輯活動資訊
**身份**：活動創建者  
**目的**：修改活動的詳細資訊  
**場景**：我的活動計劃有變動，需要更新活動資訊

**驗收標準**：
- 只有創建者可以編輯活動
- 可以修改標題、描述、日期、地點等資訊
- 可以更換封面圖和活動圖片
- 修改後所有參與者收到通知（未來功能）
- 已開始的活動不能修改關鍵資訊（日期、地點）
- 顯示修改歷史記錄（未來功能）

**整合驗證點**：
- 系統應呼叫 `PUT /api/activities/<activity_id>` 端點
- 端點應驗證當前用戶是 creator_id
- 後端應更新 Activity 記錄
- 若修改 start_date，應同步更新 date 欄位（向後兼容）

##### Story 2.8: 取消活動
**身份**：活動創建者  
**目的**：取消已發布的活動  
**場景**：因為特殊原因我需要取消這個活動

**驗收標準**：
- 只有創建者可以取消活動
- 取消前顯示確認對話框
- 需要填寫取消原因
- 取消後活動狀態變為 cancelled
- 所有參與者收到取消通知（未來功能）
- 已取消的活動仍可查看但不能申請加入
- 可以選擇刪除活動（軟刪除或硬刪除）

**整合驗證點**：
- 系統應呼叫 `PUT /api/activities/<activity_id>` 設定 status=cancelled
- 或呼叫 `DELETE /api/activities/<activity_id>` 刪除活動
- 端點應驗證當前用戶是 creator_id
- 刪除時應考慮關聯資料（參與者、討論、費用）

##### Story 2.9: 標記活動為已完成
**身份**：活動創建者  
**目的**：在活動結束後標記為已完成  
**場景**：活動已順利結束，我想標記為完成狀態

**驗收標準**：
- 只有創建者可以標記為已完成
- 活動結束後才能標記
- 標記後狀態變為 completed
- 完成後參與者可以撰寫評價
- 完成的活動不再顯示在「進行中」列表
- 可以查看活動統計報告（參與人數、評價等）

**整合驗證點**：
- 系統應呼叫 `PUT /api/activities/<activity_id>` 設定 status=completed
- 端點應驗證當前用戶是 creator_id
- 後端應檢查 end_date 是否已過
- 完成後應觸發評價系統（允許參與者評價）

---

### Epic 3: 旅伴媒合系統 (Travel Companion Matching)

#### 用戶故事

##### Story 3.1: 發起媒合申請（基於活動）
**身份**：已登入用戶  
**目的**：向活動中的其他參與者發起旅伴媒合  
**場景**：我在某個活動中看到一位感興趣的用戶，想要與他/她建立旅伴關係

**驗收標準**：
- 可以在活動參與者列表中點擊「發起媒合」
- 可以撰寫媒合申請訊息（message 欄位）
- 申請發送後顯示「等待回應」狀態
- 不能向自己發起媒合
- 不能重複向同一用戶發起媒合
- 申請記錄關聯到 activity_id

**整合驗證點**：
- 系統應呼叫 `POST /api/matches` 端點
- 請求 payload 包含：requester_id（從 JWT 取得）, requested_id, activity_id, message
- 創建 Match 記錄，預設 status=pending, match_date=當前時間
- 被申請者應收到通知（未來整合推播）

##### Story 3.2: 發起直接媒合（不基於活動）
**身份**：已登入用戶  
**目的**：直接向其他用戶發起旅伴媒合  
**場景**：我在用戶列表中找到興趣相投的用戶，想直接邀請成為旅伴

**驗收標準**：
- 可以在用戶個人資料頁點擊「邀請成為旅伴」
- 可以撰寫邀請訊息
- activity_id 為 NULL（直接媒合）
- 申請發送後顯示「等待回應」狀態
- 系統應記錄申請時間

**整合驗證點**：
- 系統應呼叫 `POST /api/matches` 端點
- activity_id 欄位可以為 NULL
- 資料庫 schema 應允許 activity_id 為 NULL
- 媒合記錄的顯示應區分「基於活動」和「直接邀請」

##### Story 3.3: 回應媒合申請
**身份**：收到媒合申請的用戶  
**目的**：確認或拒絕他人的媒合申請  
**場景**：有用戶向我發起旅伴媒合，我想查看他的資料並決定是否接受

**驗收標準**：
- 可以查看媒合申請的詳細資訊（申請者資料、申請訊息）
- 可以點擊「確認」或「拒絕」
- 確認後媒合狀態變為 confirmed，並記錄 confirmed_date
- 拒絕時可以填寫拒絕原因（rejection_reason）
- 拒絕後狀態變為 rejected
- 確認後自動創建聊天室（基於 match_id）

**整合驗證點**：
- 系統應呼叫 `PUT /api/matches/<match_id>` 端點
- 請求 payload 包含：status (confirmed/rejected), rejection_reason（選填）
- 端點應驗證當前用戶是 requested_id
- 確認時應設定 confirmed_date=當前時間，status=confirmed
- 拒絕時應設定 status=rejected, rejection_reason
- 確認後應觸發聊天室創建邏輯

##### Story 3.4: 取消媒合申請
**身份**：媒合申請發起者  
**目的**：撤回尚未被回應的媒合申請  
**場景**：我改變主意了，想要取消之前發送的媒合申請

**驗收標準**：
- 只能取消 status=pending 的申請
- 點擊「取消申請」按鈕
- 顯示確認對話框
- 取消後狀態變為 cancelled，記錄 cancel_date
- 被申請者收到取消通知（未來功能）

**整合驗證點**：
- 系統應呼叫 `PUT /api/matches/<match_id>` 端點
- 端點應驗證當前用戶是 requester_id
- 後端應檢查 status=pending
- 更新 status=cancelled, cancel_date=當前時間

##### Story 3.5: 查看我的媒合記錄
**身份**：已登入用戶  
**目的**：查看所有我發起或收到的媒合申請  
**場景**：我想查看我的旅伴媒合情況

**驗收標準**：
- 可以切換「我發起的」和「收到的」分頁
- 顯示媒合狀態（等待中/已確認/已拒絕/已取消）
- 可以查看對方的個人資料
- 顯示申請時間和訊息
- 已確認的媒合顯示「開始聊天」按鈕
- 可以篩選不同狀態的媒合記錄

**整合驗證點**：
- 系統應呼叫 `GET /api/matches?type=sent` 或 `?type=received`
- `type=sent` 過濾 requester_id=當前用戶
- `type=received` 過濾 requested_id=當前用戶
- 回應應包含對方用戶資料（name, avatar_url）
- 使用 `joinedload()` 預載用戶資料

##### Story 3.6: 查看媒合統計
**身份**：已登入用戶  
**目的**：查看我的媒合成功率和歷史記錄  
**場景**：我想了解我的媒合表現

**驗收標準**：
- 顯示媒合總數、成功數、拒絕數
- 顯示媒合成功率
- 顯示最近成功媒合的旅伴
- 顯示基於活動的媒合 vs 直接媒合的比例
- 可以查看歷史媒合記錄

**整合驗證點**：
- 系統應呼叫 `GET /api/matches/stats` 端點
- 後端應統計當前用戶的 Match 記錄
- 計算：confirmed 數量 / 總申請數量 = 成功率
- 分別統計 activity_id IS NOT NULL 和 IS NULL 的記錄

---

### Epic 4: 即時聊天系統 (Real-time Chat System)

#### 用戶故事

##### Story 4.1: 建立聊天室（媒合確認後）
**身份**：已確認媒合的用戶  
**目的**：在媒合確認後自動創建聊天室開始溝通  
**場景**：我與另一位用戶的媒合已確認，我想開始與他/她聊天

**驗收標準**：
- 媒合確認後自動創建聊天室（基於 match_id）
- 聊天室對媒合的雙方可見
- 聊天室顯示對方的姓名和頭像
- 顯示「開始對話」提示訊息
- 聊天室列表按最後訊息時間排序

**整合驗證點**：
- 媒合確認時（Match status 變為 confirmed）應自動觸發聊天室創建
- 聊天室以 match_id 作為唯一識別
- 前端聊天列表應呼叫 `GET /api/chat/conversations` 端點
- 回應應包含：match_id, 對方用戶資料, 最後訊息, 未讀數量

##### Story 4.2: 建立 WebSocket 連線
**身份**：已登入用戶  
**目的**：建立 Socket.IO 連線以接收即時訊息  
**場景**：我開啟聊天功能，系統應自動連線到 WebSocket 伺服器

**驗收標準**：
- 進入聊天頁面時自動建立 WebSocket 連線
- 連線時傳遞 JWT token 進行身分驗證
- 連線成功後顯示線上狀態
- 連線失敗時顯示錯誤訊息並重試
- 離開頁面時自動斷開連線
- 網路斷線時自動重連

**整合驗證點**：
- 前端應使用 Socket.IO Client 連線到後端
- 連線 URL: `ws://backend:5000`（開發環境）
- 連線時應在 `auth.token` 參數中傳遞 JWT access token
- 後端 Socket.IO 的 `connect` 事件應驗證 token
- 驗證失敗應 disconnect 並返回錯誤
- 連線成功後後端應將 user_id 加入 online_users 字典

##### Story 4.3: 加入聊天室
**身份**：已登入用戶  
**目的**：加入特定的聊天室以收發訊息  
**場景**：我點擊某個聊天對象，進入聊天室

**驗收標準**：
- 點擊聊天對象後加入對應的聊天室（room = match_id）
- 自動載入歷史訊息（最近 50 條）
- 顯示對方的線上/離線狀態
- 可以看到對方正在輸入的提示（未來功能）
- 離開聊天室時自動退出 room

**整合驗證點**：
- 前端應發送 `join_room` Socket.IO 事件
- Payload: `{match_id: <match_id>}`
- 後端應驗證用戶是否為該 match 的參與者（requester 或 requested）
- 驗證通過後使用 `join_room(str(match_id))` 加入房間
- 發送 `room_joined` 事件確認
- 查詢歷史訊息：`GET /api/chat/messages?match_id=<match_id>&limit=50`

##### Story 4.4: 發送即時訊息
**身份**：已加入聊天室的用戶  
**目的**：發送文字訊息給聊天對象  
**場景**：我想傳訊息給旅伴

**驗收標準**：
- 可以輸入文字訊息並發送
- 訊息即時顯示在聊天視窗
- 訊息同時儲存到資料庫
- 顯示訊息發送時間
- 顯示訊息發送狀態（發送中/已送達/已讀）
- 支援多行文字輸入
- 空白訊息不能發送

**整合驗證點**：
- 前端發送 `send_message` Socket.IO 事件
- Payload: `{match_id: <match_id>, content: <message_text>}`
- 後端應創建 ChatMessage 記錄並儲存到資料庫
- 使用 `emit()` 將訊息廣播到該 room 的所有用戶
- 發送 `new_message` 事件，包含完整訊息資料（id, sender_id, content, timestamp）
- 前端接收 `new_message` 事件並顯示訊息

##### Story 4.5: 接收即時訊息
**身份**：已加入聊天室的用戶  
**目的**：即時接收對方發送的訊息  
**場景**：對方發送訊息給我，我應該即時收到

**驗收標準**：
- 對方發送訊息時即時顯示在聊天視窗
- 新訊息自動滾動到最底部
- 未讀訊息顯示紅點或數字提示
- 收到訊息時播放提示音（可選）
- 不在聊天室時顯示桌面通知（未來功能）
- 訊息按時間順序排列

**整合驗證點**：
- 前端監聽 `new_message` Socket.IO 事件
- 收到事件後將訊息加入聊天視窗
- 若用戶不在該聊天室，增加未讀數量
- 若用戶在該聊天室，自動標記為已讀（呼叫 `PUT /api/chat/messages/<message_id>/read`）

##### Story 4.6: 查看聊天歷史記錄
**身份**：已登入用戶  
**目的**：查看與某位旅伴的歷史聊天記錄  
**場景**：我想回顧之前與旅伴的對話內容

**驗收標準**：
- 可以滾動載入更早的訊息（無限滾動）
- 顯示訊息的發送時間
- 顯示訊息的已讀/未讀狀態
- 可以搜尋歷史訊息（未來功能）
- 支援訊息分頁載入（每次 50 條）
- 可以查看訊息的完整時間戳

**整合驗證點**：
- 系統應呼叫 `GET /api/chat/messages` 端點
- Query 參數：match_id, limit=50, offset=0
- 後端應查詢 ChatMessage 表，過濾 match_id
- 使用 `order_by(ChatMessage.created_at.desc())` 按時間倒序
- 回應應包含：訊息列表、總數、是否還有更多
- 前端實作無限滾動，觸底時增加 offset 載入更多

---

### Epic 5: 費用管理與分帳系統 (Expense Management)

#### 用戶故事

##### Story 5.1: 建立活動費用記錄
**身份**：活動參與者  
**目的**：記錄活動相關費用並選擇分帳方式  
**場景**：我參加了一個活動並支付了部分費用，我想記錄這筆支出並與其他參與者分帳

**驗收標準**：
- 可以選擇所屬活動（從參與的活動清單中選擇）
- 可以輸入費用描述、金額、幣別
- 可以選擇分帳類型（平均分攤 / 按比例 / 個別金額）
- 可以選擇分帳對象（活動參與者子集）
- 系統自動記錄建立者為支付者
- 建立成功後返回費用詳情

**整合驗證點**：
- 費用記錄必須關聯到現有 Activity 記錄
- 分帳對象必須是活動的有效參與者
- 系統應呼叫 `POST /api/expenses` 端點並傳遞費用資料
- 資料應儲存到 `expenses` 表格，包含 activity_id, payer_id, description, amount, currency, split_type

##### Story 5.2: 查看活動費用清單
**身份**：活動參與者  
**目的**：查看某個活動的所有費用記錄  
**場景**：我想檢視我參加的活動總共有哪些費用支出

**驗收標準**：
- 可以查看指定活動的所有費用記錄
- 費用清單顯示支付者、描述、金額、幣別、分帳類型
- 可以看到每筆費用的應分帳人員
- 顯示費用建立時間

**整合驗證點**：
- 系統應呼叫 `GET /api/expenses/activity/<activity_id>` 端點
- 查詢應包含支付者（User）和分帳人員資訊
- 前端應正確顯示不同分帳類型（equal, percentage, exact）

##### Story 5.3: 查看個人費用統計
**身份**：用戶  
**目的**：查看我在所有活動中的費用支付和欠款情況  
**場景**：我想知道我總共支付了多少費用，以及還欠其他人多少錢

**驗收標準**：
- 顯示我作為支付者的所有費用總額
- 顯示我需要分攤的費用總額
- 顯示淨支出（支付總額 - 應分攤總額）
- 可以依活動分組查看
- 可以依時間範圍篩選

**整合驗證點**：
- 系統應呼叫 `GET /api/expenses/user/<user_id>` 端點
- 後端應計算用戶作為 payer 的費用總和
- 後端應計算用戶在 split_with 清單中的費用分攤總和

##### Story 5.4: 修改費用記錄
**身份**：費用建立者  
**目的**：修正已建立的費用記錄資訊  
**場景**：我發現之前記錄的費用金額有誤，需要更新

**驗收標準**：
- 只有費用建立者可以編輯該費用
- 可以修改描述、金額、分帳類型、分帳對象
- 修改後所有分帳人員應收到通知（未來）
- 修改歷史應被記錄（未來）

**整合驗證點**：
- 系統應呼叫 `PUT /api/expenses/<expense_id>` 端點
- 後端應驗證當前用戶是否為費用的 payer_id
- 更新應包含 JWT 認證的 `@jwt_required()` 檢查

##### Story 5.5: 刪除費用記錄
**身份**：費用建立者  
**目的**：刪除錯誤或重複的費用記錄  
**場景**：我不小心重複建立了費用記錄，需要刪除

**驗收標準**：
- 只有費用建立者可以刪除該費用
- 刪除前應顯示確認對話框
- 刪除後應從清單中移除
- 已刪除的費用不應影響統計數據

**整合驗證點**：
- 系統應呼叫 `DELETE /api/expenses/<expense_id>` 端點
- 後端應驗證當前用戶是否為費用的 payer_id
- 應使用軟刪除或硬刪除策略（視業務需求）

##### Story 5.6: 費用幣別支援
**身份**：國際旅行者  
**目的**：以不同幣別記錄費用  
**場景**：我在不同國家旅行，需要以當地幣別記錄費用

**驗收標準**：
- 可以選擇費用幣別（TWD, USD, EUR, JPY 等）
- 系統應顯示幣別符號
- 統計數據應依幣別分組
- 未來可考慮匯率轉換功能

**整合驗證點**：
- Expense 模型的 `currency` 欄位應正確儲存
- 前端應提供幣別選擇器
- API 回應應包含 currency 資訊

---

### Epic 6: 社交互動與評價系統 (Social Interaction)

#### 用戶故事

##### Story 6.1: 撰寫活動評價
**身份**：活動參與者  
**目的**：在活動結束後分享體驗和評價  
**場景**：我參加完一個活動，想分享我的體驗並給予評分

**驗收標準**：
- 只有已參與的活動可以評價
- 可以給予 1-5 星評分
- 可以撰寫文字評論（選填）
- 可以選擇評價類型（整體 / 組織者 / 地點）
- 可以匿名或公開評價
- 提交後即時顯示在活動詳情頁

**整合驗證點**：
- 系統應呼叫 `POST /api/reviews` 端點
- 後端應驗證用戶是否為活動參與者（檢查 activity_participants）
- 資料應儲存到 `activity_reviews` 表格

##### Story 6.2: 查看活動評價列表
**身份**：所有用戶  
**目的**：查看其他人對活動的評價以決定是否參加  
**場景**：我考慮參加一個活動，想先看看其他人的評價

**驗收標準**：
- 可以查看活動的所有評價
- 顯示評價者姓名（或匿名）、評分、評論內容、時間
- 可以看到活動的平均評分
- 可以依評分高低或時間排序
- 顯示評價總數

**整合驗證點**：
- 系統應呼叫 `GET /api/reviews/activity/<activity_id>` 端點
- 查詢應包含評價者（User）資訊
- 前端應計算並顯示平均評分

##### Story 6.3: 活動討論區參與
**身份**：活動參與者或感興趣的用戶  
**目的**：在活動討論區提問或分享資訊  
**場景**：我對活動的某些細節有疑問，想在討論區詢問

**驗收標準**：
- 可以發表新討論主題
- 可以回覆其他人的討論
- 討論內容應即時更新
- 可以看到討論發表時間和作者
- 活動建立者的回覆應有特殊標示

**整合驗證點**：
- 系統應呼叫 `POST /api/discussions` 端點
- 資料應儲存到 `activity_discussions` 表格
- 查詢應使用 `GET /api/discussions/activity/<activity_id>` 端點

##### Story 6.4: 修改或刪除自己的評價
**身份**：評價撰寫者  
**目的**：修正或移除我之前的評價  
**場景**：我想修改之前的評價內容或評分

**驗收標準**：
- 只能修改或刪除自己的評價
- 修改評價後應更新平均評分
- 刪除評價需要確認
- 修改歷史應被記錄（未來功能）

**整合驗證點**：
- 系統應呼叫 `PUT /api/reviews/<review_id>` 或 `DELETE /api/reviews/<review_id>` 端點
- 後端應驗證當前用戶是否為評價的 user_id

---

### Epic 7: 檔案上傳與管理 (File Upload)

#### 用戶故事

##### Story 7.1: 上傳用戶頭像
**身份**：註冊用戶  
**目的**：上傳個人頭像以建立個人形象  
**場景**：我想上傳一張照片作為我的個人頭像

**驗收標準**：
- 可以選擇圖片檔案上傳（支援 JPG, PNG, GIF）
- 檔案大小限制在 5MB 以內
- 系統應自動壓縮並產生縮圖
- 上傳成功後頭像即時更新
- 舊頭像應被刪除或覆蓋

**整合驗證點**：
- 系統應呼叫 `POST /api/upload` 端點並指定 upload_type=avatar
- 後端應驗證檔案類型和大小
- 檔案應儲存到 `backend/uploads/avatars/` 目錄
- User 模型的 `avatar_url` 欄位應更新

##### Story 7.2: 上傳活動圖片
**身份**：活動建立者  
**目的**：上傳活動宣傳圖片吸引參與者  
**場景**：我建立了一個活動，想上傳一張圖片讓活動更吸引人

**驗收標準**：
- 可以在建立或編輯活動時上傳圖片
- 支援 JPG, PNG 格式
- 檔案大小限制在 10MB 以內
- 圖片應顯示在活動詳情頁
- 每個活動可以上傳多張圖片（未來功能）

**整合驗證點**：
- 系統應呼叫 `POST /api/upload` 端點並指定 upload_type=activity
- 檔案應儲存到 `backend/uploads/activities/` 目錄
- Activity 模型的 `image_url` 欄位應更新

##### Story 7.3: 查看和刪除已上傳檔案
**身份**：檔案上傳者  
**目的**：管理我上傳的檔案  
**場景**：我想查看或刪除之前上傳的檔案

**驗收標準**：
- 可以查看我上傳的所有檔案清單
- 可以刪除自己上傳的檔案
- 刪除檔案前應顯示確認對話框
- 刪除後相關引用應更新為預設圖片

**整合驗證點**：
- 系統應提供 `GET /api/uploads/user/<user_id>` 端點查詢檔案
- 刪除應呼叫 `DELETE /api/uploads/<file_id>` 端點
- 後端應同時刪除檔案系統中的實體檔案

---
## 5. 總結

### 系統概覽

| 項目 | 數量 | 說明 |
|------|------|------|
| **Epic 總數** | 7 | 涵蓋用戶認證、活動管理、配對、聊天、費用、評價、上傳 |
| **用戶故事總數** | 51 | 完整描述系統功能需求（Epic 1-7 完整覆蓋） |
| **功能需求** | 44 | 詳細的功能規格說明 |
| **非功能需求** | 24 | 涵蓋效能、安全、可靠性等面向 |
| **兼容性需求** | 7 | 確保系統整合順暢 |
| **已知技術債務** | 5 | 需要優先處理的技術問題 |

### 技術架構亮點

- **前端**：Vue 3.3.8 + Composition API + Vite
- **後端**：Flask 2.3.3 + SQLAlchemy 2.0 + Flask-SocketIO
- **資料庫**：MariaDB 10.11（生產）+ SQLite（測試）
- **部署**：Docker Compose + Gunicorn + Gevent
- **測試**：170+ pytest 測試用例
- **即時通訊**：Socket.IO（WebSocket）

### 已知技術債務清單

1. **Socket.IO 線上用戶清單使用記憶體儲存** (優先級 P2)
   - **影響**：不支援分散式部署
   - **緩解措施**：改用 Redis 或資料庫儲存

2. **N+1 查詢效能問題** (優先級 P1)
   - **影響**：資料量增加時效能下降
   - **緩解措施**：使用 `joinedload()` 預加載關聯資料

3. **Activity 日期欄位命名不一致** (優先級 P3)
   - **影響**：程式碼可讀性較差
   - **緩解措施**：已同時保留 `date` 和 `start_date`/`end_date` 欄位

4. **缺乏 API 文件** (優先級 P2)
   - **影響**：前後端協作和維護困難
   - **緩解措施**：生成 OpenAPI/Swagger 規格文件

5. **測試覆蓋率未量化** (優先級 P3)
   - **影響**：無法確保測試品質
   - **緩解措施**：加入 pytest-cov 工具並設定覆蓋率目標

### 未來擴展方向

#### 短期增強（3-6 個月）
- **推播通知系統**：即時通知用戶活動更新、配對結果、聊天訊息
- **進階搜尋與篩選**：支援多條件組合搜尋活動
- **用戶興趣標籤**：改善配對演算法精準度
- **活動推薦引擎**：基於用戶歷史和興趣推薦活動

#### 中期擴展（6-12 個月）
- **社交網路功能**：好友系統、動態牆、追蹤功能
- **支付整合**：整合第三方支付平台（Stripe, PayPal）
- **地圖整合**：活動地點視覺化（Google Maps, Mapbox）
- **多語言支援**：國際化（i18n）英文、日文等

#### 長期願景（12+ 個月）
- **行動應用程式**：iOS 和 Android 原生應用
- **AI 智慧配對**：機器學習改善配對演算法
- **區塊鏈驗證**：用戶評價和活動記錄上鏈
- **企業版本**：團隊建設和企業活動管理功能

---

## 7. 附錄

### 參考文件

- **技術架構文件**：`docs/brownfield-architecture.md`（2025-12-15）
- **測試用例**：`backend/test/` 目錄（170+ 測試檔案）
- **資料庫初始化**：`db/init.sql`, `backend/init_docker_db.py`
- **部署指南**：`DEPLOYMENT_GUIDE.md`, `DOCKER_START_GUIDE.md`

### Epic 與用戶故事索引

| Epic | 故事數 | 涵蓋模組 |
|------|--------|----------|
| Epic 1: 用戶認證與授權 | 7 | auth, users |
| Epic 2: 活動管理系統 | 9 | activities, discussions |
| Epic 3: 旅伴媒合系統 | 6 | matches |
| Epic 4: 即時聊天系統 | 6 | chat, socketio |
| Epic 5: 費用管理與分帳 | 6 | expenses |
| Epic 6: 社交互動與評價 | 4 | reviews, discussions |
| Epic 7: 檔案上傳與管理 | 3 | upload |
| **總計** | **41** | **9 個 Blueprint 模組** |

### 資料模型快速參考

- **User**: 用戶基本資訊、認證、興趣標籤、2FA
- **Activity**: 活動基本資訊、日期、地點、參與者限制
- **ActivityParticipant**: 活動參與關係（多對多）
- **Match**: 用戶配對記錄、配對分數
- **ChatMessage**: 聊天訊息、發送者、接收者、時間戳
- **Expense**: 費用記錄、支付者、分帳資訊
- **ActivityReview**: 活動評價、評分、評論
- **ActivityDiscussion**: 活動討論區訊息

### API 端點快速參考

| Blueprint | 端點前綴 | 主要功能 |
|-----------|----------|----------|
| auth | `/api/auth` | 註冊、登入、2FA |
| users | `/api/users` | 用戶資料、興趣 |
| activities | `/api/activities` | 活動 CRUD、參與 |
| matches | `/api/matches` | 配對請求、結果 |
| chat | `/api/chat` | 聊天記錄 |
| discussions | `/api/discussions` | 活動討論 |
| expenses | `/api/expenses` | 費用管理 |
| reviews | `/api/reviews` | 活動評價 |
| upload | `/api/upload` | 檔案上傳 |

### 變更記錄

| 版本 | 日期 | 變更內容 | 作者 |
|------|------|----------|------|
| 1.0 | 2025-12-15 | 初始版本 - 基於 brownfield-architecture.md 逆向工程生成 | John (PM Agent) |

---

## 文件完成

本產品需求文檔（PRD）已完整涵蓋 EdgeSurvivor 平台的所有現有功能和技術細節。文檔基於現有程式碼庫和測試用例逆向工程生成，旨在為 AI Agent 提供完整的系統理解和開發指引。

**文檔狀態**： 完成  
**最後更新**：2025-12-15  
**維護者**：John (Product Manager Agent)
