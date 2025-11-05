# 15. 部署與 CI/CD (Deployment)

### 15.1 建置流程

```bash
# 安裝依賴
npm ci

# 執行測試
npm run test:unit
npm run test:e2e

# 程式碼檢查
npm run lint

# 生產建置
npm run build

# 建置輸出在 dist/ 目錄
```

### 15.2 Docker 部署

前端已包含在專案根目錄的 `docker-compose.yml` 中：

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "8080:80"
  environment:
    - VITE_API_TARGET=http://backend:5000
  depends_on:
    - backend
```

### 15.3 CI/CD Pipeline 建議（GitHub Actions）

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test:unit
      - run: cd frontend && npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # 部署腳本
```

---
