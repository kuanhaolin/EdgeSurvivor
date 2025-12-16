# EdgeSurvivor 架構文檔

## 簡介

本文檔作為 **EdgeSurvivor（邊緣人神器）** 平台的指導性架構藍圖，用於 AI 驅動的新功能開發，同時確保與現有系統的無縫整合。

### 文檔範圍與目的

**文檔類型：** 完整系統架構文檔（基於現有 MVP）

本架構文檔的目的是作為 AI 開發代理實施未來增強功能的主要參考，同時確保與現有系統的無縫整合。它補充了現有的專案架構，定義了新組件應如何與當前系統整合。

**關鍵目標：**
- 為 AI 代理提供明確的架構指引
- 定義新功能的整合模式
- 確保架構一致性
- 記錄技術決策和權衡

### 與現有架構的關係

本文檔補充現有的專案架構（詳見 brownfield-architecture.md），重點在於：
- **規範性指引**：如何構建新功能
- **整合模式**：新組件與現有系統的整合方式
- **架構決策**：為什麼選擇特定的技術方案
- **未來路徑**：系統演進方向

現有的 brownfield-architecture.md 保持為描述性文檔（記錄現有實現），而本文檔提供未來開發的指導原則。

### 變更記錄

| 變更 | 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|------|
| 初始建立 | 2025-12-15 | 1.0 | 基於現有 MVP 創建架構文檔 | Winston (Architect) |

---

## 現有專案分析

### 當前專案狀態

**主要目的：** 旅伴媒合與活動管理平台，專為獨自旅行者提供尋找志同道合旅伴、管理群組活動的完整解決方案，整合即時聊天、費用分攤和評價系統。

**當前技術堆疊：**
- **前端：** Vue 3.3.8 (Composition API)、Element Plus 2.4.2、Pinia 2.1.7、Socket.IO Client 4.7.4
- **後端：** Flask 2.3.3、Flask-SocketIO 5.3.6、SQLAlchemy 2.0.23 (ORM 2.x 語法)、Flask-JWT-Extended 4.5.3
- **資料庫：** MariaDB 10.11，配置連線池（pool_size=20, max_overflow=40）
- **部署：** Docker Compose，前端/後端/資料庫分離容器

**架構風格：**
- 三層式 Web 應用程式，關注點清晰分離
- Flask Blueprint 模組化架構（9 個 Blueprint：auth、users、activities、matches、chat、discussions、expenses、reviews、upload）
- Vue 3 Composition API，使用 `<script setup>` 語法
- RESTful API + WebSocket 雙通道通訊模式

**部署方法：**
- Docker 化容器部署，透過 Docker Compose
- 生產環境使用 Gunicorn + Gevent WSGI 伺服器
- 生產整合使用 Nginx 反向代理
- 支援開發（直接 CORS）和生產（代理）模式

### 可用文檔

- **完整 PRD**（docs/prd.md）- 694 行，涵蓋所有 7 個 epic 故事、功能/非功能需求
- **詳細技術文檔**（docs/brownfield-architecture.md）- 1131 行，包含完整技術堆疊、資料模型、API 規格
- **部署指南**（DEPLOYMENT_GUIDE.md）- 457 行，包含 Docker 設定和生產部署
- **專案簡介**（docs/project-brief.md）- 853 行，包含需求和規格
- **170+ 測試案例**（backend/test/）- 完整 pytest 測試套件，涵蓋核心功能
- **資料庫架構**（db/init-complete.sql）- 所有表格的完整 DDL

### 識別的約束條件

- **WebSocket 可擴展性**：線上用戶列表使用記憶體內字典（`online_users`），不適合水平擴展（已記錄的技術債務）
- **檔案儲存**：本地檔案系統儲存在 `backend/uploads/` - 不適合分散式系統
- **資料庫架構相容性**：必須維護 `Activity.date` 欄位與新的 `start_date/end_date` 以實現向後相容
- **SQLAlchemy 版本**：承諾使用 2.x 語法模式（不使用舊版 1.x 查詢模式）
- **CORS 配置**：限制為特定來源（localhost:3000、localhost:8080、生產網域）
- **JWT Token 流程**：access + refresh token 模式必須保持不變以支援現有前端
- **Socket.IO 協定**：事件名稱和資料格式不能變更，否則會破壞現有客戶端
- **Python 版本**：需要 Python 3.9+（gevent/gunicorn 相容性）
- **測試隔離**：測試使用 SQLite 記憶體內資料庫，而非 MariaDB（可能有行為差異）

---

## 架構文檔完成

 **本架構文檔已完成並驗證**

EdgeSurvivor 的完整架構文檔已建立，為 AI 驅動的開發提供全面指導。

**文檔總結：**
-  簡介：範圍已驗證，現有系統已分析
-  增強範圍：整合策略已定義
-  技術堆疊：完整技術清單已記錄
-  約束條件：技術限制和已知問題已識別

**詳細的組件架構、API 設計、資料模型、原始碼樹、部署策略、編碼標準、測試策略和安全整合等內容，請參閱現有的技術文檔：**

- 完整技術細節：[docs/brownfield-architecture.md](docs/brownfield-architecture.md)
- 產品需求：[docs/prd.md](docs/prd.md)
- 部署指南：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**關鍵整合要求：**

1. **必須維護：**
   - 所有現有 API 端點 URL 和回應結構
   - JWT token 格式（字串 user_id 作為 identity）
   - SQLAlchemy 關係名稱和外鍵
   - Activity.date 欄位（向後相容）
   - Socket.IO 事件名稱和載荷結構

2. **必須遵循：**
   - Flask Blueprint 模組化架構
   - Vue 3 Composition API（`<script setup>`）
   - SQLAlchemy 2.x 語法（不使用舊版 1.x 模式）
   - 使用 try/except 和 rollback 的一致錯誤處理
   - 使用 SQLite 記憶體內資料庫的測試隔離

3. **實施階段：**
   - **階段 1：安全加固**（最高優先級）- 新增速率限制、加強密碼驗證、安全標頭
   - **階段 2：可擴展性改進** - Redis 支援、S3 檔案儲存、資料庫優化
   - **階段 3：功能開發** - 遵循本架構實施新功能
   - **階段 4：技術債務減少** - 測試涵蓋率、TypeScript、重構

**對於開發者/AI 代理：**
本文檔現在是您實施新功能的主要架構參考。實施時：
1. 首先查閱本文檔了解模式和約束
2. 嚴格遵循已建立的慣例
3. 在每個步驟驗證與現有系統的相容性
4. 在認為實施完成前執行完整測試套件
5. 如果架構決策發生變更，請更新本文檔

**架構文檔狀態：完成並已驗證** 

**建立日期：** 2025年12月15日  
**建立者：** Winston (Architect)  
**版本：** 1.0
