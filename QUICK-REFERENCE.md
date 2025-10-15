# 🚀 EdgeSurvivor 快速上手（5 分鐘）

## 新成員快速步驟

### ✅ 步驟 1：準備環境
```powershell
# 安裝 Docker Desktop（如未安裝）
# https://www.docker.com/products/docker-desktop/
```

### ✅ 步驟 2：下載專案
```powershell
git clone https://github.com/BoBoJhong/EdgeSurvivor.git
cd EdgeSurvivor
```

### ✅ 步驟 3：啟動服務
```powershell
# 方法 1：一鍵啟動（推薦）
.\start-docker.bat

# 方法 2：手動啟動
docker-compose up -d --build
```

### ✅ 步驟 4：驗證
```powershell
# 檢查狀態
docker-compose ps

# 訪問應用
瀏覽器開啟：http://localhost:8080

# 測試帳號
用戶名：test@example.com   密碼：password123
用戶名：123@example.com     密碼：123456
```

---

## 📋 常用指令速查表

| 動作 | 指令 |
|------|------|
| 啟動服務 | `docker-compose up -d` |
| 停止服務 | `docker-compose stop` |
| 重啟服務 | `docker-compose restart` |
| 查看狀態 | `docker-compose ps` |
| 查看日誌 | `docker-compose logs -f` |
| 重新構建 | `docker-compose up -d --build` |
| 完全重置 | `docker-compose down -v` |

---

## 🔧 開發工作流

### 修改前端（自動熱重載）
```powershell
# 直接編輯 frontend/src/ 下的檔案
# 儲存後自動重載，無需重啟
```

### 修改後端（需重啟）
```powershell
# 編輯 backend/ 下的檔案後
docker-compose restart backend
```

### Git 分支管理
```bash
# 創建新功能分支
git checkout -b feature/功能名稱

# 提交變更
git add .
git commit -m "feat: 描述變更內容"
git push origin feature/功能名稱

# 在 GitHub 創建 Pull Request
```

---

## 🐛 快速排錯

### 問題：容器無法啟動
```powershell
docker-compose down -v
docker-compose up -d --build
```

### 問題：前端無法連接後端
```powershell
docker-compose restart frontend
docker-compose logs backend
```

### 問題：聊天功能不工作
```powershell
# 檢查瀏覽器 Console (F12)
# 應該看到：✅ Socket.IO 連線成功
```

### 問題：端口被占用
```powershell
# 查看占用進程
netstat -ano | findstr :8080

# 停止進程（替換 PID）
taskkill /PID <PID> /F
```

---

## 📡 服務端點

| 服務 | 本機端口 | 容器端口 | URL |
|------|---------|---------|-----|
| 前端 | 8080 | 8080 | http://localhost:8080 |
| 後端 API | 5001 | 5000 | http://localhost:5001 |
| 資料庫 | 3307 | 3306 | localhost:3307 |

---

## 📂 核心目錄結構

```
EdgeSurvivor/
├── backend/              # Flask 後端
│   ├── app.py           # 應用入口
│   ├── models/          # 資料庫模型
│   └── blueprints/      # API 路由
├── frontend/            # Vue 前端
│   └── src/
│       ├── components/  # 組件
│       └── views/       # 頁面
├── db/
│   └── init.sql        # 資料庫初始化
└── docker-compose.yml   # Docker 配置
```

---

## 📚 延伸閱讀

- 📖 **完整團隊指南**：`TEAM-SETUP.md`
- 🐳 **Docker 設定**：`DOCKER-SETUP.md`
- 💬 **聊天功能**：`CHAT-FIX.md`
- 🔐 **註冊功能**：`REGISTER-FIX.md`

---

## ✅ 新手檢查清單

- [ ] Docker 已安裝
- [ ] 專案已下載
- [ ] 服務已啟動（3 個容器都是 Up）
- [ ] 能訪問 http://localhost:8080
- [ ] 成功登入測試帳號
- [ ] 了解基本 Git 流程
- [ ] 知道如何查看日誌

**🎉 完成以上步驟，你就可以開始開發了！**
