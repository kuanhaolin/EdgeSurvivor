# EdgeSurvivor - User Stories Index
# 用戶故事索引

此目錄包含了 EdgeSurvivor MVP 階段的所有用戶故事文件。每個故事都詳細記錄了功能需求、技術實作、API 規格和資料庫架構。

##  Stories 目錄結構

所有故事檔案依據 Epic 分類，遵循命名規範：story-{epic}.{story}-{title}.md

##  已建立的核心故事 (Representative Stories)

以下是已建立的代表性故事，涵蓋了系統的核心功能：

### Epic 1: 使用者認證系統

- **[Story 1.1: 使用者註冊](story-1.1-user-registration.md)** 
  - Email/密碼註冊
  - scrypt 密碼加密
  - Email 驗證信發送

- **[Story 1.2: 使用者登入](story-1.2-user-login.md)** 
  - JWT Token 認證
  - 安全的密碼驗證
  - 登入失敗處理

### Epic 3: 活動探索與管理

- **[Story 3.1: 建立活動](story-3.1-create-activity.md)** 
  - 活動表單與資料驗證
  - 封面圖上傳
  - 活動狀態管理

### Epic 4: 媒合與參與者管理

- **[Story 4.2: 審核媒合申請](story-4.2-review-match-requests.md)** 
  - 申請批准/拒絕流程
  - 自動開啟私人聊天室
  - 人數上限檢查

### Epic 5: 溝通與討論

- **[Story 5.2: 私人聊天室](story-5.2-private-chat.md)** 
  - Socket.IO 即時通訊
  - 訊息歷史記錄
  - 未讀計數與已讀狀態

### Epic 6: 費用分攤

- **[Story 6.3: 費用自動結算](story-6.3-expense-settlement.md)** 
  - 貪婪演算法債務簡化
  - 最少轉帳次數計算
  - 結算報告生成

##  完整 Epic 與 Story 列表

以下是所有 Epic 及其包含的 Stories（依據 epic.md）：

### Epic 1: 使用者認證系統
-  Story 1.1: 註冊
-  Story 1.2: 登入
-  Story 1.3: 第三方登入 (Google)
-  Story 1.4: 忘記密碼
-  Story 1.5: 帳號管理
-  Story 1.6: 兩步驟驗證 (2FA)

### Epic 2: 個人資料管理
-  Story 2.1: 編輯資料
-  Story 2.2: 頭像上傳
-  Story 2.3: 社群連結
-  Story 2.4: 個人儀表板

### Epic 3: 活動探索與管理
-  Story 3.1: 建立活動
-  Story 3.2: 瀏覽活動
-  Story 3.3: 搜尋篩選
-  Story 3.4: 查看詳情
-  Story 3.5: 狀態管理
-  Story 3.6: 活動相簿

### Epic 4: 媒合與參與者管理
-  Story 4.1: 申請加入
-  Story 4.2: 審核申請
-  Story 4.3: 管理參與者
-  Story 4.4: 查看狀態

### Epic 5: 溝通與討論
-  Story 5.1: 活動討論串
-  Story 5.2: 私人聊天室

### Epic 6: 費用分攤
-  Story 6.1: 記錄費用
-  Story 6.2: 查看列表
-  Story 6.3: 自動結算

### Epic 7: 評價系統
-  Story 7.1: 互相評價
-  Story 7.2: 查看評價

##  Story 文件格式說明

每個故事文件包含以下標準章節：

1. **User Story** - 以用戶視角描述需求
2. **Story Context** - 現有系統整合資訊
3. **Acceptance Criteria** - 驗收標準（功能/整合/品質）
4. **Technical Notes** - 技術實作細節
5. **API Specification** - API 端點與範例
6. **Database Schema** - 相關資料表結構
7. **Definition of Done** - 完成檢查清單
8. **Risk and Compatibility Check** - 風險評估與回滾計畫
9. **Related Files** - 相關程式碼檔案
10. **Notes** - 額外說明與未來規劃

##  如何使用這些故事

這些故事文件可用於：

- **開發參考**: 了解功能的完整需求和技術實作
- **API 文件**: 查閱 API 端點規格和範例
- **資料庫設計**: 參考資料表結構和關聯
- **測試計畫**: 依據 AC 和 DoD 設計測試案例
- **新人 Onboarding**: 快速了解系統各模組的運作方式
- **未來擴展**: 基於現有模式規劃新功能

##  建立狀態

-  **已建立**: 6 個核心故事
-  **待建立**: 20 個故事（可依需求逐步建立）

##  相關文件

- [Epic 總覽](../epic.md) - 所有 Epic 與 Story 的概要
- [PRD](../prd.md) - 產品需求文件
- [Project Brief](../project-brief.md) - 專案簡介

##  注意事項

1. 所有已建立的故事標記為 ** Completed (MVP)**，代表功能已實作完成
2. 這些文件是 **Brownfield Documentation**，記錄既有系統而非新開發需求
3. 標記為  的故事可依需要建立詳細文件
4. 所有故事遵循既有系統的技術棧和架構模式

---

**Last Updated**: 2025-11-03  
**Status**: 核心故事已完成，其餘可依需求建立
