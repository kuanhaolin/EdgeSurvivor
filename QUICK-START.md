# EdgeSurvivor 快速啟動指南 ⚡

## 🎯 5 分鐘快速啟動

### 前置需求
- ✅ Docker Desktop 已安裝並運行
- ✅ 確保端口 3307, 5001, 8080 未被占用

### 一鍵啟動

```powershell
# 1. 進入專案目錄
cd C:\EdgeSurvivor

# 2. 複製環境變數文件（首次使用）
copy .env.example .env

# 3. 啟動所有服務
docker-compose up -d

# 4. 等待約 20 秒讓資料庫完全啟動

# 5. 查看狀態
docker-compose ps
```

### 預期結果

```
NAME                    STATUS         PORTS
edgesurvivor_db         Up (healthy)   0.0.0.0:3307->3306/tcp
edgesurvivor_backend    Up             0.0.0.0:5001->5000/tcp
edgesurvivor_frontend   Up             0.0.0.0:8080->8080/tcp
```

### 訪問應用

🌐 打開瀏覽器：http://localhost:8080

### 首次使用

請先**註冊新帳號**開始使用：

1. 點擊「立即註冊」按鈕
2. 填寫以下資訊：
   - 使用者名稱
   - Email（用於登入）
   - 密碼（至少 6 個字元）
3. 註冊成功後會自動登入

💡 **提示**：資料庫初始為空，請先註冊帳號才能使用所有功能。

## 🛠️ 常用命令

```powershell
# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down

# 重啟服務
docker-compose restart

# 完全重置（刪除所有資料）
docker-compose down -v
docker-compose up -d
```

## ❌ 遇到問題？

### 容器啟動失敗

```powershell
# 重啟 Docker Desktop，然後：
docker-compose down
docker-compose up -d --build
```

### 查看詳細日誌

```powershell
# 查看特定服務日誌
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### 資料庫連接失敗

```powershell
# 驗證資料庫是否健康
docker-compose ps

# 進入資料庫檢查
docker exec -it edgesurvivor_db mysql -u user -ppassword -e "SHOW DATABASES;"
```

## 📚 更多資訊

- 完整設定指南：[DOCKER-SETUP.md](DOCKER-SETUP.md)
- 開發指南：[README.md](README.md)
- API 文檔：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**就是這麼簡單！** 🎉
