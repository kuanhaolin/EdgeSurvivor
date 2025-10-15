# EdgeSurvivor Docker 完整設定指南

## 🔧 當前遇到的問題

您的 Docker Desktop 出現了 I/O 錯誤。這通常是因為：
1. Docker Desktop 緩存損壞
2. WSL2 磁盤空間不足
3. Docker 需要重啟

## 🚀 解決方案

### 步驟 1: 重啟 Docker Desktop

1. 關閉 Docker Desktop
2. 打開工作管理員，確保所有 Docker 進程都已關閉
3. 重新啟動 Docker Desktop
4. 等待 Docker 完全啟動（系統托盤圖標變綠）

### 步驟 2: 驗證配置文件

確認 `.env.docker` 內容正確：

```bash
# Flask 應用配置
FLASK_ENV=development
FLASK_DEBUG=True

# 安全密鑰
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# MariaDB 資料庫配置 (Docker 環境)
DB_HOST=db
DB_PORT=3306
DB_USER=user
DB_PASSWORD=password
DB_NAME=edgesurvivor

# 資料庫連線字串
DATABASE_URL=mysql+pymysql://user:password@db:3306/edgesurvivor
DEV_DATABASE_URL=mysql+pymysql://user:password@db:3306/edgesurvivor

# CORS 允許的來源
FRONTEND_URL=http://localhost:8080

# 其他配置
TIMEZONE=Asia/Taipei
```

### 步驟 3: 啟動服務

```powershell
# 1. 確保在專案根目錄
cd C:\EdgeSurvivor

# 2. 停止並清理所有容器
docker-compose down -v

# 3. 重新構建並啟動
docker-compose up -d --build

# 4. 查看容器狀態
docker-compose ps

# 5. 查看日誌
docker-compose logs -f
```

### 步驟 4: 驗證資料庫

```powershell
# 查看資料庫日誌
docker-compose logs db

# 進入資料庫容器
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 在 MySQL 中執行：
SHOW TABLES;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM activities;
```

您應該看到：
- ✅ 8 個表格（users, activities, matches, chat_messages, expenses, activity_participants, activity_discussions）
- ✅ 3 個測試使用者
- ✅ 3 個測試活動

## 📊 完整的資料庫結構

### 已自動創建的表格：

1. **users** - 使用者表
   - 包含測試使用者：小明、小花、阿傑
   - 密碼都是：`password123`

2. **activities** - 活動表
   - 陽明山賞花一日遊
   - 九份老街美食之旅
   - 大稻埕河濱腳踏車

3. **matches** - 媒合表
4. **chat_messages** - 聊天訊息表
5. **activity_participants** - 活動參與者表
6. **activity_discussions** - 活動討論串表
7. **expenses** - 費用表

## 🎯 訪問應用

一旦所有容器啟動成功：

- 🌐 **前端**: http://localhost:8080
- 🔌 **後端 API**: http://localhost:5001
- 🗄️ **資料庫**: localhost:3306

### 測試後端 API

```powershell
# 健康檢查
curl http://localhost:5001/api/health

# 註冊新使用者
curl -X POST http://localhost:5001/api/auth/register -H "Content-Type: application/json" -d "{\"name\":\"測試\",\"email\":\"test@example.com\",\"password\":\"password123\"}"

# 登入（使用測試帳號）
curl -X POST http://localhost:5001/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"ming@example.com\",\"password\":\"password123\"}"
```

## ⚠️ 常見問題

### 1. 後端一直重啟

**原因**: 資料庫連接失敗

**解決**:
```powershell
# 檢查 .env.docker 配置是否正確
cat .env.docker

# 確認資料庫容器健康
docker-compose ps
docker-compose logs db
```

### 2. 前端無法連接後端

**原因**: CORS 配置或後端未啟動

**解決**:
```powershell
# 檢查後端狀態
docker-compose logs backend

# 確認端口映射
netstat -an | findstr "5001"
```

### 3. 資料庫初始化失敗

**原因**: init.sql 語法錯誤或權限問題

**解決**:
```powershell
# 重新創建資料庫
docker-compose down -v
docker-compose up -d

# 手動初始化
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor < db/init.sql
```

### 4. Docker I/O 錯誤

**解決**:
1. 重啟 Docker Desktop
2. 清理 WSL2 磁盤：
   ```powershell
   wsl --shutdown
   # 重啟 Docker Desktop
   ```
3. 增加 Docker Desktop 的磁盤空間限制

## 📝 開發工作流程

### 本機開發

```powershell
# 使用 .env 配置（連接本機 MariaDB）
cd backend
python app.py

cd ../frontend
npm run dev
```

### Docker 開發

```powershell
# 使用 .env.docker 配置
docker-compose up -d

# 查看即時日誌
docker-compose logs -f backend

# 重啟特定服務
docker-compose restart backend
```

### 修改代碼後

```powershell
# 前端會自動熱重載（Hot Reload）
# 後端需要重啟
docker-compose restart backend

# 或者完全重建
docker-compose up -d --build
```

## 🔄 資料庫管理

### 備份資料

```powershell
# 備份整個資料庫
docker exec edgesurvivor_db mysqldump -u user -ppassword edgesurvivor > backup.sql

# 僅備份結構
docker exec edgesurvivor_db mysqldump -u user -ppassword --no-data edgesurvivor > schema.sql
```

### 還原資料

```powershell
# 從備份還原
docker exec -i edgesurvivor_db mysql -u user -ppassword edgesurvivor < backup.sql
```

### 重置資料庫

```powershell
# 刪除所有資料（包括 volume）
docker-compose down -v

# 重新啟動（會自動執行 init.sql）
docker-compose up -d
```

## 🎓 學習資源

- [Docker Compose 文檔](https://docs.docker.com/compose/)
- [MariaDB Docker 鏡像](https://hub.docker.com/_/mariadb)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

---

**祝您開發順利！** 🚀

有問題請參考故障排查部分或查看日誌：`docker-compose logs -f`
