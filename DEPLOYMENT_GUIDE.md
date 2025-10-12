# EdgeSurvivor 完整部署指南

## 📋 部署前準備

### 1. 環境需求
- Docker 20.10+
- Docker Compose 2.0+
- Git (可選)

### 2. 系統需求
- 最低: 2GB RAM, 20GB 硬碟空間
- 建議: 4GB RAM, 50GB 硬碟空間

---

## 🔧 步驟一：設定環境變數

### 1.1 複製環境變數範本
```bash
cd EdgeSurvivor
cp .env.example .env
```

### 1.2 編輯 `.env` 檔案

**重要設定項目：**

```bash
# === 必須修改的設定 ===

# 安全密鑰（使用隨機字串）
SECRET_KEY=請改成隨機字串-至少32字元
JWT_SECRET_KEY=請改成隨機字串-至少32字元

# 資料庫設定（需與 docker-compose.yml 一致）
DB_HOST=db                          # Docker 環境使用服務名稱
DB_PORT=3306
DB_USER=user                        # 與 docker-compose.yml 的 MYSQL_USER 一致
DB_PASSWORD=password                # 與 docker-compose.yml 的 MYSQL_PASSWORD 一致
DB_NAME=edgesurvivor               # 與 docker-compose.yml 的 MYSQL_DATABASE 一致

# 前端 URL（用於 CORS）
FRONTEND_URL=http://localhost:8080

# === 可選設定 ===

# Flask 環境
FLASK_ENV=production               # 生產環境使用 production
FLASK_DEBUG=False                  # 生產環境設為 False

# 檔案上傳
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216        # 16MB

# Redis（如需要 Socket.IO 擴展）
REDIS_URL=redis://redis:6379/0
```

### 1.3 產生安全密鑰

**方法 1: Python**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**方法 2: PowerShell**
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

將產生的字串填入 `SECRET_KEY` 和 `JWT_SECRET_KEY`

---

## 🗄️ 步驟二：設定資料庫

### 2.1 檢查 `docker-compose.yml` 資料庫設定

確認以下設定與 `.env` 一致：

```yaml
db:
  image: mariadb:10.11
  environment:
    MYSQL_ROOT_PASSWORD: root        # root 密碼
    MYSQL_DATABASE: edgesurvivor     # 資料庫名稱
    MYSQL_USER: user                 # 使用者名稱
    MYSQL_PASSWORD: password         # 使用者密碼
  ports:
    - "3306:3306"
```

### 2.2 修改資料庫密碼（建議）

**編輯 `docker-compose.yml`：**
```yaml
db:
  environment:
    MYSQL_ROOT_PASSWORD: 你的強密碼123
    MYSQL_DATABASE: edgesurvivor
    MYSQL_USER: edgesurvivor_user
    MYSQL_PASSWORD: 你的使用者密碼456
```

**同步更新 `.env`：**
```bash
DB_USER=edgesurvivor_user
DB_PASSWORD=你的使用者密碼456
DB_NAME=edgesurvivor
```

---

## 🚀 步驟三：啟動服務

### 3.1 建立並啟動所有容器
```bash
docker-compose up -d --build
```

### 3.2 查看容器狀態
```bash
docker-compose ps
```

應該看到三個容器都是 `Up` 狀態：
- `edgesurvivor_frontend`
- `edgesurvivor_backend`
- `edgesurvivor_db`

### 3.3 查看日誌（如有問題）
```bash
# 查看所有服務日誌
docker-compose logs

# 查看特定服務日誌
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

---

## 🗃️ 步驟四：初始化資料庫

### 4.1 進入後端容器
```bash
docker exec -it edgesurvivor_backend bash
```

### 4.2 執行資料庫初始化
```bash
python init_db.py
```

應該看到類似輸出：
```
🔧 開始初始化資料庫...
✅ 資料庫表已創建！
✅ 資料庫初始化成功！
```

### 4.3 退出容器
```bash
exit
```

---

## ✅ 步驟五：驗證部署

### 5.1 訪問應用

- **前端**: http://localhost:8080
- **後端 API**: http://localhost:5001
- **資料庫**: localhost:3306

### 5.2 測試註冊與登入

1. 訪問 http://localhost:8080
2. 點擊「註冊」
3. 填寫資料並註冊
4. 使用帳號登入
5. 查看控制台是否正常顯示

### 5.3 檢查 Socket.IO 連線

打開瀏覽器開發者工具 (F12) → Console
應該看到：
```
Socket.IO 已連線
```

---

## 🔒 生產環境額外設定

### 1. 反向代理（Nginx）

**安裝 Nginx**
```bash
sudo apt-get install nginx
```

**配置範例** (`/etc/nginx/sites-available/edgesurvivor`)：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 後端 API
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Socket.IO
    location /socket.io {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 上傳檔案
    location /uploads {
        proxy_pass http://localhost:5001;
        client_max_body_size 20M;
    }
}
```

### 2. HTTPS（Let's Encrypt）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 防火牆設定

```bash
# 允許 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 禁止直接訪問應用端口
sudo ufw deny 8080/tcp
sudo ufw deny 5001/tcp
sudo ufw deny 3306/tcp
```

### 4. 資料庫備份

**自動備份腳本**：
```bash
#!/bin/bash
# backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker exec edgesurvivor_db mysqldump -u user -ppassword edgesurvivor > backup_$DATE.sql
```

**設定 Crontab（每天凌晨2點備份）**：
```bash
0 2 * * * /path/to/backup_db.sh
```

---

## 📦 打包方式

### 方式 1: Git 倉庫（推薦）

```bash
# 提交所有更改
git add .
git commit -m "Ready for production"
git push origin main

# 在生產環境
git clone https://github.com/BoBoJhong/EdgeSurvivor.git
cd EdgeSurvivor
cp .env.example .env
# 編輯 .env
docker-compose up -d
```

### 方式 2: ZIP 壓縮包

**排除以下檔案/資料夾**：
```
node_modules/
__pycache__/
.git/
.env
uploads/
*.log
.DS_Store
.vscode/
.bmad-core/
web-bundles/
```

**打包命令**（Linux/Mac）：
```bash
tar -czf edgesurvivor.tar.gz \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='uploads' \
  EdgeSurvivor/
```

**Windows（PowerShell）**：
```powershell
Compress-Archive -Path EdgeSurvivor -DestinationPath edgesurvivor.zip `
  -Force -CompressionLevel Optimal
```

### 方式 3: Docker 映像導出

```bash
# 建立映像
docker-compose build

# 導出映像
docker save edgesurvivor_frontend:latest -o frontend.tar
docker save edgesurvivor_backend:latest -o backend.tar

# 在目標機器載入
docker load -i frontend.tar
docker load -i backend.tar
docker-compose up -d
```

---

## 🛠️ 常見問題

### Q1: 容器啟動失敗
```bash
# 查看日誌
docker-compose logs backend

# 常見原因：
# - 端口被佔用 (修改 docker-compose.yml 端口)
# - 資料庫連線失敗 (檢查 .env 設定)
# - 權限不足 (使用 sudo)
```

### Q2: 資料庫連線失敗
```bash
# 檢查資料庫容器是否運行
docker-compose ps db

# 測試資料庫連線
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 確認 .env 的 DB_HOST=db (不是 localhost)
```

### Q3: 前端無法連接後端
```bash
# 檢查 CORS 設定
# .env 中的 FRONTEND_URL 應該是前端實際 URL
FRONTEND_URL=http://localhost:8080

# 檢查前端 API 設定
# frontend/src/utils/axios.js 應該指向正確的後端 URL
```

### Q4: Socket.IO 連線失敗
```bash
# 確認後端容器正常運行
docker-compose logs backend | grep socket

# 檢查瀏覽器控制台是否有 CORS 錯誤
# 確認 socketService.js 的連線 URL 正確
```

### Q5: 上傳檔案失敗
```bash
# 確認 uploads 目錄權限
docker exec -it edgesurvivor_backend ls -la uploads

# 如需要，修改權限
docker exec -it edgesurvivor_backend chmod 777 uploads
```

---

## 🔄 更新部署

```bash
# 1. 拉取最新代碼
git pull origin main

# 2. 重新建立並啟動
docker-compose up -d --build

# 3. 如有資料庫變更，執行遷移
docker exec -it edgesurvivor_backend python migrate.py
```

---

## 🛑 停止服務

```bash
# 停止所有容器
docker-compose down

# 停止並刪除資料庫卷（⚠️ 會刪除所有資料）
docker-compose down -v
```

---

## 📊 監控與維護

### 查看資源使用
```bash
docker stats
```

### 清理未使用的映像
```bash
docker system prune -a
```

### 查看容器日誌
```bash
# 即時查看
docker-compose logs -f

# 最後 100 行
docker-compose logs --tail=100
```

---

**部署完成！🎉**

如有問題，請查看：
- 後端日誌: `docker-compose logs backend`
- 前端日誌: `docker-compose logs frontend`
- 資料庫日誌: `docker-compose logs db`
