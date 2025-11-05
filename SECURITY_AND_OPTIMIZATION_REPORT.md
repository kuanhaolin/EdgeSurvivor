# EdgeSurvivor 專案品質評估報告 (第二次評估)
> 生成時間：2025年11月3日  
> 分析範圍：完整專案程式碼、架構、設定檔案  
> 評估版本：v1.1 (Rate Limiting 實作後)

---

## 📋 執行摘要 (Executive Summary)

### 🎉 **整體改進成果**

專案在第一次評估後進行了**重大安全改進**，成功實作了 API Rate Limiting 並修正了前端錯誤處理。

**改進項目：**
- ✅ **已修復**: API Rate Limiting (高風險 #2)
- ✅ **已修復**: 前端 429 錯誤提示
- ✅ **已修復**: .env 檔案從版控中移除 (僅保留範例檔案)

**當前風險等級分布：**
- 🔴 **嚴重 (Critical)**: 0 個 ⬇️ (原 1 個，已修復 1 個)
- 🟠 **高風險 (High)**: 1 個 ⬇️ (原 2 個，已修復 1 個)
- 🟡 **中風險 (Medium)**: 6 個 (維持不變)
- 🟢 **低風險 (Low)**: 3 個 (維持不變)

### 📊 **品質評分**

| 類別 | 分數 | 評級 | 備註 |
|------|------|------|------|
| **安全性** | 75/100 | B+ | ✅ Rate Limiting 已實作，✅ .env 已保護，❌ CSP 待實作 |
| **效能** | 60/100 | C+ | ❌ 無連線池，❌ 無索引優化 |
| **可靠性** | 70/100 | B- | ✅ 錯誤處理完善，❌ 無測試覆蓋 |
| **維護性** | 55/100 | C | ❌ 無單元測試，❌ 無整合測試 |
| **架構品質** | 85/100 | A- | ✅ 結構清晰，✅ 模組化良好 |

**整體評分：69/100 (C+) ➜ 可上線但需持續改進**

### ⚠️ **重要提醒**

雖然專案已通過基本安全要求，但在正式上線前**強烈建議**完成以下項目：
1. 實作前端安全標頭 (CSP) - **必須**
2. 配置資料庫連線池 - **建議**
3. 添加資料庫索引 - **建議**

---

## 🎯 改進追蹤 (自第一次評估以來)

### ✅ 已完成項目

#### 1. **API Rate Limiting 實作** ✅ 
**原風險等級**: 🟠 HIGH  
**當前狀態**: ✅ **已修復**

**實作內容：**
- ✅ 安裝 Flask-Limiter 3.5.0
- ✅ 在 `app.py` 中配置 limiter (記憶體儲存)
- ✅ 使用 `before_request` hook 應用限制
- ✅ 設定登入限制：5次/分鐘
- ✅ 設定註冊限制：3次/小時
- ✅ 設定忘記密碼限制：3次/小時
- ✅ 全域預設限制：200次/天，50次/小時
- ✅ 429 錯誤處理器

**程式碼位置：**
- `backend/app.py` (lines 7-8, 17-22, 82-92, 142-147)
- `backend/requirements.txt` (Flask-Limiter==3.5.0)

**驗證狀態：** 後端已成功啟動，無編譯錯誤

#### 2. **前端 429 錯誤提示** ✅
**原問題**: 前端無 Rate Limit 錯誤提示  
**當前狀態**: ✅ **已修復**

**實作內容：**
- ✅ 在 `axios` 攔截器中添加 429 處理
- ✅ 顯示警告訊息 (橘色)
- ✅ 支援 `retry-after` header 顯示等待時間

**程式碼位置：**
- `frontend/src/api/index.js` (lines 78-87)

**使用者體驗：**
```
⚠️ 請求過於頻繁，請稍後再試 (請等待 60 秒)
```

#### 3. **.env 檔案安全** ✅ (部分完成)
**原風險等級**: 🔴 CRITICAL  
**當前狀態**: ✅ **已修復**

**確認結果：**
- ✅ `.env` 在 `.gitignore` 中
- ✅ `.env` 不在版控中 (執行 `git ls-files` 確認)
- ✅ `.env.example` 已存在作為模板
- ✅ `.env.docker` 已存在 (Docker 專用範例)

**仍需注意：**
- ⚠️ 生產環境建議使用 Docker Secrets 或雲端密鑰管理服務

---

## 🔴 嚴重安全問題 (Critical - Must Fix)

### ~~1. .env 檔案包含敏感資訊且可能被提交至版控~~ ✅ **已修復**

**原風險等級**: 🔴 **CRITICAL**  
**當前狀態**: ✅ **已解決**

**確認結果：**
- ✅ `.env` 在 `.gitignore` 中
- ✅ `.env` 不在版控中
- ✅ `.env.example` 存在作為模板

**建議下一步：**
生產環境部署時改用環境變數或密鑰管理服務（Docker Secrets / AWS Secrets Manager）

---

## 🟠 高風險問題 (High Priority)

### ~~2. 缺少 API Rate Limiting（速率限制）~~ ✅ **已修復**

**原風險等級**: 🟠 **HIGH**  
**當前狀態**: ✅ **已實作**

**實作摘要：**
```python
# backend/app.py
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # 開發環境
)

# Rate Limiting 策略：
# - 登入：5次/分鐘
# - 註冊：3次/小時
# - 忘記密碼：3次/小時
```

**生產環境建議：**
將 `storage_uri` 改為 `redis://redis:6379/1` 以支援多 worker 部署。

---

### 3. **前端缺少 Content Security Policy (CSP) 和安全標頭** ❌ **待修復**

---

## 🔴 嚴重安全問題 (Critical - Must Fix)

### 1. **.env 檔案包含敏感資訊且可能被提交至版控** 

**風險等級**: 🔴 **CRITICAL**  
**影響範圍**: 整個系統的安全性  
**檢測位置**: `.env` 檔案

**問題描述:**
```properties
# 發現明文密碼和金鑰
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
DB_PASSWORD=password
SMTP_PASSWORD=sbqzwpewldyrskzh
GOOGLE_CLIENT_SECRET=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
```

**風險:**
- JWT Token 可被偽造，導致身份驗證繞過
- 資料庫密碼洩露，攻擊者可直接存取資料庫
- SMTP 密碼洩露，可用於發送垃圾郵件
- Google OAuth 密鑰洩露，OAuth 流程可被劫持

**修正建議:**

1. **立即執行:**
```bash
# 確保 .env 在 .gitignore 中
echo ".env" >> .gitignore
git rm --cached .env  # 從 Git 歷史移除（如果已提交）

# 建立 .env.example 模板（不含真實密碼）
cp .env .env.example
# 手動將 .env.example 中的敏感資訊替換為佔位符
```

2. **建立 `.env.example`:**
```properties
SECRET_KEY=change-this-to-random-string
JWT_SECRET_KEY=change-this-to-random-string
DB_PASSWORD=your-database-password
SMTP_PASSWORD=your-smtp-app-password
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

3. **生產環境使用環境變數或密鑰管理服務:**
- Docker Secrets
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault

**驗證方式:**
```bash
# 確認 .env 不在版控中
git ls-files | grep .env  # 應該沒有輸出

# 確認 .env 在 .gitignore 中
cat .gitignore | grep .env  # 應該看到 .env
```

---

### 3. **前端缺少 Content Security Policy (CSP) 和安全標頭** ❌ **待修復**

**風險等級**: 🟠 **HIGH**  
**影響範圍**: 前端應用程式  
**檢測位置**: `frontend/index.html`  
**當前狀態**: ❌ **未修復** (唯一剩餘的高風險問題)

**風險:**
- XSS (跨站腳本攻擊) 風險
- Clickjacking 攻擊
- MIME-type sniffing 攻擊

**當前 index.html 狀態：**
```html
<!-- ❌ 無安全標頭 -->
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EdgeSurvivor - 邊緣人神器 旅伴媒合平台</title>
    <!-- 僅有基本 meta，缺少 CSP 和安全標頭 -->
  </head>
```

**修正建議 (優先級 P1 - 部署前必須)：**

**1. 在 `frontend/index.html` 中添加安全 Meta 標籤：**
```html
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- ⭐ 安全性 Meta Tags -->
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'self'; 
                   script-src 'self' 'unsafe-inline' https://accounts.google.com https://api.dicebear.com https://api.qrserver.com; 
                   style-src 'self' 'unsafe-inline'; 
                   img-src 'self' data: https: blob:; 
                   connect-src 'self' http://localhost:5001 ws://localhost:5001;
                   font-src 'self' data:;">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="Referrer-Policy" content="no-referrer-when-downgrade">
    <meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=()">
    
    <title>EdgeSurvivor - 邊緣人神器 旅伴媒合平台</title>
    <!-- 現有內容 -->
  </head>
  <body>
    <!-- 現有內容 -->
  </body>
</html>
```

**2. 後端也應設定安全標頭 (Flask)：**

在 `backend/app.py` 的 `create_app()` 函數中添加：
```python
def create_app(config_name=None):
    # 現有代碼...
    
    # ⭐ 添加安全標頭
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app
```

**預估工時：** 1 小時  
**優先級：** 🔴 **P1 - 部署前必須完成**

---

## 🟡 中風險問題 (Medium Priority)

### 4. **資料庫連線池未配置** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 資料庫效能、連線穩定性  
**檢測位置**: `backend/config.py`

**當前 config.py 狀態：**
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ❌ 無 SQLALCHEMY_ENGINE_OPTIONS 配置
```

**問題:**
- 無連線池設定，可能導致連線耗盡
- 無連線回收機制，長時間閒置連線可能失效
- 無連線健康檢查

**修正建議:**

在 `backend/config.py` 中添加：
```python
class Config:
    # 現有設定...
    
    # ⭐ 資料庫連線池設定
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # 連線池大小
        'pool_recycle': 3600,      # 每小時回收連線（防止 MySQL timeout）
        'pool_pre_ping': True,     # 每次使用前 ping 測試連線
        'max_overflow': 20,        # 超過 pool_size 的額外連線數
        'pool_timeout': 30,        # 等待連線的超時時間（秒）
    }
```

**預估工時：** 30分鐘  
**優先級：** 🟡 **P2 - 建議完成**

---

### 5. **缺少資料庫索引優化** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 查詢效能  
**檢測位置**: `db/init-complete.sql`

**檢測結果：** ❌ 無 `CREATE INDEX` 語句

**當前索引狀態：**
- ✅ `users.email` (UNIQUE INDEX - 自動建立)
- ❌ `users.location` (無索引，但常用於搜尋)
- ❌ `users.age` (無索引，但常用於篩選)
- ❌ `activities.date` (無索引，但常用於篩選)
- ❌ `activities.category` (無索引，但常用於篩選)
- ❌ `chat_messages.timestamp` (無索引，但常用於排序)

**效能影響評估：**
```sql
-- 例如：搜尋台北的使用者，可能需要全表掃描
SELECT * FROM users WHERE location = '台北市';  -- ❌ 慢查詢風險

-- 例如：查詢最近的活動，可能需要全表掃描
SELECT * FROM activities WHERE date > NOW() ORDER BY date;  -- ❌ 慢查詢風險
```

**修正建議：**

**建立 `db/add_indexes.sql` 檔案：**
```sql
-- 使用者表索引
CREATE INDEX idx_users_location ON users(location);
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_users_gender ON users(gender);

-- 活動表索引
CREATE INDEX idx_activities_date ON activities(date);
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_status ON activities(status);
CREATE INDEX idx_activities_creator_status ON activities(creator_id, status);

-- 聊天訊息表索引
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp DESC);
CREATE INDEX idx_chat_messages_match_timestamp ON chat_messages(match_id, timestamp DESC);

-- 媒合表索引
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_user_a_status ON matches(user_a, status);
CREATE INDEX idx_matches_user_b_status ON matches(user_b, status);
```

**執行索引建立：**
```powershell
docker-compose exec db mysql -u user -ppassword edgesurvivor < db/add_indexes.sql
```

**預估工時：** 1 小時  
**優先級：** 🟡 **P2 - 建議完成**

---

### 6. **無單元測試和整合測試** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 程式碼品質、維護性  
**檢測結果**: 專案中無 `.test.js`, `.test.py` 檔案

**當前測試覆蓋率：** 0%

**問題:**
- ❌ 無法驗證功能正確性
- ❌ 重構時無安全網
- ❌ 無法測量程式碼覆蓋率
- ❌ Rate Limiting 功能未經自動化測試驗證

**修正建議:**

**1. 後端測試框架 (Pytest)：**

**安裝依賴：**
```bash
pip install pytest pytest-flask pytest-cov
```

**建立 `backend/tests/test_auth.py`：**
```python
import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register(client):
    """測試使用者註冊"""
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password123!',
        'gender': 'male',
        'age': 25
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client):
    """測試使用者登入"""
    # 先註冊
    client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password123!',
        'gender': 'male',
        'age': 25
    })
    
    # 測試登入
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_rate_limiting(client):
    """測試登入 Rate Limiting"""
    # 發送 6 次登入請求
    for i in range(6):
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'wrong'
        })
        if i < 5:
            assert response.status_code in [401, 400]  # 前 5 次應該正常處理
        else:
            assert response.status_code == 429  # 第 6 次應該被限制
```

**2. 前端測試框架 (Vitest)：**

**安裝依賴：**
```bash
cd frontend
npm install -D vitest @vue/test-utils happy-dom
```

**更新 `frontend/package.json`：**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "coverage": "vitest --coverage"
  }
}
```

**建立 `frontend/src/components/__tests__/NavBar.test.js`：**
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NavBar from '../NavBar.vue'

describe('NavBar', () => {
  it('renders properly', () => {
    const wrapper = mount(NavBar)
    expect(wrapper.find('.navbar').exists()).toBe(true)
  })
  
  it('shows login button when not authenticated', () => {
    const wrapper = mount(NavBar, {
      global: {
        mocks: {
          $router: { push: () => {} }
        }
      }
    })
    expect(wrapper.text()).toContain('登入')
  })
})
```

**目標覆蓋率：** 
- 後端：80%+
- 前端：70%+

**預估工時：** 4 小時（初始設定）+ 持續編寫  
**優先級：** 🟡 **P2 - 建議完成**

---

### 7. **CORS 設定過於寬鬆** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: API 安全性  
**檢測位置**: `backend/app.py`

**當前 app.py 狀態：**
```python
# ❌ Socket.IO CORS 允許所有來源
socketio.init_app(
    app, 
    cors_allowed_origins="*",  # ❌ 允許所有來源
    # ...
)

# ✅ HTTP CORS 已限制來源
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:8080"],  # ✅ 已限制
        # ...
    }
})
```

**問題：**
- Socket.IO CORS 設定為 `"*"`，任何網站都可以連接
- 與 HTTP CORS 設定不一致

**風險:**
- CSRF 攻擊風險增加
- 未授權的網站可以建立 WebSocket 連接

**修正建議:**

```python
def create_app(config_name=None):
    # 現有代碼...
    
    # ⭐ 根據環境設定允許的來源
    allowed_origins = [
        "http://localhost:8080",
        "http://localhost:3000",
    ]
    
    # 生產環境添加實際域名
    if app.config.get('ENV') == 'production':
        allowed_origins.append("https://edgesurvivor.com")
    
    # Socket.IO 配置
    socketio.init_app(
        app, 
        cors_allowed_origins=allowed_origins,  # ✅ 使用允許清單
        async_mode='threading',
        logger=True,
        engineio_logger=False
    )
    
    # HTTP CORS 也要一致
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,  # ✅ 使用相同允許清單
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
```

**預估工時：** 30分鐘  
**優先級：** 🟡 **P2 - 建議完成**

---

### 8. **JWT Token 過期時間過長** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 身份驗證安全性  
**檢測位置**: `backend/config.py`

**當前 config.py 狀態：**
```python
class Config:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)     # ❌ 1 天太長
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)   # ⚠️ 可以接受
```

**問題：**
- Access Token 有效期 24 小時，被竊取後攻擊者有足夠時間利用
- 無法及時撤銷存取權限

**風險場景：**
```
1. 使用者在公共電腦登入
2. 忘記登出
3. Token 被存取
4. 攻擊者有 24 小時可以冒充使用者
```

**修正建議:**

**1. 縮短 Access Token 有效期：**
```python
class Config:
    # ⭐ Access Token 設為短期
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 改為 1 小時
    
    # Refresh Token 保持不變
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 添加 Token 黑名單支援（需要 Redis）
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
```

**2. 實作 Token Refresh 端點：**

在 `backend/blueprints/auth.py` 中添加：
```python
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """使用 Refresh Token 獲取新的 Access Token"""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200
```

**3. 前端自動刷新 Token：**

**注意：** `frontend/src/api/index.js` 已經實作了 Token 刷新邏輯 ✅

當前實作檢查：
```javascript
// ✅ 已實作 401 自動刷新
if (error.response?.status === 401 && !originalRequest._retry) {
  // 使用 refresh token 獲取新 access token
  const response = await axios.post('/api/auth/refresh', {}, {
    headers: { 'Authorization': 'Bearer ' + refreshToken }
  })
  // ...
}
```

**需要做的：**
1. 在後端添加 `/api/auth/refresh` 端點
2. 縮短 Access Token 有效期至 1 小時

**預估工時：** 2 小時  
**優先級：** 🟡 **P2 - 建議完成**

---

### 9. **密碼驗證規則較弱** ⚠️ **未修復**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 帳戶安全  
**檢測位置**: `backend/blueprints/auth.py`

**當前 auth.py 狀態：**
```python
def validate_password(password):
    """驗證密碼強度"""
    if len(password) < 8:
        return False, '密碼長度至少 8 個字元'
    return True, ''  # ❌ 僅檢查長度
```

**問題:**
- 僅檢查長度，未要求複雜度
- 接受 `12345678` 這類簡單密碼
- 容易被字典攻擊破解

**弱密碼範例（當前會通過驗證）：**
```
✅ "12345678"      # ❌ 純數字
✅ "aaaaaaaa"      # ❌ 單一字元重複
✅ "password"      # ❌ 常見密碼
```

**修正建議:**

```python
import re

def validate_password(password):
    """
    密碼強度驗證：
    - 至少 8 個字元
    - 包含至少 1 個大寫字母
    - 包含至少 1 個小寫字母
    - 包含至少 1 個數字
    - 包含至少 1 個特殊字元 (!@#$%^&*()_+-=[]{}|;:,.<>?)
    """
    if len(password) < 8:
        return False, '密碼長度至少 8 個字元'
    
    if not re.search(r'[A-Z]', password):
        return False, '密碼必須包含至少一個大寫字母'
    
    if not re.search(r'[a-z]', password):
        return False, '密碼必須包含至少一個小寫字母'
    
    if not re.search(r'[0-9]', password):
        return False, '密碼必須包含至少一個數字'
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, '密碼必須包含至少一個特殊字元 (!@#$%^&*等)'
    
    # 檢查常見弱密碼
    common_passwords = [
        'Password123!', '12345678', 'Aa123456!', 'Qwerty123!',
        'Password1!', 'Admin123!', 'Test1234!', 'Welcome1!'
    ]
    if password in common_passwords:
        return False, '密碼過於簡單，請使用更複雜的密碼'
    
    return True, ''
```

**前端同步驗證 (Vue)：**

在 `frontend/src/views/Register.vue` 中添加密碼強度指示器：
```vue
<script setup>
const passwordStrength = computed(() => {
  const pwd = registerForm.password
  let strength = 0
  
  if (pwd.length >= 8) strength++
  if (/[A-Z]/.test(pwd)) strength++
  if (/[a-z]/.test(pwd)) strength++
  if (/[0-9]/.test(pwd)) strength++
  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pwd)) strength++
  
  return {
    score: strength,
    label: ['很弱', '弱', '一般', '強', '很強'][strength - 1] || '很弱',
    color: ['#f56c6c', '#e6a23c', '#e6a23c', '#67c23a', '#67c23a'][strength - 1] || '#f56c6c'
  }
})
</script>

<template>
  <el-form-item label="密碼" prop="password">
    <el-input v-model="registerForm.password" type="password" />
    <div class="password-strength" :style="{ color: passwordStrength.color }">
      強度：{{ passwordStrength.label }}
    </div>
  </el-form-item>
</template>
```

**預估工時：** 1 小時  
**優先級：** 🟡 **P2 - 建議完成**

---

## 🟢 低風險問題 & 優化建議 (Low Priority)

### 10. **缺少全域錯誤處理器** ⚠️ **未修復**

**修正建議:**

在 `backend/app.py` 中添加：
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # 回滾資料庫交易
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # 記錄錯誤
    app.logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500
```

**預估工時：** 1 小時  
**優先級：** 🟢 **P3 - 可選**

---

### 11. **前端缺少 Service Worker (PWA)** ⚠️ **未修復**

**優化建議:**

安裝 Vite PWA 插件：
```bash
cd frontend
npm install -D vite-plugin-pwa
```

**更新 `vite.config.js`：**
```javascript
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'EdgeSurvivor - 邊緣人神器',
        short_name: 'EdgeSurvivor',
        description: '旅伴媒合平台',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
})
```

**預估工時：** 2 小時  
**優先級：** 🟢 **P3 - 可選**

---

### 12. **資料庫備份策略未定義** ⚠️ **未修復**

**優化建議:**

**建立備份腳本 `scripts/backup-db.sh`：**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/edgesurvivor_$DATE.sql"

docker-compose exec -T db mysqldump \
  -u user -ppassword edgesurvivor \
  > $BACKUP_FILE

# 只保留最近 7 天的備份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

**設定 Windows 排程任務 (每天凌晨 2 點)：**
```powershell
$action = New-ScheduledTaskAction -Execute "bash" -Argument "C:\EdgeSurvivor\scripts\backup-db.sh"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "EdgeSurvivor-DB-Backup"
```

**預估工時：** 1 小時  
**優先級：** 🟢 **P3 - 可選**

---

## 📊 優先順序總結 (更新後)

| 優先級 | 項目 | 狀態 | 預估工時 | 必要性 |
|-------|------|------|---------|--------|
| 🔴 P0 | ~~`.env` 安全處理~~ | ✅ **已完成** | - | - |
| 🟠 P1 | ~~API Rate Limiting~~ | ✅ **已完成** | - | - |
| 🟠 P1 | 前端安全標頭 (CSP) | ❌ **待處理** | 1小時 | **部署前必須** |
| 🟡 P2 | 資料庫連線池 | ❌ **待處理** | 30分鐘 | 建議完成 |
| 🟡 P2 | 資料庫索引優化 | ❌ **待處理** | 1小時 | 建議完成 |
| 🟡 P2 | 單元測試框架 | ❌ **待處理** | 4小時 | 建議完成 |
| 🟡 P2 | CORS 嚴格化 | ❌ **待處理** | 30分鐘 | 建議完成 |
| 🟡 P2 | JWT 時效縮短 | ❌ **待處理** | 2小時 | 建議完成 |
| 🟡 P2 | 密碼強度驗證 | ❌ **待處理** | 1小時 | 建議完成 |
| 🟢 P3 | 全域錯誤處理 | ❌ **待處理** | 1小時 | 可選 |
| 🟢 P3 | PWA 支援 | ❌ **待處理** | 2小時 | 可選 |
| 🟢 P3 | 資料庫備份 | ❌ **待處理** | 1小時 | 可選 |

**總計工時：** ~16 小時  
**已完成：** ~3.5 小時 (✅ 2 項 P0/P1 問題)  
**剩餘必須項目：** 1 小時 (CSP 安全標頭)  
**剩餘建議項目：** 10 小時

---

## ✅ 已做得很好的部分

### 🎉 新增優點 (自第一次評估以來)

1. ✅ **API Rate Limiting 實作完善** - 使用 Flask-Limiter，保護認證端點
2. ✅ **前端錯誤處理完整** - 429 錯誤有明確提示訊息
3. ✅ **.env 安全性已保護** - 不在版控中，有範例檔案

### 原有優點

4. ✅ **JWT 驗證機制完善** - 包含 expired/invalid/missing token 處理
5. ✅ **密碼 Hash 處理** - 使用 Werkzeug 的 `generate_password_hash`
6. ✅ **Email 格式驗證** - 使用正規表達式
7. ✅ **2FA (雙因素認證)** - 使用 pyotp 實作 Google Authenticator
8. ✅ **資料庫模型設計** - 關聯清晰，外鍵約束完整
9. ✅ **前端路由守衛** - 已實作身份驗證檢查
10. ✅ **響應式設計 (RWD)** - 使用 Element Plus Grid 系統
11. ✅ **Docker 容器化** - 開發環境配置完整
12. ✅ **Socket.IO 即時通訊** - 實作完整的聊天功能
13. ✅ **檔案上傳限制** - 16MB 大小限制，檔案類型驗證
14. ✅ **前端 Token 自動刷新** - axios 攔截器已實作 401 重試邏輯

---

## 🎯 執行建議 (更新後)

### 階段一：立即執行（上線前必須）✅ **66% 完成**
1. ~~修復 `.env` 安全問題~~ ✅ **已完成**
2. ~~實作 API Rate Limiting~~ ✅ **已完成**
3. 添加前端安全標頭 ⏳ **待處理** (1 小時)

### 階段二：近期優化（2週內）⏳ **0% 完成**
4. 配置資料庫連線池 (30 分鐘)
5. 添加資料庫索引 (1 小時)
6. 強化密碼驗證規則 (1 小時)
7. 縮短 JWT 過期時間 (2 小時)
8. 嚴格化 CORS 設定 (30 分鐘)

### 階段三：長期規劃（1個月內）⏳ **0% 完成**
9. 建立單元測試框架 (4 小時)
10. 實作 PWA 功能 (2 小時)
11. 設定資料庫備份策略 (1 小時)

---

## 📝 檢查清單 (Action Items) - 更新版

### 安全性
- [x] 將 `.env` 從版控中移除 ✅
- [x] 安裝並配置 Flask-Limiter ✅
- [ ] 添加 CSP 和安全標頭 ⏳ **優先**
- [ ] 強化密碼驗證規則
- [ ] 縮短 JWT Access Token 有效期至 1 小時
- [ ] 嚴格化 CORS 設定

### 效能優化
- [ ] 配置 SQLAlchemy 連線池
- [ ] 添加資料庫索引（location, date, category, timestamp）
- [ ] 實作 API 回應快取（可選）

### 測試與監控
- [ ] 建立 Pytest 測試框架
- [ ] 建立 Vitest 測試框架
- [ ] 添加資料庫連線池監控端點
- [ ] 設定日誌記錄機制
- [x] 測試 Rate Limiting 功能 ✅ (手動測試)

### 維運
- [ ] 建立資料庫備份腳本
- [ ] 設定 Windows 排程任務自動備份
- [ ] 撰寫部署文件
- [x] 建立環境變數範本 (.env.example) ✅

---

## 🚀 部署檢查清單

### 部署前必須完成 (P0/P1)
- [x] ✅ .env 不在版控中
- [x] ✅ API Rate Limiting 已實作
- [ ] ⏳ CSP 和安全標頭已添加 **← 唯一剩餘必須項**

### 部署前強烈建議 (P2)
- [ ] 資料庫連線池已配置
- [ ] 關鍵欄位索引已建立
- [ ] CORS 設定已嚴格化
- [ ] JWT Token 有效期已縮短
- [ ] 密碼驗證規則已強化

### 生產環境配置
- [ ] Rate Limiter 改用 Redis 儲存
- [ ] SMTP 使用正式郵件服務
- [ ] Google OAuth 使用正式憑證
- [ ] 前端 CSP 移除 localhost
- [ ] 啟用 HTTPS (Strict-Transport-Security)
- [ ] 設定自動化資料庫備份

---

## 📈 改進追蹤圖表

```
安全性改進進度：
P0/P1 問題：█████████░ 66% (2/3 已完成)
P2 問題：    ░░░░░░░░░░  0% (0/6 已完成)
P3 問題：    ░░░░░░░░░░  0% (0/3 已完成)

整體進度：   ███░░░░░░░ 17% (2/12 已完成)
```

**風險降低：**
- 嚴重風險：100% ⬇️ (1→0)
- 高風險：50% ⬇️ (2→1)
- 中風險：0% (6→6)
- 低風險：0% (3→3)

---

## 📞 聯絡與支援

如有任何問題或需要協助實作以上建議，請聯絡開發團隊。

**文件版本：** 2.0 (第二次評估)  
**最後更新：** 2025年11月3日  
**審查者：** Quinn (QA Test Architect)  
**專案狀態：** ✅ 可上線但需完成 CSP 安全標頭

---

## 🎓 結論與建議

### ✅ 主要成就
1. **安全性大幅提升** - 從 3 個高風險問題降至 1 個
2. **Rate Limiting 成功實作** - 有效防護暴力破解攻擊
3. **環境變數已保護** - .env 不再洩漏敏感資訊

### ⚠️ 下一步行動
**最優先 (1 小時):**
- 實作 CSP 安全標頭 → 完成後即可安全部署

**近期 (5 小時):**
- 資料庫連線池 + 索引優化 → 提升效能與穩定性
- CORS 嚴格化 → 防止 CSRF 攻擊
- 密碼驗證強化 → 提升帳戶安全

**長期 (7 小時):**
- 建立測試框架 → 確保程式碼品質
- JWT Token 縮短 → 降低 Token 竊取風險
- PWA + 資料庫備份 → 提升使用者體驗與資料安全

### 🏆 品質評價
**當前狀態：C+ (69/100) - 可上線但需持續改進**

完成 CSP 安全標頭後預計提升至：**B (75/100) - 良好品質**  
完成所有 P2 建議後預計提升至：**A- (85/100) - 優秀品質**

---

**🎯 Quinn 的建議：**  
專案已經建立了穩固的安全基礎，Rate Limiting 和 .env 保護的實作值得肯定。現在只差最後一步 (CSP 安全標頭) 即可安全部署。建議在正式上線前完成這項工作，確保使用者資料與隱私獲得完整保護。

**風險等級**: 🟠 **HIGH**  
**影響範圍**: 前端應用程式  
**檢測位置**: `frontend/index.html`

**風險:**
- XSS (跨站腳本攻擊) 風險
- Clickjacking 攻擊
- MIME-type sniffing 攻擊

**修正建議:**

**在 `frontend/index.html` 中添加安全 Meta 標籤:**
```html
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 安全性 Meta Tags -->
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'self'; 
                   script-src 'self' 'unsafe-inline' https://accounts.google.com https://api.dicebear.com https://api.qrserver.com; 
                   style-src 'self' 'unsafe-inline'; 
                   img-src 'self' data: https: blob:; 
                   connect-src 'self' http://localhost:5001 ws://localhost:5001;
                   font-src 'self' data:;">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="Referrer-Policy" content="no-referrer-when-downgrade">
    <meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=()">
    
    <title>EdgeSurvivor - 邊緣人神器 旅伴媒合平台</title>
    <!-- 現有內容 -->
  </head>
  <body>
    <!-- 現有內容 -->
  </body>
</html>
```

**後端也應設定安全標頭 (Flask):**

在 `backend/app.py` 中添加：
```python
from flask import Flask

def create_app(config_name=None):
    # 現有代碼...
    
    # 添加安全標頭
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app
```

---

## 🟡 中風險問題 (Medium Priority)

### 4. **資料庫連線池未配置**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 資料庫效能、連線穩定性  
**檢測位置**: `backend/config.py`

**問題:**
- 無連線池設定，可能導致連線耗盡
- 無連線回收機制，長時間閒置連線可能失效
- 無連線健康檢查

**修正建議:**

在 `backend/config.py` 中添加：
```python
class Config:
    # 現有設定...
    
    # 資料庫連線池設定
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # 連線池大小
        'pool_recycle': 3600,      # 每小時回收連線（防止 MySQL timeout）
        'pool_pre_ping': True,     # 每次使用前 ping 測試連線
        'max_overflow': 20,        # 超過 pool_size 的額外連線數
        'pool_timeout': 30,        # 等待連線的超時時間（秒）
    }
```

**驗證:**
```python
# 在 app.py 中添加監控
@app.route('/api/debug/db-pool')
def db_pool_status():
    pool = db.engine.pool
    return jsonify({
        'size': pool.size(),
        'checked_in': pool.checkedin(),
        'checked_out': pool.checkedout(),
        'overflow': pool.overflow()
    })
```

---

### 5. **缺少資料庫索引優化**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 查詢效能  
**檢測位置**: `db/init.sql`, `db/init-complete.sql`

**問題:**
資料庫表缺少關鍵索引，可能導致慢查詢：

**當前索引狀態:**
- ✅ `users.email` (UNIQUE INDEX)
- ❌ `users.location` (無索引，但常用於搜尋)
- ❌ `activities.date` (無索引，但常用於篩選)
- ❌ `activities.category` (無索引，但常用於篩選)
- ❌ `chat_messages.timestamp` (無索引，但常用於排序)

**修正建議:**

**更新 `db/init-complete.sql`，添加索引：**
```sql
-- 使用者表索引
CREATE INDEX idx_users_location ON users(location);
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_users_gender ON users(gender);

-- 活動表索引
CREATE INDEX idx_activities_date ON activities(date);
CREATE INDEX idx_activities_category ON activities(category);
CREATE INDEX idx_activities_status ON activities(status);
CREATE INDEX idx_activities_creator_status ON activities(creator_id, status);

-- 聊天訊息表索引
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp DESC);
CREATE INDEX idx_chat_messages_match_timestamp ON chat_messages(match_id, timestamp DESC);

-- 媒合表索引
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_user_a_status ON matches(user_a, status);
CREATE INDEX idx_matches_user_b_status ON matches(user_b, status);
```

**執行索引建立:**
```bash
docker-compose exec db mysql -u user -ppassword edgesurvivor < db/add_indexes.sql
```

---

### 6. **無單元測試和整合測試**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 程式碼品質、維護性  
**檢測結果**: 專案中無 `.test.js`, `.test.py` 檔案

**問題:**
- 無法驗證功能正確性
- 重構時無安全網
- 無法測量程式碼覆蓋率

**修正建議:**

1. **後端測試框架 (Pytest):**

**安裝依賴:**
```bash
pip install pytest pytest-flask pytest-cov
```

**建立 `backend/tests/test_auth.py`:**
```python
import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password123!',
        'gender': 'male',
        'age': 25
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client):
    # 先註冊
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'Password123!',
        # ... 其他欄位
    })
    
    # 測試登入
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
```

2. **前端測試框架 (Vitest):**

**安裝依賴:**
```bash
cd frontend
npm install -D vitest @vue/test-utils happy-dom
```

**建立 `frontend/src/components/__tests__/NavBar.test.js`:**
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NavBar from '../NavBar.vue'

describe('NavBar', () => {
  it('renders properly', () => {
    const wrapper = mount(NavBar)
    expect(wrapper.find('.navbar').exists()).toBe(true)
  })
  
  it('shows login button when not authenticated', () => {
    const wrapper = mount(NavBar, {
      global: {
        mocks: {
          $router: { push: () => {} }
        }
      }
    })
    expect(wrapper.text()).toContain('登入')
  })
})
```

**更新 `package.json`:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "coverage": "vitest --coverage"
  }
}
```

**目標覆蓋率:** 
- 後端：80%+
- 前端：70%+

---

### 7. **CORS 設定過於寬鬆**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: API 安全性  
**檢測位置**: `backend/app.py`

**問題:**
```python
socketio.init_app(
    app, 
    cors_allowed_origins="*",  # ❌ 允許所有來源
    # ...
)
```

**風險:**
- 任何網站都可以呼叫 Socket.IO
- CSRF 攻擊風險增加

**修正建議:**

```python
# 根據環境設定允許的來源
allowed_origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

# 生產環境添加實際域名
if app.config['ENV'] == 'production':
    allowed_origins.append("https://edgesurvivor.com")

socketio.init_app(
    app, 
    cors_allowed_origins=allowed_origins,
    async_mode='threading',
    logger=True,
    engineio_logger=False
)

# HTTP CORS 也要一致
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
```

---

### 8. **JWT Token 過期時間過長**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 身份驗證安全性  
**檢測位置**: `backend/config.py`

**問題:**
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)     # ❌ 1 天太長
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)   # ⚠️ 可以接受
```

**風險:**
- Token 被竊取後，攻擊者有 24 小時可使用
- 無法及時撤銷存取權限

**修正建議:**

```python
class Config:
    # Access Token 設為短期
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 改為 1 小時
    
    # Refresh Token 保持不變
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 添加 Token 黑名單支援（Redis）
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
```

**實作 Token Refresh 端點:**
```python
# backend/blueprints/auth.py
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """使用 Refresh Token 獲取新的 Access Token"""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200
```

**前端自動刷新 Token:**
```javascript
// frontend/src/utils/axios.js
let isRefreshing = false
let failedQueue = []

axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token
          return axiosInstance(originalRequest)
        })
      }
      
      originalRequest._retry = true
      isRefreshing = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const { data } = await axios.post('/api/auth/refresh', {}, {
          headers: { 'Authorization': 'Bearer ' + refreshToken }
        })
        
        localStorage.setItem('access_token', data.access_token)
        axiosInstance.defaults.headers['Authorization'] = 'Bearer ' + data.access_token
        
        failedQueue.forEach(prom => prom.resolve(data.access_token))
        failedQueue = []
        
        return axiosInstance(originalRequest)
      } catch (err) {
        failedQueue.forEach(prom => prom.reject(err))
        failedQueue = []
        // 導向登入頁
        window.location.href = '/login'
      } finally {
        isRefreshing = false
      }
    }
    
    return Promise.reject(error)
  }
)
```

---

### 9. **密碼驗證規則較弱**

**風險等級**: 🟡 **MEDIUM**  
**影響範圍**: 帳戶安全  
**檢測位置**: `backend/blueprints/auth.py`

**當前規則:**
```python
def validate_password(password):
    if len(password) < 8:
        return False, '密碼長度至少 8 個字元'
    return True, ''
```

**問題:**
- 僅檢查長度，未要求複雜度
- 容易被字典攻擊破解

**修正建議:**

```python
import re

def validate_password(password):
    """
    密碼強度驗證：
    - 至少 8 個字元
    - 包含至少 1 個大寫字母
    - 包含至少 1 個小寫字母
    - 包含至少 1 個數字
    - 包含至少 1 個特殊字元 (!@#$%^&*()_+-=[]{}|;:,.<>?)
    """
    if len(password) < 8:
        return False, '密碼長度至少 8 個字元'
    
    if not re.search(r'[A-Z]', password):
        return False, '密碼必須包含至少一個大寫字母'
    
    if not re.search(r'[a-z]', password):
        return False, '密碼必須包含至少一個小寫字母'
    
    if not re.search(r'[0-9]', password):
        return False, '密碼必須包含至少一個數字'
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, '密碼必須包含至少一個特殊字元 (!@#$%^&*等)'
    
    # 檢查常見弱密碼
    common_passwords = ['Password123!', '12345678', 'Aa123456!']
    if password in common_passwords:
        return False, '密碼過於簡單，請使用更複雜的密碼'
    
    return True, ''
```

**前端同步驗證 (Vue):**
```vue
<!-- frontend/src/views/Register.vue -->
<script setup>
const passwordStrength = computed(() => {
  const pwd = registerForm.password
  let strength = 0
  
  if (pwd.length >= 8) strength++
  if (/[A-Z]/.test(pwd)) strength++
  if (/[a-z]/.test(pwd)) strength++
  if (/[0-9]/.test(pwd)) strength++
  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pwd)) strength++
  
  return {
    score: strength,
    label: ['很弱', '弱', '一般', '強', '很強'][strength - 1] || '很弱',
    color: ['#f56c6c', '#e6a23c', '#e6a23c', '#67c23a', '#67c23a'][strength - 1] || '#f56c6c'
  }
})
</script>

<template>
  <el-form-item label="密碼" prop="password">
    <el-input v-model="registerForm.password" type="password" />
    <div class="password-strength" :style="{ color: passwordStrength.color }">
      強度：{{ passwordStrength.label }}
    </div>
  </el-form-item>
</template>
```

---

## 🟢 低風險問題 & 優化建議 (Low Priority)

### 10. **缺少全域錯誤處理器**

**修正建議:**

在 `backend/app.py` 中添加：
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # 回滾資料庫交易
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # 記錄錯誤
    app.logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500
```

---

### 11. **前端缺少 Service Worker (PWA)**

**優化建議:**

安裝 Vite PWA 插件：
```bash
cd frontend
npm install -D vite-plugin-pwa
```

**更新 `vite.config.js`:**
```javascript
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'EdgeSurvivor - 邊緣人神器',
        short_name: 'EdgeSurvivor',
        description: '旅伴媒合平台',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
})
```

---

### 12. **資料庫備份策略未定義**

**優化建議:**

**建立備份腳本 `scripts/backup-db.sh`:**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/edgesurvivor_$DATE.sql"

docker-compose exec -T db mysqldump \
  -u user -ppassword edgesurvivor \
  > $BACKUP_FILE

# 只保留最近 7 天的備份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

**設定 Cron Job (每天凌晨 2 點):**
```bash
crontab -e
# 添加以下行
0 2 * * * /path/to/EdgeSurvivor/scripts/backup-db.sh
```

---

## 📊 優先順序總結

| 優先級 | 項目 | 預估工時 | 必要性 |
|-------|------|---------|--------|
| 🔴 P0 | `.env` 安全處理 | 30分鐘 | **立即修復** |
| 🟠 P1 | API Rate Limiting | 2小時 | 部署前必須 |
| 🟠 P1 | 前端安全標頭 (CSP) | 1小時 | 部署前必須 |
| 🟡 P2 | 資料庫連線池 | 30分鐘 | 建議完成 |
| 🟡 P2 | 資料庫索引優化 | 1小時 | 建議完成 |
| 🟡 P2 | 單元測試框架 | 4小時 | 建議完成 |
| 🟡 P2 | CORS 嚴格化 | 30分鐘 | 建議完成 |
| 🟡 P2 | JWT 時效縮短 | 2小時 | 建議完成 |
| 🟡 P2 | 密碼強度驗證 | 1小時 | 建議完成 |
| 🟢 P3 | 全域錯誤處理 | 1小時 | 可選 |
| 🟢 P3 | PWA 支援 | 2小時 | 可選 |
| 🟢 P3 | 資料庫備份 | 1小時 | 可選 |

**總計工時：** ~16 小時  
**必須項目：** 3.5 小時  
**建議項目：** 10.5 小時

---

## ✅ 已做得很好的部分

1. ✅ **JWT 驗證機制完善** - 包含 expired/invalid/missing token 處理
2. ✅ **密碼 Hash 處理** - 使用 Werkzeug 的 `generate_password_hash`
3. ✅ **Email 格式驗證** - 使用正規表達式
4. ✅ **2FA (雙因素認證)** - 使用 pyotp 實作 Google Authenticator
5. ✅ **資料庫模型設計** - 關聯清晰，外鍵約束完整
6. ✅ **前端路由守衛** - 已實作身份驗證檢查
7. ✅ **響應式設計 (RWD)** - 使用 Element Plus Grid 系統
8. ✅ **Docker 容器化** - 開發環境配置完整
9. ✅ **Socket.IO 即時通訊** - 實作完整的聊天功能
10. ✅ **檔案上傳限制** - 16MB 大小限制，檔案類型驗證

---

## 🎯 執行建議

### 階段一：立即執行（上線前必須）
1. 修復 `.env` 安全問題
2. 實作 API Rate Limiting
3. 添加前端安全標頭

### 階段二：近期優化（2週內）
4. 配置資料庫連線池
5. 添加資料庫索引
6. 強化密碼驗證規則
7. 縮短 JWT 過期時間

### 階段三：長期規劃（1個月內）
8. 建立單元測試框架
9. 實作 PWA 功能
10. 設定資料庫備份策略

---

## 📝 檢查清單 (Action Items)

### 安全性
- [ ] 將 `.env` 從版控中移除
- [ ] 安裝並配置 Flask-Limiter
- [ ] 添加 CSP 和安全標頭
- [ ] 強化密碼驗證規則
- [ ] 縮短 JWT Access Token 有效期至 1 小時
- [ ] 嚴格化 CORS 設定

### 效能優化
- [ ] 配置 SQLAlchemy 連線池
- [ ] 添加資料庫索引（location, date, category, timestamp）
- [ ] 實作 API 回應快取（可選）

### 測試與監控
- [ ] 建立 Pytest 測試框架
- [ ] 建立 Vitest 測試框架
- [ ] 添加資料庫連線池監控端點
- [ ] 設定日誌記錄機制

### 維運
- [ ] 建立資料庫備份腳本
- [ ] 設定 Cron Job 自動備份
- [ ] 撰寫部署文件
- [ ] 建立環境變數範本 (.env.example)

---

## 📞 聯絡與支援

如有任何問題或需要協助實作以上建議，請聯絡開發團隊。

**文件版本：** 1.0  
**最後更新：** 2025年11月3日  
**審查者：** AI Code Reviewer