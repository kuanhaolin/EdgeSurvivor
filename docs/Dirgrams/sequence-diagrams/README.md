# EdgeSurvivor 循序圖文件

本目錄包含 EdgeSurvivor 系統所有主要 Use Case 的循序圖。

## 檔案列表

| 檔案名稱 | Use Case | 說明 |
|---------|----------|------|
| `uc1-user-registration.puml` | UC1: 使用者註冊 | 包含 Email 驗證流程 |
| `uc2-create-activity.puml` | UC2: 建立活動 | 活動建立與參與者加入 |
| `uc3-apply-activity.puml` | UC3: 申請加入活動 | 申請流程與條件檢查 |
| `uc4-review-application.puml` | UC4: 審核參與申請 | 創建者審核流程 |
| `uc5-match-and-chat.puml` | UC5: 媒合與開啟聊天室 | 包含 Socket.IO 即時通訊 |
| `uc6-expense-settlement.puml` | UC6: 費用分攤與結算 | 費用計算與結算方案 |
| `uc7-activity-review.puml` | UC7: 活動互評 | 評價流程與重複檢查 |

## 圖表特色

### 標註說明
- **HTTP 方法**：所有 HTTP 請求都標註了方法（GET、POST、PUT、DELETE）
- **HTTP 狀態碼**：回應中包含狀態碼（200、201、400 等）
- **SQL 操作**：資料庫操作標註了 SQL 語句類型（SELECT、INSERT、UPDATE）
- **檔案路徑**：參與者標註了對應的程式檔案路徑
- **WebSocket**：Socket.IO 互動標註了 WebSocket 事件

### 參與者說明
- **使用者/創建者/參與者**：系統使用者
- **前端 SPA (Vue 3)**：Vue 3 前端應用
- **後端 API (Flask)**：Flask 後端服務，標註對應的 Blueprint 檔案
- **資料庫 (MariaDB)**：資料庫，標註對應的 Model 檔案
- **Socket.IO 伺服器**：即時通訊服務
- **Email 服務**：Email 發送服務

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

## 檔案結構對應

### 後端檔案結構
```
backend/
├── blueprints/
│   ├── auth.py          # UC1: 使用者註冊/登入
│   ├── activities.py     # UC2, UC3, UC4: 活動相關
│   ├── matches.py        # UC5: 媒合
│   ├── expenses.py       # UC6: 費用
│   └── reviews.py        # UC7: 評價
├── models/
│   ├── user.py           # 使用者模型
│   ├── activity.py       # 活動模型
│   ├── activity_participant.py  # 參與者模型
│   ├── match.py          # 媒合模型
│   ├── expense.py        # 費用模型
│   └── activity_review.py # 評價模型
├── utils/
│   └── email.py          # Email 服務
└── socketio_events.py    # Socket.IO 事件處理
```

### 前端檔案結構
```
frontend/src/
├── views/
│   ├── Register.vue      # UC1: 註冊頁面
│   ├── ActivityCreate.vue # UC2: 建立活動
│   └── ActivityDetail.vue # UC3, UC4: 活動詳情
├── api/
│   ├── auth.js          # UC1: 認證 API
│   ├── activities.js    # UC2, UC3, UC4: 活動 API
│   ├── matches.js       # UC5: 媒合 API
│   ├── expenses.js      # UC6: 費用 API
│   └── reviews.js       # UC7: 評價 API
└── services/
    └── socket.js        # UC5: Socket.IO 客戶端
```

## 注意事項

1. 所有圖表都包含錯誤處理流程（使用 `alt/else`）
2. HTTP 請求都包含 Authorization Header（JWT Token）
3. 資料庫操作都標註了對應的 SQL 語句類型
4. Socket.IO 互動標註了 WebSocket 事件名稱

## 更新記錄

- 2025-01-XX: 初始版本，包含所有 7 個 Use Case 的循序圖

