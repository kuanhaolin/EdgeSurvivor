<template>
  <div class="home">
    <!-- Hero 區域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title animate-slideInDown">
          <span class="gradient-text">EdgeSurvivor</span>
          <br />
          邊緣人神器
        </h1>
        <p class="hero-subtitle animate-fadeIn">
          🌍 不再獨自旅行，找到志同道合的旅伴
        </p>
        <p class="hero-description">
          一個專為獨自旅行者打造的社交平台<br />
          讓你輕鬆找到興趣相投的夥伴，一起探索世界
        </p>
        
        <div class="actions animate-slideInUp">
          <el-button type="primary" size="large" @click="goToLogin" class="primary-btn">
            <el-icon><UserFilled /></el-icon>
            立即開始冒險
          </el-button>
          <el-button size="large" @click="scrollToFeatures" class="secondary-btn">
            <el-icon><ArrowDown /></el-icon>
            了解更多
          </el-button>
        </div>
        
        <!-- 統計數據 -->
        <div class="stats">
          <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">活躍用戶</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">500+</div>
            <div class="stat-label">成功活動</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">城市覆蓋</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心功能介紹 -->
    <section ref="featuresSection" class="features-section">
      <div class="section-header">
        <h2 class="section-title">核心功能</h2>
        <p class="section-subtitle">四大核心功能，讓旅行更精彩</p>
      </div>
      
      <div class="features-grid">
        <div class="feature-card glass-card" v-for="(feature, index) in features" :key="index">
          <div class="feature-icon-wrapper">
            <div class="feature-icon">{{ feature.icon }}</div>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <ul class="feature-list">
            <li v-for="(item, i) in feature.items" :key="i">
              <el-icon color="#667eea"><Check /></el-icon>
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 使用流程 -->
    <section class="how-it-works-section">
      <div class="section-header">
        <h2 class="section-title">如何使用</h2>
        <p class="section-subtitle">簡單三步驟，開始你的冒險之旅</p>
      </div>
      
      <div class="steps-container">
        <div class="step-card" v-for="(step, index) in steps" :key="index">
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-icon">{{ step.icon }}</div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
        </div>
        
        <!-- 連接線 -->
        <div class="step-connector" v-if="index < steps.length - 1" :key="`connector-${index}`"></div>
      </div>
    </section>

    <!-- 使用案例 -->
    <section class="use-cases-section">
      <div class="section-header">
        <h2 class="section-title">適合你的場景</h2>
        <p class="section-subtitle">無論是什麼類型的活動，我們都能幫你找到夥伴</p>
      </div>
      
      <div class="use-cases-grid">
        <div class="use-case-card" v-for="(useCase, index) in useCases" :key="index">
          <div class="use-case-image">{{ useCase.emoji }}</div>
          <h3>{{ useCase.title }}</h3>
          <p>{{ useCase.description }}</p>
          <div class="use-case-tags">
            <el-tag v-for="(tag, i) in useCase.tags" :key="i" size="small">
              {{ tag }}
            </el-tag>
          </div>
        </div>
      </div>
    </section>

    <!-- 用戶評價 -->
    <section class="testimonials-section">
      <div class="section-header">
        <h2 class="section-title">用戶好評</h2>
        <p class="section-subtitle">看看其他旅行者怎麼說</p>
      </div>
      
      <div class="testimonials-grid">
        <div class="testimonial-card glass-card" v-for="(testimonial, index) in testimonials" :key="index">
          <div class="testimonial-header">
            <el-avatar :size="50" :src="testimonial.avatar">
              {{ testimonial.name[0] }}
            </el-avatar>
            <div class="testimonial-info">
              <div class="testimonial-name">{{ testimonial.name }}</div>
              <div class="testimonial-role">{{ testimonial.role }}</div>
            </div>
          </div>
          <div class="testimonial-rating">
            <el-icon v-for="i in 5" :key="i" color="#f59e0b"><StarFilled /></el-icon>
          </div>
          <p class="testimonial-content">"{{ testimonial.content }}"</p>
        </div>
      </div>
    </section>

    <!-- CTA 區域 -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>準備好開始你的冒險了嗎？</h2>
        <p>加入 EdgeSurvivor，找到你的旅行夥伴</p>
        <div class="cta-buttons">
          <el-button type="primary" size="large" @click="goToRegister" class="cta-btn">
            <el-icon><UserFilled /></el-icon>
            免費註冊
          </el-button>
          <el-button size="large" @click="goToLogin" class="cta-btn-secondary">
            已有帳號？立即登入
          </el-button>
        </div>
      </div>
    </section>

    <!-- 頁腳 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>EdgeSurvivor</h3>
          <p>邊緣人神器 - 你的旅伴媒合平台</p>
        </div>
        <div class="footer-section">
          <h4>快速連結</h4>
          <ul>
            <li><a @click="goToLogin">登入</a></li>
            <li><a @click="goToRegister">註冊</a></li>
            <li><a @click="scrollToFeatures">功能介紹</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>聯絡我們</h4>
          <ul>
            <li>📧 support@edgesurvivor.com</li>
            <li>📱 +886 912-345-678</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 EdgeSurvivor. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserFilled, ArrowDown, Check, StarFilled } from '@element-plus/icons-vue'

const router = useRouter()
const featuresSection = ref(null)

// 核心功能
const features = [
  {
    icon: '🎯',
    title: '活動創建與管理',
    description: '輕鬆創建你的旅行活動',
    items: [
      '自由設定活動時間、地點',
      '靈活管理參與人數',
      '多種活動類型選擇',
      '實時狀態更新'
    ]
  },
  {
    icon: '🤝',
    title: '智能媒合配對',
    description: '找到最適合的旅伴',
    items: [
      '興趣標籤智能匹配',
      '活動偏好分析',
      '參與者背景審核',
      '安全可靠的配對機制'
    ]
  },
  {
    icon: '💬',
    title: '即時聊天系統',
    description: '隨時隨地保持聯繫',
    items: [
      '實時訊息推送',
      '群組討論功能',
      '多媒體訊息支援',
      '已讀未讀狀態'
    ]
  },
  {
    icon: '📊',
    title: '活動追蹤管理',
    description: '掌握每個活動細節',
    items: [
      '費用分攤計算',
      '行程規劃工具',
      '參與者管理',
      '活動歷史記錄'
    ]
  }
]

// 使用步驟
const steps = [
  {
    icon: '📝',
    title: '註冊帳號',
    description: '快速註冊，填寫你的興趣和偏好，讓系統更了解你'
  },
  {
    icon: '🔍',
    title: '探索活動',
    description: '瀏覽其他用戶創建的活動，或者自己創建一個新活動'
  },
  {
    icon: '🎉',
    title: '開始冒險',
    description: '與志同道合的夥伴一起出發，創造美好回憶'
  }
]

// 使用案例
const useCases = [
  {
    emoji: '🏔️',
    title: '登山健行',
    description: '找到熱愛大自然的夥伴，一起征服高山',
    tags: ['戶外運動', '冒險', '健康']
  },
  {
    emoji: '🏕️',
    title: '露營野炊',
    description: '與露營愛好者分享篝火旁的美好時光',
    tags: ['露營', '野外', '團體活動']
  },
  {
    emoji: '✈️',
    title: '城市旅遊',
    description: '探索新城市，與當地人或旅行者交流',
    tags: ['旅遊', '文化', '美食']
  },
  {
    emoji: '🍜',
    title: '美食探索',
    description: '和吃貨們一起尋找隱藏的美味',
    tags: ['美食', '社交', '探店']
  },
  {
    emoji: '📸',
    title: '攝影外拍',
    description: '與攝影愛好者交流，捕捉精彩瞬間',
    tags: ['攝影', '藝術', '創作']
  },
  {
    emoji: '🎭',
    title: '文化體驗',
    description: '參加展覽、音樂會等文化活動',
    tags: ['文化', '藝術', '娛樂']
  }
]

// 用戶評價
const testimonials = [
  {
    name: '小明',
    role: '登山愛好者',
    avatar: '',
    content: '透過 EdgeSurvivor 找到了很多志同道合的山友，現在每個週末都有人一起爬山！'
  },
  {
    name: '小美',
    role: '旅遊達人',
    content: '這個平台讓我認識了好多有趣的朋友，一起去了很多想去但不敢獨自前往的地方。'
  },
  {
    name: '阿傑',
    role: '攝影師',
    content: '找到了很多攝影同好，現在每次外拍都不寂寞，還能互相學習技巧！'
  }
]

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  min-height: -webkit-fill-available; /* iOS Safari 修復 */
  background: var(--bg-primary);
  overflow-x: hidden;
}

/* ==================== Hero 區域 ==================== */
.hero-section {
  min-height: 100vh;
  min-height: -webkit-fill-available; /* iOS Safari 修復 */
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) var(--spacing-xl);
  padding-bottom: calc(var(--spacing-2xl) + env(safe-area-inset-bottom)); /* iOS 安全區域 */
  position: relative;
  overflow: hidden;
}

/* 背景動畫元素 */
.hero-section::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  top: -200px;
  right: -200px;
  animation: float 25s ease-in-out infinite;
}

.hero-section::after {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  bottom: -150px;
  left: -150px;
  animation: float 20s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(50px, -50px) rotate(120deg); }
  66% { transform: translate(-50px, 50px) rotate(240deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 900px;
}

.hero-title {
  font-size: 72px;
  font-weight: 800;
  color: white;
  margin-bottom: var(--spacing-md);
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-subtitle {
  font-size: 28px;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: var(--spacing-md);
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.hero-description {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: var(--spacing-xl);
  line-height: 1.8;
}

.actions {
  display: flex;
  gap: var(--spacing-lg);
  justify-content: center;
  margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}

.primary-btn {
  height: 56px;
  padding: 0 var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  background: white !important;
  color: var(--primary-color) !important;
  border: none !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
  /* iOS 觸控優化 */
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.primary-btn:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2) !important;
}

.secondary-btn {
  height: 56px;
  padding: 0 var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  border: 2px solid rgba(255, 255, 255, 0.3) !important;
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
  transform: translateY(-4px);
}

/* 統計數據 */
.stats {
  display: flex;
  justify-content: center;
  gap: var(--spacing-2xl);
  margin-top: var(--spacing-2xl);
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  padding: var(--spacing-lg);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 150px;
}

.stat-number {
  font-size: 48px;
  font-weight: 800;
  color: white;
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

/* ==================== 區塊通用樣式 ==================== */
section {
  padding: var(--spacing-2xl) var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  font-size: 42px;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--spacing-md);
}

.section-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
}

/* ==================== 核心功能區 ==================== */
.features-section {
  background: var(--bg-secondary);
  padding: var(--spacing-2xl) var(--spacing-xl);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.feature-card {
  padding: var(--spacing-xl);
  text-align: left;
  transition: all var(--transition-base);
  background: var(--bg-primary);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.feature-icon-wrapper {
  display: inline-block;
  margin-bottom: var(--spacing-md);
}

.feature-icon {
  font-size: 56px;
  animation: bounce 2s ease-in-out infinite;
}

.feature-card:nth-child(2) .feature-icon {
  animation-delay: 0.2s;
}

.feature-card:nth-child(3) .feature-icon {
  animation-delay: 0.4s;
}

.feature-card:nth-child(4) .feature-icon {
  animation-delay: 0.6s;
}

.feature-card h3 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.feature-card p {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) 0;
  color: var(--text-secondary);
  font-size: 15px;
}

/* ==================== 使用流程區 ==================== */
.how-it-works-section {
  background: var(--bg-primary);
}

.steps-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-xl);
  flex-wrap: wrap;
  position: relative;
}

.step-card {
  flex: 1;
  min-width: 250px;
  max-width: 320px;
  text-align: center;
  padding: var(--spacing-xl);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
  position: relative;
}

.step-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.step-number {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 48px;
  height: 48px;
  background: var(--gradient-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  box-shadow: var(--shadow-lg);
}

.step-icon {
  font-size: 64px;
  margin: var(--spacing-lg) 0;
}

.step-card h3 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.step-card p {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ==================== 使用案例區 ==================== */
.use-cases-section {
  background: var(--bg-secondary);
}

.use-cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.use-case-card {
  padding: var(--spacing-xl);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
  text-align: center;
}

.use-case-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.use-case-image {
  font-size: 72px;
  margin-bottom: var(--spacing-md);
}

.use-case-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.use-case-card p {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.use-case-tags {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
  justify-content: center;
}

/* ==================== 用戶評價區 ==================== */
.testimonials-section {
  background: var(--bg-primary);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.testimonial-card {
  padding: var(--spacing-xl);
  background: var(--bg-primary);
  transition: all var(--transition-base);
}

.testimonial-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.testimonial-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.testimonial-info {
  flex: 1;
}

.testimonial-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.testimonial-role {
  font-size: 14px;
  color: var(--text-secondary);
}

.testimonial-rating {
  margin-bottom: var(--spacing-md);
  display: flex;
  gap: 4px;
}

.testimonial-content {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.8;
  font-style: italic;
}

/* ==================== CTA 區域 ==================== */
.cta-section {
  background: var(--gradient-primary);
  padding: var(--spacing-2xl) var(--spacing-xl);
  text-align: center;
  color: white;
}

.cta-content h2 {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: var(--spacing-md);
}

.cta-content p {
  font-size: 20px;
  margin-bottom: var(--spacing-xl);
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: var(--spacing-lg);
  justify-content: center;
  flex-wrap: wrap;
}

.cta-btn {
  height: 56px;
  padding: 0 var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  background: white !important;
  color: var(--primary-color) !important;
  border: none !important;
}

.cta-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.cta-btn-secondary {
  height: 56px;
  padding: 0 var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  background: transparent !important;
  color: white !important;
  border: 2px solid white !important;
}

.cta-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  transform: translateY(-4px);
}

/* ==================== 頁腳 ==================== */
.footer {
  background: var(--bg-tertiary);
  padding: var(--spacing-2xl) var(--spacing-xl);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.footer-section h3 {
  font-size: 20px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--spacing-md);
}

.footer-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.footer-section p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: var(--spacing-xs);
  color: var(--text-secondary);
}

.footer-section a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition-fast);
  cursor: pointer;
}

.footer-section a:hover {
  color: var(--primary-color);
}

.footer-bottom {
  text-align: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  color: var(--text-secondary);
}

/* ==================== 響應式設計 ==================== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 42px;
  }
  
  .hero-subtitle {
    font-size: 20px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .actions,
  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .primary-btn,
  .secondary-btn,
  .cta-btn,
  .cta-btn-secondary {
    width: 100%;
  }
  
  .stats {
    gap: var(--spacing-md);
  }
  
  .stat-item {
    min-width: 120px;
  }
  
  .stat-number {
    font-size: 36px;
  }
  
  .steps-container {
    flex-direction: column;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  section {
    padding: var(--spacing-xl) var(--spacing-md);
  }
  
  .hero-section {
    padding: var(--spacing-xl) var(--spacing-md);
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .features-grid,
  .use-cases-grid,
  .testimonials-grid {
    grid-template-columns: 1fr;
  }
}
</style>
