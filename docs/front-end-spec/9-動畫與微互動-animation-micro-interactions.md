# 9. 動畫與微互動 (Animation & Micro-interactions)

## 9.1 動畫原則

1. **有目的性**：動畫應強化理解，而非干擾
2. **快速流暢**：持續時間 150-350ms
3. **自然緩動**：使用 ease-out 或 cubic-bezier
4. **可關閉**：尊重使用者偏好設定（prefers-reduced-motion）

## 9.2 關鍵動畫

| 動畫名稱 | 持續時間 | 緩動函數 | 用途 |
|---------|---------|---------|------|
| fadeIn | 250ms | ease-out | 內容淡入 |
| slideInUp | 250ms | ease-out | 從下滑入 |
| slideInDown | 250ms | ease-out | 從上滑入 |
| slideInLeft | 250ms | ease-out | 從左滑入 |
| slideInRight | 250ms | ease-out | 從右滑入 |
| scaleIn | 250ms | ease-out | 縮放進入 |
| pulse | 2s | ease-in-out | 脈衝動畫（徽章） |
| rotate | 1s | linear | 旋轉動畫（Loading） |
| bounce | 0.6s | cubic-bezier | 彈跳動畫（強調） |
| shake | 0.5s | ease-in-out | 搖晃動畫（錯誤） |

## 9.3 微互動範例

- **按鈕點擊**：上移 2px（150ms）  按下回彈（100ms）
- **卡片懸停**：上移 4px + 陰影增強（250ms）
- **輸入聚焦**：藍紫光暈淡入（200ms）
- **Toast 通知**：從頂部滑下（300ms）  停留 3s  淡出（300ms）
- **Loading**：旋轉動畫 + 脈衝效果
- **新訊息**：輕微彈跳 + 聲音提示（可選）
- **頁面切換**：淡出舊頁（200ms）  淡入新頁（200ms）

---
