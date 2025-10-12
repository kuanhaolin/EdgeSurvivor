<template>
  <div class="matches">
    <NavBar />
    
    <div class="matches-container">
      <el-page-header @back="goBack" content="旅伴媒合">
        <template #extra>
          <el-button type="success" @click="findMatches">
            <el-icon><Search /></el-icon>
            尋找旅伴
          </el-button>
        </template>
      </el-page-header>
      
      <!-- 篩選條件 -->
      <el-card class="filter-card">
        <el-form :inline="true">
          <el-form-item label="性別">
            <el-select v-model="filters.gender" placeholder="不限">
              <el-option label="不限" value="" />
              <el-option label="男性" value="male" />
              <el-option label="女性" value="female" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="年齡範圍">
            <el-slider
              v-model="filters.ageRange"
              range
              :min="18"
              :max="65"
              :step="1"
              show-stops
              style="width: 200px"
            />
          </el-form-item>
          
          <el-form-item label="地區">
            <el-input v-model="filters.location" placeholder="例如：台北" clearable />
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 媒合列表標籤頁 -->
      <el-tabs v-model="activeTab" class="matches-tabs">
        <!-- 推薦媒合 -->
        <el-tab-pane label="推薦媒合" name="recommended">
          <el-row :gutter="20">
            <el-col
              v-for="match in recommendedMatches"
              :key="match.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="match-card" shadow="hover">
                <div class="match-avatar">
                  <el-avatar :size="100" :src="match.avatar" />
                  <el-tag v-if="match.verified" type="success" size="small" class="verified-tag">
                    <el-icon><Select /></el-icon>
                    已驗證
                  </el-tag>
                </div>
                
                <div class="match-info">
                  <h3>{{ match.name }}</h3>
                  <div class="match-detail">
                    <el-icon><Location /></el-icon>
                    <span>{{ match.location }}</span>
                  </div>
                  <div class="match-detail">
                    <el-icon><User /></el-icon>
                    <span>{{ match.age }} 歲 · {{ getGenderText(match.gender) }}</span>
                  </div>
                  <p class="match-bio">{{ match.bio }}</p>
                  
                  <div class="match-tags">
                    <el-tag
                      v-for="interest in match.interests"
                      :key="interest"
                      size="small"
                      type="info"
                    >
                      {{ interest }}
                    </el-tag>
                  </div>
                </div>
                
                <template #footer>
                  <el-button-group style="width: 100%">
                    <el-button size="small" @click="viewProfile(match.id)">
                      查看資料
                    </el-button>
                    <el-button size="small" type="success" @click="sendMatchRequest(match.id)">
                      發送媒合
                    </el-button>
                  </el-button-group>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="recommendedMatches.length === 0" description="目前沒有推薦的旅伴" />
        </el-tab-pane>
        
        <!-- 待回應 -->
        <el-tab-pane label="待回應" name="pending">
          <el-table :data="pendingMatches" style="width: 100%">
            <el-table-column prop="name" label="姓名" width="150">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <el-avatar :size="40" :src="row.avatar" />
                  <span>{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="interests" label="興趣標籤" width="200">
              <template #default="{ row }">
                <div v-if="row.interests && row.interests.length > 0" style="display: flex; gap: 5px; flex-wrap: wrap;">
                  <el-tag
                    v-for="interest in row.interests.slice(0, 3)"
                    :key="interest"
                    size="small"
                    type="info"
                  >
                    {{ interest }}
                  </el-tag>
                  <el-tag v-if="row.interests.length > 3" size="small" type="info">
                    +{{ row.interests.length - 3 }}
                  </el-tag>
                </div>
                <span v-else class="text-secondary">未設定</span>
              </template>
            </el-table-column>
            <el-table-column prop="activity" label="活動" />
            <el-table-column prop="requestDate" label="申請時間" width="180" />
            <el-table-column prop="message" label="留言" show-overflow-tooltip />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button size="small" type="success" @click="acceptMatch(row.id)">
                  接受
                </el-button>
                <el-button size="small" type="danger" @click="rejectMatch(row.id)">
                  拒絕
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="pendingMatches.length === 0" description="沒有待回應的媒合請求" />
        </el-tab-pane>
        
        <!-- 已發送 -->
        <el-tab-pane label="已發送" name="sent">
          <el-table :data="sentMatches" style="width: 100%">
            <el-table-column prop="name" label="姓名" width="150">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <el-avatar :size="40" :src="row.avatar" />
                  <span>{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="interests" label="興趣標籤" width="200">
              <template #default="{ row }">
                <div v-if="row.interests && row.interests.length > 0" style="display: flex; gap: 5px; flex-wrap: wrap;">
                  <el-tag
                    v-for="interest in row.interests.slice(0, 3)"
                    :key="interest"
                    size="small"
                    type="info"
                  >
                    {{ interest }}
                  </el-tag>
                  <el-tag v-if="row.interests.length > 3" size="small" type="info">
                    +{{ row.interests.length - 3 }}
                  </el-tag>
                </div>
                <span v-else class="text-secondary">未設定</span>
              </template>
            </el-table-column>
            <el-table-column prop="activity" label="活動" />
            <el-table-column prop="requestDate" label="發送時間" width="180" />
            <el-table-column prop="status" label="狀態" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.status === 'pending'" type="warning">待回應</el-tag>
                <el-tag v-else-if="row.status === 'accepted'" type="success">已接受</el-tag>
                <el-tag v-else-if="row.status === 'rejected'" type="danger">已拒絕</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button 
                  v-if="row.status === 'pending'" 
                  size="small" 
                  type="danger" 
                  @click="cancelMatch(row.id)"
                >
                  取消
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="sentMatches.length === 0" description="還沒有發送過媒合請求" />
        </el-tab-pane>
        
        <!-- 已媒合 -->
        <el-tab-pane label="已媒合" name="matched">
          <el-row :gutter="20">
            <el-col
              v-for="match in matchedUsers"
              :key="match.id"
              :xs="24"
              :sm="12"
              :md="8"
            >
              <el-card class="matched-card">
                <div class="matched-header">
                  <el-avatar :size="60" :src="match.avatar" />
                  <div class="matched-user-info">
                    <h3>{{ match.name }}</h3>
                    <el-tag size="small" type="success">已媒合</el-tag>
                  </div>
                </div>
                
                <div class="matched-activity">
                  <div class="activity-label">共同活動</div>
                  <div class="activity-name">{{ match.activity }}</div>
                  <div class="activity-date">{{ match.activityDate }}</div>
                </div>
                
                <template #footer>
                  <el-button-group style="width: 100%">
                    <el-button size="small" @click="viewProfile(match.id)">
                      查看資料
                    </el-button>
                    <el-button size="small" type="primary" @click="goToChat(match.id)">
                      <el-icon><ChatLineRound /></el-icon>
                      聊天
                    </el-button>
                  </el-button-group>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="matchedUsers.length === 0" description="還沒有成功媒合的旅伴">
            <el-button type="success" @click="activeTab = 'recommended'">尋找旅伴</el-button>
          </el-empty>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 用戶資料對話框 -->
    <el-dialog
      v-model="showProfileDialog"
      title="用戶資料"
      width="500px"
    >
      <el-descriptions v-if="selectedUser" :column="1" border>
        <el-descriptions-item label="用戶名">
          {{ selectedUser.username }}
        </el-descriptions-item>
        <el-descriptions-item label="Email">
          {{ selectedUser.email }}
        </el-descriptions-item>
        <el-descriptions-item label="性別">
          {{ selectedUser.gender === 'male' ? '男' : selectedUser.gender === 'female' ? '女' : '其他' }}
        </el-descriptions-item>
        <el-descriptions-item label="年齡">
          {{ selectedUser.age || '未設定' }}
        </el-descriptions-item>
        <el-descriptions-item label="地點">
          {{ selectedUser.location || '未設定' }}
        </el-descriptions-item>
        <el-descriptions-item label="興趣標籤">
          <div v-if="selectedUser.interests && selectedUser.interests.length > 0" class="interest-tags">
            <el-tag
              v-for="interest in selectedUser.interests"
              :key="interest"
              size="small"
              type="info"
              style="margin: 2px;"
            >
              {{ interest }}
            </el-tag>
          </div>
          <span v-else class="text-secondary">未設定</span>
        </el-descriptions-item>
        <el-descriptions-item label="簡介">
          {{ selectedUser.bio || '這個用戶還沒有填寫簡介' }}
        </el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <el-button @click="showProfileDialog = false">關閉</el-button>
        <el-button type="primary" @click="goToChat(selectedUser.id); showProfileDialog = false">
          發送訊息
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  Location,
  User,
  Select,
  ChatLineRound
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

const router = useRouter()

const activeTab = ref('recommended')

// Dialog state
const showProfileDialog = ref(false)
const selectedUser = ref(null)

// 篩選條件
const filters = ref({
  gender: '',
  ageRange: [20, 40],
  location: ''
})

// 推薦媒合
const recommendedMatches = ref([])

// 待回應媒合
const pendingMatches = ref([])

// 已發送媒合
const sentMatches = ref([])

// 已媒合用戶
const matchedUsers = ref([])

// 載入推薦媒合
const loadRecommendedMatches = async () => {
  try {
    console.log('載入推薦媒合...')
    
    const response = await axios.get('/matches/recommended', {
      params: {
        gender: filters.value.gender,
        min_age: filters.value.ageRange[0],
        max_age: filters.value.ageRange[1],
        location: filters.value.location
      }
    })
    
    console.log('推薦媒合響應:', response.data)
    
    if (response.data && response.data.matches) {
      recommendedMatches.value = response.data.matches.map(match => ({
        id: match.user_id,
        name: match.name,
        age: match.age,
        gender: match.gender,
        location: match.location,
        bio: match.bio || '這個用戶還沒有填寫個人簡介',
        interests: match.interests || [],
        avatar: match.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        verified: match.is_verified || false
      }))
      
      console.log('推薦媒合列表:', recommendedMatches.value)
    }
  } catch (error) {
    console.error('載入推薦媒合失敗:', error)
    if (error.response?.status === 401) {
      ElMessage.error('登入已過期，請重新登入')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    } else {
      ElMessage.error('載入推薦媒合失敗')
    }
  }
}

// 載入待回應媒合
const loadPendingMatches = async () => {
  try {
    console.log('載入待回應媒合...')
    
    const response = await axios.get('/matches/pending')
    
    console.log('待回應媒合響應:', response.data)
    
    if (response.data && response.data.matches) {
      pendingMatches.value = response.data.matches.map(match => ({
        id: match.match_id,
        userId: match.requester.user_id,
        name: match.requester.name,
        avatar: match.requester.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        interests: match.requester.interests || [],
        activity: match.activity?.title || '一般媒合',
        requestDate: new Date(match.created_at).toLocaleString('zh-TW'),
        message: match.message || '希望能一起參加活動'
      }))
      
      console.log('待回應媒合列表:', pendingMatches.value)
    }
  } catch (error) {
    console.error('載入待回應媒合失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    }
  }
}

// 載入已發送媒合
const loadSentMatches = async () => {
  try {
    console.log('載入已發送媒合...')
    
    const response = await axios.get('/matches/sent')
    
    console.log('已發送媒合響應:', response.data)
    
    if (response.data && response.data.matches) {
      sentMatches.value = response.data.matches.map(match => ({
        id: match.match_id,
        userId: match.responder.user_id,
        name: match.responder.name,
        avatar: match.responder.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        interests: match.responder.interests || [],
        activity: match.activity?.title || '一般媒合',
        requestDate: new Date(match.created_at).toLocaleString('zh-TW'),
        status: match.status
      }))
      
      console.log('已發送媒合列表:', sentMatches.value)
    }
  } catch (error) {
    console.error('載入已發送媒合失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    }
  }
}

// 載入已媒合用戶
const loadMatchedUsers = async () => {
  try {
    console.log('載入已媒合用戶...')
    
    const response = await axios.get('/matches', {
      params: {
        status: 'accepted'
      }
    })
    
    console.log('已媒合用戶響應:', response.data)
    
    if (response.data && response.data.matches) {
      const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
      
      matchedUsers.value = response.data.matches.map(match => {
        const otherUser = match.requester_id === currentUserId 
          ? match.responder 
          : match.requester
        
        return {
          id: otherUser.user_id,
          name: otherUser.name,
          avatar: otherUser.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          interests: otherUser.interests || [],
          activity: match.activity?.title || '一般媒合',
          activityDate: match.activity?.start_date 
            ? new Date(match.activity.start_date).toLocaleDateString('zh-TW')
            : '待定'
        }
      })
      
      console.log('已媒合用戶列表:', matchedUsers.value)
    }
  } catch (error) {
    console.error('載入已媒合用戶失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    }
  }
}

// 載入所有媒合資料
const loadAllMatches = () => {
  loadRecommendedMatches()
  loadPendingMatches()
  loadSentMatches()
  loadMatchedUsers()
}

// 組件掛載時載入資料
onMounted(() => {
  loadAllMatches()
})

// 性別文字
const getGenderText = (gender) => {
  const texts = {
    male: '男性',
    female: '女性',
    other: '其他'
  }
  return texts[gender] || '未設定'
}

// 返回
const goBack = () => {
  router.back()
}

// 尋找旅伴
const findMatches = () => {
  loadRecommendedMatches()
  ElMessage.success('正在為您尋找合適的旅伴...')
}

// 查看個人資料
const viewProfile = async (id) => {
  try {
    const response = await axios.get(`/users/${id}`)
    
    if (response.data && response.data.user) {
      selectedUser.value = response.data.user
      showProfileDialog.value = true
    }
  } catch (error) {
    console.error('載入用戶資料失敗:', error)
    ElMessage.error('無法載入用戶資料')
  }
}

// 發送媒合請求
const sendMatchRequest = async (userId) => {
  try {
    console.log('發送媒合請求給用戶:', userId)
    
    const response = await axios.post('/matches', {
      responder_id: userId,
      activity_id: null,  // 一般媒合不綁定特定活動
      message: '希望能成為旅伴，一起探索世界！'
    })
    
    console.log('媒合請求響應:', response.data)
    
    ElMessage.success('媒合請求已發送！')
    // 從推薦列表中移除已發送請求的用戶
    recommendedMatches.value = recommendedMatches.value.filter(m => m.id !== userId)
  } catch (error) {
    console.error('發送媒合請求失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('發送媒合請求失敗')
    }
  }
}

// 接受媒合
const acceptMatch = async (matchId) => {
  try {
    console.log('接受媒合:', matchId)
    
    const response = await axios.put(`/matches/${matchId}/accept`)
    
    console.log('接受響應:', response.data)
    
    ElMessage.success('已接受媒合請求！')
    loadPendingMatches()
    loadMatchedUsers()
  } catch (error) {
    console.error('接受媒合失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('接受媒合失敗')
    }
  }
}

// 拒絕媒合
const rejectMatch = async (matchId) => {
  try {
    await ElMessageBox.confirm('確定要拒絕此媒合請求嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    console.log('拒絕媒合:', matchId)
    
    const response = await axios.put(`/matches/${matchId}/reject`)
    
    console.log('拒絕響應:', response.data)
    
    ElMessage.success('已拒絕媒合請求')
    loadPendingMatches()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒絕媒合失敗:', error)
      if (error.response?.data?.error) {
        ElMessage.error(error.response.data.error)
      } else {
        ElMessage.error('拒絕媒合失敗')
      }
    }
  }
}

// 取消媒合
const cancelMatch = async (matchId) => {
  try {
    await ElMessageBox.confirm('確定要取消此媒合請求嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    console.log('取消媒合:', matchId)
    
    const response = await axios.delete(`/matches/${matchId}`)
    
    console.log('取消響應:', response.data)
    
    ElMessage.success('已取消媒合請求')
    loadSentMatches()
    loadRecommendedMatches()  // 重新載入推薦列表
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消媒合失敗:', error)
      if (error.response?.data?.error) {
        ElMessage.error(error.response.data.error)
      } else {
        ElMessage.error('取消媒合失敗')
      }
    }
  }
}

// 前往聊天
const goToChat = (userId) => {
  router.push(`/chat?userId=${userId}`)
}
</script>

<style scoped>
.matches {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.matches-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filter-card {
  margin: 20px 0;
}

.matches-tabs {
  margin-top: 20px;
}

.match-card {
  margin-bottom: 20px;
  text-align: center;
}

.match-avatar {
  position: relative;
  margin-bottom: 15px;
}

.verified-tag {
  position: absolute;
  bottom: 0;
  right: 50%;
  transform: translateX(50%);
}

.match-info h3 {
  margin: 10px 0;
  font-size: 18px;
}

.match-detail {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.match-bio {
  margin: 15px 0;
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
  text-align: left;
}

.match-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: center;
  margin-top: 10px;
}

.matched-card {
  margin-bottom: 20px;
}

.matched-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.matched-user-info h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.matched-activity {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.activity-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.activity-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.activity-date {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .matches-container {
    padding: 10px;
  }
}
</style>
