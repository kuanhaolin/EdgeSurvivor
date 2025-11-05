# 16. 故障排除 (Troubleshooting)

### 16.1 常見問題

#### 問題 1：Vite 開發伺服器無法啟動

**症狀**：執行 `npm run dev` 失敗

**解決方案**：
1. 檢查端口 8080 是否被占用
2. 刪除 `node_modules` 和 `package-lock.json`，重新安裝
3. 檢查 Node.js 版本（需 16+）

```bash
# 檢查端口
netstat -ano | findstr :8080

# 重新安裝
rm -rf node_modules package-lock.json
npm install
```

#### 問題 2：API 請求失敗（CORS 錯誤）

**症狀**：瀏覽器控制台顯示 CORS 錯誤

**解決方案**：
1. 檢查後端 CORS 配置
2. 確認 Vite proxy 配置正確
3. 使用正確的 API URL

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

#### 問題 3：Socket.IO 連接失敗

**症狀**：即時聊天無法使用

**解決方案**：
1. 檢查後端 Socket.IO 是否啟動
2. 確認 WebSocket proxy 配置
3. 檢查防火牆設定

```javascript
// vite.config.js
'/socket.io': {
  target: 'http://localhost:5000',
  changeOrigin: true,
  ws: true
}
```

#### 問題 4：建置失敗（記憶體不足）

**症狀**：`npm run build` 出現 JavaScript heap out of memory

**解決方案**：
```bash
# 增加 Node.js 記憶體限制
set NODE_OPTIONS=--max_old_space_size=4096
npm run build
```

---
