# 2. 前端技術棧 (Frontend Tech Stack)

### 2.1 技術棧總覽表

| 類別 | 技術 | 版本 | 用途 | 選擇理由 |
|------|------|------|------|---------|
| **核心框架** | Vue.js | 3.3.8+ | 前端 UI 框架 | 漸進式框架、Composition API、優秀的效能、豐富的生態系統 |
| **UI 組件庫** | Element Plus | 2.4.2+ | 企業級 UI 組件庫 | 完整的組件集、優秀的設計、活躍的社群、良好的 Vue 3 支援 |
| **狀態管理** | Pinia | 2.1.7+ | 應用狀態管理 | Vue 3 官方推薦、TypeScript 友善、模組化設計、DevTools 支援 |
| **路由** | Vue Router | 4.2.5+ | 單頁應用路由 | Vue 官方路由、支援嵌套路由、路由守衛、懶載入 |
| **建構工具** | Vite | 4.5.3+ | 開發伺服器與打包工具 | 極快的冷啟動、HMR、原生 ESM、優化的打包輸出 |
| **HTTP 客戶端** | Axios | 1.6.0+ | HTTP 請求函式庫 | 攔截器支援、Promise API、廣泛使用、易於測試 |
| **即時通訊** | Socket.IO Client | 4.7.4+ | WebSocket 客戶端 | 自動重連、房間機制、與後端 Flask-SocketIO 完美配合 |
| **樣式方案** | SCSS + CSS Variables | - | CSS 預處理器與主題系統 | 支援嵌套、變數、混合；CSS Variables 支援動態主題 |
| **日期處理** | Day.js | 1.11.10+ | 日期格式化與處理 | 輕量（僅 2KB）、Moment.js 替代方案、豐富的 API |
| **圖示庫** | Element Plus Icons | 2.1.0+ | 圖示組件 | 與 Element Plus 集成、SVG 圖示、Tree-shakable |
| **Cookie 管理** | js-cookie | 3.0.5+ | Cookie 操作 | 輕量、簡單的 API、跨瀏覽器相容 |
| **程式碼規範** | ESLint + Prettier | 8.54.0+ | 程式碼檢查與格式化 | 統一程式碼風格、自動修復、Vue 3 支援 |
| **測試框架** | Vitest (建議) | - | 單元測試 | Vite 原生整合、快速執行、與 Jest API 相容 |
| **E2E 測試** | Playwright (建議) | - | 端到端測試 | 跨瀏覽器、自動等待、強大的選擇器 |

### 2.2 瀏覽器支援

根據 PRD 的 NFR3.1 要求：

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Browserslist 配置**：
```
> 1%
last 2 versions
not dead
not ie 11
```

---
