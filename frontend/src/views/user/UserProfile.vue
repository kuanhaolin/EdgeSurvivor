<template>
  <div class="user-profile">
    <NavBar />
    
    <div class="profile-container" v-if="!loading">
      <el-page-header @back="goBack" :content="userProfile.name + ' 的個人資料'" />
      
      <el-row :gutter="20" class="profile-row">
        <!-- 用戶資訊卡片 -->
        <el-col :xs="24" :md="8">
          <el-card class="profile-card">
            <div class="avatar-section">
              <el-avatar :size="120" :src="userProfile.avatar" />
            </div>
            
            <div class="user-basic-info">
              <h2>{{ userProfile.name }}</h2>
              <el-tag v-if="userProfile.verified" type="success">
                <el-icon><Select /></el-icon>
                已驗證
              </el-tag>
              <el-tag v-else type="info">未驗證</el-tag>
            </div>
            
            <el-descriptions :column="1" border class="user-details">
              <el-descriptions-item label="性別">
                {{ getGenderText(userProfile.gender) }}
              </el-descriptions-item>
              <el-descriptions-item label="年齡">
                {{ userProfile.age }} 歲
              </el-descriptions-item>
              <el-descriptions-item label="地區">
                {{ userProfile.location || '未設定' }}
              </el-descriptions-item>
              <el-descriptions-item label="加入時間">
                {{ userProfile.joinDate }}
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.activities }}</div>
                <div class="stat-label">活動</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.matches }}</div>
                <div class="stat-label">好友</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.reviews }}</div>
                <div class="stat-label">評價</div>
              </div>
              <div class="stat-item" v-if="userProfile.average_rating > 0">
                <div class="stat-value" style="font-size: 20px; font-weight: bold; color: #ff9900;">
                  ⭐ {{ userProfile.average_rating }}
                </div>
                <div class="stat-label">平均評分</div>
              </div>
            </div>
            
            <!-- 社群帳號展示 -->
            <el-divider content-position="center">
              <span style="color: #909399; font-size: 14px;">社群帳號</span>
            </el-divider>
            <div class="social-links-display">
              <el-button
                v-if="socialLinks.instagram"
                circle
                size="large"
                style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); color: white; border: none;"
                @click="openSocialLink(socialLinks.instagram)"
                title="Instagram"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M7.8,2H16.2C19.4,2 22,4.6 22,7.8V16.2A5.8,5.8 0 0,1 16.2,22H7.8C4.6,22 2,19.4 2,16.2V7.8A5.8,5.8 0 0,1 7.8,2M7.6,4A3.6,3.6 0 0,0 4,7.6V16.4C4,18.39 5.61,20 7.6,20H16.4A3.6,3.6 0 0,0 20,16.4V7.6C20,5.61 18.39,4 16.4,4H7.6M17.25,5.5A1.25,1.25 0 0,1 18.5,6.75A1.25,1.25 0 0,1 17.25,8A1.25,1.25 0 0,1 16,6.75A1.25,1.25 0 0,1 17.25,5.5M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.facebook"
                circle
                size="large"
                style="background: #1877F2; color: white; border: none;"
                @click="openSocialLink(socialLinks.facebook)"
                title="Facebook"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.line"
                circle
                size="large"
                style="background: #00B900; color: white; border: none;"
                @click="showLineQRCode"
                title="LINE (點擊顯示 QR Code)"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M19.365,9.863c.349,0,.698.025,1.041.083,0-5.094-5.098-9.233-11.381-9.233C3.75.713,0,4.853,0,9.948s3.75,9.235,8.988,9.235c1.031,0,2.025-.149,2.949-.43L19.373,24V18.048a6.644,6.644,0,0,0,2.065-4.784A6.618,6.618,0,0,0,19.365,9.863Z" /></svg></el-icon>
              </el-button>
              
              <el-button
                v-if="socialLinks.twitter"
                circle
                size="large"
                style="background: #000000; color: white; border: none;"
                @click="openSocialLink(socialLinks.twitter)"
                title="Twitter (X)"
              >
                <el-icon :size="20"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.70,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z" /></svg></el-icon>
              </el-button>
              
              <div v-if="!socialLinks.instagram && !socialLinks.facebook && !socialLinks.line && !socialLinks.twitter" style="color: #909399; font-size: 14px; text-align: center; padding: 10px;">
                未公開/未綁定社群帳號
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 右側內容區域 -->
        <el-col :xs="24" :md="16">
          <el-card>
            <template #header>
              <span>關於我</span>
            </template>
            <div class="bio-section">
              <p v-if="userProfile.bio">{{ userProfile.bio }}</p>
              <p v-else style="color: #909399;">這個用戶還沒有填寫簡介</p>
            </div>
            
            <el-divider />
            
            <div class="interests-section">
              <h4>興趣標籤</h4>
              <div v-if="userProfile.interests && userProfile.interests.length > 0" class="interest-tags">
                <el-tag
                  v-for="interest in userProfile.interests"
                  :key="interest"
                  size="large"
                  type="info"
                  style="margin: 5px;"
                >
                  {{ interest }}
                </el-tag>
              </div>
              <p v-else style="color: #909399;">尚未設定興趣標籤</p>
            </div>
          </el-card>
          
          <!-- 操作按鈕（僅非自己的個人資料顯示） -->
          <el-card v-if="!isOwnProfile" style="margin-top: 20px;">
            <el-space :size="10" wrap>
              <!-- 根據好友狀態顯示不同按鈕 -->
              <el-button 
                v-if="friendStatus === 'none'" 
                type="primary" 
                @click="sendMatchRequest"
              >
                <el-icon><UserFilled /></el-icon>
                邀請成為旅伴
              </el-button>
              <el-button 
                v-else-if="friendStatus === 'pending'" 
                type="warning" 
                disabled
              >
                <el-icon><Clock /></el-icon>
                已發送請求
              </el-button>
              <el-button 
                v-else-if="friendStatus === 'accepted'" 
                type="danger" 
                @click="removeFriend"
              >
                <el-icon><Delete /></el-icon>
                刪除好友
              </el-button>
              <el-button type="success" @click="goToChat">
                <el-icon><ChatLineRound /></el-icon>
                發送訊息
              </el-button>
            </el-space>
          </el-card>
          
          <!-- 評價列表（所有使用者都可以看到） -->
          <el-card style="margin-top: 20px;">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>收到的評價</span>
                <el-tag v-if="userProfile.average_rating > 0" type="warning">
                  ⭐ 平均 {{ userProfile.average_rating }} 分 ({{ userProfile.stats.reviews }} 則評價)
                </el-tag>
              </div>
            </template>
            
            <div v-if="loadingReviews" style="text-align: center; padding: 20px;">
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
                <div class="review-header">
                  <div class="reviewer-info">
                    <el-avatar :size="40" :src="review.reviewer?.avatar">
                      {{ review.reviewer?.name?.charAt(0) }}
                    </el-avatar>
                    <div class="reviewer-details">
                      <strong>{{ review.reviewer?.name || '匿名' }}</strong>
                      <div style="font-size: 12px; color: #909399; margin-top: 2px;">
                        {{ review.activity?.title || '一般評價' }}
                      </div>
                    </div>
                  </div>
                  <div class="review-rating">
                    <el-rate
                      :model-value="review.rating"
                      disabled
                      show-score
                      text-color="#ff9900"
                      score-template="{value} 分"
                      size="small"
                    />
                    <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                      {{ formatDate(review.created_at) }}
                    </div>
                  </div>
                </div>
                <div class="review-comment" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ebeef5;">
                  {{ review.comment }}
                </div>
              </el-card>
            </el-space>
            
            <el-empty v-if="!loadingReviews && userReviews.length === 0" description="還沒有收到任何評價" />
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div v-else class="loading-container">
      <el-icon class="is-loading" :size="50"><Loading /></el-icon>
      <p>載入中...</p>
    </div>

    <!-- LINE QR Code 對話框 -->
    <el-dialog v-model="showLineQRDialog" :title="`${userProfile.name} 的 LINE`" width="400px" align-center>
      <div style="text-align: center;">
        <div id="userLineQRCode" style="display: inline-block;"></div>
        <p style="margin-top: 20px; color: #606266;">
          掃描此 QR Code 加好友
        </p>
        <p style="color: #909399; font-size: 14px;">
          LINE ID: <strong>{{ socialLinks.line }}</strong>
        </p>
      </div>
      <template #footer>
        <el-button type="primary" @click="showLineQRDialog = false">關閉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Select,
  UserFilled,
  ChatLineRound,
  Loading,
  Clock,
  Delete
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const loadingReviews = ref(false)
const showLineQRDialog = ref(false)
const friendStatus = ref('none') // none, pending, accepted
const userReviews = ref([])
const isOwnProfile = ref(false) // 是否為自己的個人資料

const userProfile = ref({
  name: '',
  email: '',
  gender: 'male',
  age: 0,
  location: '',
  bio: '',
  avatar: '',
  verified: false,
  joinDate: '',
  interests: [],
  average_rating: 0,
  stats: {
    activities: 0,
    matches: 0,
    reviews: 0
  }
})

const socialLinks = ref({
  instagram: '',
  facebook: '',
  line: '',
  twitter: ''
})

// 返回上一頁
const goBack = () => {
  router.back()
}

// 性別文字
const getGenderText = (gender) => {
  const genderMap = {
    male: '男性',
    female: '女性',
    other: '其他'
  }
  return genderMap[gender] || '未設定'
}

// 檢查好友狀態
const checkFriendStatus = async () => {
  try {
    const userId = route.params.id
    const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
    
    // 檢查已接受的好友關係
    const acceptedResponse = await axios.get('/matches', {
      params: { status: 'accepted' }
    })
    
    if (acceptedResponse.data && acceptedResponse.data.matches) {
      const isAcceptedFriend = acceptedResponse.data.matches.some(match => {
        const otherUserId = match.requester_id === currentUserId 
          ? match.responder_id 
          : match.requester_id
        return otherUserId === parseInt(userId)
      })
      
      if (isAcceptedFriend) {
        friendStatus.value = 'accepted'
        return
      }
    }
    
    // 檢查已發送的請求
    const sentResponse = await axios.get('/matches/sent')
    
    if (sentResponse.data && sentResponse.data.matches) {
      const hasPendingRequest = sentResponse.data.matches.some(match => 
        match.responder.user_id === parseInt(userId) && match.status === 'pending'
      )
      
      if (hasPendingRequest) {
        friendStatus.value = 'pending'
        return
      }
    }
    
    friendStatus.value = 'none'
  } catch (error) {
    console.error('檢查好友狀態失敗:', error)
    friendStatus.value = 'none'
  }
}

// 載入用戶資料
const loadUserProfile = async () => {
  try {
    const userId = route.params.id
    const currentUserId = JSON.parse(localStorage.getItem('user'))?.user_id
    
    // 檢查是否為自己的個人資料
    isOwnProfile.value = parseInt(userId) === parseInt(currentUserId)
    
    const response = await axios.get(`/users/${userId}`)
    
    if (response.data && response.data.user) {
      const user = response.data.user
      userProfile.value = {
        name: user.name,
        email: user.email,
        gender: user.gender || 'male',
        age: user.age || 0,
        location: user.location || '',
        bio: user.bio || '',
        avatar: user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        verified: user.is_verified || false,
        joinDate: new Date(user.join_date).toLocaleDateString('zh-TW'),
        interests: user.interests || [],
        average_rating: user.average_rating || 0,
        stats: {
          activities: 0,
          matches: 0,
          reviews: 0
        }
      }
      
      // 載入社群帳號
      if (user.social_links) {
        socialLinks.value = {
          instagram: user.social_links.instagram || '',
          facebook: user.social_links.facebook || '',
          line: user.social_links.line || '',
          twitter: user.social_links.twitter || ''
        }
      }
      
      // 載入統計數據
      if (user.stats) {
        userProfile.value.stats = {
          activities: user.stats.activities || 0,
          matches: user.stats.matches || 0,
          reviews: user.stats.reviews || 0
        }
      }
      
      // 確保平均評分被載入
      if (user.average_rating !== undefined) {
        userProfile.value.average_rating = user.average_rating || 0
      }
    }
    
    // 檢查好友狀態
    await checkFriendStatus()
    
    // 載入評價列表
    await loadUserReviews()
    
    loading.value = false
  } catch (error) {
    console.error('載入用戶資料失敗:', error)
    ElMessage.error('載入用戶資料失敗')
    loading.value = false
  }
}

// 載入使用者評價列表
const loadUserReviews = async () => {
  try {
    loadingReviews.value = true
    const userId = route.params.id
    const response = await axios.get(`/users/${userId}/reviews`)
    
    console.log('評價列表 API 響應:', response.data)
    
    if (response.data && response.data.reviews) {
      userReviews.value = response.data.reviews
      console.log('載入的評價列表:', userReviews.value)
      // 更新平均評分（如果 API 有返回）
      if (response.data.average_rating !== undefined) {
        userProfile.value.average_rating = response.data.average_rating
      }
      // 更新評價數量
      if (response.data.rating_count !== undefined) {
        userProfile.value.stats.reviews = response.data.rating_count
      }
    } else {
      userReviews.value = []
    }
  } catch (error) {
    console.error('載入評價列表失敗:', error)
    console.error('錯誤詳情:', error.response?.data)
    // 顯示錯誤訊息以便調試
    if (error.response?.status === 404) {
      console.warn('評價列表 API 不存在，可能尚未實作')
    } else if (error.response?.status === 403) {
      console.warn('無權限查看評價列表')
    } else {
      ElMessage.warning('載入評價列表時發生錯誤，請稍後再試')
    }
    userReviews.value = []
  } finally {
    loadingReviews.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 打開社群連結
const openSocialLink = (url) => {
  if (url) {
    const fullUrl = url.startsWith('http') ? url : `https://${url}`
    window.open(fullUrl, '_blank')
  }
}

// 顯示 LINE QR Code
const showLineQRCode = () => {
  if (!socialLinks.value.line) {
    ElMessage.warning('該用戶未綁定 LINE')
    return
  }
  
  showLineQRDialog.value = true
  setTimeout(() => {
    generateLineQRCode()
  }, 100)
}

// 生成 LINE QR Code
const generateLineQRCode = () => {
  const container = document.getElementById('userLineQRCode')
  if (!container) return
  
  container.innerHTML = ''
  
  const lineUrl = `https://line.me/ti/p/${encodeURIComponent(socialLinks.value.line)}`
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(lineUrl)}`
  
  const img = document.createElement('img')
  img.src = qrCodeUrl
  img.alt = 'LINE QR Code'
  img.style.maxWidth = '100%'
  
  container.appendChild(img)
}

// 發送直接媒合請求（不基於活動）
const sendMatchRequest = async () => {
  try {
    // 使用對話框讓用戶輸入邀請訊息
    const { value: message } = await ElMessageBox.prompt(
      '請輸入邀請訊息',
      '邀請成為旅伴',
      {
        confirmButtonText: '發送',
        cancelButtonText: '取消',
        inputPlaceholder: '希望能成為旅伴，一起探索世界！',
        inputValue: '希望能成為旅伴，一起探索世界！'
      }
    )
    
    const userId = route.params.id
    await axios.post('/matches', {
      responder_id: userId,
      activity_id: null,  // 直接媒合（不基於活動）
      message: message || '希望能成為旅伴！'
    })
    
    ElMessage.success('邀請已發送！')
    friendStatus.value = 'pending'
  } catch (error) {
    // 用戶取消輸入不顯示錯誤
    if (error === 'cancel') return
    
    console.error('發送邀請失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('發送邀請失敗')
    }
  }
}

// 刪除好友
const removeFriend = async () => {
  try {
    const userId = route.params.id
    const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
    
    // 確認刪除
    await ElMessageBox.confirm(
      '確定要刪除此好友嗎？刪除後將無法直接聯繫，需要重新發送交友請求。',
      '確認刪除好友',
      {
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 找到對應的 match 記錄
    const response = await axios.get('/matches', {
      params: { status: 'accepted' }
    })
    
    if (response.data && response.data.matches) {
      const matchRecord = response.data.matches.find(match => {
        const otherUserId = match.requester_id === currentUserId 
          ? match.responder_id 
          : match.requester_id
        return otherUserId === parseInt(userId)
      })
      
      if (matchRecord) {
        // 刪除好友關係
        await axios.delete(`/matches/${matchRecord.match_id}`)
        ElMessage.success('已刪除好友')
        friendStatus.value = 'none'
      } else {
        ElMessage.error('找不到好友記錄')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('刪除好友失敗:', error)
      if (error.response?.data?.error) {
        ElMessage.error(error.response.data.error)
      } else {
        ElMessage.error('刪除好友失敗')
      }
    }
  }
}

// 前往聊天
const goToChat = () => {
  const userId = route.params.id
  router.push(`/chat?userId=${userId}`)
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.user-profile {
  min-height: 100vh;
  min-height: -webkit-fill-available;
  background-color: #f5f7fa;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-row {
  margin-top: 20px;
}

.profile-card {
  text-align: center;
}

.avatar-section {
  margin-bottom: 20px;
}

.user-basic-info {
  margin-bottom: 20px;
}

.user-basic-info h2 {
  margin: 10px 0;
}

.user-details {
  margin: 20px 0;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #dcdfe6;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.social-links-display {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 15px 0;
  flex-wrap: wrap;
}

.social-links-display .el-button {
  transition: transform 0.2s, box-shadow 0.2s;
}

.social-links-display .el-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.bio-section {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
  min-height: 100px;
}

.interests-section {
  margin-top: 20px;
}

.interests-section h4 {
  margin-bottom: 15px;
  color: #606266;
}

.interest-tags {
  display: flex;
  flex-wrap: wrap;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.review-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
}

.review-rating {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.review-comment {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .review-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .review-rating {
    align-items: flex-start;
  }
}
</style>
