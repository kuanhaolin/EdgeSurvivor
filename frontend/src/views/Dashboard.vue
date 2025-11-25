<template>
  <div class="dashboard">
    <NavBar />
    
    <div class="dashboard-container">
      <!-- 歡迎卡片 -->
      <el-card class="welcome-card">
        <div class="welcome-card-content">
          <div class="welcome-left">
            <h1 class="welcome-title">{{ welcomeMessage }}，{{ userName }}！</h1>
            <p class="welcome-text">準備好開始你的旅程了嗎？找到志同道合的旅伴，創造美好回憶！</p>
          </div>
          <div class="welcome-right">
            <el-tag :type="userStatus.type" class="status-tag" size="large">
              <el-icon><Check v-if="userStatus.type === 'success'" /><Warning v-else /></el-icon>
              {{ userStatus.text }}
            </el-tag>
          </div>
        </div>
      </el-card>
      
      <!-- 統計卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <el-statistic title="我的活動" :value="stats.activities">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <el-statistic title="好友數量" :value="stats.matches">
              <template #prefix>
                <el-icon><UserFilled /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <el-statistic title="未讀訊息" :value="stats.unreadMessages">
              <template #prefix>
                <el-icon><ChatDotRound /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <el-statistic title="評價次數" :value="stats.reviews">
              <template #prefix>
                <el-icon><Star /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 快捷功能 -->
      <el-card class="quick-actions">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>快捷功能</span>
            <el-button type="primary" size="small" @click="goToActivities">
              <el-icon><Plus /></el-icon>
              發布新活動
            </el-button>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8">
            <el-button type="primary" size="large" class="action-btn" @click="goToActivities">
              <el-icon><Calendar /></el-icon>
              我的活動
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-button type="success" size="large" class="action-btn" @click="goToMatches">
              <el-icon><Search /></el-icon>
              尋找旅伴
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-button type="info" size="large" class="action-btn" @click="goToChat">
              <el-icon><ChatLineRound /></el-icon>
              查看訊息
            </el-button>
          </el-col>
        </el-row>
      </el-card>
      
      <!-- 最近活動 -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <el-card class="recent-card">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>最近的活動</span>
                <el-button type="text" size="small" @click="showCalendarDialog = true">
                  <el-icon><Calendar /></el-icon>
                  查看行事曆
                </el-button>
              </div>
            </template>
            <el-empty v-if="recentActivities.length === 0" description="還沒有活動，趕快創建一個吧！">
              <el-button type="primary" @click="goToActivities">創建活動</el-button>
            </el-empty>
            <div v-else class="activities-list">
              <div
                v-for="activity in recentActivities.slice(0, 5)"
                :key="activity.id"
                class="activity-item"
                @click="viewActivity(activity.id)"
              >
                <div class="activity-date-badge">
                  <div class="date-month">{{ getMonth(activity.startDate) }}</div>
                  <div class="date-day">{{ getDay(activity.startDate) }}</div>
                </div>
                <div class="activity-content">
                  <h4>{{ activity.title }}</h4>
                  <p class="activity-date-range">
                    <el-icon><Calendar /></el-icon>
                    {{ formatDateRange(activity.startDate, activity.endDate, activity.startTime, activity.endTime) }}
                  </p>
                  <p>
                    <el-icon><Location /></el-icon>
                    {{ activity.location }}
                  </p>
                </div>
                <el-icon class="activity-arrow"><ArrowRight /></el-icon>
              </div>
              <div v-if="recentActivities.length > 5" class="view-more-activities" @click="showCalendarDialog = true">
                查看全部 {{ recentActivities.length }} 個活動
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :md="12">
          <el-card class="recent-card">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>收到的評價</span>
                <el-button 
                  v-if="userReviews.length > 0" 
                  type="text" 
                  size="small"
                  @click="showReviewsDialog = true"
                >
                  查看全部
                </el-button>
              </div>
            </template>
            <el-empty v-if="userReviews.length === 0" description="還沒有收到任何評價">
              <el-button type="success" @click="goToActivities">參與活動</el-button>
            </el-empty>
            <div v-else class="reviews-preview">
              <div 
                v-for="review in userReviews.slice(0, 3)" 
                :key="review.review_id" 
                class="review-item"
                @click="showReviewsDialog = true"
              >
                <el-avatar :size="40" :src="review.reviewer?.avatar" />
                <div class="review-content">
                  <div class="review-header">
                    <strong>{{ review.reviewer?.name || '匿名' }}</strong>
                    <el-rate
                      :model-value="review.rating"
                      disabled
                      size="small"
                      style="margin-left: 8px;"
                    />
                  </div>
                  <p class="review-comment">{{ review.comment }}</p>
                  <span class="review-date">{{ formatDate(review.created_at) }}</span>
                </div>
              </div>
              <div v-if="userReviews.length > 3" class="view-more" @click="showReviewsDialog = true">
                查看全部 {{ userReviews.length }} 則評價
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 評價詳情對話框 -->
    <el-dialog 
      v-model="showReviewsDialog" 
      title="收到的評價" 
      width="700px"
    >
      <div v-if="loadingReviews" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" :size="30"><Loading /></el-icon>
        <p>載入評價中...</p>
      </div>
      <el-space v-else direction="vertical" style="width: 100%" :size="15">
        <el-card
          v-for="review in userReviews"
          :key="review.review_id"
          shadow="hover"
          class="review-card"
        >
          <div class="review-header-full">
            <div class="reviewer-info-full">
              <el-avatar :size="50" :src="review.reviewer?.avatar">
                {{ review.reviewer?.name?.charAt(0) }}
              </el-avatar>
              <div class="reviewer-details-full">
                <strong>{{ review.reviewer?.name || '匿名' }}</strong>
                <div style="font-size: 12px; color: #909399; margin-top: 2px;">
                  {{ review.activity?.title || '一般評價' }}
                </div>
              </div>
            </div>
            <div class="review-rating-full">
              <el-rate
                :model-value="review.rating"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value} 分"
              />
              <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                {{ formatDate(review.created_at) }}
              </div>
            </div>
          </div>
          <div class="review-comment-full" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ebeef5;">
            {{ review.comment }}
          </div>
        </el-card>
      </el-space>
      <el-empty v-if="!loadingReviews && userReviews.length === 0" description="還沒有收到任何評價" />
      <template #footer>
        <el-button @click="showReviewsDialog = false">關閉</el-button>
      </template>
    </el-dialog>
    
    <!-- 行事曆對話框 -->
    <el-dialog 
      v-model="showCalendarDialog" 
      title="活動行事曆" 
      width="800px"
    >
      <el-calendar v-model="calendarDate">
        <template #date-cell="{ data }">
          <div class="calendar-cell">
            <div class="calendar-date">{{ data.day.split('-').slice(2).join('-') }}</div>
            <div class="calendar-events">
              <div
                v-for="activity in getActivitiesForDate(data.day)"
                :key="activity.id"
                class="calendar-event"
                @click.stop="viewActivity(activity.id)"
              >
                {{ activity.title }}
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
      <template #footer>
        <el-button @click="showCalendarDialog = false">關閉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Calendar,
  UserFilled,
  ChatDotRound,
  Star,
  Plus,
  Search,
  ChatLineRound,
  User,
  Loading,
  Location,
  ArrowRight,
  Check,
  Warning
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'
import socketService from '@/services/socket'

const router = useRouter()

// 用戶資訊
const user = ref(null)
const userName = computed(() => {
  if (!user.value) return '旅行者'
  // 優先使用 name，如果沒有則使用 email 的前半部分
  if (user.value.name && user.value.name !== '用戶') {
    return user.value.name
  }
  // 從 email 提取用戶名（@ 之前的部分）
  if (user.value.email) {
    return user.value.email.split('@')[0]
  }
  return '旅行者'
})

const userStatus = computed(() => {
  if (!user.value) {
    return {
      type: 'info',
      text: '未登入'
    }
  }
  
  // 檢查 email 驗證狀態（使用後端的 is_verified 欄位）
  if (user.value.is_verified === false || user.value.is_verified === 0) {
    return {
      type: 'warning',
      text: '未驗證'
    }
  }
  
  return {
    type: 'success',
    text: '已驗證'
  }
})

// 根據時間顯示不同的歡迎訊息
const welcomeMessage = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 12) return '早安'
  if (hour < 18) return '午安'
  if (hour < 22) return '晚安'
  return '夜深了'
})

// 統計數據
const stats = ref({
  activities: 0,
  matches: 0,
  unreadMessages: 0,
  travelDays: 0,
  reviews: 0
})

// 最近的活動
const recentActivities = ref([])

// 最新媒合
const recentMatches = ref([])

// 評價相關
const userReviews = ref([])
const showReviewsDialog = ref(false)
const loadingReviews = ref(false)

// 行事曆相關
const showCalendarDialog = ref(false)
const calendarDate = ref(new Date())

// 載入用戶資訊
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
  
  // 從 API 載入實際數據
  loadDashboardData()
  
  // 連接 Socket.IO 並監聽新訊息
  socketService.connect()
  
  // 監聽新訊息事件
  socketService.onNewMessage((message) => {
    // 當收到新訊息時，重新載入未讀數量
    const currentUserId = user.value?.user_id
    if (currentUserId && message.receiver_id === currentUserId) {
      loadUnreadCount()
    }
  })
  
  // 監聽訊息已讀事件（如果有實作）
  if (socketService.socket) {
    socketService.socket.on('message_read', () => {
      loadUnreadCount()
    })
  }
})

// 清理
onUnmounted(() => {
  // 移除監聽器
  if (socketService.socket) {
    socketService.socket.off('message_read')
  }
})

const loadDashboardData = async () => {
  try {
    // 載入統計數據
    const statsResponse = await axios.get('/users/stats')
    if (statsResponse.data && statsResponse.data.stats) {
      stats.value = statsResponse.data.stats
    }
    
    // 載入未讀訊息數量
    await loadUnreadCount()
    
    // 載入最近的活動
    const activitiesResponse = await axios.get('/users/recent-activities')
    if (activitiesResponse.data && activitiesResponse.data.activities) {
      recentActivities.value = activitiesResponse.data.activities.map(activity => ({
        id: activity.activity_id,
        title: activity.title,
        location: activity.location,
        startDate: activity.start_date || activity.date || activity.created_at,
        endDate: activity.end_date || activity.start_date || activity.date || activity.created_at,
        startTime: activity.start_time,
        endTime: activity.end_time,
        rawDate: activity.start_date || activity.date || activity.created_at
      }))
      
      // 確保按時間由新到舊排序
      recentActivities.value.sort((a, b) => {
        return new Date(b.startDate) - new Date(a.startDate)
      })
    }
    
    // TODO: 載入最新媒合數據
    // const matchesResponse = await axios.get('/users/recent-matches')
    
    // 載入評價列表
    await loadUserReviews()
    
  } catch (error) {
    console.error('載入 Dashboard 數據失敗:', error)
    ElMessage.error('載入數據失敗')
  }
}

// 載入使用者評價列表
const loadUserReviews = async () => {
  try {
    loadingReviews.value = true
    const userStr = localStorage.getItem('user')
    if (!userStr) return
    
    const currentUser = JSON.parse(userStr)
    const userId = currentUser.user_id
    
    const response = await axios.get(`/users/${userId}/reviews`)
    
    if (response.data && response.data.reviews) {
      userReviews.value = response.data.reviews
    }
  } catch (error) {
    console.error('載入評價列表失敗:', error)
  } finally {
    loadingReviews.value = false
  }
}

// 載入未讀訊息數量
const loadUnreadCount = async () => {
  try {
    const response = await axios.get('/chat/unread-count')
    if (response.data) {
      stats.value.unreadMessages = response.data.unread_count || 0
    }
  } catch (error) {
    console.error('載入未讀訊息數量失敗:', error)
  }
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 導航功能
const goToActivities = () => {
  router.push('/activities')
}

const goToMatches = () => {
  router.push('/matches')
}

const goToChat = () => {
  router.push('/chat')
}

const goToProfile = () => {
  router.push('/profile')
}

// 查看活動詳情
const viewActivity = (id) => {
  router.push(`/activities/${id}`)
}

// 格式化日期區間
const formatDateRange = (startDate, endDate, startTime, endTime) => {
  if (!startDate) return ''
  
  const start = new Date(startDate)
  const end = new Date(endDate)
  
  // 使用獨立的時間欄位
  const hasTime = startTime || endTime
  
  // 如果開始和結束是同一天
  if (start.toDateString() === end.toDateString()) {
    const dateStr = `${start.getMonth() + 1}/${start.getDate()}`
    if (hasTime && startTime !== endTime) {
      return `${dateStr} ${startTime || '00:00'}-${endTime || '23:59'}`
    }
    return dateStr
  }
  
  // 如果同一個月
  if (start.getMonth() === end.getMonth() && start.getFullYear() === end.getFullYear()) {
    const monthStr = `${start.getMonth() + 1}月`
    if (hasTime) {
      return `${monthStr}${start.getDate()}日 ${startTime || '00:00'} - ${end.getDate()}日 ${endTime || '23:59'}`
    }
    return `${monthStr}${start.getDate()}-${end.getDate()}日`
  }
  
  // 不同月份
  const startStr = `${start.getMonth() + 1}/${start.getDate()}`
  const endStr = `${end.getMonth() + 1}/${end.getDate()}`
  if (hasTime) {
    return `${startStr} ${startTime || '00:00'} - ${endStr} ${endTime || '23:59'}`
  }
  return `${startStr} - ${endStr}`
}

// 格式化日期 - 獲取日期
const getDay = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.getDate()
}

// 格式化日期 - 獲取月份（數字）
const getMonth = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getMonth() + 1}月`
}

// 獲取指定日期的活動
const getActivitiesForDate = (dateStr) => {
  return recentActivities.value.filter(activity => {
    if (!activity.startDate || !activity.endDate) return false
    
    const date = new Date(dateStr)
    const start = new Date(activity.startDate)
    const end = new Date(activity.endDate)
    
    // 設定時間為 0 點以便比較日期
    date.setHours(0, 0, 0, 0)
    start.setHours(0, 0, 0, 0)
    end.setHours(0, 0, 0, 0)
    
    // 檢查日期是否在活動區間內
    return date >= start && date <= end
  })
}
</script>

<style scoped>
/* 全局卡片樣式 */
:deep(.el-card) {
  border-radius: 16px !important;
  border: none !important;
}

:deep(.el-card__header) {
  padding: 18px 20px !important;
}

:deep(.el-card__body) {
  padding: 20px !important;
}

/* 歡迎卡片特殊樣式優先 */
.welcome-card :deep(.el-card) {
  overflow: visible !important;
}

.dashboard {
  min-height: 100vh;
  min-height: -webkit-fill-available;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf1 50%, #dfe4ea 100%);
  width: 100%;
  position: relative;
  overflow-x: hidden;
}

.dashboard::before {
  content: '';
  position: fixed;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 15s ease-in-out infinite;
  pointer-events: none;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  50% {
    transform: translate(-50px, 50px) rotate(180deg);
  }
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: calc(20px + env(safe-area-inset-bottom)); /* iOS 安全區域 */
  flex: 1;
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden; /* 防止橫向滾動 */
  position: relative;
  z-index: 1;
  /* iOS 強制可見性 */
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateZ(0) !important;
  -webkit-transform: translateZ(0) !important;
}

.welcome-card {
  margin-bottom: 24px;
  opacity: 1 !important;
  visibility: visible !important;
  display: block !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.35) !important;
  border-radius: 20px !important;
  overflow: visible !important;
  position: relative;
  min-height: 140px;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: -30%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
  border-radius: 50%;
  pointer-events: none;
}

.welcome-card::after {
  content: '';
  position: absolute;
  bottom: -20%;
  left: -5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(240, 147, 251, 0.2) 0%, transparent 60%);
  border-radius: 50%;
  pointer-events: none;
}

.welcome-card :deep(.el-card__body) {
  background: transparent !important;
  padding: 32px 36px !important;
}

.welcome-card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  position: relative;
  z-index: 2;
}

.welcome-left {
  flex: 1;
}

.welcome-title {
  margin: 0 0 12px 0;
  font-size: 28px;
  font-weight: 800;
  color: white !important;
  line-height: 1.3;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.welcome-text {
  margin: 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.92) !important;
  line-height: 1.6;
  letter-spacing: 0.3px;
  font-weight: 400;
}

.welcome-right {
  display: flex;
  align-items: center;
}

.status-tag {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 2px solid rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  padding: 10px 20px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.status-tag.el-tag--success {
  color: #67c23a !important;
}

.status-tag.el-tag--warning {
  color: #e6a23c !important;
}

.status-tag.el-tag--info {
  color: #909399 !important;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  text-align: center;
  opacity: 1 !important;
  visibility: visible !important;
  border-radius: 16px;
  border: none;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
}

.stat-card:hover::before {
  transform: scaleX(1);
}

.stat-card :deep(.el-statistic__head) {
  color: #606266;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-card :deep(.el-statistic__content) {
  font-size: 32px !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}

.stat-card :deep(.el-icon) {
  font-size: 24px;
  margin-right: 8px;
  color: #667eea;
  transition: transform 0.3s ease;
}

.stat-card:hover :deep(.el-icon) {
  transform: scale(1.2) rotate(10deg);
}

.quick-actions {
  margin-bottom: 24px;
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: white;
}

.quick-actions :deep(.el-card__header) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(240, 147, 251, 0.05) 100%) !important;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1) !important;
  font-weight: 600 !important;
}

.action-btn {
  width: 100%;
  margin-bottom: 10px;
  height: 56px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  border: 2px solid;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.action-btn:hover::before {
  width: 400px;
  height: 400px;
}

.action-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.action-btn :deep(.el-icon) {
  font-size: 20px;
  margin-right: 8px;
  transition: transform 0.3s ease;
}

.action-btn:hover :deep(.el-icon) {
  transform: scale(1.15) rotate(5deg);
}

.recent-card {
  margin-bottom: 24px;
  min-height: 420px;
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: white;
  transition: all 0.3s ease;
}

.recent-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.recent-card :deep(.el-card__header) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(240, 147, 251, 0.05) 100%) !important;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1) !important;
  font-weight: 600 !important;
  font-size: 16px !important;
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.match-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  border-radius: 8px;
  background-color: #f5f7fa;
}

.match-info {
  flex: 1;
}

.match-info h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.match-info p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

/* 評價預覽樣式 */
.reviews-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-item {
  display: flex;
  gap: 14px;
  padding: 14px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(102, 126, 234, 0.08);
  position: relative;
  overflow: hidden;
}

.review-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #f093fb 0%, #f5576c 100%);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.review-item:hover {
  background: linear-gradient(135deg, #ffffff 0%, #f0f2f5 100%);
  transform: translateX(6px);
  box-shadow: 0 6px 20px rgba(240, 147, 251, 0.15);
  border-color: #f093fb;
}

.review-item:hover::before {
  transform: scaleY(1);
}

.review-content {
  flex: 1;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
}

.review-comment {
  margin: 6px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.review-date {
  font-size: 12px;
  color: #909399;
}

.view-more {
  text-align: center;
  padding: 14px;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(240, 147, 251, 0.05) 100%);
  border: 2px dashed rgba(102, 126, 234, 0.3);
}

.view-more:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(240, 147, 251, 0.12) 100%);
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

/* 評價詳情對話框樣式 */
.review-header-full {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.reviewer-info-full {
  display: flex;
  gap: 12px;
  align-items: center;
}

.reviewer-details-full strong {
  display: block;
  margin-bottom: 4px;
}

.review-rating-full {
  text-align: right;
}

.review-comment-full {
  color: #606266;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* 活動列表樣式 */
.activities-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(102, 126, 234, 0.1);
  position: relative;
  overflow: hidden;
}

.activity-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.activity-item:hover {
  background: linear-gradient(135deg, #ffffff 0%, #f0f2f5 100%);
  border-color: #667eea;
  transform: translateX(8px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.activity-item:hover::before {
  transform: scaleY(1);
}

.activity-date-badge {
  min-width: 68px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 14px;
  padding: 12px 10px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.activity-date-badge::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.activity-item:hover .activity-date-badge {
  transform: scale(1.05) rotate(-2deg);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.activity-item:hover .activity-date-badge::before {
  opacity: 1;
}

.date-month {
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}

.date-day {
  font-size: 26px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.5px;
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  margin: 0 0 6px 0;
  font-size: 16px;
  color: #303133;
}

.activity-content p {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 6px;
}

.activity-content p:last-child {
  margin-bottom: 0;
}

.activity-date-range {
  color: #667eea !important;
  font-weight: 500;
}

.activity-arrow {
  color: #909399;
  font-size: 20px;
  transition: all 0.3s ease;
}

.activity-item:hover .activity-arrow {
  color: #409eff;
  transform: translateX(4px);
}

.view-more-activities {
  text-align: center;
  padding: 16px;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  margin-top: 10px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(240, 147, 251, 0.03) 100%);
}

.view-more-activities:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
  border-color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
}

/* 行事曆樣式 */
.calendar-cell {
  height: 100%;
  min-height: 80px;
  padding: 4px;
}

.calendar-date {
  font-weight: 600;
  margin-bottom: 4px;
  color: #303133;
}

.calendar-events {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.calendar-event {
  font-size: 11px;
  padding: 2px 6px;
  background: #409eff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.calendar-event:hover {
  background: #337ecc;
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
    padding-bottom: calc(10px + env(safe-area-inset-bottom));
  }
  
  .welcome-card-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .welcome-text {
    font-size: 14px;
  }
  
  .welcome-right {
    width: 100%;
    justify-content: flex-start;
  }
  
  .action-btn {
    font-size: 14px;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .stats-row .el-col {
    margin-bottom: 10px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  /* iOS 優化 */
  .el-card {
    overflow: hidden;
  }
  
  .quick-actions .el-row .el-col {
    margin-bottom: 10px;
  }
}
</style>
