<template>
  <div class="matches">
    <NavBar />
    
    <div class="matches-container">
      <el-page-header @back="goBack" content="旅伴交友">
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
          
          <el-form-item label="興趣">
            <el-select
              v-model="filters.interests"
              multiple
              filterable
              allow-create
              default-first-option
              placeholder="選擇或輸入興趣"
              style="min-width: 260px"
            >
              <el-option
                v-for="interest in commonInterests"
                :key="interest"
                :label="interest"
                :value="interest"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-switch v-model="filters.verifiedOnly" inline-prompt active-text="只看已驗證" />
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 交友列表標籤頁 -->
      <el-tabs v-model="activeTab" class="matches-tabs">
        <!-- 推薦交友 -->
        <el-tab-pane label="推薦交友" name="recommended">
          <el-row :gutter="20">
            <el-col
              v-for="match in filteredRecommendedMatches"
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
                  
                  <!-- 社群帳號 -->
                  <div v-if="match.social_links" class="match-social-links">
                    <el-button
                      v-if="match.social_links.instagram"
                      circle
                      size="small"
                      style="background: #E4405F; color: white; border: none;"
                      @click.stop="openSocialLink(match.social_links.instagram)"
                      title="Instagram"
                    >
                      <el-icon :size="16"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M7.8,2H16.2C19.4,2 22,4.6 22,7.8V16.2A5.8,5.8 0 0,1 16.2,22H7.8C4.6,22 2,19.4 2,16.2V7.8A5.8,5.8 0 0,1 7.8,2M7.6,4A3.6,3.6 0 0,0 4,7.6V16.4C4,18.39 5.61,20 7.6,20H16.4A3.6,3.6 0 0,0 20,16.4V7.6C20,5.61 18.39,4 16.4,4H7.6M17.25,5.5A1.25,1.25 0 0,1 18.5,6.75A1.25,1.25 0 0,1 17.25,8A1.25,1.25 0 0,1 16,6.75A1.25,1.25 0 0,1 17.25,5.5M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9Z" /></svg></el-icon>
                    </el-button>
                    <el-button
                      v-if="match.social_links.facebook"
                      circle
                      size="small"
                      style="background: #1877F2; color: white; border: none;"
                      @click.stop="openSocialLink(match.social_links.facebook)"
                      title="Facebook"
                    >
                      <el-icon :size="16"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z" /></svg></el-icon>
                    </el-button>
                    <el-button
                      v-if="match.social_links.line"
                      circle
                      size="small"
                      style="background: #00B900; color: white; border: none;"
                      @click.stop="showUserLineQRCode(match)"
                      title="LINE"
                    >
                      <el-icon :size="16"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M19.365,9.863c.349,0,.698.025,1.041.083,0-5.094-5.098-9.233-11.381-9.233C3.75.713,0,4.853,0,9.948s3.75,9.235,8.988,9.235c1.031,0,2.025-.149,2.949-.43L19.373,24V18.048a6.644,6.644,0,0,0,2.065-4.784A6.618,6.618,0,0,0,19.365,9.863Z" /></svg></el-icon>
                    </el-button>
                    <el-button
                      v-if="match.social_links.twitter"
                      circle
                      size="small"
                      style="background: #000000; color: white; border: none;"
                      @click.stop="openSocialLink(match.social_links.twitter)"
                      title="Twitter (X)"
                    >
                      <el-icon :size="16"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.70,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z" /></svg></el-icon>
                    </el-button>
                    <div v-if="!match.social_links.instagram && !match.social_links.facebook && !match.social_links.line && !match.social_links.twitter" style="color: #909399; font-size: 12px; text-align: center;">
                      未公開/未綁定
                    </div>
                  </div>
                </div>
                
                <template #footer>
                  <el-button-group style="width: 100%">
                    <el-button size="small" @click="viewProfile(match.id)">
                      查看資料
                    </el-button>
                    <el-button size="small" type="success" @click="sendMatchRequest(match.id)">
                      發送交友
                    </el-button>
                  </el-button-group>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="filteredRecommendedMatches.length === 0" description="目前沒有符合條件的旅伴" />
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
          
          <el-empty v-if="pendingMatches.length === 0" description="沒有待回應的交友請求" />
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
          
          <el-empty v-if="sentMatches.length === 0" description="還沒有發送過交友請求" />
        </el-tab-pane>
        
        <!-- 已成為好友 -->
        <el-tab-pane label="已成為好友" name="matched">
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
                    <el-tag size="small" type="success">已成為好友</el-tag>
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
          
          <el-empty v-if="matchedUsers.length === 0" description="還沒有成為好友的旅伴">
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

    <!-- LINE QR Code 對話框 -->
    <el-dialog v-model="showLineQRDialog" :title="`${selectedLineUser?.name} 的 LINE`" width="400px" align-center>
      <div style="text-align: center;">
        <div id="matchLineQRCode" style="display: inline-block;"></div>
        <p style="margin-top: 20px; color: #606266;">
          掃描此 QR Code 加好友
        </p>
        <p style="color: #909399; font-size: 14px;">
          LINE ID: <strong>{{ selectedLineUser?.lineId }}</strong>
        </p>
      </div>
      <template #footer>
        <el-button type="primary" @click="showLineQRDialog = false">關閉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
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
const showLineQRDialog = ref(false)
const selectedLineUser = ref(null)

// 篩選條件
const filters = ref({
  gender: '',
  ageRange: [20, 40],
  location: '',
  interests: [],
  verifiedOnly: false
})

// 常見興趣清單（可自行擴充）
const commonInterests = [
  '登山', '露營', '健行', '旅遊', '攝影',
  '美食', '咖啡', '閱讀', '電影', '音樂',
  '運動', '健身', '跑步', '游泳', '瑜伽',
  '烹飪', '烘焙', '繪畫', '寫作'
]

// 推薦媒合（原始資料）
const recommendedMatches = ref([])

// 依前端條件進行即時篩選
const filteredRecommendedMatches = computed(() => {
  const gender = filters.value.gender
  const [minAge, maxAge] = filters.value.ageRange || [18, 65]
  const location = (filters.value.location || '').toLowerCase()
  const interests = filters.value.interests || []
  const verifiedOnly = !!filters.value.verifiedOnly

  return recommendedMatches.value.filter((m) => {
    if (gender && m.gender !== gender) return false
    if (typeof m.age === 'number') {
      if (m.age < minAge || m.age > maxAge) return false
    }
    if (location && !(m.location || '').toLowerCase().includes(location)) return false
    if (verifiedOnly && !m.verified) return false
    if (interests.length > 0) {
      const set = new Set((m.interests || []).map(String))
      const hasAny = interests.some((i) => set.has(String(i)))
      if (!hasAny) return false
    }
    return true
  })
})

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
        location: filters.value.location,
        interests: filters.value.interests,
        verified_only: filters.value.verifiedOnly
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
        verified: match.is_verified || false,
        social_links: match.social_links || null
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
const viewProfile = (id) => {
  // 導航到用戶資料頁面
  router.push(`/user/${id}`)
}

// 發送媒合請求
const sendMatchRequest = async (userId) => {
  try {
    console.log('發送交友請求給用戶:', userId)
    
    const response = await axios.post('/matches', {
      responder_id: userId,
      activity_id: null,  // 一般交友不綁定特定活動
      message: '希望能成為旅伴，一起探索世界！'
    })
    
    console.log('交友請求響應:', response.data)
    
    ElMessage.success('交友請求已發送！')
    // 從推薦列表中移除已發送請求的用戶
    recommendedMatches.value = recommendedMatches.value.filter(m => m.id !== userId)
  } catch (error) {
    console.error('發送交友請求失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('發送交友請求失敗')
    }
  }
}

// 接受交友
const acceptMatch = async (matchId) => {
  try {
    console.log('接受交友:', matchId)
    
    const response = await axios.put(`/matches/${matchId}/accept`)
    
    console.log('接受響應:', response.data)
    
    ElMessage.success('已接受交友請求！')
    loadPendingMatches()
    loadMatchedUsers()
  } catch (error) {
    console.error('接受交友失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('接受交友失敗')
    }
  }
}

// 拒絕交友
const rejectMatch = async (matchId) => {
  try {
    await ElMessageBox.confirm('確定要拒絕此交友請求嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    console.log('拒絕交友:', matchId)
    
    const response = await axios.put(`/matches/${matchId}/reject`)
    
    console.log('拒絕響應:', response.data)
    
    ElMessage.success('已拒絕交友請求')
    loadPendingMatches()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒絕交友失敗:', error)
      if (error.response?.data?.error) {
        ElMessage.error(error.response.data.error)
      } else {
        ElMessage.error('拒絕交友失敗')
      }
    }
  }
}

// 取消交友
const cancelMatch = async (matchId) => {
  try {
    await ElMessageBox.confirm('確定要取消此交友請求嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    console.log('取消交友:', matchId)
    
    const response = await axios.delete(`/matches/${matchId}`)
    
    console.log('取消響應:', response.data)
    
    ElMessage.success('已取消交友請求')
    loadSentMatches()
    loadRecommendedMatches()  // 重新載入推薦列表
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消交友失敗:', error)
      if (error.response?.data?.error) {
        ElMessage.error(error.response.data.error)
      } else {
        ElMessage.error('取消交友失敗')
      }
    }
  }
}

// 前往聊天
const goToChat = (userId) => {
  router.push(`/chat?userId=${userId}`)
}

// 打開社群連結
const openSocialLink = (url) => {
  if (url) {
    const fullUrl = url.startsWith('http') ? url : `https://${url}`
    window.open(fullUrl, '_blank')
  }
}

// 顯示用戶 LINE QR Code
const showUserLineQRCode = (user) => {
  if (!user.social_links?.line) {
    ElMessage.warning('該用戶未綁定 LINE')
    return
  }
  
  selectedLineUser.value = {
    name: user.name,
    lineId: user.social_links.line
  }
  showLineQRDialog.value = true
  
  setTimeout(() => {
    generateMatchLineQRCode()
  }, 100)
}

// 生成 LINE QR Code (for Matches page)
const generateMatchLineQRCode = () => {
  const container = document.getElementById('matchLineQRCode')
  if (!container) return
  
  container.innerHTML = ''
  
  const lineUrl = `https://line.me/ti/p/${encodeURIComponent(selectedLineUser.value.lineId)}`
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(lineUrl)}`
  
  const img = document.createElement('img')
  img.src = qrCodeUrl
  img.alt = 'LINE QR Code'
  img.style.maxWidth = '100%'
  
  container.appendChild(img)
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

.match-social-links {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.match-social-links .el-button {
  transition: transform 0.2s, box-shadow 0.2s;
}

.match-social-links .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
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
