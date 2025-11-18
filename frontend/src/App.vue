<template>
  <div id="app" :data-theme="theme">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 主題狀態
const theme = ref('light')

// 切換主題
const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', theme.value)
}

// 載入主題設定
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    theme.value = savedTheme
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    theme.value = 'dark'
  }
})

// 將切換函數暴露給全局使用
window.toggleTheme = toggleTheme
</script>

<style>
/* 引入主題樣式 */
@import './styles/theme.css';

/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 字體優化 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    'Microsoft YaHei', '微软雅黑', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  line-height: 1.6;
  /* iOS Safari 優化 */
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: transparent;
}

/* App 容器 */
#app {
  min-height: 100vh;
  min-height: -webkit-fill-available; /* iOS Safari 修復 */
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: background var(--transition-base), color var(--transition-base);
  position: relative;
  overflow-x: hidden;
  /* iOS 優化 */
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

/* 動態背景漸變 */
#app::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(102, 126, 234, 0.1) 0%,
    rgba(118, 75, 162, 0.05) 50%,
    transparent 100%
  );
  animation: backgroundMove 20s ease-in-out infinite;
  pointer-events: none;
  z-index: -1; /* 確保在內容下方 */
}

@keyframes backgroundMove {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(5%, 5%) rotate(90deg);
  }
  50% {
    transform: translate(-5%, 5%) rotate(180deg);
  }
  75% {
    transform: translate(-5%, -5%) rotate(270deg);
  }
}

/* 頁面內容在背景之上 */
#app > * {
  position: relative;
  z-index: 1;
}

/* 頁面切換動畫 */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Element Plus 組件主題覆蓋 */
:root {
  --el-color-primary: var(--primary-color);
  --el-color-success: var(--success-color);
  --el-color-warning: var(--warning-color);
  --el-color-danger: var(--danger-color);
  --el-color-info: var(--info-color);
  --el-border-radius-base: var(--radius-md);
  --el-transition-duration: var(--transition-base);
}

/* 卡片美化 - 強化 iOS 可見性 */
.el-card {
  border-radius: var(--radius-lg) !important;
  border: none !important;
  box-shadow: var(--shadow-md) !important;
  transition: all var(--transition-base) !important;
  background: var(--bg-primary) !important;
  /* iOS 強制可見性修復 */
  opacity: 1 !important;
  visibility: visible !important;
  display: block !important;
  position: relative !important;
  z-index: 10 !important;
  transform: translateZ(0) !important;
  -webkit-transform: translateZ(0) !important;
  backface-visibility: visible !important;
  -webkit-backface-visibility: visible !important;
}

.el-card:hover {
  box-shadow: var(--shadow-lg) !important;
}

/* 按鈕美化 */
.el-button {
  border-radius: var(--radius-md) !important;
  font-weight: 500 !important;
  transition: all var(--transition-fast) !important;
  /* iOS 觸控優化 */
  -webkit-tap-highlight-color: transparent !important;
  touch-action: manipulation !important;
}

.el-button--primary {
  background: var(--gradient-primary) !important;
  border: none !important;
}

.el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md) !important;
}

.el-button--primary:active {
  transform: translateY(0);
}

/* 輸入框美化 */
.el-input__wrapper {
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-sm) !important;
  transition: all var(--transition-base) !important;
}

.el-input__wrapper:hover {
  box-shadow: var(--shadow-md) !important;
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* iOS 輸入框優化 - 防止自動縮放 */
.el-input__inner {
  font-size: 16px !important;
}

/* 對話框美化 */
.el-dialog {
  border-radius: var(--radius-xl) !important;
  box-shadow: var(--shadow-2xl) !important;
}

/* 標籤美化 */
.el-tag {
  border-radius: var(--radius-full) !important;
  font-weight: 500 !important;
}

/* 頭像美化 */
.el-avatar {
  box-shadow: var(--shadow-sm) !important;
  transition: all var(--transition-base) !important;
}

.el-avatar:hover {
  box-shadow: var(--shadow-md) !important;
  transform: scale(1.05);
}

/* 徽章美化 */
.el-badge__content {
  border-radius: var(--radius-full) !important;
  font-weight: 600 !important;
  box-shadow: var(--shadow-sm) !important;
}

/* iOS Safari 強制可見性 */
.el-row,
.el-col,
.el-button,
.el-statistic,
.el-timeline,
.el-empty,
.el-avatar,
.el-tag {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateZ(0) !important;
  -webkit-transform: translateZ(0) !important;
}

/* 響應式優化 */
@media (max-width: 640px) {
  body {
    font-size: 14px;
  }
  
  .el-card {
    margin: var(--spacing-sm) !important;
  }
}
</style>
