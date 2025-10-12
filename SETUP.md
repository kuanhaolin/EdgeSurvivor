# EdgeSurvivor 環境設定指南

## 1. 環境變數設定

### 複製環境變數範例
```bash
cp .env.example .env
```

### 編輯 .env 檔案
修改 `.env` 檔案中的以下設定：
```env
# 重要：修改這些密碼和密鑰
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# MariaDB 設定 - 只需要修改密碼
DB_PASSWORD=your_actual_mariadb_password

# 其他設定通常不需要修改
```

## 2. 資料庫設定 (MariaDB)

### 方法一：使用自動化腳本 (推薦)
```bash
# 安裝 Python 依賴
pip install -r backend/requirements.txt

# 執行自動設定腳本
python setup_database.py
```
此腳本會：
- 自動讀取 `.env` 檔案的設定
- 建立資料庫和使用者
- 設定權限
- 測試連線

### 方法二：手動執行 SQL
如果偏好手動設定：
```bash
# 生成 SQL 腳本
python setup_database.py
# 選擇選項 2 來生成 SQL 檔案

# 執行生成的 SQL
mysql -u root -p < database_setup_generated.sql
```

## 3. 應用程式初始化

### 測試資料庫連線
```bash
cd backend
python init_db.py test
```

### 初始化資料庫表格
```bash
python init_db.py
```

### 建立測試資料 (可選)
```bash
set CREATE_TEST_DATA=true
python init_db.py
```

## 4. 啟動服務

### 後端服務
```bash
cd backend
python app.py
```

### 前端服務
```bash
cd frontend
npm install
npm run dev
```

## 5. 驗證安裝

### 檢查後端 API
- 健康檢查: http://localhost:5000/api/health
- API 根目錄: http://localhost:5000

### 檢查前端應用
- 前端應用: http://localhost:3000

## 6. 常用命令

### 資料庫管理
```bash
# 測試連線
python init_db.py test

# 重置資料庫
python init_db.py reset

# 刪除所有表格
python init_db.py drop
```

### 開發工具
```bash
# 檢查程式碼錯誤
cd backend
python -m py_compile app.py

# 前端建置
cd frontend
npm run build
```

## 7. Docker 部署 (可選)

### docker-compose.yml 範例
```yaml
version: '3.8'
services:
  db:
    image: mariadb:10.11
    environment:
      MARIADB_ROOT_PASSWORD: root_password
      MARIADB_DATABASE: edgesurvivor
      MARIADB_USER: edgesurvivor_user
      MARIADB_PASSWORD: ${DB_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - db
    env_file:
      - .env
    environment:
      - DB_HOST=db

volumes:
  mariadb_data:
```

### 啟動 Docker
```bash
docker-compose up -d
```

## 8. 故障排除

### 常見問題

#### 1. 資料庫連線失敗
```bash
# 檢查 MariaDB 是否運行
systemctl status mariadb  # Linux
# 或檢查服務管理員 (Windows)

# 測試連線
python init_db.py test
```

#### 2. 權限錯誤
```sql
-- 檢查使用者權限
SHOW GRANTS FOR 'edgesurvivor_user'@'localhost';

-- 重新授權
GRANT ALL PRIVILEGES ON edgesurvivor.* TO 'edgesurvivor_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 匯入錯誤
```bash
# 檢查 Python 路徑
python -c "import sys; print(sys.path)"

# 重新安裝依賴
pip install -r backend/requirements.txt
```

#### 4. 前端錯誤
```bash
# 清除緩存
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 9. 安全建議

### 生產環境
- 使用強密碼 (至少12位，包含大小寫、數字、符號)
- 更改所有預設密鑰
- 設定防火牆
- 使用 HTTPS
- 定期備份資料庫

### 開發環境
- 不要提交 `.env` 檔案到版本控制
- 定期更新依賴套件
- 使用不同的密鑰用於開發和生產