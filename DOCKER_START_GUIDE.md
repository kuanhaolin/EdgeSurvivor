# EdgeSurvivor Docker 啟動指南

## 📋 前置檢查

### 1. 確認 Docker 狀態
```powershell
# 檢查 Docker 版本
docker --version

# 檢查 Docker Compose 版本
docker-compose --version

# 檢查 Docker 服務是否運行
docker ps
```

### 2. 確認環境變數檔案
確保專案根目錄有 `.env` 或 `.env.docker` 檔案，包含以下配置：

```ini
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

---

## 🚀 完整啟動流程

### 步驟 1: 停止並清理舊容器（可選）

```powershell
# 如果之前有運行過，先停止並清理
docker-compose down -v

# 注意：-v 會刪除所有資料，包括資料庫資料
# 如果只想停止不刪除資料，使用：
docker-compose down
```

### 步驟 2: 構建並啟動所有服務

```powershell
# 在專案根目錄執行
docker-compose up -d --build
```

這會啟動三個服務：
- ✅ **前端** (edgesurvivor_frontend) - Port 8080
- ✅ **後端** (edgesurvivor_backend) - Port 5001
- ✅ **資料庫** (edgesurvivor_db) - Port 3307

### 步驟 3: 檢查容器狀態

```powershell
# 查看所有容器狀態
docker-compose ps

# 應該看到三個容器都是 "Up" 狀態
```

### 步驟 4: 等待資料庫完全啟動

```powershell
# 等待約 10-15 秒讓資料庫完全初始化
timeout /t 15

# 查看資料庫日誌確認初始化完成
docker-compose logs db | Select-String "ready for connections"
```

### 步驟 5: 初始化資料庫結構

```powershell
# 使用 Python 腳本初始化資料庫（會自動建立表格）
docker exec -it edgesurvivor_backend python init_db.py
```

### 步驟 6: 執行資料庫遷移（新增評分功能）

由於我們新增了評分功能，需要執行遷移腳本來新增欄位：

```powershell
# 執行遷移腳本，新增 rating 和 average_rating 欄位
docker exec -it edgesurvivor_backend python -c "from migrations.add_rating_fields import upgrade; from app import create_app; from models import db; app = create_app('development'); app.app_context().push(); upgrade()"
```

或者更簡單的方式：

```powershell
# 進入後端容器
docker exec -it edgesurvivor_backend bash

# 在容器內執行
python -c "from migrations.add_rating_fields import upgrade; from app import create_app; from models import db; app = create_app('development'); app.app_context().push(); upgrade()"

# 退出容器
exit
```

### 步驟 7: 驗證資料庫結構

```powershell
# 進入資料庫容器
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 在 MySQL 中執行以下命令檢查表格結構：
SHOW TABLES;
DESCRIBE activity_reviews;  # 應該看到 rating 欄位
DESCRIBE users;              # 應該看到 average_rating 欄位
EXIT;
```

---

## 📊 驗證服務運行

### 檢查後端 API

```powershell
# 健康檢查
curl http://localhost:5001/api/health

# 或使用瀏覽器訪問
# http://localhost:5001/api/health
```

### 檢查前端

```powershell
# 在瀏覽器訪問
# http://localhost:8080
```

### 查看服務日誌

```powershell
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## 🔧 常用命令

### 重啟服務

```powershell
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart backend
docker-compose restart frontend
```

### 停止服務

```powershell
# 停止所有容器（保留資料）
docker-compose stop

# 停止並刪除容器（保留資料）
docker-compose down

# 停止並刪除所有資料（包括資料庫）
docker-compose down -v
```

### 重新構建

```powershell
# 重新構建並啟動
docker-compose up -d --build

# 強制重新構建（不使用快取）
docker-compose build --no-cache
docker-compose up -d
```

### 進入容器

```powershell
# 進入後端容器
docker exec -it edgesurvivor_backend bash

# 進入資料庫容器
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 進入前端容器
docker exec -it edgesurvivor_frontend sh
```

---

## ⚠️ 常見問題

### 1. 後端無法連接資料庫

**解決方法：**
```powershell
# 檢查資料庫容器是否健康
docker-compose ps

# 查看資料庫日誌
docker-compose logs db

# 確認環境變數
docker exec edgesurvivor_backend env | grep DB_
```

### 2. 資料庫遷移失敗

**解決方法：**
```powershell
# 檢查資料庫連線
docker exec -it edgesurvivor_backend python init_db.py test

# 手動執行 SQL（如果需要）
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor
# 然後執行：
# ALTER TABLE activity_reviews ADD COLUMN rating INTEGER NOT NULL DEFAULT 5;
# ALTER TABLE users ADD COLUMN average_rating FLOAT NOT NULL DEFAULT 0.0;
```

### 3. 前端無法連接後端

**解決方法：**
```powershell
# 檢查後端是否運行
docker-compose logs backend

# 檢查端口是否被占用
netstat -an | findstr "5001"
netstat -an | findstr "8080"
```

### 4. 容器一直重啟

**解決方法：**
```powershell
# 查看容器日誌找出錯誤
docker-compose logs backend

# 檢查環境變數配置
docker-compose config
```

---

## 📝 快速啟動腳本

創建一個 `start-docker.ps1` 腳本：

```powershell
# start-docker.ps1
Write-Host "🚀 啟動 EdgeSurvivor Docker 環境..." -ForegroundColor Green

# 停止舊容器
Write-Host "停止舊容器..." -ForegroundColor Yellow
docker-compose down

# 構建並啟動
Write-Host "構建並啟動服務..." -ForegroundColor Yellow
docker-compose up -d --build

# 等待資料庫啟動
Write-Host "等待資料庫啟動..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# 初始化資料庫
Write-Host "初始化資料庫..." -ForegroundColor Yellow
docker exec -it edgesurvivor_backend python init_db.py

# 執行遷移
Write-Host "執行資料庫遷移..." -ForegroundColor Yellow
docker exec edgesurvivor_backend python -c "from migrations.add_rating_fields import upgrade; from app import create_app; from models import db; app = create_app('development'); app.app_context().push(); upgrade()"

Write-Host "✅ 啟動完成！" -ForegroundColor Green
Write-Host "前端: http://localhost:8080" -ForegroundColor Cyan
Write-Host "後端: http://localhost:5001" -ForegroundColor Cyan
```

執行方式：
```powershell
.\start-docker.ps1
```

---

## 🎯 訪問地址

- 🌐 **前端應用**: http://localhost:8080
- 🔌 **後端 API**: http://localhost:5001
- 🗄️ **資料庫**: localhost:3307 (用戶: user, 密碼: password)

---

**祝您使用愉快！** 🐳

