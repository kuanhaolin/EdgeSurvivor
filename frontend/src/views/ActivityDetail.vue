<template>
  <div class="activity-detail">
    <NavBar />
    
    <div class="detail-container" v-if="activity">
      <el-page-header @back="goBack" :title="activity.title">
        <template #extra>
          <el-space>
            <!-- 活動狀態 -->
            <el-tag :type="getStatusType(activity.status)">
              {{ getStatusText(activity.status) }}
            </el-tag>
            
            <!-- 創建者可以更改狀態 -->
            <el-dropdown v-if="isCreator" @command="handleStatusChange">
              <el-button type="primary" size="small">
                更改狀態
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="open" :disabled="activity.status === 'open'">
                    開放報名
                  </el-dropdown-item>
                  <el-dropdown-item command="ongoing" :disabled="activity.status === 'ongoing'">
                    進行中
                  </el-dropdown-item>
                  <el-dropdown-item command="completed" :disabled="activity.status === 'completed'">
                    已完成
                  </el-dropdown-item>
                  <el-dropdown-item command="cancelled" :disabled="activity.status === 'cancelled'" divided>
                    取消活動
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-space>
        </template>
      </el-page-header>
      
      <!-- Tabs 導航 -->
      <el-tabs v-model="activeTab" class="detail-tabs">
        <!-- 活動資訊 -->
        <el-tab-pane label="活動資訊" name="info">
          <el-card>
            <!-- 封面圖片 -->
            <div v-if="activity.cover_image" class="cover-image">
              <el-image :src="activity.cover_image" fit="cover" />
            </div>
            
            <el-descriptions :column="2" border>
              <el-descriptions-item label="活動類型">
                {{ getTypeText(activity.category) }}
              </el-descriptions-item>
              <el-descriptions-item label="地點">
                {{ activity.location }}
              </el-descriptions-item>
              <el-descriptions-item label="日期">
                {{ formatDate(activity.date) }}
              </el-descriptions-item>
              <el-descriptions-item label="參與人數">
                {{ activity.current_participants }} / {{ activity.max_participants }} 人
              </el-descriptions-item>
              <el-descriptions-item label="創建者" :span="2">
                {{ activity.creator?.name }}
              </el-descriptions-item>
              <el-descriptions-item label="活動說明" :span="2">
                {{ activity.description || '無說明' }}
              </el-descriptions-item>
            </el-descriptions>
            
            <!-- 編輯按鈕（僅創建者） -->
            <div v-if="isCreator" style="margin-top: 20px;">
              <el-button type="primary" @click="editActivity">
                <el-icon><Edit /></el-icon>
                編輯活動
              </el-button>
            </div>
          </el-card>
        </el-tab-pane>
        
        <!-- 參與者列表 -->
        <el-tab-pane name="participants">
          <template #label>
            <span>
              參與者
              <el-badge
                :value="activity.current_participants"
                :max="99"
                class="item"
              />
            </span>
          </template>
          
          <el-card>
            <el-space wrap>
              <el-card
                v-for="participant in participants"
                :key="participant.user_id"
                shadow="hover"
                class="participant-card"
              >
                <div class="participant-info">
                  <el-avatar :size="60" :src="participant.avatar">
                    {{ participant.name?.charAt(0) }}
                  </el-avatar>
                  <div class="participant-details">
                    <strong>{{ participant.name }}</strong>
                    <el-tag v-if="participant.role === 'creator'" type="success" size="small">
                      創建者
                    </el-tag>
                    <el-tag v-else type="info" size="small">
                      參與者
                    </el-tag>
                  </div>
                </div>
              </el-card>
            </el-space>
            
            <el-empty v-if="participants.length === 0" description="還沒有參與者" />
          </el-card>
        </el-tab-pane>
        
        <!-- 討論區 -->
        <el-tab-pane label="討論區" name="discussion">
          <ActivityDiscussion
            :activity-id="activityId"
            :creator-id="activity.creator_id"
          />
        </el-tab-pane>
        
        <!-- 費用分攤 -->
        <el-tab-pane label="費用分攤" name="expenses">
          <ExpenseManager
            :activity-id="activityId"
            :creator-id="activity.creator_id"
          />
        </el-tab-pane>
        
        <!-- 相簿 -->
        <el-tab-pane label="相簿" name="album">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>活動相簿</span>
                <el-button v-if="canUploadPhoto" type="primary" @click="showUploadDialog = true">
                  <el-icon><Plus /></el-icon>
                  上傳照片
                </el-button>
              </div>
            </template>
            
            <div v-if="albumImages.length > 0" class="image-gallery">
              <el-image
                v-for="(image, index) in albumImages"
                :key="index"
                :src="image"
                :preview-src-list="albumImages"
                :initial-index="index"
                fit="cover"
                class="gallery-image"
              />
            </div>
            
            <el-empty v-else description="還沒有照片">
              <el-button v-if="canUploadPhoto" type="primary" @click="showUploadDialog = true">
                上傳第一張照片
              </el-button>
            </el-empty>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 載入中 -->
    <div v-else class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 上傳照片對話框 -->
    <el-dialog v-model="showUploadDialog" title="上傳照片" width="500px">
      <ImageUploader
        v-model="newImageUrl"
        placeholder="點擊上傳活動照片"
        @success="handleImageUpload"
      />
      
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" :disabled="!newImageUrl" @click="addToAlbum">
          加入相簿
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 編輯活動對話框 -->
    <el-dialog v-model="showEditDialog" title="編輯活動" width="600px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="封面圖片">
          <ImageUploader
            v-model="editForm.cover_image"
            placeholder="上傳活動封面"
          />
        </el-form-item>
        
        <el-form-item label="活動名稱" required>
          <el-input v-model="editForm.title" />
        </el-form-item>
        
        <el-form-item label="活動類型" required>
          <el-select v-model="editForm.category">
            <el-option label="登山" value="hiking" />
            <el-option label="露營" value="camping" />
            <el-option label="旅遊" value="travel" />
            <el-option label="美食" value="food" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="地點" required>
          <el-input v-model="editForm.location" />
        </el-form-item>
        
        <el-form-item label="活動日期" required>
          <el-date-picker
            v-model="editForm.date"
            type="date"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="人數上限" required>
          <el-input-number v-model="editForm.max_participants" :min="2" :max="50" />
        </el-form-item>
        
        <el-form-item label="活動描述">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="updateActivity">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, Plus, ArrowDown } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import ActivityDiscussion from '@/components/ActivityDiscussion.vue'
import ExpenseManager from '@/components/ExpenseManager.vue'
import ImageUploader from '@/components/ImageUploader.vue'
import axios from '@/utils/axios'

const route = useRoute()
const router = useRouter()

const activityId = computed(() => parseInt(route.params.id))
const activeTab = ref('info')
const activity = ref(null)
const participants = ref([])
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const newImageUrl = ref('')

const currentUserId = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.user_id
})

const isCreator = computed(() => {
  return activity.value?.creator_id === currentUserId.value
})

const isParticipant = computed(() => {
  return participants.value.some(p =>
    p.user_id === currentUserId.value &&
    ['approved', 'joined'].includes(p.status)
  )
})

// 創建人或參與者可以上傳照片
const canUploadPhoto = computed(() => {
  return isCreator.value || isParticipant.value
})

const albumImages = computed(() => {
  try {
    return activity.value?.images ? JSON.parse(activity.value.images) : []
  } catch {
    return []
  }
})

const editForm = reactive({
  cover_image: '',
  title: '',
  category: '',
  location: '',
  date: '',
  max_participants: 5,
  description: ''
})

// 載入活動詳情
const loadActivity = async () => {
  try {
    const response = await axios.get(`/activities/${activityId.value}`)
    activity.value = response.data.activity
    participants.value = response.data.activity.participants || []
  } catch (error) {
    console.error('載入活動失敗:', error)
    ElMessage.error('載入活動失敗')
    router.back()
  }
}

// 編輯活動
const editActivity = () => {
  editForm.cover_image = activity.value.cover_image || ''
  editForm.title = activity.value.title
  editForm.category = activity.value.category
  editForm.location = activity.value.location
  editForm.date = activity.value.date
  editForm.max_participants = activity.value.max_participants
  editForm.description = activity.value.description || ''
  showEditDialog.value = true
}

// 更新活動
const updateActivity = async () => {
  try {
    await axios.put(`/activities/${activityId.value}`, {
      cover_image: editForm.cover_image,
      title: editForm.title,
      type: editForm.category,
      location: editForm.location,
      start_date: editForm.date,
      max_members: editForm.max_participants,
      description: editForm.description
    })
    
    ElMessage.success('活動已更新')
    showEditDialog.value = false
    await loadActivity()
  } catch (error) {
    console.error('更新活動失敗:', error)
    ElMessage.error(error.response?.data?.error || '更新活動失敗')
  }
}

// 處理圖片上傳
const handleImageUpload = (url) => {
  newImageUrl.value = url
}

// 加入相簿
const addToAlbum = async () => {
  if (!newImageUrl.value) return
  
  try {
    const currentImages = albumImages.value
    currentImages.push(newImageUrl.value)
    
    await axios.put(`/activities/${activityId.value}`, {
      images: JSON.stringify(currentImages)
    })
    
    ElMessage.success('照片已加入相簿')
    showUploadDialog.value = false
    newImageUrl.value = ''
    await loadActivity()
  } catch (error) {
    console.error('加入相簿失敗:', error)
    ElMessage.error('加入相簿失敗')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '待定'
  return new Date(dateString).toLocaleDateString('zh-TW')
}

// 狀態相關
const getStatusType = (status) => {
  const types = {
    planning: 'info',
    recruiting: 'success',
    active: 'success',
    open: 'success',
    confirmed: 'warning',
    ongoing: 'warning',
    completed: '',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    planning: '籌備中',
    recruiting: '招募中',
    active: '招募中',
    open: '開放報名',
    confirmed: '已成團',
    ongoing: '進行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

const getTypeText = (type) => {
  const types = {
    hiking: '登山',
    camping: '露營',
    travel: '旅遊',
    food: '美食',
    other: '其他'
  }
  return types[type] || type
}

const getParticipantStatus = (status) => {
  const statuses = {
    pending: '待審核',
    approved: '已批准',
    joined: '已加入',
    rejected: '已拒絕',
    left: '已退出'
  }
  return statuses[status] || status
}

// 更改活動狀態
const handleStatusChange = async (newStatus) => {
  try {
    await axios.put(`/activities/${activityId.value}`, {
      status: newStatus
    })
    
    ElMessage.success('活動狀態已更新')
    await loadActivity()
  } catch (error) {
    console.error('更新狀態失敗:', error)
    ElMessage.error(error.response?.data?.error || '更新狀態失敗')
  }
}

// 返回
const goBack = () => {
  router.back()
}

// 組件掛載
onMounted(() => {
  loadActivity()
})
</script>

<style scoped>
.activity-detail {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.detail-tabs {
  margin-top: 20px;
}

.cover-image {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.cover-image .el-image {
  width: 100%;
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.participant-card {
  width: 200px;
}

.participant-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.participant-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.gallery-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  cursor: pointer;
}

.loading-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

@media (max-width: 768px) {
  .detail-container {
    padding: 10px;
  }
  
  .image-gallery {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
