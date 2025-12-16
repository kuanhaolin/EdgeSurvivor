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
                  <el-dropdown-item command="completed" :disabled="activity.status === 'completed' || !isActivityEnded">
                    已完成 {{ !isActivityEnded ? '(活動尚未結束)' : '' }}
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
                {{ formatDateRange(activity) }}
              </el-descriptions-item>
              <el-descriptions-item label="參與人數">
                {{ activity.current_participants }} / {{ activity.max_participants }} 人
              </el-descriptions-item>
              <el-descriptions-item label="創建者" :span="2">
                {{ activity.creator?.name }}
              </el-descriptions-item>
              <el-descriptions-item label="活動說明" :span="2">
                <div class="activity-description-full">
                  {{ activity.description || '無說明' }}
                </div>
              </el-descriptions-item>
            </el-descriptions>
            
            <!-- 動作按鈕區 -->
            <div style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
              <!-- 編輯按鈕（僅創建者） -->
              <el-button v-if="isCreator" type="primary" @click="editActivity">
                <el-icon><Edit /></el-icon>
                編輯活動
              </el-button>
              <!-- 刪除按鈕（僅創建者） -->
              <el-button v-if="isCreator" type="danger" @click="deleteActivity">
                <el-icon><Delete /></el-icon>
                刪除活動
              </el-button>
              <!-- 取消參與按鈕（參與者但不是創建者） -->
              <el-button v-if="isParticipant && !isCreator" type="warning" @click="leaveActivity">
                <el-icon><Close /></el-icon>
                取消參與
              </el-button>
              <!-- 傳訊息給創建者（非創建者且非參與者顯示） -->
              <el-button v-if="!isCreator && !isParticipant" type="success" @click="messageCreator">
                <el-icon><ChatDotRound /></el-icon>
                傳訊息給創建者
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
                v-for="participant in sortedParticipants"
                :key="participant.user_id"
                shadow="hover"
                class="participant-card"
              >
                <div class="participant-info" style="cursor: pointer;" @click="viewUserProfile(participant.user_id)">
                  <el-avatar :size="60" :src="participant.avatar">
                    {{ participant.name?.charAt(0) }}
                  </el-avatar>
                  <div class="participant-details">
                    <strong>{{ participant.name }}</strong>
                    <el-tag v-if="participant.user_id === activity.creator_id" type="warning" size="small">
                      創建者
                    </el-tag>
                    <el-tag v-else type="success" size="small">
                      {{ getParticipantStatus(participant.status) || '參與者' }}
                    </el-tag>
                  </div>
                </div>
                <!-- 動作按鈕區 -->
                <div v-if="participant.user_id !== currentUserId" style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap;">
                  <!-- 發起媒合按鈕（非自己的參與者都可見） -->
                  <el-button
                    type="success"
                    size="small"
                    @click.stop="sendMatchToParticipant(participant)"
                  >
                    <el-icon><User /></el-icon>
                    發起媒合
                  </el-button>
                  
                  <!-- 移除按鈕（僅創建者可見） -->
                  <el-button
                    v-if="isCreator"
                    type="danger"
                    size="small"
                    @click.stop="removeParticipant(participant)"
                  >
                    <el-icon><Close /></el-icon>
                    移除
                  </el-button>
                </div>
              </el-card>
            </el-space>
            
            <el-empty v-if="participants.length === 0" description="還沒有參與者" />
          </el-card>
        </el-tab-pane>
        
        <!-- 討論區 -->
        <el-tab-pane label="討論區" name="discussion">
          <template v-if="isCreator || isParticipant">
            <ActivityDiscussion
              :activity-id="activityId"
              :creator-id="activity.creator_id"
            />
          </template>
          <el-empty v-else description="只有活動參與者才能查看討論">
            <template #default>
              <div style="text-align:center; color:#909399;">申請加入或由創建者批准後即可查看</div>
            </template>
          </el-empty>
        </el-tab-pane>
        
        <!-- 費用分攤 -->
        <el-tab-pane label="費用分攤" name="expenses">
          <template v-if="isCreator || isParticipant">
            <ExpenseManager
              :activity-id="activityId"
              :creator-id="activity.creator_id"
            />
          </template>
          <el-empty v-else description="只有活動參與者才能查看費用與結算" />
        </el-tab-pane>
        
        <!-- 互評 -->
        <el-tab-pane label="互評" name="reviews">
          <ActivityReviews
            :activity-id="activityId"
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
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :on-change="handleFileChange"
        :show-file-list="true"
        :limit="1"
        accept="image/*"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖曳檔案至此或 <em>點擊上傳</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支援 JPG/PNG/GIF/WEBP 格式，檔案大小不超過 5MB
          </div>
        </template>
      </el-upload>
      
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" :disabled="!selectedFile" @click="handleImageUpload" :loading="uploading">
          上傳
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
            v-model="editForm.dateRange"
            type="daterange"
            range-separator="到"
            start-placeholder="開始日期"
            end-placeholder="結束日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="活動時間">
          <div style="display: flex; gap: 10px; width: 100%;">
            <el-time-picker
              v-model="editForm.start_time"
              placeholder="開始時間"
              format="HH:mm"
              value-format="HH:mm"
              style="flex: 1;"
            />
            <span style="line-height: 32px;">-</span>
            <el-time-picker
              v-model="editForm.end_time"
              placeholder="結束時間"
              format="HH:mm"
              value-format="HH:mm"
              style="flex: 1;"
            />
          </div>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Plus, ArrowDown, ChatDotRound, Delete, Close, UploadFilled, User } from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import ActivityDiscussion from '@/components/ActivityDiscussion.vue'
import ExpenseManager from '@/components/ExpenseManager.vue'
import ImageUploader from '@/components/ImageUploader.vue'
import ActivityReviews from '@/components/ActivityReviews.vue'
import axios from '@/utils/axios'
import { validateActivityUpdateForm } from '@/utils/activityValidation'
import { validateImageFile } from '@/utils/imageValidation'

const route = useRoute()
const router = useRouter()

const activityId = computed(() => parseInt(route.params.id))
const activeTab = ref('info')
const activity = ref(null)
const participants = ref([])
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const newImageUrl = ref('')
const selectedFile = ref(null)
const uploading = ref(false)
const uploadRef = ref(null)

const currentUserId = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.user_id
})

const isCreator = computed(() => {
  return activity.value?.creator_id === currentUserId.value
})

const isParticipant = computed(() => {
  // 後端只返回已加入/已批准的參與者清單，因此只需比對 user_id
  return participants.value.some(p => p.user_id === currentUserId.value)
})

// 檢查活動是否已結束
const isActivityEnded = computed(() => {
  if (!activity.value) return false
  const endDate = activity.value.end_date || activity.value.start_date || activity.value.date
  if (!endDate) return false
  return new Date(endDate) < new Date()
})

// 排序參與者：創建者排在最前面
const sortedParticipants = computed(() => {
  if (!participants.value || participants.value.length === 0) return []
  
  const creatorId = activity.value?.creator_id
  if (!creatorId) return participants.value
  
  // 將參與者分為創建者和其他參與者
  const creator = participants.value.find(p => p.user_id === creatorId)
  const others = participants.value.filter(p => p.user_id !== creatorId)
  
  // 創建者在前，其他參與者在後
  return creator ? [creator, ...others] : participants.value
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
  dateRange: [],
  start_time: '09:00',
  end_time: '17:00',
  max_participants: 5,
  description: ''
})

// 傳訊息給創建者
const messageCreator = () => {
  if (!activity.value?.creator_id) return
  router.push({
    path: '/chat',
    query: { userId: activity.value.creator_id }
  })
}

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
  
  // 處理日期範圍
  const startDate = activity.value.start_date || activity.value.date
  const endDate = activity.value.end_date
  if (startDate && endDate) {
    editForm.dateRange = [new Date(startDate), new Date(endDate)]
  } else if (startDate) {
    const date = new Date(startDate)
    editForm.dateRange = [date, date]
  } else {
    editForm.dateRange = []
  }
  
  // 處理時間
  editForm.start_time = activity.value.start_time || '09:00'
  editForm.end_time = activity.value.end_time || '17:00'
  
  editForm.max_participants = activity.value.max_participants
  editForm.description = activity.value.description || ''
  showEditDialog.value = true
}

// 更新活動
const updateActivity = async () => {
  // 使用統一的驗證函數
  const validation = validateActivityUpdateForm(editForm)
  if (!validation.valid) {
    ElMessage.error(validation.error)
    return
  }
  
  try {
    const [startDate, endDate] = editForm.dateRange
    
    await axios.put(`/activities/${activityId.value}`, {
      cover_image: editForm.cover_image,
      title: editForm.title,
      type: editForm.category,
      location: editForm.location,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      start_time: editForm.start_time || '09:00',
      end_time: editForm.end_time || '17:00',
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

// 處理文件選擇
const handleFileChange = (file, fileList) => {
  const validation = validateImageFile(file?.raw)
  if (!validation.valid) {
    ElMessage.error(validation.error)
    selectedFile.value = null
    // 清除 el-upload 的檔案列表
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
    return
  }
  selectedFile.value = file.raw
}

// 處理圖片上傳
const handleImageUpload = async () => {
  if (!selectedFile.value) return
  
  try {
    uploading.value = true
    const formData = new FormData()
    formData.append('image', selectedFile.value)
    
    const response = await axios.post(`/activities/${activityId.value}/photos`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    ElMessage.success('照片上傳成功')
    showUploadDialog.value = false
    selectedFile.value = null
    await loadActivity()
  } catch (error) {
    console.error('上傳照片失敗:', error)
    ElMessage.error(error.response?.data?.error || '上傳照片失敗')
  } finally {
    uploading.value = false
  }
}

// 加入相簿 (已廢棄 - 使用 handleImageUpload)
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

// 格式化日期範圍
const formatDateRange = (activity) => {
  const startDate = activity.start_date || activity.date
  const endDate = activity.end_date
  const startTime = activity.start_time
  const endTime = activity.end_time
  
  if (!startDate) return '待定'
  
  if (startDate && endDate) {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const startStr = `${start.getMonth() + 1}/${start.getDate()}`
    const endStr = `${end.getMonth() + 1}/${end.getDate()}`
    
    // 檢查是否有時間
    if (startTime || endTime) {
      if (start.toDateString() === end.toDateString()) {
        // 同一天，顯示時間區間
        return `${startStr} ${startTime || '00:00'}-${endTime || '23:59'}`
      } else {
        // 不同天，顯示日期和時間
        return `${startStr} ${startTime || '00:00'} - ${endStr} ${endTime || '23:59'}`
      }
    }
    
    if (startStr === endStr) {
      return startStr
    } else {
      return `${startStr} - ${endStr}`
    }
  }
  
  return new Date(startDate).toLocaleDateString('zh-TW')
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

// 刪除活動
const deleteActivity = async () => {
  try {
    await ElMessageBox.confirm('確定要刪除這個活動嗎？刪除後無法恢復。', '警告', {
      confirmButtonText: '確定刪除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    })
    
    await axios.delete(`/activities/${activityId.value}`)
    ElMessage.success('活動已刪除')
    router.push('/activities')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('刪除活動失敗:', error)
      ElMessage.error(error.response?.data?.error || '刪除活動失敗')
    }
  }
}

// 取消參與活動
const leaveActivity = async () => {
  try {
    await ElMessageBox.confirm('確定要取消參與這個活動嗎？', '提示', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.post(`/activities/${activityId.value}/leave`)
    ElMessage.success('已取消參與活動')
    await loadActivity()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消參與失敗:', error)
      ElMessage.error(error.response?.data?.error || '取消參與失敗')
    }
  }
}

// 移除參與者（僅創建者）
const removeParticipant = async (participant) => {
  try {
    await ElMessageBox.confirm(
      `確定要移除 ${participant.name} 嗎？移除後對方將無法再查看活動詳情。`,
      '移除參與者',
      {
        confirmButtonText: '確定移除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    // 需要先取得 participant_id
    // 從 participants 中找到對應的 participant_id
    const participantRecord = participants.value.find(p => p.user_id === participant.user_id)
    if (!participantRecord || !participantRecord.participant_id) {
      ElMessage.error('找不到參與者記錄')
      return
    }
    
    await axios.delete(`/activities/${activityId.value}/participants/${participantRecord.participant_id}`)
    ElMessage.success('已移除參與者')
    await loadActivity()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('移除參與者失敗:', error)
      ElMessage.error(error.response?.data?.error || '移除參與者失敗')
    }
  }
}

// 發起媒合申請
const sendMatchToParticipant = async (participant) => {
  try {
    const { value: message } = await ElMessageBox.prompt(
      `向 ${participant.name} 發起旅伴媒合`,
      '發起媒合',
      {
        confirmButtonText: '發送',
        cancelButtonText: '取消',
        inputPlaceholder: '希望能成為旅伴！',
        inputValue: '希望能成為旅伴！'
      }
    ).catch(() => ({ value: null }))
    
    if (!message) return
    
    await axios.post('/matches', {
      responder_id: participant.user_id,
      activity_id: activityId.value,
      message: message
    })
    
    ElMessage.success('媒合申請已發送！')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('發送媒合失敗:', error)
      ElMessage.error(error.response?.data?.error || '發送媒合失敗')
    }
  }
}

// 查看使用者資料
const viewUserProfile = (userId) => {
  router.push(`/user/${userId}`)
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
  min-height: -webkit-fill-available;
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
  transition: transform 0.2s, box-shadow 0.2s;
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.participant-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.participant-details strong {
  color: #409eff;
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

/* 活動說明：保留換行並自動換行 */
.activity-description-full {
  white-space: pre-wrap; /* 保留使用者輸入的換行 */
  word-break: break-word; /* 長字或 URL 可以安全換行 */
  overflow-wrap: anywhere;
  line-height: 1.6;
  color: #606266;
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
