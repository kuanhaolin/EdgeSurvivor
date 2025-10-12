<template>
  <div class="profile">
    <NavBar />
    
    <div class="profile-container">
      <el-page-header @back="goBack" content="個人資料" />
      
      <el-row :gutter="20" class="profile-row">
        <!-- 左側個人資訊卡片 -->
        <el-col :xs="24" :md="8">
          <el-card class="profile-card">
            <div class="avatar-section">
              <el-avatar :size="120" :src="userProfile.avatar" />
              <el-button type="primary" size="small" class="upload-btn" @click="uploadAvatar">
                <el-icon><Upload /></el-icon>
                更換頭像
              </el-button>
              <!-- 隱藏的文件輸入 -->
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleAvatarUpload"
              />
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
              <el-descriptions-item label="電子郵件">
                {{ userProfile.email }}
              </el-descriptions-item>
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
                <div class="stat-label">媒合</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userProfile.stats.reviews }}</div>
                <div class="stat-label">評價</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 右側編輯區域 -->
        <el-col :xs="24" :md="16">
          <el-tabs v-model="activeTab">
            <!-- 基本資料 -->
            <el-tab-pane label="基本資料" name="basic">
              <el-card>
                <el-form :model="editForm" label-width="100px">
                  <el-form-item label="姓名">
                    <el-input v-model="editForm.name" />
                  </el-form-item>
                  
                  <el-form-item label="性別">
                    <el-select v-model="editForm.gender" placeholder="請選擇">
                      <el-option label="男性" value="male" />
                      <el-option label="女性" value="female" />
                      <el-option label="其他" value="other" />
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="年齡">
                    <el-input-number v-model="editForm.age" :min="18" :max="100" />
                  </el-form-item>
                  
                  <el-form-item label="地區">
                    <el-cascader
                      v-model="selectedLocation"
                      :options="locationOptions"
                      :props="cascaderProps"
                      placeholder="請選擇國家和城市"
                      style="width: 100%"
                      @change="handleLocationChange"
                      filterable
                    />
                  </el-form-item>
                  
                  <el-form-item label="個人簡介">
                    <el-input
                      v-model="editForm.bio"
                      type="textarea"
                      :rows="4"
                      placeholder="介紹一下自己..."
                    />
                  </el-form-item>
                  
                  <el-form-item label="興趣標籤">
                    <el-tag
                      v-for="tag in editForm.interests"
                      :key="tag"
                      closable
                      @close="removeInterest(tag)"
                      style="margin-right: 8px; margin-bottom: 8px;"
                    >
                      {{ tag }}
                    </el-tag>
                    <el-input
                      v-if="showInterestInput"
                      v-model="newInterest"
                      size="small"
                      style="width: 100px;"
                      @blur="addInterest"
                      @keyup.enter="addInterest"
                    />
                    <el-button v-else size="small" @click="showInterestInput = true">
                      + 新增標籤
                    </el-button>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="saveProfile">儲存變更</el-button>
                    <el-button @click="cancelEdit">取消</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
            
            <!-- 隱私設定 -->
            <el-tab-pane label="隱私設定" name="privacy">
              <el-card>
                <el-form label-width="150px">
                  <el-form-item label="個人資料可見性">
                    <el-radio-group v-model="privacySettings.profileVisibility">
                      <el-radio label="public">公開</el-radio>
                      <el-radio label="partial">部分公開</el-radio>
                      <el-radio label="private">僅自己可見</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  
                  <el-form-item label="顯示年齡">
                    <el-switch v-model="privacySettings.showAge" />
                  </el-form-item>
                  
                  <el-form-item label="顯示地區">
                    <el-switch v-model="privacySettings.showLocation" />
                  </el-form-item>
                  
                  <el-form-item label="允許陌生人訊息">
                    <el-switch v-model="privacySettings.allowStrangerMessages" />
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="savePrivacySettings">儲存設定</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
            
            <!-- 帳號安全 -->
            <el-tab-pane label="帳號安全" name="security">
              <el-card>
                <el-form label-width="120px">
                  <el-form-item label="電子郵件">
                    <el-input v-model="userProfile.email" disabled />
                    <el-button type="text" @click="changeEmail">更改電子郵件</el-button>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="變更密碼">
                    <el-button @click="showPasswordDialog = true">變更密碼</el-button>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="兩步驟驗證">
                    <el-switch v-model="securitySettings.twoFactorAuth" />
                    <div style="margin-top: 8px; color: #909399; font-size: 12px;">
                      啟用後需要輸入驗證碼才能登入
                    </div>
                  </el-form-item>
                  
                  <el-divider />
                  
                  <el-form-item label="危險區域">
                    <el-button type="danger" @click="deleteAccount">刪除帳號</el-button>
                    <div style="margin-top: 8px; color: #f56c6c; font-size: 12px;">
                      刪除後將無法恢復
                    </div>
                  </el-form-item>
                </el-form>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>
    
    <!-- 變更密碼對話框 -->
    <el-dialog v-model="showPasswordDialog" title="變更密碼" width="500px">
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="目前密碼">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密碼">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="確認密碼">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="changePassword">確認變更</el-button>
      </template>
    </el-dialog>

    <!-- 更改電子郵件對話框 -->
    <el-dialog v-model="showEmailDialog" title="更改電子郵件" width="500px">
      <el-form label-width="100px">
        <el-form-item label="新電子郵件">
          <el-input v-model="emailForm.newEmail" type="email" placeholder="請輸入新的電子郵件地址" />
        </el-form-item>
        <el-form-item label="確認密碼">
          <el-input v-model="emailForm.password" type="password" placeholder="請輸入密碼以確認" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEmailDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmChangeEmail">確認更改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Upload,
  Select
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

const router = useRouter()

const activeTab = ref('basic')

// 地區選擇器配置
const selectedLocation = ref([])
const cascaderProps = {
  expandTrigger: 'hover',
  value: 'value',
  label: 'label',
  children: 'children'
}

// 地區選項數據
const locationOptions = [
  {
    value: '台灣',
    label: '台灣',
    children: [
      { value: '台北市', label: '台北市' },
      { value: '新北市', label: '新北市' },
      { value: '桃園市', label: '桃園市' },
      { value: '台中市', label: '台中市' },
      { value: '台南市', label: '台南市' },
      { value: '高雄市', label: '高雄市' },
      { value: '基隆市', label: '基隆市' },
      { value: '新竹市', label: '新竹市' },
      { value: '嘉義市', label: '嘉義市' },
      { value: '新竹縣', label: '新竹縣' },
      { value: '苗栗縣', label: '苗栗縣' },
      { value: '彰化縣', label: '彰化縣' },
      { value: '南投縣', label: '南投縣' },
      { value: '雲林縣', label: '雲林縣' },
      { value: '嘉義縣', label: '嘉義縣' },
      { value: '屏東縣', label: '屏東縣' },
      { value: '宜蘭縣', label: '宜蘭縣' },
      { value: '花蓮縣', label: '花蓮縣' },
      { value: '台東縣', label: '台東縣' },
      { value: '澎湖縣', label: '澎湖縣' },
      { value: '金門縣', label: '金門縣' },
      { value: '連江縣', label: '連江縣' }
    ]
  },
  {
    value: '日本',
    label: '日本',
    children: [
      { value: '東京', label: '東京' },
      { value: '大阪', label: '大阪' },
      { value: '京都', label: '京都' },
      { value: '北海道', label: '北海道' },
      { value: '沖繩', label: '沖繩' },
      { value: '福岡', label: '福岡' },
      { value: '名古屋', label: '名古屋' },
      { value: '神戶', label: '神戶' },
      { value: '橫濱', label: '橫濱' },
      { value: '奈良', label: '奈良' }
    ]
  },
  {
    value: '韓國',
    label: '韓國',
    children: [
      { value: '首爾', label: '首爾' },
      { value: '釜山', label: '釜山' },
      { value: '濟州島', label: '濟州島' },
      { value: '仁川', label: '仁川' },
      { value: '大邱', label: '大邱' },
      { value: '光州', label: '光州' }
    ]
  },
  {
    value: '中國',
    label: '中國',
    children: [
      { value: '北京', label: '北京' },
      { value: '上海', label: '上海' },
      { value: '廣州', label: '廣州' },
      { value: '深圳', label: '深圳' },
      { value: '成都', label: '成都' },
      { value: '杭州', label: '杭州' },
      { value: '西安', label: '西安' },
      { value: '重慶', label: '重慶' },
      { value: '南京', label: '南京' },
      { value: '武漢', label: '武漢' }
    ]
  },
  {
    value: '香港',
    label: '香港',
    children: [
      { value: '香港島', label: '香港島' },
      { value: '九龍', label: '九龍' },
      { value: '新界', label: '新界' }
    ]
  },
  {
    value: '新加坡',
    label: '新加坡',
    children: [
      { value: '新加坡', label: '新加坡' }
    ]
  },
  {
    value: '泰國',
    label: '泰國',
    children: [
      { value: '曼谷', label: '曼谷' },
      { value: '清邁', label: '清邁' },
      { value: '普吉', label: '普吉' },
      { value: '芭達雅', label: '芭達雅' },
      { value: '蘇梅島', label: '蘇梅島' }
    ]
  },
  {
    value: '美國',
    label: '美國',
    children: [
      { value: '紐約', label: '紐約' },
      { value: '洛杉磯', label: '洛杉磯' },
      { value: '舊金山', label: '舊金山' },
      { value: '西雅圖', label: '西雅圖' },
      { value: '芝加哥', label: '芝加哥' },
      { value: '波士頓', label: '波士頓' },
      { value: '拉斯維加斯', label: '拉斯維加斯' },
      { value: '邁阿密', label: '邁阿密' }
    ]
  },
  {
    value: '英國',
    label: '英國',
    children: [
      { value: '倫敦', label: '倫敦' },
      { value: '曼徹斯特', label: '曼徹斯特' },
      { value: '愛丁堡', label: '愛丁堡' },
      { value: '利物浦', label: '利物浦' },
      { value: '劍橋', label: '劍橋' },
      { value: '牛津', label: '牛津' }
    ]
  },
  {
    value: '法國',
    label: '法國',
    children: [
      { value: '巴黎', label: '巴黎' },
      { value: '馬賽', label: '馬賽' },
      { value: '里昂', label: '里昂' },
      { value: '尼斯', label: '尼斯' },
      { value: '史特拉斯堡', label: '史特拉斯堡' }
    ]
  },
  {
    value: '澳洲',
    label: '澳洲',
    children: [
      { value: '雪梨', label: '雪梨' },
      { value: '墨爾本', label: '墨爾本' },
      { value: '布里斯本', label: '布里斯本' },
      { value: '伯斯', label: '伯斯' },
      { value: '阿德萊德', label: '阿德萊德' }
    ]
  },
  {
    value: '其他',
    label: '其他',
    children: [
      { value: '其他地區', label: '其他地區' }
    ]
  }
]

// 處理地區變更
const handleLocationChange = (value) => {
  if (value && value.length === 2) {
    // 組合為 "國家 - 城市" 格式
    editForm.location = `${value[0]} - ${value[1]}`
  } else {
    editForm.location = ''
  }
}

// 用戶資料
const userProfile = ref({
  name: 'Test User',
  email: 'test@example.com',
  gender: 'male',
  age: 28,
  location: '台北市',
  bio: '喜歡登山、露營，尋找志同道合的旅伴！',
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  verified: true,
  joinDate: '2025-01-01',
  stats: {
    activities: 5,
    matches: 12,
    reviews: 8
  }
})

// 編輯表單
const editForm = reactive({
  name: '',
  gender: '',
  age: 0,
  location: '',
  bio: '',
  interests: []
})

// 興趣標籤
const showInterestInput = ref(false)
const newInterest = ref('')

// 隱私設定
const privacySettings = reactive({
  profileVisibility: 'public',
  showAge: true,
  showLocation: true,
  allowStrangerMessages: true
})

// 安全設定
const securitySettings = reactive({
  twoFactorAuth: false
})

// 密碼變更
const showPasswordDialog = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 載入用戶資料
onMounted(async () => {
  try {
    // 從 API 載入用戶資料
    const response = await axios.get('/users/profile')
    
    if (response.data && response.data.user) {
      const user = response.data.user
      userProfile.value = {
        name: user.name,
        email: user.email,
        gender: user.gender || 'male',
        age: user.age || 18,
        location: user.location || '',
        bio: user.bio || '',
        avatar: user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        verified: user.is_verified || false,
        joinDate: new Date(user.join_date).toLocaleDateString('zh-TW'),
        stats: {
          activities: 0,
          matches: 0,
          reviews: 0
        }
      }
      
      // 初始化編輯表單
      editForm.name = userProfile.value.name
      editForm.gender = userProfile.value.gender
      editForm.age = userProfile.value.age
      editForm.location = userProfile.value.location
      editForm.bio = userProfile.value.bio
      editForm.interests = user.interests || []  // 載入興趣標籤
      
      // 解析地區並設置級聯選擇器
      parseLocationString(userProfile.value.location)
    }
    
    // 載入統計數據
    const statsResponse = await axios.get('/users/stats')
    if (statsResponse.data && statsResponse.data.stats) {
      userProfile.value.stats.activities = statsResponse.data.stats.activities
      userProfile.value.stats.matches = statsResponse.data.stats.matches
    }
    
  } catch (error) {
    console.error('載入用戶資料失敗:', error)
    
    // 如果 API 失敗，從 localStorage 讀取
    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      userProfile.value = { ...userProfile.value, ...user }
    }
    
    // 初始化編輯表單
    editForm.name = userProfile.value.name
    editForm.gender = userProfile.value.gender
    editForm.age = userProfile.value.age
    editForm.location = userProfile.value.location
    editForm.bio = userProfile.value.bio
    editForm.interests = userProfile.value.interests || []  // 載入興趣標籤
    
    // 解析地區並設置級聯選擇器
    parseLocationString(userProfile.value.location)
  }
})

// 解析地區字串並設置級聯選擇器
const parseLocationString = (locationStr) => {
  if (!locationStr) {
    selectedLocation.value = []
    return
  }
  
  // 如果格式是 "國家 - 城市"
  if (locationStr.includes(' - ')) {
    const parts = locationStr.split(' - ')
    selectedLocation.value = [parts[0], parts[1]]
  } else {
    // 舊格式,嘗試匹配
    // 檢查是否為台灣的縣市
    const taiwanCities = locationOptions[0].children.map(c => c.value)
    if (taiwanCities.includes(locationStr)) {
      selectedLocation.value = ['台灣', locationStr]
    } else {
      // 無法解析,清空
      selectedLocation.value = []
    }
  }
}

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

// 上傳頭像
const avatarInput = ref(null)

const uploadAvatar = () => {
  avatarInput.value?.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    ElMessage.error('請選擇圖片檔案')
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('圖片大小不能超過 2MB')
    return
  }

  try {
    // 上傳到服務器
    const formData = new FormData()
    formData.append('image', file)
    
    const token = localStorage.getItem('token')
    const response = await fetch('/api/upload/image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('上傳失敗')
    }
    
    const data = await response.json()
    
    // 更新頭像 URL
    editForm.avatar = data.url
    userProfile.value.avatar = data.url
    
    // 更新到後端用戶資料
    await axios.put('/users/profile', {
      profile_picture: data.url
    })
    
    // 更新本地存儲
    const user = JSON.parse(localStorage.getItem('user'))
    user.profile_picture = data.url
    user.avatar = data.url
    localStorage.setItem('user', JSON.stringify(user))
    
    ElMessage.success('頭像上傳成功！')
    
    // 重新載入用戶資料
    await loadUserProfile()
  } catch (error) {
    console.error('上傳頭像失敗:', error)
    ElMessage.error('頭像上傳失敗，請重試')
  }
  
  // 清空 input
  event.target.value = ''
}

// 新增興趣
const addInterest = () => {
  if (newInterest.value && !editForm.interests.includes(newInterest.value)) {
    editForm.interests.push(newInterest.value)
  }
  newInterest.value = ''
  showInterestInput.value = false
}

// 移除興趣
const removeInterest = (tag) => {
  editForm.interests = editForm.interests.filter(t => t !== tag)
}

// 儲存個人資料
const saveProfile = async () => {
  try {
    const response = await axios.put('/users/profile', {
      name: editForm.name,
      gender: editForm.gender,
      age: editForm.age,
      location: editForm.location,
      bio: editForm.bio,
      interests: editForm.interests  // 添加興趣標籤
    })
    
    if (response.data) {
      userProfile.value.name = editForm.name
      userProfile.value.gender = editForm.gender
      userProfile.value.age = editForm.age
      userProfile.value.location = editForm.location
      userProfile.value.bio = editForm.bio
      userProfile.value.interests = editForm.interests  // 更新興趣
      
      // 更新 localStorage
      const user = JSON.parse(localStorage.getItem('user'))
      user.name = editForm.name
      user.interests = editForm.interests  // 保存興趣到 localStorage
      localStorage.setItem('user', JSON.stringify(user))
      
      ElMessage.success('個人資料已更新')
    }
  } catch (error) {
    console.error('更新個人資料失敗:', error)
    ElMessage.error('更新失敗，請稍後再試')
  }
}

// 取消編輯
const cancelEdit = () => {
  editForm.name = userProfile.value.name
  editForm.gender = userProfile.value.gender
  editForm.age = userProfile.value.age
  editForm.location = userProfile.value.location
  editForm.bio = userProfile.value.bio
  editForm.interests = userProfile.value.interests || []  // 恢復興趣標籤
}

// 儲存隱私設定
const savePrivacySettings = async () => {
  try {
    await axios.put('/users/privacy', {
      privacy_setting: privacySettings.profileVisibility
    })
    
    ElMessage.success('隱私設定已更新')
  } catch (error) {
    console.error('更新隱私設定失敗:', error)
    ElMessage.error('更新失敗，請稍後再試')
  }
}

// 更改電子郵件
const showEmailDialog = ref(false)
const emailForm = ref({
  newEmail: '',
  password: ''
})

const changeEmail = () => {
  showEmailDialog.value = true
  emailForm.value = { newEmail: '', password: '' }
}

const confirmChangeEmail = async () => {
  if (!emailForm.value.newEmail || !emailForm.value.password) {
    ElMessage.error('請填寫所有欄位')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(emailForm.value.newEmail)) {
    ElMessage.error('請輸入有效的電子郵件地址')
    return
  }

  // TODO: 需要後端API支援
  ElMessage.info('更改電子郵件功能需要後端API支援，包括驗證碼發送和驗證流程')
  showEmailDialog.value = false
}

// 變更密碼
const changePassword = async () => {
  if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    ElMessage.error('請填寫所有欄位')
    return
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('兩次輸入的密碼不一致')
    return
  }
  
  if (passwordForm.newPassword.length < 6) {
    ElMessage.error('密碼長度至少需要 6 個字元')
    return
  }
  
  try {
    await axios.post('/auth/change-password', {
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    
    ElMessage.success('密碼已變更，請重新登入')
    showPasswordDialog.value = false
    
    // 重置表單
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    // 登出並跳轉到登入頁
    setTimeout(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }, 1500)
    
  } catch (error) {
    console.error('變更密碼失敗:', error)
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('變更密碼失敗')
    }
  }
}

// 刪除帳號
const deleteAccount = async () => {
  try {
    await ElMessageBox.confirm(
      '刪除帳號後將無法恢復，所有資料將被永久刪除。確定要刪除嗎？',
      '危險操作',
      {
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )

    // 二次確認
    await ElMessageBox.prompt(
      '請輸入您的密碼以確認刪除帳號',
      '確認密碼',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        inputType: 'password',
        inputPlaceholder: '請輸入密碼',
        inputValidator: (value) => {
          if (!value) {
            return '請輸入密碼'
          }
          return true
        }
      }
    )

    // TODO: 需要後端API支援
    ElMessage.info('帳號刪除功能需要後端API支援（DELETE /users/account）')
    
    // 實際實作時應該這樣：
    // await axios.delete('/users/account', {
    //   data: { password: result.value }
    // })
    // localStorage.removeItem('token')
    // router.push('/login')
    // ElMessage.success('帳號已刪除')
    
  } catch (error) {
    if (error === 'cancel') {
      // 用戶取消
      return
    }
    console.error('刪除帳號失敗:', error)
  }
}
</script>

<style scoped>
.profile {
  min-height: 100vh;
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

.upload-btn {
  margin-top: 10px;
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

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
}
</style>
