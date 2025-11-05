# 10. 環境配置 (Environment Configuration)

### 10.1 環境變數定義

EdgeSurvivor 使用 Vite 的環境變數系統。所有環境變數必須以 `VITE_` 開頭才能在客戶端代碼中訪問。

#### 10.1.1 開發環境 (.env.development)

```bash
# API 配置
VITE_API_BASE_URL=http://localhost:5000/api
VITE_API_TARGET=http://localhost:5000
VITE_SOCKET_URL=http://localhost:5000

# 上傳配置
VITE_UPLOAD_URL=http://localhost:5000/uploads
VITE_MAX_FILE_SIZE=16777216

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your-google-client-id-here

# 功能開關
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# 其他
NODE_ENV=development
```

#### 10.1.2 生產環境 (.env.production)

```bash
# API 配置
VITE_API_BASE_URL=https://api.edgesurvivor.com/api
VITE_API_TARGET=https://api.edgesurvivor.com
VITE_SOCKET_URL=https://api.edgesurvivor.com

# 上傳配置
VITE_UPLOAD_URL=https://api.edgesurvivor.com/uploads
VITE_MAX_FILE_SIZE=16777216

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your-production-google-client-id

# 功能開關
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false

# 其他
NODE_ENV=production
```

#### 10.1.3 測試環境 (.env.test)

```bash
# API 配置
VITE_API_BASE_URL=http://localhost:5000/api
VITE_SOCKET_URL=http://localhost:5000

# 功能開關
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# 其他
NODE_ENV=test
```

### 10.2 環境變數使用範例

```javascript
// ✅ 在代碼中訪問環境變數
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
const mode = import.meta.env.MODE

// ✅ 使用範例
if (import.meta.env.VITE_ENABLE_DEBUG) {
  console.log('Debug mode enabled')
}

// ❌ 避免：未以 VITE_ 開頭的變數無法訪問
const secret = import.meta.env.SECRET_KEY // undefined
```

### 10.3 TypeScript 類型定義（可選）

創建 `src/vite-env.d.ts`：

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TARGET: string
  readonly VITE_SOCKET_URL: string
  readonly VITE_UPLOAD_URL: string
  readonly VITE_MAX_FILE_SIZE: string
  readonly VITE_GOOGLE_CLIENT_ID: string
  readonly VITE_ENABLE_ANALYTICS: string
  readonly VITE_ENABLE_DEBUG: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

---
