# EdgeSurvivor 註冊問題已修復 ✅

## 🔍 問題分析

### 原因
在 Docker 環境中，前端容器嘗試通過 `localhost:5000` 連接後端，但：
- `localhost` 在容器內部指向容器自己
- 應該使用 Docker 服務名稱 `backend` 來連接

### 錯誤日誌
```
Error: connect ECONNREFUSED ::1:5000
```

## ✅ 已修復

### 修改文件
**`frontend/vite.config.js`**

**修改前**：
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',  // ❌ 錯誤
    changeOrigin: true,
    secure: false
  }
}
```

**修改後**：
```javascript
proxy: {
  '/api': {
    target: process.env.VITE_API_TARGET || 'http://backend:5000',  // ✅ 正確
    changeOrigin: true,
    secure: false
  }
}
```

### 優點
- 使用環境變數 `VITE_API_TARGET`，可彈性切換
- Docker 環境自動使用 `backend:5000`
- 本機開發可設定 `VITE_API_TARGET=http://localhost:5000`

## 🧪 測試註冊

### 方式 1: 網頁測試
1. 打開瀏覽器：http://localhost:8080
2. 點擊「註冊」
3. 填寫資料：
   - 用戶名：測試用戶
   - Email：test@example.com
   - 密碼：password123
   - 確認密碼：password123
4. 點擊「註冊」按鈕

### 方式 2: API 測試
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/auth/register" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name":"測試","email":"test2@example.com","password":"password123"}'
```

## 📊 驗證結果

### 檢查資料庫中的用戶
```powershell
docker exec -it edgesurvivor_db mysql -u user -ppassword -e "
USE edgesurvivor;
SELECT user_id, name, email, join_date FROM users ORDER BY user_id DESC LIMIT 5;
"
```

### 預期輸出
```
+------+---------+---------------------+---------------------+
| user_id | name  | email               | join_date           |
+------+---------+---------------------+---------------------+
| 4    | 測試    | test2@example.com   | 2025-10-15 07:10:00 |
| 3    | 阿傑    | jay@example.com     | 2025-10-15 00:00:00 |
| 2    | 小花    | hua@example.com     | 2025-10-15 00:00:00 |
| 1    | 小明    | ming@example.com    | 2025-10-15 00:00:00 |
+------+---------+---------------------+---------------------+
```

## 🚀 完整服務狀態

```powershell
docker-compose ps
```

所有服務應該都是 `Up` 狀態：
- ✅ edgesurvivor_db (port 3307)
- ✅ edgesurvivor_backend (port 5001)
- ✅ edgesurvivor_frontend (port 8080)

## 💡 本機開發 vs Docker

### Docker 環境（當前）
```yaml
# 前端連接後端
target: http://backend:5000

# 訪問方式
前端: http://localhost:8080
後端: http://localhost:5001
資料庫: localhost:3307
```

### 本機開發
如果要在本機運行（不用 Docker）：

```bash
# 設定環境變數
$env:VITE_API_TARGET="http://localhost:5000"

# 啟動後端
cd backend
python app.py

# 啟動前端
cd frontend
npm run dev
```

## 🎉 現在可以正常註冊了！

訪問 http://localhost:8080 並嘗試註冊新帳號。
