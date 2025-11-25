<template>
  <div class="home">
    <!-- Hero 區域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title animate-slideInDown">
          <span class="gradient-text">EdgeSurvivor</span>
          <br />
          <span class="subtitle-text">你的旅伴媒合平台</span>
        </h1>
        <p class="hero-subtitle animate-fadeIn">
          ✈️ 不再獨自旅行，找到志同道合的旅伴
        </p>
        <p class="hero-description">
          一個專為熱愛旅行的你打造的社交平台<br />
          輕鬆找到興趣相投的夥伴，一起探索世界的美好
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
            <div class="stat-label">活躍旅人</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">500+</div>
            <div class="stat-label">精彩旅程</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">城市探索</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">滿意度</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心功能介紹 -->
    <section ref="featuresSection" class="features-section">
      <div class="section-content">
        <div class="section-header">
          <h2 class="section-title">為什麼選擇 EdgeSurvivor？</h2>
          <p class="section-subtitle">四大核心功能，讓你的每一次旅行都充滿驚喜</p>
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
      </div>
    </section>

    <!-- 使用流程 -->
    <section class="how-it-works-section">
      <div class="section-content">
        <div class="section-header">
          <h2 class="section-title">開始你的旅程</h2>
          <p class="section-subtitle">簡單四步驟，開啟精彩的旅行冒險</p>
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
      </div>
    </section>

    <!-- 使用案例 -->
    <section class="use-cases-section">
      <div class="section-content">
        <div class="section-header">
          <h2 class="section-title">探索各種旅行方式</h2>
          <p class="section-subtitle">無論你喜歡什麼樣的旅行風格，都能找到志同道合的夥伴</p>
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
      </div>
    </section>

    <!-- 用戶評價 -->
    <section class="testimonials-section">
      <div class="section-content">
        <div class="section-header">
          <h2 class="section-title">旅人們的真實分享</h2>
          <p class="section-subtitle">聽聽其他旅行者使用 EdgeSurvivor 的精彩體驗</p>
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
      </div>
    </section>

    <!-- CTA 區域 -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>準備好開始你的旅行冒險了嗎？</h2>
        <p>加入 EdgeSurvivor，找到志同道合的旅伴，一起探索世界的美好</p>
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
    icon: '🗺️',
    title: '探索精彩活動',
    description: '發現世界各地的旅行活動',
    items: [
      '瀏覽豐富的活動清單',
      '依興趣、地點篩選',
      '查看活動詳情與參與者',
      '一鍵加入心儀活動'
    ]
  },
  {
    icon: '✈️',
    title: '創建你的旅程',
    description: '發起專屬的旅行活動',
    items: [
      '自由規劃行程路線',
      '設定活動時間與地點',
      '邀請志同道合的夥伴',
      '管理活動參與者'
    ]
  },
  {
    icon: '🤝',
    title: '智能旅伴配對',
    description: '找到最適合的旅行夥伴',
    items: [
      '興趣標籤智能匹配',
      '個人資料完整展示',
      '評價系統建立信任',
      '安全可靠的配對機制'
    ]
  },
  {
    icon: '💬',
    title: '即時溝通協調',
    description: '與旅伴保持緊密聯繫',
    items: [
      '即時聊天功能',
      '活動討論區',
      '行程規劃協作',
      '費用分攤透明化'
    ]
  }
]

// 使用步驟
const steps = [
  {
    icon: '📝',
    title: '註冊成為會員',
    description: '快速註冊，完善個人資料，分享你的旅行興趣和偏好'
  },
  {
    icon: '🔍',
    title: '探索或創建活動',
    description: '瀏覽豐富的旅行活動，或發起屬於你的專屬旅程'
  },
  {
    icon: '🤝',
    title: '找到理想旅伴',
    description: '透過智能配對找到志同道合的夥伴，建立信任關係'
  },
  {
    icon: '🎉',
    title: '開始精彩旅程',
    description: '與新朋友一起出發，創造難忘的旅行回憶'
  }
]

// 使用案例
const useCases = [
  {
    emoji: '🏔️',
    title: '登山健行',
    description: '找到熱愛大自然的夥伴，一起征服高山，欣賞絕美風景',
    tags: ['戶外運動', '冒險', '健康']
  },
  {
    emoji: '🏕️',
    title: '露營野炊',
    description: '與露營愛好者分享篝火旁的美好時光，體驗野外生活',
    tags: ['露營', '野外', '團體活動']
  },
  {
    emoji: '✈️',
    title: '城市旅遊',
    description: '探索新城市，與當地人或旅行者交流，深度體驗在地文化',
    tags: ['旅遊', '文化', '美食']
  },
  {
    emoji: '🏖️',
    title: '海島度假',
    description: '尋找一起享受陽光、沙灘、海浪的旅伴',
    tags: ['海島', '度假', '放鬆']
  },
  {
    emoji: '🍜',
    title: '美食探索',
    description: '和吃貨們一起尋找隱藏的美味，品嚐各地特色料理',
    tags: ['美食', '社交', '探店']
  },
  {
    emoji: '📸',
    title: '攝影旅行',
    description: '與攝影愛好者一起捕捉世界各地的精彩瞬間',
    tags: ['攝影', '藝術', '創作']
  }
]

// 用戶評價
const testimonials = [
  {
    name: '小明',
    role: '登山愛好者',
    avatar: '',
    content: '透過 EdgeSurvivor 找到了很多志同道合的山友，現在每個週末都有人一起爬山！一起征服了玉山、雪山等台灣百岳，每次旅程都充滿歡笑。'
  },
  {
    name: '小美',
    role: '旅遊達人',
    avatar: '',
    content: '這個平台讓我認識了好多有趣的朋友，一起去了日本、韓國、泰國等國家。每次旅行都因為有旅伴而變得更加精彩，也省了不少住宿和交通費用！'
  },
  {
    name: '阿傑',
    role: '攝影師',
    avatar: '',
    content: '找到了很多攝影同好，現在每次外拍都不寂寞，還能互相學習技巧！我們一起去了很多絕美的攝影景點，拍出了許多令人驚艷的作品。'
  },
  {
    name: '小華',
    role: '美食愛好者',
    avatar: '',
    content: '最愛和旅伴們一起探索各地美食！透過平台認識了同樣熱愛美食的朋友，一起品嚐了無數道地料理，每次旅行都像是一場美食冒險。'
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
  width: 100%;
  margin: 0;
  padding: 0;
}

/* ==================== Hero 區域 ==================== */
.hero-section {
  min-height: 100vh;
  min-height: -webkit-fill-available; /* iOS Safari 修復 */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) var(--spacing-xl);
  padding-bottom: calc(var(--spacing-2xl) + env(safe-area-inset-bottom)); /* iOS 安全區域 */
  position: relative;
  overflow: hidden;
  width: 100%;
  margin: 0;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
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
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
}

.hero-title {
  font-size: 72px;
  font-weight: 800;
  color: white;
  margin-bottom: var(--spacing-md);
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.subtitle-text {
  font-size: 48px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
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
  align-items: center;
  margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}

.primary-btn {
  height: 56px;
  min-width: 200px;
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
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.primary-btn:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2) !important;
}

.secondary-btn {
  height: 56px;
  min-width: 200px;
  padding: 0 var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  border: 2px solid rgba(255, 255, 255, 0.3) !important;
  backdrop-filter: blur(10px);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
  transform: translateY(-4px);
}

/* 統計數據 */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-2xl);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.stat-item {
  text-align: center;
  padding: var(--spacing-lg);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  border-radius: var(--radius-lg);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  min-width: 150px;
}

.stat-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
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
  width: 100%;
  margin: 0 auto;
}

/* 內容容器限制寬度 */
.section-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
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
  width: 100%;
  margin: 0;
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
  width: 100%;
  margin: 0;
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  position: relative;
  width: 100%;
}

.step-card {
  text-align: center;
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
  position: relative;
  border: 2px solid transparent;
}

.step-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border-color: #667eea;
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
}

.step-number {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  border: 3px solid white;
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
  width: 100%;
  margin: 0;
}

.use-cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.use-case-card {
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: var(--radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all var(--transition-base);
  text-align: center;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.use-case-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
  background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
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
  width: 100%;
  margin: 0;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  padding: var(--spacing-2xl) var(--spacing-xl);
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  width: 100%;
  margin: 0;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h100v100H0z" fill="none"/><path d="M20 20h60v60H20z" fill="rgba(255,255,255,0.05)"/></svg>');
  opacity: 0.3;
}

.cta-content {
  position: relative;
  z-index: 1;
}

.cta-content h2 {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: var(--spacing-md);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
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
  width: 100%;
  margin: 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  width: 100%;
  padding: 0 var(--spacing-xl);
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
