# 12. 前端開發者標準 (Frontend Developer Standards)

### 12.1 關鍵編碼規則

#### 12.1.1 Vue 3 Composition API 規則

```javascript
// ✅ 正確：使用 Composition API
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

onMounted(() => {
  console.log('Component mounted')
})
</script>

// ❌ 錯誤：不要混用 Options API
<script>
export default {
  data() {
    return { count: 0 }
  }
}
</script>
```

#### 12.1.2 響應式數據規則

```javascript
// ✅ 正確：使用 ref 和 reactive
import { ref, reactive } from 'vue'

const count = ref(0)
const user = reactive({ name: 'John', age: 30 })

// 訪問值
console.log(count.value)
console.log(user.name)

// ❌ 錯誤：直接賦值給 reactive 對象
user = { name: 'Jane' } // 會失去響應式

// ✅ 正確：使用 Object.assign 或展開運算符
Object.assign(user, { name: 'Jane' })
```

#### 12.1.3 組件通信規則

```vue
<!-- ✅ 正確：父傳子使用 Props -->
<template>
  <ChildComponent :user="user" :count="count" />
</template>

<!-- ✅ 正確：子傳父使用 Emits -->
<script setup>
const emit = defineEmits(['update', 'delete'])

const handleUpdate = () => {
  emit('update', { id: 1 })
}
</script>

<!-- ❌ 錯誤：不要直接修改 Props -->
<script setup>
const props = defineProps(['count'])
props.count++ // 錯誤！
</script>
```

#### 12.1.4 異步處理規則

```javascript
// ✅ 正確：使用 async/await
const fetchData = async () => {
  try {
    loading.value = true
    const response = await getActivities()
    activities.value = response.data
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

// ❌ 錯誤：未處理錯誤
const fetchData = async () => {
  const response = await getActivities()
  activities.value = response.data
}
```

#### 12.1.5 性能優化規則

```vue
<!-- ✅ 正確：使用 v-show 用於頻繁切換 -->
<div v-show="isVisible">Content</div>

<!-- ✅ 正確：使用 v-if 用於條件渲染 -->
<div v-if="isLoggedIn">Welcome</div>

<!-- ✅ 正確：使用 :key 在 v-for 中 -->
<div v-for="item in items" :key="item.id">
  {{ item.name }}
</div>

<!-- ❌ 錯誤：不要使用 index 作為 key -->
<div v-for="(item, index) in items" :key="index">
  {{ item.name }}
</div>

<!-- ✅ 正確：使用 computed 緩存計算結果 -->
<script setup>
const expensiveComputation = computed(() => {
  return items.value.filter(...).map(...)
})
</script>

<!-- ❌ 錯誤：在模板中進行複雜計算 -->
<template>
  <div>{{ items.filter(...).map(...) }}</div>
</template>
```

### 12.2 程式碼風格規範

#### 12.2.1 ESLint 配置 (.eslintrc.js)

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    '@vue/eslint-config-prettier'
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module'
  },
  rules: {
    // Vue 相關
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'error',
    'vue/require-prop-types': 'error',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/html-self-closing': ['error', {
      html: {
        void: 'always',
        normal: 'never',
        component: 'always'
      }
    }],

    // JavaScript 相關
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'prefer-const': 'error',
    'no-var': 'error',

    // 程式碼風格
    'quotes': ['error', 'single'],
    'semi': ['error', 'never'],
    'comma-dangle': ['error', 'never'],
    'arrow-parens': ['error', 'always'],
    'space-before-function-paren': ['error', 'never']
  }
}
```

#### 12.2.2 Prettier 配置 (.prettierrc)

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "none",
  "arrowParens": "always",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "endOfLine": "lf",
  "vueIndentScriptAndStyle": false
}
```

### 12.3 Git 提交規範

#### 12.3.1 提交訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 12.3.2 Type 類型

| Type | 說明 | 範例 |
|------|------|------|
| **feat** | 新功能 | `feat(activities): add activity filter` |
| **fix** | 修復 Bug | `fix(chat): resolve message ordering issue` |
| **docs** | 文件更新 | `docs(readme): update setup instructions` |
| **style** | 程式碼格式（不影響邏輯） | `style(auth): format login component` |
| **refactor** | 重構 | `refactor(api): simplify axios interceptor` |
| **perf** | 性能優化 | `perf(list): implement virtual scrolling` |
| **test** | 測試相關 | `test(utils): add formatters unit tests` |
| **chore** | 建置/工具變更 | `chore(deps): update dependencies` |

#### 12.3.3 提交範例

```bash
# 好的提交訊息
git commit -m "feat(activities): add activity search and filter functionality"
git commit -m "fix(chat): resolve WebSocket reconnection issue on network error"
git commit -m "refactor(stores): migrate from Vuex to Pinia"

# 不好的提交訊息
git commit -m "update"
git commit -m "fix bug"
git commit -m "WIP"
```

### 12.4 快速參考指南

#### 12.4.1 常用命令

```bash
# 開發伺服器
npm run dev

# 生產建置
npm run build

# 預覽生產建置
npm run preview

# 程式碼檢查
npm run lint

# 程式碼格式化
npm run format

# 單元測試
npm run test:unit

# 覆蓋率測試
npm run test:coverage

# E2E 測試
npm run test:e2e
```

#### 12.4.2 關鍵導入模式

```javascript
// Vue 核心
import { ref, reactive, computed, watch, onMounted } from 'vue'

// Router
import { useRouter, useRoute } from 'vue-router'

// Store
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

// Element Plus
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

// API
import { getActivities, createActivity } from '@/api/activities'

// Utils
import { formatDate, formatCurrency } from '@/utils/formatters'

// Composables
import { useAuth } from '@/composables/useAuth'
```

#### 12.4.3 常用程式碼片段

```javascript
// 基礎響應式狀態
const data = ref(null)
const loading = ref(false)
const error = ref(null)

// API 請求模式
const fetchData = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await getData()
    data.value = response.data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// 表單驗證
const rules = {
  email: [
    { required: true, message: '請輸入 Email', trigger: 'blur' },
    { type: 'email', message: '請輸入有效的 Email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
    { min: 8, message: '密碼至少 8 個字元', trigger: 'blur' }
  ]
}

// Computed 屬性
const filteredItems = computed(() => {
  return items.value.filter((item) => {
    return item.status === 'active'
  })
})

// Watch 監聽
watch(searchTerm, (newValue, oldValue) => {
  console.log(`Search changed from ${oldValue} to ${newValue}`)
  fetchSearchResults(newValue)
})

// Store 使用
const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)
const { login, logout } = authStore
```

---
