# 10. 效能考量 (Performance Considerations)

## 10.1 效能目標

| 指標 | 目標值 | 測量方式 |
|-----|-------|---------|
| 首次內容繪製 (FCP) | < 1.5s | Lighthouse |
| 最大內容繪製 (LCP) | < 2.5s | Lighthouse |
| 首次輸入延遲 (FID) | < 100ms | Lighthouse |
| 累積版面配置位移 (CLS) | < 0.1 | Lighthouse |
| 頁面載入時間 | < 3s | DevTools Network |

## 10.2 設計策略

### 圖片優化

- 使用 WebP 格式（降級 JPEG/PNG）
- 響應式圖片（srcset）
- 延遲載入（Lazy Loading）
- 圖片壓縮（TinyPNG、ImageOptim）
- 封面圖：最大 800x600px
- 頭像：最大 200x200px

### 程式碼優化

- 路由懶載入（Vue Router Lazy Loading）
- 組件按需載入
- Tree Shaking（移除未使用程式碼）
- 壓縮與醜化（Production Build）

### 渲染優化

- 骨架屏（Skeleton Screen）替代 Loading Spinner
- 虛擬滾動（長列表）
- 防抖與節流（搜尋、滾動事件）
- CSS 動畫優先於 JS 動畫

### 快取策略

- Service Worker（PWA 快取）
- LocalStorage（用戶偏好、草稿）
- API 回應快取（適當的 Cache-Control）

---
