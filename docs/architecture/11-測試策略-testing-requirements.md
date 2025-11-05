# 11. 測試策略 (Testing Requirements)

### 11.1 測試金字塔

```
         /\
        /  \  E2E Tests (5%)
       /____\
      /      \
     / Integration Tests (15%)
    /________\
   /          \
  / Unit Tests (80%)
 /____________\
```

### 11.2 單元測試設置

#### 11.2.1 安裝 Vitest

```bash
npm install -D vitest @vue/test-utils jsdom @vitest/ui
```

#### 11.2.2 Vitest 配置 (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.spec.js',
        '**/*.test.js'
      ]
    }
  }
})
```

#### 11.2.3 組件測試模板

```javascript
// tests/unit/components/ActivityCard.spec.js
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ActivityCard from '@/components/activity/ActivityCard.vue'
import ElementPlus from 'element-plus'

describe('ActivityCard.vue', () => {
  // Setup
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  // 測試案例 1: 正確渲染
  it('renders activity information correctly', () => {
    const activity = {
      id: 1,
      title: '陽明山登山之旅',
      status: '招募中',
      start_date: '2025-11-10',
      location: '陽明山',
      current_participants: 3,
      max_participants: 10,
      description: '一起去爬山吧！'
    }

    const wrapper = mount(ActivityCard, {
      props: { activity },
      global: {
        plugins: [ElementPlus]
      }
    })

    expect(wrapper.text()).toContain('陽明山登山之旅')
    expect(wrapper.text()).toContain('招募中')
    expect(wrapper.text()).toContain('陽明山')
    expect(wrapper.text()).toContain('3/10 人')
  })

  // 測試案例 2: 點擊事件
  it('emits view-detail event when button clicked', async () => {
    const activity = {
      id: 1,
      title: 'Test Activity',
      status: '招募中'
    }

    const wrapper = mount(ActivityCard, {
      props: { activity },
      global: {
        plugins: [ElementPlus]
      }
    })

    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('view-detail')).toBeTruthy()
    expect(wrapper.emitted('view-detail')[0]).toEqual([1])
  })

  // 測試案例 3: 描述截斷
  it('truncates long description', () => {
    const longDescription = 'A'.repeat(150)
    const activity = {
      id: 1,
      title: 'Test',
      status: '招募中',
      description: longDescription
    }

    const wrapper = mount(ActivityCard, {
      props: { 
        activity,
        truncateLength: 100
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    const description = wrapper.find('.activity-card__description').text()
    expect(description.length).toBeLessThanOrEqual(103) // 100 + '...'
    expect(description).toContain('...')
  })
})
```

#### 11.2.4 工具函數測試模板

```javascript
// tests/unit/utils/formatters.spec.js
import { describe, it, expect } from 'vitest'
import { formatDate, formatCurrency, truncateText } from '@/utils/formatters'

describe('formatters.js', () => {
  describe('formatDate', () => {
    it('formats date correctly', () => {
      const date = '2025-11-03'
      expect(formatDate(date)).toBe('2025-11-03')
      expect(formatDate(date, 'YYYY/MM/DD')).toBe('2025/11/03')
    })

    it('handles invalid date', () => {
      expect(formatDate(null)).toBe('')
      expect(formatDate('invalid')).toBe('')
    })
  })

  describe('formatCurrency', () => {
    it('formats currency correctly', () => {
      expect(formatCurrency(1000)).toBe('NT$ 1,000')
      expect(formatCurrency(1500.5)).toBe('NT$ 1,501')
    })

    it('handles zero and negative values', () => {
      expect(formatCurrency(0)).toBe('NT$ 0')
      expect(formatCurrency(-500)).toBe('NT$ -500')
    })
  })

  describe('truncateText', () => {
    it('truncates text correctly', () => {
      const text = 'This is a long text'
      expect(truncateText(text, 10)).toBe('This is a...')
    })

    it('does not truncate short text', () => {
      const text = 'Short'
      expect(truncateText(text, 10)).toBe('Short')
    })
  })
})
```

### 11.3 E2E 測試設置（使用 Playwright）

#### 11.3.1 安裝 Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

#### 11.3.2 Playwright 配置 (playwright.config.js)

```javascript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
})
```

#### 11.3.3 E2E 測試範例

```javascript
// tests/e2e/login.spec.js
import { test, expect } from '@playwright/test'

test.describe('Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    // 訪問登入頁
    await page.goto('/login')

    // 填寫表單
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')

    // 點擊登入按鈕
    await page.click('button[type="submit"]')

    // 等待跳轉到控制台
    await page.waitForURL('/dashboard')

    // 驗證頁面元素
    await expect(page.locator('h1')).toContainText('控制台')
    await expect(page.locator('.user-info')).toBeVisible()
  })

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'wrong@example.com')
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // 驗證錯誤訊息
    await expect(page.locator('.el-message--error')).toBeVisible()
    await expect(page.locator('.el-message--error')).toContainText('登入失敗')

    // 確認仍在登入頁
    await expect(page).toHaveURL('/login')
  })
})
```

### 11.4 測試最佳實踐

| 原則 | 說明 | 範例 |
|-----|------|------|
| **單元測試** | 測試單一組件或函數的邏輯 | 測試 `ActivityCard` 組件的渲染邏輯 |
| **整合測試** | 測試多個組件的互動 | 測試表單提交流程 |
| **E2E 測試** | 測試完整的使用者流程 | 測試登入到建立活動的完整流程 |
| **測試結構** | 使用 Arrange-Act-Assert 模式 | 1. 設置 2. 執行 3. 驗證 |
| **Mock 外部依賴** | API 呼叫、路由、Store | 使用 `vi.mock()` |
| **覆蓋率目標** | 80% 以上 | 使用 `vitest --coverage` 檢查 |

### 11.5 測試腳本 (package.json)

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

---
