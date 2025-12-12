# 前端測試執行指南

## 測試檔案結構

```
EdgeSurvivor/
├── frontend/
│   └── test/
│       ├── TC_1.1.1.test.js      ← 實際可執行的測試檔
|       ├── ...
│       └── conftest.py           ← Backend pytest fixtures  
├── backend/
│   ├── test/
│   │   ├── TC_1_1_1.py           ← 實際可執行的測試檔
|   |   ├── ...
│   │   └── setup.js              ← Vitest 全域設定
│   └── vitest.config.js          ← Vitest 配置
└── test/
    └── unit/
        ├── TEST_GUIDE.md
        └── UNIT_TEST_PLAN.md  
```

## 執行測試

### 前端測試 (Vitest)

```bash

當前活動的刪除事件# 進入 frontend 目錄
cd frontend

# 執行單一測試
npx vitest run test/TC_1.1.1.test.js

# 執行所有測試
npx vitest run

# 監聽模式（開發時使用）
npx vitest watch

# UI 模式
npx vitest --ui

# 已生成的 report 是互動式的 SPA ，需要服務
cd ./frontend/html && python3 -m http.server 8081
```

### 後端測試 (Pytest)

```bash
# 在專案根目錄執行
cd /backend/test/

# 執行註冊 API 測試
pytest test_TC_1_1_1.py -v --no-cov -s

# 使用 pytest-html 自動產生測試報告
# pytest.ini 設定檔可以改檔案的命名規則
pytest . --html=report.html

```

## 已安裝的依賴

### 前端測試工具

```json
{
  "vitest": "^4.0.15",
  "@vue/test-utils": "latest",
  "jsdom": "latest",
  "@vitest/ui": "latest"
}
```

### 後端測試工具

- pytest 9.0.1
- Flask test client
- SQLite (in-memory for tests)
