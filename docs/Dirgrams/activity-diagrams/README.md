# EdgeSurvivor 活動圖文件

本目錄包含 EdgeSurvivor 系統所有主要 Use Case 的活動圖。

## 檔案列表

| 檔案名稱 | Use Case | 說明 |
|---------|----------|------|
| `uc1-user-registration.puml` | UC1: 使用者註冊 | 註冊流程與 Email 驗證 |
| `uc2-create-activity.puml` | UC2: 建立活動 | 活動建立與驗證流程 |
| `uc3-apply-activity.puml` | UC3: 申請加入活動 | 申請流程與條件檢查 |
| `uc4-review-application.puml` | UC4: 審核參與申請 | 創建者審核流程 |
| `uc5-match-and-chat.puml` | UC5: 媒合與開啟聊天室 | 媒合流程與 Socket.IO 連線 |
| `uc6-expense-settlement.puml` | UC6: 費用分攤與結算 | 費用記錄與結算演算法 |
| `uc7-activity-review.puml` | UC7: 活動互評 | 評價流程與重複檢查 |

## 活動圖特色

### 流程元素
- **開始節點** (`start`) - 流程開始
- **活動節點** (`:活動描述`) - 具體操作步驟
- **決策節點** (`if/else`) - 條件判斷分支
- **迴圈節點** (`repeat`) - 重複操作（UC6）
- **結束節點** (`stop`) - 流程結束

### 標註說明
- **檔案路徑**：活動中標註了對應的程式檔案
- **HTTP 方法**：API 呼叫標註了 HTTP 方法和端點
- **SQL 操作**：資料庫操作標註了 SQL 語句類型
- **錯誤處理**：包含完整的錯誤處理分支

### 流程特點
- **條件分支**：使用 `if/else` 表示決策點
- **錯誤處理**：每個驗證點都有錯誤分支
- **檔案對應**：每個步驟都標註了對應的檔案路徑
- **技術細節**：包含 HTTP、SQL、Socket.IO 等技術細節

## 使用方式

### 渲染單一圖表
```bash
# 使用 PlantUML CLI
java -jar plantuml.jar uc1-user-registration.puml

# 或使用 VS Code 擴充功能
# 安裝 PlantUML 擴充功能後，按 Alt+D 預覽
```

### 線上渲染
- 使用 [PlantText](https://www.planttext.com/) 貼上程式碼
- 使用 [PlantUML Server](http://www.plantuml.com/plantuml/uml/)

## 活動圖說明

### UC1: 使用者註冊
- 包含 Email 格式驗證
- 包含 Email 唯一性檢查
- 包含密碼長度驗證
- 包含 Email 驗證流程

### UC2: 建立活動
- 包含必填欄位驗證
- 包含日期邏輯驗證
- 包含 JWT Token 驗證

### UC3: 申請加入活動
- 包含活動狀態檢查
- 包含人數檢查
- 包含性別/年齡限制檢查
- 多層決策點

### UC4: 審核參與申請
- 包含批准/拒絕分支
- 包含活動人數檢查
- 包含權限驗證

### UC5: 媒合與開啟聊天室
- 包含媒合申請流程
- 包含接受/拒絕分支
- 包含 Socket.IO 連線流程

### UC6: 費用分攤與結算
- 使用 `repeat` 迴圈表示重複新增費用
- 包含結算演算法流程
- 包含貪婪演算法計算

### UC7: 活動互評
- 包含活動狀態檢查
- 包含重複評價檢查
- 包含評價數量更新

## 相關文件

- [Use Case 泳道圖](../use-case-swimlane.puml)
- [循序圖](../sequence-diagrams/)
- [類別圖](../class-diagram.puml)
- [ERD 圖](../erd-diagram-chen.puml)

## 更新記錄

- 2025-01-XX: 初始版本，包含所有 7 個 Use Case 的活動圖

