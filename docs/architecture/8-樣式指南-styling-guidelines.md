# 8. 樣式指南 (Styling Guidelines)

### 8.1 CSS 變數系統 (styles/theme.css)

```css
/**
 * EdgeSurvivor 主題變數系統
 * 基於 UX 規格的設計系統
 */

:root {
  /* ========== 色彩系統 ========== */
  
  /* 主色調 */
  --color-primary: #667eea;
  --color-primary-light: #818cf8;
  --color-primary-dark: #5b63d3;
  --color-secondary: #764ba2;
  --color-secondary-light: #9d6cc1;
  --color-secondary-dark: #5e3a7f;

  /* 功能色 */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #3b82f6;

  /* 中性色 - Light Mode */
  --color-text-primary: #1f2937;
  --color-text-secondary: #6b7280;
  --color-text-disabled: #9ca3af;
  --color-border: #e5e7eb;
  --color-divider: #f3f4f6;
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;

  /* 漸變色 */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-success: linear-gradient(135deg, #4ade80 0%, #10b981 100%);
  --gradient-info: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);

  /* ========== 間距系統 ========== */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* ========== 字體系統 ========== */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
                 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 
                 'Helvetica Neue', 'Microsoft YaHei', '微软雅黑', sans-serif;
  --font-family-mono: 'Courier New', Courier, monospace;

  /* 字級 */
  --font-size-h1: 32px;
  --font-size-h2: 24px;
  --font-size-h3: 20px;
  --font-size-h4: 18px;
  --font-size-body: 16px;
  --font-size-small: 14px;
  --font-size-caption: 12px;

  /* 字重 */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* 行高 */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;

  /* ========== 圓角系統 ========== */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  --border-radius-2xl: 24px;
  --border-radius-full: 9999px;

  /* ========== 陰影系統 ========== */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

  /* ========== 過渡系統 ========== */
  --transition-fast: 150ms;
  --transition-base: 250ms;
  --transition-slow: 350ms;
  --transition-function: cubic-bezier(0.4, 0, 0.2, 1);

  /* ========== Z-Index 系統 ========== */
  --z-index-dropdown: 1000;
  --z-index-sticky: 1020;
  --z-index-fixed: 1030;
  --z-index-modal-backdrop: 1040;
  --z-index-modal: 1050;
  --z-index-popover: 1060;
  --z-index-tooltip: 1070;
}

/* ========== Dark Mode ========== */
[data-theme='dark'] {
  /* 中性色 - Dark Mode */
  --color-text-primary: #f9fafb;
  --color-text-secondary: #d1d5db;
  --color-text-disabled: #6b7280;
  --color-border: #374151;
  --color-divider: #1f2937;
  --color-bg-primary: #111827;
  --color-bg-secondary: #1f2937;
  --color-bg-tertiary: #374151;
}

/* ========== 響應式字級調整 ========== */
@media (max-width: 640px) {
  :root {
    --font-size-h1: 28px;
    --font-size-h2: 22px;
    --font-size-h3: 18px;
    --font-size-h4: 16px;
    --font-size-body: 14px;
    --font-size-small: 12px;
    --font-size-caption: 11px;
  }
}
```

### 8.2 全域樣式 (styles/global.scss)

```scss
/**
 * 全域樣式
 */

// 導入變數
@import './mixins.scss';

// 重置與基礎樣式
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  line-height: var(--line-height-normal);
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  min-height: 100vh;
}

// 標題樣式
h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-md);
}

h2 {
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-sm);
}

h3 {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-sm);
}

h4 {
  font-size: var(--font-size-h4);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  margin-bottom: var(--spacing-xs);
}

// 連結樣式
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast) var(--transition-function);

  &:hover {
    color: var(--color-primary-light);
  }
}

// 按鈕重置
button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

// 輸入框重置
input,
textarea,
select {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

// 列表重置
ul,
ol {
  list-style: none;
}

// 圖片
img {
  max-width: 100%;
  height: auto;
  display: block;
}

// 滾動條樣式（Webkit）
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg-tertiary);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--border-radius-full);

  &:hover {
    background: var(--color-text-disabled);
  }
}

// 選擇文字顏色
::selection {
  background-color: var(--color-primary-light);
  color: white;
}

// 玻璃擬態效果
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

[data-theme='dark'] .glass-effect {
  background: rgba(31, 41, 55, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### 8.3 SCSS Mixins (styles/mixins.scss)

```scss
/**
 * SCSS Mixins
 */

// 響應式斷點
$breakpoints: (
  'mobile': 640px,
  'tablet': 1024px,
  'desktop': 1440px,
);

// 響應式 Mixin
@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (max-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Breakpoint #{$breakpoint} not found.";
  }
}

// Flexbox 居中
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

// Flexbox 列
@mixin flex-column {
  display: flex;
  flex-direction: column;
}

// 文字省略
@mixin text-ellipsis($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

// 清除浮動
@mixin clearfix {
  &::after {
    content: '';
    display: table;
    clear: both;
  }
}

// 絕對定位居中
@mixin absolute-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

// 卡片樣式
@mixin card {
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-md);
}

// 按鈕樣式
@mixin button-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base) var(--transition-function);
  cursor: pointer;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

// 漸變背景
@mixin gradient-bg($gradient) {
  background: $gradient;
  background-size: 200% 200%;
  transition: background-position var(--transition-base) var(--transition-function);

  &:hover {
    background-position: right center;
  }
}

// 使用範例
// .my-card {
//   @include card;
//   @include respond-to('mobile') {
//     padding: var(--spacing-sm);
//   }
// }
```

### 8.4 動畫定義 (styles/animations.scss)

```scss
/**
 * 動畫定義
 */

// 淡入
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// 從下滑入
@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

// 從上滑入
@keyframes slideInDown {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

// 縮放進入
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

// 脈衝
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

// 旋轉
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

// 彈跳
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

// 搖晃
@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-5px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(5px);
  }
}

// 工具類
.fade-in {
  animation: fadeIn var(--transition-base) var(--transition-function);
}

.slide-in-up {
  animation: slideInUp var(--transition-base) var(--transition-function);
}

.slide-in-down {
  animation: slideInDown var(--transition-base) var(--transition-function);
}

.scale-in {
  animation: scaleIn var(--transition-base) var(--transition-function);
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

.rotate {
  animation: rotate 1s linear infinite;
}

.bounce {
  animation: bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.shake {
  animation: shake 0.5s ease-in-out;
}
```

---
