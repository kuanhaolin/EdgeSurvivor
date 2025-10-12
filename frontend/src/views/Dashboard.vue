<template>
  <div class="dashboard">
    <NavBar />
    
    <div class="dashboard-container">
      <!-- 歡迎卡片 -->
      <el-card class="welcome-card">
        <template #header>
          <div class="card-header">
            <span>{{ welcomeMessage }}，{{ userName }}！</span>
            <el-tag :type="userStatus.type">{{ userStatus.text }}</el-tag>
          </div>
        </template>
        <div class="welcome-content">
          <p>準備好開始你的旅程了嗎？找到志同道合的旅伴，創造美好回憶！</p>
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
            <el-statistic title="媒合成功" :value="stats.matches">
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
            <el-statistic title="旅遊天數" :value="stats.travelDays" suffix="天">
              <template #prefix>
                <el-icon><Location /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 快速操作 -->
      <el-card class="quick-actions">
        <template #header>
          <span>快速操作</span>
        </template>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="6">
            <el-button type="primary" size="large" class="action-btn" @click="goToActivities">
              <el-icon><Plus /></el-icon>
              發布活動
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-button type="success" size="large" class="action-btn" @click="goToMatches">
              <el-icon><Search /></el-icon>
              尋找旅伴
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-button type="info" size="large" class="action-btn" @click="goToChat">
              <el-icon><ChatLineRound /></el-icon>
              查看訊息
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-button type="warning" size="large" class="action-btn" @click="goToProfile">
              <el-icon><User /></el-icon>
              編輯個人資料
            </el-button>
          </el-col>
        </el-row>
      </el-card>
      
      <!-- 最近活動 -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <el-card class="recent-card">
            <template #header>
              <span>最近的活動</span>
            </template>
            <el-empty v-if="recentActivities.length === 0" description="還沒有活動，趕快創建一個吧！">
              <el-button type="primary" @click="goToActivities">創建活動</el-button>
            </el-empty>
            <el-timeline v-else>
              <el-timeline-item
                v-for="activity in recentActivities"
                :key="activity.id"
                :timestamp="activity.date"
                placement="top"
              >
                <el-card>
                  <h4>{{ activity.title }}</h4>
                  <p>{{ activity.location }}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :md="12">
          <el-card class="recent-card">
            <template #header>
              <span>最新媒合</span>
            </template>
            <el-empty v-if="recentMatches.length === 0" description="還沒有媒合記錄">
              <el-button type="success" @click="goToMatches">尋找旅伴</el-button>
            </el-empty>
            <div v-else class="matches-list">
              <div v-for="match in recentMatches" :key="match.id" class="match-item">
                <el-avatar :src="match.avatar" />
                <div class="match-info">
                  <h4>{{ match.name }}</h4>
                  <p>{{ match.activity }}</p>
                </div>
                <el-tag :type="match.status === 'accepted' ? 'success' : 'warning'">
                  {{ match.statusText }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Calendar,
  UserFilled,
  ChatDotRound,
  Location,
  Plus,
  Search,
  ChatLineRound,
  User
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

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
const userStatus = computed(() => ({
  type: 'success',
  text: '已驗證'
}))

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
  travelDays: 0
})

// 最近的活動
const recentActivities = ref([])

// 最新媒合
const recentMatches = ref([])

// 載入用戶資訊
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
  
  // 從 API 載入實際數據
  loadDashboardData()
})

const loadDashboardData = async () => {
  try {
    // 載入統計數據
    const statsResponse = await axios.get('/users/stats')
    if (statsResponse.data && statsResponse.data.stats) {
      stats.value = statsResponse.data.stats
    }
    
    // 載入最近的活動
    const activitiesResponse = await axios.get('/users/recent-activities')
    if (activitiesResponse.data && activitiesResponse.data.activities) {
      recentActivities.value = activitiesResponse.data.activities.map(activity => ({
        id: activity.activity_id,
        title: activity.title,
        location: activity.location,
        date: formatDate(activity.date)
      }))
    }
    
    // TODO: 載入最新媒合數據
    // const matchesResponse = await axios.get('/users/recent-matches')
    
  } catch (error) {
    console.error('載入 Dashboard 數據失敗:', error)
    ElMessage.error('載入數據失敗')
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
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.welcome-content p {
  margin: 0;
  color: #606266;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  text-align: center;
}

.stat-card :deep(.el-statistic__head) {
  color: #909399;
  font-size: 14px;
}

.stat-card :deep(.el-statistic__content) {
  font-size: 28px;
  font-weight: bold;
}

.quick-actions {
  margin-bottom: 20px;
}

.action-btn {
  width: 100%;
  margin-bottom: 10px;
}

.recent-card {
  margin-bottom: 20px;
  min-height: 400px;
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

@media (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
  }
  
  .action-btn {
    font-size: 14px;
  }
}
</style>
