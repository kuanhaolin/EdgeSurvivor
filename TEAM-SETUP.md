# EdgeSurvivor 團隊協作快速指南 👥

## 📋 新成員加入步驟

### 1️⃣ 環境準備（5 分鐘）

#### 必要軟體
- **Docker Desktop**：https://www.docker.com/products/docker-desktop/
  - Windows: 下載並安裝，重啟電腦
  - Mac: 下載 .dmg 安裝檔
  - Linux: `sudo apt-get install docker docker-compose`
  
- **Git**：https://git-scm.com/downloads

- **程式碼編輯器**（擇一）
  - VS Code（推薦）：https://code.visualstudio.com/
  - WebStorm
  - Sublime Text

---

### 2️⃣ 下載專案（1 分鐘）

```powershell
# 克隆專案
git clone https://github.com/BoBoJhong/EdgeSurvivor.git

# 進入專案目錄
cd EdgeSurvivor
```

---

### 3️⃣ 啟動服務（2 分鐘）

```powershell
# 方法 1：使用一鍵啟動腳本（推薦）
.\start-docker.bat

# 方法 2：使用 Docker Compose 命令
docker-compose up -d --build
```

等待約 **20 秒**，讓所有服務完全啟動。

---

### 4️⃣ 驗證安裝（1 分鐘）

#### 檢查容器狀態
```powershell
docker-compose ps
```

**預期結果**：
```
NAME                    STATUS         PORTS
edgesurvivor_db         Up (healthy)   0.0.0.0:3307->3306/tcp
edgesurvivor_backend    Up             0.0.0.0:5001->5000/tcp
edgesurvivor_frontend   Up             0.0.0.0:8080->8080/tcp
```

#### 訪問應用
- 🌐 **前端**：http://localhost:8080
- 🔧 **後端 API**：http://localhost:5001
- 🗄️ **資料庫**：localhost:3307

#### 測試帳號登入
| 用戶名 | 密碼 | 說明 |
|--------|------|------|
| alice | password123 | 測試用戶 A |
| bob | password123 | 測試用戶 B |
| charlie | password123 | 測試用戶 C |

---

## 🔧 開發工作流程

### 日常開發

#### 啟動開發環境
```powershell
# 啟動所有服務
docker-compose up -d

# 查看即時日誌（可選）
docker-compose logs -f
```

#### 停止開發環境
```powershell
# 停止服務（保留資料）
docker-compose stop

# 停止並移除容器（保留資料庫資料）
docker-compose down
```

#### 重啟服務
```powershell
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart backend
docker-compose restart frontend
```

---

### 程式碼變更

#### 前端變更（自動熱重載）
```powershell
# 前端使用 Vite 開發模式，檔案變更會自動重載
# 無需重啟容器，直接編輯 frontend/src/ 下的檔案
```

#### 後端變更（需重啟）
```powershell
# 修改 backend/ 下的檔案後，重啟後端
docker-compose restart backend

# 或重新構建（如果改了依賴）
docker-compose up -d --build backend
```

#### 資料庫變更
```powershell
# 修改 db/init.sql 後，需要重建資料庫
docker-compose down -v
docker-compose up -d
```

---

### 分支管理

#### 創建新功能分支
```bash
# 切換到最新的 main 分支
git checkout main
git pull origin main

# 創建新功能分支
git checkout -b feature/your-feature-name

# 例如：
git checkout -b feature/add-payment
git checkout -b fix/chat-bug
git checkout -b refactor/api-structure
```

#### 提交變更
```bash
# 查看變更
git status

# 添加變更
git add .

# 提交（使用有意義的訊息）
git commit -m "feat: 添加支付功能"
git commit -m "fix: 修復聊天室連線問題"
git commit -m "refactor: 重構 API 結構"

# 推送到遠端
git push origin feature/your-feature-name
```

#### 合併流程
1. 在 GitHub 上創建 **Pull Request (PR)**
2. 等待 **Code Review**
3. 通過審核後，由專案負責人合併到 `main` 分支

---

## 🧪 測試與驗證

### 後端 API 測試

#### 使用 PowerShell 測試
```powershell
# 健康檢查
Invoke-RestMethod -Uri "http://localhost:5001/api/health"

# 登入測試
$body = @{
    username = "alice"
    password = "password123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/auth/login" -Method POST -Body $body -ContentType "application/json"
```

#### 使用 Postman 或 Insomnia
1. 匯入 API 文檔（如有提供）
2. 測試各個 endpoint
3. 分享測試結果給團隊

---

### 前端功能測試

#### 核心功能檢查清單
- [ ] 註冊新用戶
- [ ] 登入/登出
- [ ] 建立活動
- [ ] 參加活動
- [ ] 媒合系統
- [ ] 即時聊天
- [ ] 活動討論
- [ ] 費用分攤

#### 使用瀏覽器開發工具
```
F12 → Console: 檢查錯誤訊息
F12 → Network: 檢查 API 請求
F12 → Application → Local Storage: 檢查 Token
```

---

## 🗄️ 資料庫操作

### 查看資料

```powershell
# 進入資料庫 CLI
docker exec -it edgesurvivor_db mysql -u user -ppassword edgesurvivor

# 查看所有表
SHOW TABLES;

# 查看用戶資料
SELECT * FROM users;

# 查看活動資料
SELECT * FROM activities;

# 離開
exit
```

### 重置資料庫

```powershell
# 完全重置（刪除所有資料）
docker-compose down -v
docker-compose up -d

# 等待資料庫初始化完成（約 10 秒）
```

---

## 📂 專案結構

```
EdgeSurvivor/
├── backend/                 # 後端 Flask 應用
│   ├── app.py              # 應用入口
│   ├── config.py           # 配置檔
│   ├── models/             # 資料庫模型
│   ├── blueprints/         # API 路由
│   ├── socketio_events.py  # Socket.IO 事件
│   └── requirements.txt    # Python 依賴
│
├── frontend/               # 前端 Vue 應用
│   ├── src/
│   │   ├── components/    # Vue 組件
│   │   ├── views/         # 頁面視圖
│   │   ├── stores/        # Pinia 狀態管理
│   │   ├── services/      # API 服務
│   │   └── utils/         # 工具函數
│   ├── vite.config.js     # Vite 配置
│   └── package.json       # npm 依賴
│
├── db/                     # 資料庫相關
│   └── init.sql           # 資料庫初始化 SQL
│
├── docker-compose.yml      # Docker 編排配置
├── .env.docker            # Docker 環境變數
├── start-docker.bat       # 一鍵啟動腳本
├── README.md              # 專案說明
└── TEAM-SETUP.md          # 本文檔
```

---

## 🐛 常見問題排查

### ❌ 問題 1：容器無法啟動

**症狀**：`docker-compose up -d` 失敗

**解決方案**：
```powershell
# 1. 重啟 Docker Desktop
# 2. 清理舊容器
docker-compose down -v
docker system prune -a

# 3. 重新啟動
docker-compose up -d --build
```

---

### ❌ 問題 2：前端無法連接後端

**症狀**：瀏覽器 Console 顯示 `ECONNREFUSED` 或 API 錯誤

**檢查**：
```powershell
# 1. 確認後端運行正常
docker-compose logs backend

# 2. 測試後端 API
Invoke-RestMethod -Uri "http://localhost:5001/api/health"

# 3. 重啟前端
docker-compose restart frontend
```

**參考文檔**：`REGISTER-FIX.md`

---

### ❌ 問題 3：Socket.IO 聊天無法連線

**症狀**：無法發送或接收即時訊息

**檢查**：
```powershell
# 1. 查看瀏覽器 Console
# 應該看到：✅ Socket.IO 連線成功

# 2. 查看後端日誌
docker-compose logs backend | Select-String -Pattern "Socket|用戶|連線"

# 3. 確認已登入（有 Token）
# F12 → Application → Local Storage → token
```

**參考文檔**：`CHAT-FIX.md`

---

### ❌ 問題 4：資料庫連接失敗

**症狀**：後端日誌顯示資料庫錯誤

**檢查**：
```powershell
# 1. 確認資料庫容器健康
docker-compose ps

# 2. 查看資料庫日誌
docker-compose logs db

# 3. 測試連線
docker exec -it edgesurvivor_db mysql -u user -ppassword -e "SELECT 1;"

# 4. 重啟資料庫
docker-compose restart db
```

---

### ❌ 問題 5：端口被占用

**症狀**：`port is already allocated`

**解決方案**：
```powershell
# 1. 查看占用端口的程序（以 3307 為例）
netstat -ano | findstr :3307

# 2. 停止占用程序（替換 PID）
taskkill /PID <PID> /F

# 3. 或修改 docker-compose.yml 中的端口映射
# 例如將 "3307:3306" 改為 "3308:3306"
```

---

## 📚 進階開發

### 安裝新的 Python 套件

```powershell
# 1. 在 backend/requirements.txt 添加套件
# 例如：requests==2.31.0

# 2. 重新構建後端
docker-compose up -d --build backend
```

### 安裝新的 npm 套件

```powershell
# 1. 進入前端容器
docker exec -it edgesurvivor_frontend sh

# 2. 安裝套件
npm install <package-name>

# 3. 離開容器
exit

# 4. 更新 package.json（套件已自動添加）
```

### 查看即時日誌

```powershell
# 查看所有服務
docker-compose logs -f

# 查看特定服務
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# 只看最新 50 行
docker-compose logs --tail=50 backend
```

---

## 🔐 環境變數說明

### `.env.docker`（Docker 環境）

```env
# 資料庫配置
DB_HOST=db              # Docker 服務名稱
DB_PORT=3306            # 容器內部端口
DB_USER=user
DB_PASSWORD=password
DB_NAME=edgesurvivor

# Flask 配置
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# 資料庫 URL（自動組合上述配置）
DATABASE_URL=mysql+pymysql://user:password@db:3306/edgesurvivor
DEV_DATABASE_URL=mysql+pymysql://user:password@db:3306/edgesurvivor
```

**⚠️ 注意**：
- **生產環境**必須修改所有密鑰和密碼
- 不要將 `.env` 文件提交到 Git
- `.env.docker` 已在 `.gitignore` 中排除

---

## 👥 團隊溝通

### Code Review 準則

1. **PR 標題格式**：`[類型] 簡短描述`
   - `[feat]` 新功能
   - `[fix]` 錯誤修復
   - `[refactor]` 重構
   - `[docs]` 文檔更新
   - `[test]` 測試相關

2. **PR 描述應包含**：
   - 變更原因
   - 主要修改內容
   - 測試方法
   - 截圖（如有 UI 變更）

3. **審核重點**：
   - 程式碼可讀性
   - 是否符合專案風格
   - 有無潛在安全問題
   - 效能考量

---

## 📞 需要協助？

### 文檔資源
- **Docker 配置**：`DOCKER-SETUP.md`
- **快速啟動**：`QUICK-START.md`
- **註冊功能修復**：`REGISTER-FIX.md`
- **聊天功能修復**：`CHAT-FIX.md`
- **資料庫修復**：`CHAT-MESSAGE-FIX.md`

### 聯絡方式
- **GitHub Issues**：回報問題或建議功能
- **團隊通訊軟體**：（請填入 Slack/Discord/LINE 群組連結）
- **專案負責人**：（請填入聯絡方式）

---

## ✅ 完成檢查清單

新成員加入後，請確認以下項目：

- [ ] Docker Desktop 已安裝並運行
- [ ] 成功克隆專案到本機
- [ ] 執行 `docker-compose up -d` 成功
- [ ] 三個容器都顯示 `Up` 狀態
- [ ] 可以訪問 http://localhost:8080
- [ ] 成功使用測試帳號登入
- [ ] 可以建立新活動
- [ ] 聊天功能正常（看到「✅ Socket.IO 連線成功」）
- [ ] 已閱讀專案結構說明
- [ ] 已了解 Git 分支管理流程
- [ ] 知道如何查看日誌和排查問題

---

**🎉 恭喜！你已準備好開始開發了！**

有任何問題，隨時查閱文檔或聯絡團隊成員。
