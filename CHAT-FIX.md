# 即時聊天功能修復說明

## 問題描述
即時聊天功能無法執行，Socket.IO 無法連接。

## 根本原因
前端 Socket.IO 客戶端配置錯誤：
- **問題配置**：`socket.js` 中 Socket.IO URL 設定為 `http://localhost:5000`
- **Docker 環境**：容器內的 `localhost` 指向容器自己，無法連接到後端容器
- **正確做法**：使用 `window.location.origin`（當前頁面的 origin），讓 Vite 的 proxy 轉發請求到後端

## 修復內容

### 1. 修正 `frontend/src/services/socket.js`

**修改前：**
```javascript
const SOCKET_URL = import.meta.env.DEV 
  ? 'http://localhost:5000'  // ❌ Docker 環境中無效
  : window.location.origin

this.socket = io(SOCKET_URL, {
  auth: { token: token },
  transports: ['websocket', 'polling'],
  // ...
})
```

**修改後：**
```javascript
const SOCKET_URL = import.meta.env.DEV 
  ? window.location.origin  // ✅ 使用當前 origin，透過 proxy 轉發
  : window.location.origin

this.socket = io(SOCKET_URL, {
  auth: { token: token },
  path: '/socket.io',  // ✅ 明確指定路徑
  transports: ['websocket', 'polling'],
  // ...
})
```

### 2. 確認 `frontend/vite.config.js` 已配置 Socket.IO proxy

```javascript
server: {
  proxy: {
    '/socket.io': {
      target: process.env.VITE_API_TARGET || 'http://backend:5000',
      changeOrigin: true,
      ws: true  // ✅ 啟用 WebSocket 支援
    }
  }
}
```

## 網絡流程

```
瀏覽器 (http://localhost:8080)
    ↓
前端容器 (port 8080)
    ↓ Socket.IO 連線到 window.location.origin
Vite Proxy (/socket.io)
    ↓ 轉發到 http://backend:5000
後端容器 (port 5000)
    ↓
Flask-SocketIO
```

## 測試步驟

### 1. 準備測試環境

```powershell
# 確認所有容器運行中
docker-compose ps

# 應該看到：
# edgesurvivor_db        Up (healthy)
# edgesurvivor_backend   Up
# edgesurvivor_frontend  Up
```

### 2. 測試使用者登入

```powershell
# 使用測試帳號登入
# 用戶名: alice / 密碼: password123
# 用戶名: bob / 密碼: password123
```

訪問：http://localhost:8080

### 3. 檢查 Socket.IO 連線

打開瀏覽器開發者工具（F12）→ Console，應該看到：

```
正在連線到 Socket.IO... http://localhost:8080
✅ Socket.IO 連線成功 <socket_id>
```

### 4. 測試即時聊天

1. **建立媒合**：
   - 兩個不同用戶（如 alice 和 bob）需要有媒合關係
   - 可以透過「活動媒合」功能建立

2. **進入聊天室**：
   - 點擊「聊天」頁面
   - 選擇一個媒合對象
   - Console 應該顯示：`加入聊天室: chat_<match_id>`

3. **發送訊息**：
   - 輸入訊息並發送
   - Console 應該顯示：`訊息發送成功`
   - 對方應該即時收到訊息（如果開啟兩個瀏覽器窗口測試）

4. **檢查即時功能**：
   - ✅ 對方在輸入時顯示「正在輸入...」
   - ✅ 訊息即時出現（無需刷新頁面）
   - ✅ 訊息已讀狀態更新

### 5. 檢查後端日誌

```powershell
# 查看 Socket.IO 連線日誌
docker-compose logs backend | Select-String -Pattern "用戶|連線|訊息|chat"
```

應該看到類似：
```
用戶 1 已連線 (SID: xxx)
用戶 1 加入聊天室 chat_1
訊息已發送到聊天室 chat_1
```

## 故障排查

### 問題 1：Socket.IO 連線失敗

**症狀**：Console 顯示 `❌ Socket.IO 連線錯誤`

**檢查**：
```powershell
# 1. 確認後端容器運行
docker-compose ps backend

# 2. 檢查後端日誌
docker-compose logs backend

# 3. 測試後端健康狀態
Invoke-RestMethod -Uri "http://localhost:5001/api/health"
```

**解決**：
```powershell
# 重啟後端
docker-compose restart backend
```

### 問題 2：無法加入聊天室

**症狀**：Console 顯示 `加入聊天室失敗`

**檢查**：
```powershell
# 檢查資料庫中的媒合資料
docker exec -it edgesurvivor_db mysql -u user -ppassword -e "USE edgesurvivor; SELECT * FROM matches;"
```

**確認**：
- 媒合記錄存在
- `status` 為 'matched'
- 當前用戶是 `user_a` 或 `user_b` 之一

### 問題 3：訊息無法發送

**症狀**：點擊發送後無反應

**檢查**：
```powershell
# 查看前端日誌
docker-compose logs frontend

# 查看後端日誌
docker-compose logs backend
```

**常見原因**：
1. Socket.IO 未連線 → 重新登入
2. JWT Token 過期 → 重新登入
3. 資料庫連線問題 → 檢查 db 容器狀態

### 問題 4：前端 API 代理錯誤

**症狀**：Console 或 Network 顯示 `ECONNREFUSED ::1:5000`

**解決**：
```powershell
# 確認 vite.config.js 的 proxy 配置正確
cat frontend/vite.config.js | Select-String -Pattern "proxy"

# 重新構建前端容器
docker-compose up -d --build frontend
```

## 重要配置文件

### frontend/src/services/socket.js
Socket.IO 客戶端設定，處理所有即時通訊功能。

### backend/socketio_events.py
Socket.IO 伺服器端事件處理器，包含：
- 連線/斷線處理
- 聊天室管理
- 訊息發送/接收
- 活動討論功能

### frontend/vite.config.js
開發服務器配置，包含：
- API 代理設定 (`/api`)
- Socket.IO 代理設定 (`/socket.io`)
- WebSocket 支援

## 功能清單

### 聊天功能
- ✅ 即時訊息發送/接收
- ✅ 輸入狀態顯示
- ✅ 訊息已讀狀態
- ✅ 用戶上線/離線通知
- ✅ 支援文字、圖片、語音訊息

### 活動討論功能
- ✅ 活動討論室
- ✅ 即時討論訊息
- ✅ 多人參與

## 技術架構

```
前端：Vue 3 + Socket.IO Client
      ↓
Vite Proxy：/socket.io → backend:5000
      ↓
後端：Flask + Flask-SocketIO
      ↓
WebSocket / Polling 雙向通訊
```

## 相關指令

```powershell
# 查看所有容器狀態
docker-compose ps

# 重啟所有服務
docker-compose restart

# 查看前端日誌（即時）
docker-compose logs -f frontend

# 查看後端日誌（即時）
docker-compose logs -f backend

# 重新構建並啟動
docker-compose up -d --build

# 進入資料庫檢查
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor
```

## 注意事項

1. **認證 Token**：Socket.IO 連線需要有效的 JWT token，請確保已登入
2. **CORS 設定**：後端已設定允許來自前端的請求
3. **雙向通訊**：Socket.IO 會優先使用 WebSocket，失敗時降級為 Polling
4. **容器網絡**：在 Docker 環境中，所有服務間通訊使用服務名稱（backend, db）
5. **開發環境**：建議使用兩個瀏覽器窗口（或無痕模式）測試即時功能

## 更新日誌

- **2025-10-15**：修正 Socket.IO 連線 URL 配置，從 `localhost:5000` 改為 `window.location.origin`
- 添加 `path: '/socket.io'` 明確指定 Socket.IO 路徑
- 確認 vite.config.js 已配置 Socket.IO proxy with WebSocket 支援
