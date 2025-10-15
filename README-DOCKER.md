# EdgeSurvivor Docker 部署指南

## 📦 環境配置說明

本專案支援兩種開發模式：

### 1️⃣ 本機開發模式
使用 `.env` 文件，直接在本機運行 Python 和 Node.js

```bash
# 配置文件：.env
DB_HOST=localhost
DB_USER=edgesurvivor_user
DB_PASSWORD=910929
```

### 2️⃣ Docker 容器模式
使用 `.env.docker` 文件，所有服務運行在 Docker 容器中

```bash
# 配置文件：.env.docker
DB_HOST=db
DB_USER=user
DB_PASSWORD=password
```

---

## 🚀 Docker 快速啟動

### 步驟 1: 啟動所有容器

```powershell
# 構建並啟動所有服務（前端、後端、資料庫）
docker-compose up -d --build

# 查看容器狀態
docker-compose ps
```

您應該看到三個容器都在運行：
- ✅ edgesurvivor_frontend (port 8080)
- ✅ edgesurvivor_backend (port 5001)
- ✅ edgesurvivor_db (port 3306)

### 步驟 2: 初始化資料庫

```powershell
# 等待資料庫完全啟動（約 10 秒）
timeout /t 10

# 初始化資料庫表結構
docker exec -it edgesurvivor_backend python init_db.py
```

### 步驟 3: 訪問應用

- 🌐 前端應用: http://localhost:8080
- 🔌 後端 API: http://localhost:5001
- 🗄️ 資料庫: localhost:3306

---

## 📊 常用 Docker 命令

### 查看日誌

```powershell
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 重啟服務

```powershell
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart backend
```

### 停止服務

```powershell
# 停止所有容器
docker-compose down

# 停止並刪除所有資料（包括資料庫）
docker-compose down -v
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

## 🔧 開發工作流程

### 本機開發 → Docker 部署

```powershell
# 1. 本機開發完成後，提交代碼
git add .
git commit -m "Feature: 新功能"

# 2. 使用 Docker 測試
docker-compose down
docker-compose up -d --build

# 3. 測試通過後推送
git push
```

### 快速切換模式

```powershell
# 切換到 Docker 模式
docker-compose up -d

# 切換回本機模式
docker-compose down
cd backend && python app.py
cd frontend && npm run dev
```

---

## ⚠️ 常見問題排查

### 1. 資料庫連線失敗

```powershell
# 檢查資料庫容器是否運行
docker-compose ps

# 查看資料庫日誌
docker-compose logs db

# 確認後端使用正確的環境變數
docker-compose config
```

### 2. 前端無法連接後端

```powershell
# 檢查後端是否正常運行
docker-compose logs backend

# 確認端口映射
docker-compose ps
```

### 3. 修改代碼後沒有生效

```powershell
# 重新構建容器
docker-compose up -d --build

# 或強制重建
docker-compose build --no-cache
docker-compose up -d
```

### 4. 資料庫資料遺失

- Docker 使用 volume 持久化資料
- 除非執行 `docker-compose down -v`，否則資料不會遺失
- 查看 volume: `docker volume ls`

---

## 📁 檔案結構說明

```
EdgeSurvivor/
├── .env                    # 本機開發配置
├── .env.docker            # Docker 部署配置 ⭐
├── docker-compose.yml     # Docker 服務編排
├── backend/
│   ├── Dockerfile         # 後端容器定義
│   ├── app.py
│   └── init_db.py         # 資料庫初始化腳本
├── frontend/
│   ├── Dockerfile         # 前端容器定義
│   └── package.json
└── db/
    └── init.sql           # 資料庫初始化 SQL
```

---

## 🎯 生產環境建議

在生產環境部署時，請修改 `.env.docker`：

```ini
# 使用強密碼
SECRET_KEY=<隨機生成的長字串>
JWT_SECRET_KEY=<隨機生成的長字串>

# 資料庫密碼
DB_PASSWORD=<強密碼>

# 關閉 Debug
FLASK_DEBUG=False
FLASK_ENV=production
```

並在 `docker-compose.yml` 中移除 volume 映射（避免代碼洩漏）。

---

**享受 Docker 帶來的便利！** 🐳
