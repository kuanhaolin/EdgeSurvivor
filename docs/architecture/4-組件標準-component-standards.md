# 4. 組件標準 (Component Standards)

### 4.1 組件命名規範

#### 4.1.1 文件命名

- **PascalCase**：所有 Vue 組件文件使用 PascalCase 命名
- **語意化**：名稱應清楚描述組件用途

```
✅ 正確：
  - ActivityCard.vue
  - ChatWindow.vue
  - ImageUploader.vue

❌ 錯誤：
  - activityCard.vue
  - chat-window.vue
  - img-uploader.vue
```

#### 4.1.2 組件名稱規則

| 類型 | 規則 | 範例 |
|------|------|------|
| **基礎組件** | 以 `Base` 開頭 | `BaseButton.vue`, `BaseInput.vue` |
| **單一實例組件** | 以 `The` 開頭 | `TheNavBar.vue`, `TheSidebar.vue` |
| **緊密耦合組件** | 以父組件名稱開頭 | `ActivityCard.vue` → `ActivityCardActions.vue` |
| **頁面組件** | 描述性名稱 | `Dashboard.vue`, `ActivityDetail.vue` |

#### 4.1.3 組件註冊

```javascript
// ✅ 全域註冊（main.js）- 僅用於基礎組件
import BaseButton from '@/components/common/BaseButton.vue'
app.component('BaseButton', BaseButton)

// ✅ 局部註冊（推薦）
import ActivityCard from '@/components/activity/ActivityCard.vue'
export default {
  components: { ActivityCard }
}

// ✅ 使用時採用 PascalCase
<ActivityCard :activity="activity" />
```

### 4.2 組件模板範例

#### 4.2.1 基礎組件模板（Composition API）

```vue
<template>
  <div class="activity-card" :class="cardClasses">
    <!-- 封面圖 -->
    <div v-if="activity.cover_image" class="activity-card__cover">
      <img :src="activity.cover_image" :alt="activity.title" loading="lazy" />
    </div>

    <!-- 內容區 -->
    <div class="activity-card__content">
      <div class="activity-card__header">
        <h3 class="activity-card__title">{{ activity.title }}</h3>
        <el-tag :type="statusTagType" size="small">
          {{ activity.status }}
        </el-tag>
      </div>

      <div class="activity-card__info">
        <div class="info-item">
          <el-icon><Calendar /></el-icon>
          <span>{{ formattedDate }}</span>
        </div>
        <div class="info-item">
          <el-icon><Location /></el-icon>
          <span>{{ activity.location }}</span>
        </div>
        <div class="info-item">
          <el-icon><User /></el-icon>
          <span>{{ participantsText }}</span>
        </div>
      </div>

      <p class="activity-card__description">
        {{ truncatedDescription }}
      </p>
    </div>

    <!-- 操作區 -->
    <div class="activity-card__actions">
      <el-button type="primary" @click="handleViewDetail">
        查看詳情
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Calendar, Location, User } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

// Props
const props = defineProps({
  activity: {
    type: Object,
    required: true,
    validator: (value) => {
      return value.id && value.title && value.status
    }
  },
  truncateLength: {
    type: Number,
    default: 100
  }
})

// Emits
const emit = defineEmits(['view-detail'])

// Router
const router = useRouter()

// Computed
const formattedDate = computed(() => {
  return dayjs(props.activity.start_date).format('YYYY-MM-DD')
})

const participantsText = computed(() => {
  const current = props.activity.current_participants || 0
  const max = props.activity.max_participants || 0
  return `${current}/${max} 人`
})

const truncatedDescription = computed(() => {
  const desc = props.activity.description || ''
  if (desc.length <= props.truncateLength) {
    return desc
  }
  return desc.substring(0, props.truncateLength) + '...'
})

const statusTagType = computed(() => {
  const statusMap = {
    '招募中': 'success',
    '進行中': 'warning',
    '已完成': 'info',
    '已取消': 'danger'
  }
  return statusMap[props.activity.status] || 'info'
})

const cardClasses = computed(() => ({
  'activity-card--clickable': true,
  'activity-card--featured': props.activity.is_featured
}))

// Methods
const handleViewDetail = () => {
  emit('view-detail', props.activity.id)
  router.push(`/activities/${props.activity.id}`)
}
</script>

<style lang="scss" scoped>
.activity-card {
  background: var(--el-bg-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--el-box-shadow-light);
  overflow: hidden;
  transition: all 0.3s var(--el-transition-function);

  &--clickable {
    cursor: pointer;

    &:hover {
      transform: translateY(-4px);
      box-shadow: var(--el-box-shadow-dark);
    }
  }

  &__cover {
    width: 100%;
    height: 200px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: var(--spacing-md);
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-sm);
  }

  &__title {
    font-size: var(--font-size-h4);
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin: 0;
    flex: 1;
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-sm);

    .info-item {
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
      font-size: var(--font-size-small);
      color: var(--el-text-color-secondary);

      .el-icon {
        font-size: 16px;
      }
    }
  }

  &__description {
    font-size: var(--font-size-body);
    color: var(--el-text-color-regular);
    line-height: 1.6;
    margin: 0;
  }

  &__actions {
    padding: var(--spacing-md);
    border-top: 1px solid var(--el-border-color-lighter);
  }
}

// 響應式
@media (max-width: 640px) {
  .activity-card {
    &__cover {
      height: 150px;
    }
  }
}
</style>
```

### 4.3 組件編寫最佳實踐

#### 4.3.1 組件結構順序

```vue
<template>
  <!-- 模板內容 -->
</template>

<script setup>
// 1. 導入
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 2. Props
const props = defineProps({...})

// 3. Emits
const emit = defineEmits(['event-name'])

// 4. 響應式數據
const data = ref(null)

// 5. Computed
const computed = computed(() => {...})

// 6. Methods
const handleClick = () => {...}

// 7. 生命週期
onMounted(() => {...})
</script>

<style lang="scss" scoped>
/* 樣式內容 */
</style>
```

#### 4.3.2 Props 定義規範

```javascript
// ✅ 完整的 Props 定義
const props = defineProps({
  // 基本類型
  title: {
    type: String,
    required: true
  },
  
  // 帶預設值
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  
  // 對象類型（提供預設值工廠函數）
  user: {
    type: Object,
    default: () => ({})
  },
  
  // 數組類型
  items: {
    type: Array,
    default: () => []
  },
  
  // 多種類型
  value: {
    type: [String, Number],
    default: ''
  }
})

// ❌ 避免：缺少類型定義
const props = defineProps(['title', 'size'])
```

#### 4.3.3 Emits 定義規範

```javascript
// ✅ 定義並驗證 Emits
const emit = defineEmits({
  // 帶驗證
  submit: (payload) => {
    return payload && typeof payload.id === 'number'
  },
  
  // 不帶驗證
  cancel: null,
  
  // 事件名稱使用 kebab-case
  'update:modelValue': (value) => typeof value === 'string'
})

// 使用
emit('submit', { id: 1, name: 'Test' })
emit('update:modelValue', 'new value')

// ❌ 避免：直接 emit 未定義的事件
this.$emit('unknownEvent')
```

---
