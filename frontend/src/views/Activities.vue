<template>
  <div class="activities">
    <NavBar />
    
    <div class="activities-container">
      <el-page-header @back="goBack" content="活動管理">
        <template #extra>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            創建新活動
          </el-button>
        </template>
      </el-page-header>
      
      <!-- 搜尋和篩選 -->
      <el-card class="search-card">
        <el-form :inline="true">
          <el-form-item label="搜尋">
            <el-input
              v-model="searchQuery"
              placeholder="搜尋活動名稱或地點"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item label="類型">
            <el-select v-model="filterType" placeholder="全部" clearable style="min-width: 150px;">
              <el-option label="全部" value="" />
              <el-option label="登山" value="hiking" />
              <el-option label="露營" value="camping" />
              <el-option label="旅遊" value="travel" />
              <el-option label="美食" value="food" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="狀態">
            <el-select v-model="filterStatus" placeholder="全部" clearable style="min-width: 150px;">
              <el-option label="全部" value="" />
              <el-option label="籌備中" value="planning" />
              <el-option label="招募中" value="recruiting" />
              <el-option label="已成團" value="confirmed" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 活動列表 -->
      <el-tabs v-model="activeTab" class="activities-tabs">
        <el-tab-pane label="我的所有活動" name="all">
          <el-row :gutter="20">
            <el-col
              v-for="activity in filteredAllActivities"
              :key="activity.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="activity-card" shadow="hover">
                <template #header>
                  <div class="activity-header">
                    <span class="activity-title">{{ activity.title }}</span>
                    <el-tag :type="getStatusType(activity.status)">
                      {{ getStatusText(activity.status) }}
                    </el-tag>
                  </div>
                </template>
                
                <div class="activity-content">
                  <div class="activity-info">
                    <el-icon><User /></el-icon>
                    <span>{{ activity.creatorName }}</span>
                    <el-tag v-if="activity.isCreator" type="success" size="small" style="margin-left: 8px;">創建者</el-tag>
                  </div>
                  <div class="activity-info">
                    <el-icon><Location /></el-icon>
                    <span>{{ activity.location }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ activity.date }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><UserFilled /></el-icon>
                    <span>{{ activity.currentMembers }}/{{ activity.maxMembers }} 人</span>
                  </div>
                  <p class="activity-description">{{ activity.description }}</p>
                </div>
                
                <template #footer>
                  <div class="card-footer-actions">
                    <el-button size="small" @click="viewActivity(activity.id)">
                      查看詳情
                    </el-button>
                    <el-button 
                      v-if="activity.isCreator" 
                      size="small" 
                      type="primary" 
                      @click="editActivity(activity.id)"
                    >
                      編輯
                    </el-button>
                    <el-button 
                      v-else
                      size="small" 
                      type="success"
                      disabled
                    >
                      已參加
                    </el-button>
                  </div>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="filteredAllActivities.length === 0" description="還沒有任何活動">
            <el-button type="primary" @click="showCreateDialog = true">創建第一個活動</el-button>
          </el-empty>
        </el-tab-pane>
        
        <el-tab-pane label="我創建的活動" name="created">
          <el-row :gutter="20">
            <el-col
              v-for="activity in filteredCreatedActivities"
              :key="activity.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="activity-card" shadow="hover">
                <template #header>
                  <div class="activity-header">
                    <span class="activity-title">{{ activity.title }}</span>
                    <el-tag :type="getStatusType(activity.status)">
                      {{ getStatusText(activity.status) }}
                    </el-tag>
                  </div>
                </template>
                
                <div class="activity-content">
                  <div class="activity-info">
                    <el-icon><Location /></el-icon>
                    <span>{{ activity.location }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ activity.date }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><UserFilled /></el-icon>
                    <span>{{ activity.currentMembers }}/{{ activity.maxMembers }} 人</span>
                  </div>
                  <p class="activity-description">{{ activity.description }}</p>
                </div>
                
                <template #footer>
                  <el-button-group style="width: 100%">
                    <el-button size="small" @click="viewActivity(activity.id)">
                      查看詳情
                    </el-button>
                    <el-button size="small" type="warning" @click="viewPendingApplicants(activity.id)">
                      <el-badge :value="activity.pendingCount || 0" :hidden="!activity.pendingCount">
                        待審核
                      </el-badge>
                    </el-button>
                    <el-button size="small" type="primary" @click="editActivity(activity.id)">
                      編輯
                    </el-button>
                    <el-button size="small" type="danger" @click="deleteActivity(activity.id)">
                      刪除
                    </el-button>
                  </el-button-group>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="filteredCreatedActivities.length === 0" description="還沒有創建任何活動">
            <el-button type="primary" @click="showCreateDialog = true">創建第一個活動</el-button>
          </el-empty>
        </el-tab-pane>
        
        <el-tab-pane label="我參加的活動" name="joined">
          <el-row :gutter="20">
            <el-col
              v-for="activity in filteredJoinedActivities"
              :key="activity.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="activity-card" shadow="hover">
                <template #header>
                  <div class="activity-header">
                    <span class="activity-title">{{ activity.title }}</span>
                    <el-tag :type="getStatusType(activity.status)">
                      {{ getStatusText(activity.status) }}
                    </el-tag>
                  </div>
                </template>
                
                <div class="activity-content">
                  <div class="activity-info">
                    <el-icon><User /></el-icon>
                    <span>創建者: {{ activity.creatorName }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Location /></el-icon>
                    <span>{{ activity.location }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ activity.date }}</span>
                  </div>
                  <p class="activity-description">{{ activity.description }}</p>
                </div>
                
                <template #footer>
                  <el-button size="small" style="width: 100%" @click="viewActivity(activity.id)">
                    查看詳情
                  </el-button>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="filteredJoinedActivities.length === 0" description="還沒有參加任何活動">
            <el-button type="success" @click="activeTab = 'discover'">探索活動</el-button>
          </el-empty>
        </el-tab-pane>
        
        <el-tab-pane label="探索活動" name="discover">
          <el-row :gutter="20">
            <el-col
              v-for="activity in filteredDiscoverActivities"
              :key="activity.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <el-card class="activity-card" shadow="hover">
                <template #header>
                  <div class="activity-header">
                    <span class="activity-title">{{ activity.title }}</span>
                    <el-tag :type="getStatusType(activity.status)">
                      {{ getStatusText(activity.status) }}
                    </el-tag>
                  </div>
                </template>
                
                <div class="activity-content">
                  <div class="activity-info">
                    <el-icon><User /></el-icon>
                    <span>{{ activity.creatorName }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Location /></el-icon>
                    <span>{{ activity.location }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ activity.date }}</span>
                  </div>
                  <div class="activity-info">
                    <el-icon><UserFilled /></el-icon>
                    <span>{{ activity.currentMembers }}/{{ activity.maxMembers }} 人</span>
                  </div>
                  <p class="activity-description">{{ activity.description }}</p>
                </div>
                
                <template #footer>
                  <div class="card-footer-actions">
                    <el-button size="small" @click="viewActivity(activity.id)">
                      查看詳情
                    </el-button>
                    <el-button size="small" type="info" @click="messageCreator(activity)">
                      詢問資訊
                    </el-button>
                    <el-button class="apply-btn" type="success" size="small" @click="joinActivity(activity.id)">
                      申請加入
                    </el-button>
                  </div>
                </template>
              </el-card>
            </el-col>
          </el-row>
          
          <el-empty v-if="filteredDiscoverActivities.length === 0" description="目前沒有可加入的活動" />
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 創建活動對話框 -->
    <el-dialog 
      v-model="showCreateDialog" 
      :title="editingActivityId ? '編輯活動' : '創建新活動'" 
      width="600px"
    >
      <el-form :model="newActivity" label-width="100px">
        <el-form-item label="活動名稱" required>
          <el-input v-model="newActivity.title" placeholder="例如：陽明山登山之旅" />
        </el-form-item>
        
        <el-form-item label="活動類型" required>
          <el-select v-model="newActivity.type" placeholder="請選擇">
            <el-option label="登山" value="hiking" />
            <el-option label="露營" value="camping" />
            <el-option label="旅遊" value="travel" />
            <el-option label="美食" value="food" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="地點" required>
          <el-input v-model="newActivity.location" placeholder="例如：台北市陽明山" />
        </el-form-item>
        
        <el-form-item label="活動日期" required>
          <el-date-picker
            v-model="newActivity.dateRange"
            type="daterange"
            range-separator="到"
            start-placeholder="開始日期"
            end-placeholder="結束日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="人數上限" required>
          <el-input-number v-model="newActivity.maxMembers" :min="2" :max="50" />
        </el-form-item>
        
        <el-form-item label="活動描述">
          <el-input
            v-model="newActivity.description"
            type="textarea"
            :rows="4"
            placeholder="詳細描述活動內容、行程安排等..."
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createActivity">創建活動</el-button>
      </template>
    </el-dialog>
    
    <!-- 活動詳情對話框 -->
    <el-dialog v-model="showActivityDialog" :title="selectedActivity?.title" width="700px">
      <div v-if="selectedActivity" class="activity-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="活動類型">
            {{ getTypeText(selectedActivity.type) }}
          </el-descriptions-item>
          <el-descriptions-item label="地點">
            {{ selectedActivity.location }}
          </el-descriptions-item>
          <el-descriptions-item label="日期">
            {{ selectedActivity.date }}
          </el-descriptions-item>
          <el-descriptions-item label="參與人數">
            {{ selectedActivity.currentMembers }} / {{ selectedActivity.maxMembers }} 人
          </el-descriptions-item>
          <el-descriptions-item label="創建者" :span="2">
            {{ selectedActivity.creatorName }}
          </el-descriptions-item>
          <el-descriptions-item label="活動說明" :span="2">
            <div class="activity-description-full">
              {{ selectedActivity.description || '無說明' }}
            </div>
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- 參與者列表 -->
        <div v-if="selectedActivity.participants && selectedActivity.participants.length > 0" style="margin-top: 20px;">
          <h4>參與者列表</h4>
          <el-space wrap>
            <el-tag
              v-for="participant in selectedActivity.participants"
              :key="participant.user_id"
              :type="participant.role === 'creator' ? 'success' : 'info'"
              size="large"
            >
              <el-avatar :size="24" :src="participant.avatar" style="margin-right: 8px;" />
              {{ participant.name }}
              <span v-if="participant.role === 'creator'"> (創建者)</span>
            </el-tag>
          </el-space>
        </div>
      </div>
      <template #footer>
        <el-button @click="showActivityDialog = false">關閉</el-button>
        <el-button 
          v-if="createdActivities.find(a => a.id === selectedActivity?.id)" 
          type="primary" 
          @click="editActivity(selectedActivity.id); showActivityDialog = false"
        >
          編輯活動
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 待審核申請對話框 -->
    <el-dialog v-model="showPendingDialog" title="待審核申請" width="600px">
      <el-empty v-if="pendingApplicants.length === 0" description="目前沒有待審核的申請" />
      
      <el-space v-else direction="vertical" style="width: 100%">
        <el-card 
          v-for="applicant in pendingApplicants" 
          :key="applicant.participant_id"
          shadow="hover"
        >
          <div style="display: flex; align-items: center; gap: 15px;">
            <el-avatar :size="50" :src="applicant.avatar" />
            <div style="flex: 1;">
              <h4 style="margin: 0 0 5px 0;">{{ applicant.name }}</h4>
              <el-text type="info" size="small">
                申請時間: {{ new Date(applicant.joined_at).toLocaleString('zh-TW') }}
              </el-text>
              <p v-if="applicant.message" style="margin: 10px 0 0 0; color: #606266;">
                <el-icon><ChatDotRound /></el-icon>
                {{ applicant.message }}
              </p>
            </div>
            <div>
              <el-button 
                type="success" 
                size="small" 
                @click="approveApplicant(applicant.participant_id)"
              >
                批准
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="rejectApplicant(applicant.participant_id)"
              >
                拒絕
              </el-button>
            </div>
          </div>
        </el-card>
      </el-space>
      
      <template #footer>
        <el-button @click="showPendingDialog = false">關閉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Location,
  Calendar,
  UserFilled,
  User,
  ChatDotRound
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'

const router = useRouter()

// 當前標籤頁（預設顯示所有活動）
const activeTab = ref('all')

// 搜尋和篩選
const searchQuery = ref('')
const filterType = ref('')
const filterStatus = ref('')

// 活動列表
const createdActivities = ref([])
const joinedActivities = ref([])
const discoverActivities = ref([])

// 創建活動對話框
const showCreateDialog = ref(false)
const showActivityDialog = ref(false)
const showPendingDialog = ref(false)
const selectedActivity = ref(null)
const editingActivityId = ref(null)
const currentActivityId = ref(null)
const pendingApplicants = ref([])

const activityForm = reactive({
  title: '',
  type: '',
  location: '',
  dateRange: [],  // 改為日期範圍陣列 [startDate, endDate]
  maxMembers: 5,
  description: ''
})

// 保留舊的 newActivity 別名以兼容現有代碼
const newActivity = activityForm

// 載入活動列表
const loadActivities = async () => {
  try {
    const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
    
    // 分別載入三種類型的活動
    const [createdResponse, joinedResponse, allResponse] = await Promise.all([
      axios.get('/activities?type=created'),
      axios.get('/activities?type=joined'),
      axios.get('/activities')
    ])
    
    console.log('我創建的活動響應:', createdResponse.data)
    console.log('我參加的活動響應:', joinedResponse.data)
    console.log('所有活動響應:', allResponse.data)
    
    // 我創建的活動
    if (createdResponse.data && createdResponse.data.activities) {
      createdActivities.value = createdResponse.data.activities.map(formatActivity)
    }
    
    // 我參加的活動（不包含自己創建的）
    if (joinedResponse.data && joinedResponse.data.activities) {
      joinedActivities.value = joinedResponse.data.activities.map(formatActivity)
    }
    
    // 探索活動（排除自己創建的和已參加的）
    if (allResponse.data && allResponse.data.activities) {
      const createdIds = createdActivities.value.map(a => a.id)
      const joinedIds = joinedActivities.value.map(a => a.id)
      const excludeIds = new Set([...createdIds, ...joinedIds])
      
      discoverActivities.value = allResponse.data.activities
        .filter(a => {
          // 排除已創建和已參加的
          if (excludeIds.has(a.activity_id)) return false
          
          // 只顯示可報名狀態的活動（active, recruiting, open）
          if (!['active', 'recruiting', 'open'].includes(a.status)) return false
          
          // 可選：排除已滿的活動
          // if (a.current_participants >= a.max_participants) return false
          
          return true
        })
        .map(formatActivity)
    }
    
    console.log('我創建的活動:', createdActivities.value)
    console.log('我參加的活動:', joinedActivities.value)
    console.log('探索活動:', discoverActivities.value)
    
  } catch (error) {
    console.error('載入活動失敗:', error)
    if (error.response?.status === 401) {
      ElMessage.error('登入已過期，請重新登入')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    } else {
      ElMessage.error('載入活動失敗')
    }
  }
}

// 格式化活動資料
const formatActivity = (activity) => {
  const startDate = activity.start_date || activity.date || activity.created_at
  const endDate = activity.end_date
  
  // 格式化日期顯示
  let dateDisplay = '待定'
  if (startDate && endDate) {
    const start = new Date(startDate).toLocaleDateString('zh-TW', { month: '2-digit', day: '2-digit' })
    const end = new Date(endDate).toLocaleDateString('zh-TW', { month: '2-digit', day: '2-digit' })
    if (start === end) {
      dateDisplay = start
    } else {
      dateDisplay = `${start} - ${end}`
    }
  } else if (startDate) {
    dateDisplay = new Date(startDate).toLocaleDateString('zh-TW')
  }
  
  return {
    id: activity.activity_id,
    title: activity.title,
    type: activity.category,  // 後端返回 category
    location: activity.location,
    date: dateDisplay,
    rawDate: startDate,  // 保留原始開始日期用於排序
    startDate: startDate,
    endDate: endDate,
    currentMembers: activity.current_participants || 1,  // 後端返回 current_participants
    maxMembers: activity.max_participants,  // 後端返回 max_participants
    description: activity.description || '',
    creatorName: activity.creator?.name || '未知',
    creatorId: activity.creator?.user_id || null,
    status: activity.status,
    pendingCount: activity.pending_count || 0  // 待審核數量
  }
}

// 組件掛載時載入活動
onMounted(() => {
  loadActivities()
})

// ------ 搜尋與篩選（前端）------
const normalized = (s) => (s || '').toString().toLowerCase()

const statusMatches = (status) => {
  if (!filterStatus.value) return true
  // 將「招募中」視為 recruiting/active/open 的統稱
  if (filterStatus.value === 'recruiting') {
    return ['recruiting', 'active', 'open'].includes(status)
  }
  return status === filterStatus.value
}

const typeMatches = (type) => {
  if (!filterType.value) return true
  return type === filterType.value
}

const textMatches = (activity) => {
  if (!searchQuery.value) return true
  const q = normalized(searchQuery.value)
  return [activity.title, activity.location, activity.description, activity.creatorName]
    .some((f) => normalized(f).includes(q))
}

const filterList = (list) => {
  return list.filter((a) => statusMatches(a.status) && typeMatches(a.type) && textMatches(a))
}

// 合併所有活動（創建 + 參加）
const allActivities = computed(() => {
  const created = createdActivities.value.map(a => ({ ...a, isCreator: true }))
  const joined = joinedActivities.value.map(a => ({ ...a, isCreator: false }))
  
  // 合併並按日期排序（最新在前）
  return [...created, ...joined].sort((a, b) => {
    const dateA = new Date(a.rawDate || a.date)
    const dateB = new Date(b.rawDate || b.date)
    return dateB - dateA
  })
})

const filteredAllActivities = computed(() => filterList(allActivities.value))
const filteredCreatedActivities = computed(() => filterList(createdActivities.value))
const filteredJoinedActivities = computed(() => filterList(joinedActivities.value))
const filteredDiscoverActivities = computed(() => filterList(discoverActivities.value))

// 狀態類型對應
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

// 返回
const goBack = () => {
  router.back()
}

// 查看活動詳情
const viewActivity = async (id) => {
  router.push(`/activities/${id}`)
}

// 編輯活動
const editActivity = (id) => {
  // 找到活動
  const activity = createdActivities.value.find(a => a.id === id)
  
  if (!activity) {
    ElMessage.error('只能編輯自己創建的活動')
    return
  }
  
  // 填充表單
  activityForm.title = activity.title
  activityForm.type = activity.type
  activityForm.location = activity.location
  
  // 處理日期範圍
  if (activity.startDate && activity.endDate) {
    activityForm.dateRange = [new Date(activity.startDate), new Date(activity.endDate)]
  } else if (activity.rawDate) {
    // 如果只有單一日期，設為同一天
    const date = new Date(activity.rawDate)
    activityForm.dateRange = [date, date]
  } else {
    activityForm.dateRange = []
  }
  
  activityForm.maxMembers = activity.maxMembers
  activityForm.description = activity.description
  
  // 設置為編輯模式
  editingActivityId.value = id
  showCreateDialog.value = true
}

// 詢問創建者（先發訊息溝通）
const messageCreator = (activity) => {
  if (!activity?.creatorId) return
  router.push({
    path: '/chat',
    query: { userId: activity.creatorId }
  })
}

// 刪除活動
const deleteActivity = async (id) => {
  try {
    await ElMessageBox.confirm('確定要刪除這個活動嗎？', '警告', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('活動已刪除')
  } catch {
    // 取消刪除
  }
}

// 加入活動
const joinActivity = async (id) => {
  try {
    // 詢問是否要添加申請訊息
    const { value: message } = await ElMessageBox.prompt('請輸入申請訊息（可選）', '申請加入活動', {
      confirmButtonText: '發送申請',
      cancelButtonText: '取消',
      inputPlaceholder: '例如：您好，我對這個活動很感興趣！'
    }).catch(() => ({ value: '' }))
    
    const response = await axios.post(`/activities/${id}/join`, {
      message: message || ''
    })
    ElMessage.success(response.data.message || '申請已發送！')
    
    // 重新載入活動列表
    await loadActivities()
  } catch (error) {
    console.error('申請失敗:', error)
    ElMessage.error(error.response?.data?.error || '申請失敗')
  }
}

// 查看待審核申請
const viewPendingApplicants = async (activityId) => {
  try {
    currentActivityId.value = activityId
    const response = await axios.get(`/activities/${activityId}/participants/pending`)
    pendingApplicants.value = response.data.pending_participants || []
    showPendingDialog.value = true
  } catch (error) {
    console.error('載入待審核申請失敗:', error)
    ElMessage.error('無法載入待審核申請')
  }
}

// 批准申請
const approveApplicant = async (participantId) => {
  try {
    await ElMessageBox.confirm('確定要批准此申請嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'success'
    })
    
    await axios.post(`/activities/${currentActivityId.value}/participants/${participantId}/approve`)
    ElMessage.success('已批准申請')
    
    // 重新載入待審核列表
    await viewPendingApplicants(currentActivityId.value)
    // 重新載入活動列表
    await loadActivities()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批准失敗:', error)
      ElMessage.error(error.response?.data?.error || '批准失敗')
    }
  }
}

// 拒絕申請
const rejectApplicant = async (participantId) => {
  try {
    const { value: reason } = await ElMessageBox.prompt('請輸入拒絕原因（可選）', '拒絕申請', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      inputPlaceholder: '例如：人數已滿、不符合條件等',
      inputType: 'textarea'
    }).catch(() => ({ value: '' }))
    
    await axios.post(`/activities/${currentActivityId.value}/participants/${participantId}/reject`, {
      reason: reason || ''
    })
    ElMessage.success('已拒絕申請')
    
    // 重新載入待審核列表
    await viewPendingApplicants(currentActivityId.value)
    // 重新載入活動列表
    await loadActivities()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒絕失敗:', error)
      ElMessage.error(error.response?.data?.error || '拒絕失敗')
    }
  }
}

// 創建/更新活動
const createActivity = async () => {
  if (!activityForm.title || !activityForm.type || !activityForm.location || !activityForm.dateRange || activityForm.dateRange.length !== 2) {
    ElMessage.error('請填寫所有必填欄位')
    return
  }
  
  try {
    const [startDate, endDate] = activityForm.dateRange
    
    if (editingActivityId.value) {
      // 編輯模式
      console.log('更新活動:', editingActivityId.value, activityForm)
      
      const response = await axios.put(`/activities/${editingActivityId.value}`, {
        title: activityForm.title,
        type: activityForm.type,
        location: activityForm.location,
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        max_members: activityForm.maxMembers,
        description: activityForm.description
      })
      
      console.log('更新活動響應:', response.data)
      ElMessage.success('活動更新成功！')
    } else {
      // 創建模式
      console.log('創建活動數據:', activityForm)
      
      const response = await axios.post('/activities', {
        title: activityForm.title,
        type: activityForm.type,
        location: activityForm.location,
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        max_members: activityForm.maxMembers,
        description: activityForm.description,
        status: 'recruiting'
      })
      
      console.log('創建活動響應:', response.data)
      ElMessage.success('活動創建成功！')
    }
    
    showCreateDialog.value = false
    
    // 重置表單和編輯狀態
    activityForm.title = ''
    activityForm.type = ''
    activityForm.location = ''
    activityForm.dateRange = []
    activityForm.maxMembers = 5
    activityForm.description = ''
    editingActivityId.value = null
    
    // 重新載入活動列表
    await loadActivities()
  } catch (error) {
    console.error('操作失敗:', error)
    ElMessage.error(error.response?.data?.error || '操作失敗')
  }
}
</script>

<style scoped>
.activities {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.activities-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-card {
  margin: 20px 0;
}

.activities-tabs {
  margin-top: 20px;
}

.activity-card {
  margin-bottom: 20px;
  height: 100%;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-title {
  font-weight: bold;
  font-size: 16px;
}

.activity-content {
  min-height: 150px;
}

.activity-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.activity-description {
  margin-top: 12px;
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
  /* 即使沒有描述也預留兩行的高度，讓按鈕區對齊 */
  min-height: calc(1.6em * 2);
  /* 讓長字/URL也能換行 */
  word-break: break-word;
  overflow-wrap: anywhere;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  line-clamp: 2; /* 標準屬性，部分瀏覽器支援 */
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 行動優先：預設單欄堆疊（最穩定，不影響其他版面） */
.card-footer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-footer-actions :deep(.el-button) {
  width: 100%;
}

/* 消除 Element Plus 預設的相鄰按鈕 margin-left，避免第二行看起來縮排 */
.card-footer-actions :deep(.el-button + .el-button) {
  margin-left: 0;
}

/* 活動詳情中的完整描述：保留使用者輸入的換行並自動換行 */
.activity-description-full {
  white-space: pre-wrap; /* 保留\n 並自動換行 */
  word-break: break-word; /* 長字或 URL 時安全換行 */
  overflow-wrap: anywhere;
  line-height: 1.6;
  color: #606266;
}

@media (max-width: 768px) {
  .activities-container {
    padding: 10px;
  }
}
</style>
