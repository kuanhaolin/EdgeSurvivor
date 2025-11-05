# 13. 效能優化檢查清單 (Performance Optimization Checklist)

### 13.1 建置優化

- [x] **程式碼分割**：使用路由懶載入，減少初始載入包大小
- [x] **Tree Shaking**：移除未使用的程式碼
- [x] **Chunk 分割**：將第三方庫分離到 vendor chunk
- [x] **壓縮與醜化**：生產環境自動壓縮 JS 和 CSS
- [ ] **Gzip 壓縮**：伺服器端啟用 Gzip 壓縮
- [ ] **Source Map**：生產環境禁用或上傳到錯誤追蹤服務

### 13.2 資源優化

- [x] **圖片懶載入**：使用 `loading="lazy"` 屬性
- [ ] **圖片格式**：使用 WebP 格式，降級到 JPEG/PNG
- [ ] **響應式圖片**：使用 `srcset` 提供不同尺寸
- [x] **圖示優化**：使用 SVG 圖示，支援 Tree-shaking
- [ ] **字型優化**：使用系統字型或 font-display: swap

### 13.3 渲染優化

- [x] **虛擬滾動**：長列表使用虛擬滾動（如活動列表）
- [x] **骨架屏**：使用骨架屏替代 Loading Spinner
- [x] **防抖與節流**：搜尋、滾動事件使用防抖/節流
- [x] **Computed 緩存**：使用 computed 替代 methods 進行計算
- [x] **v-show vs v-if**：頻繁切換使用 v-show，條件渲染使用 v-if

### 13.4 網路優化

- [x] **API 快取**：適當使用 HTTP 快取頭
- [x] **請求合併**：避免重複請求，使用快取
- [ ] **CDN**：靜態資源使用 CDN
- [x] **預載入**：關鍵資源使用 `<link rel="preload">`
- [ ] **Service Worker**：使用 PWA 快取策略

---
