<template>
  <div class="activity-reviews">
    <el-alert
      v-if="!canReview"
      title="提示"
      type="info"
      :closable="false"
      style="margin-bottom: 20px"
    >
      只有活動狀態為「已完成」且活動結束日期已過時才能進行互評
    </el-alert>
    
    <!-- 待評價的參與者 -->
    <el-card v-if="pendingReviews.length > 0 && canReview" class="review-section">
      <template #header>
        <div class="card-header">
          <span>待評價</span>
          <el-tag type="warning">{{ pendingReviews.length }} 人</el-tag>
        </div>
      </template>
      
      <el-space direction="vertical" style="width: 100%" :size="15">
        <el-card
          v-for="user in pendingReviews"
          :key="user.user_id"
          shadow="hover"
          class="user-card"
        >
          <div class="user-info">
            <el-avatar :size="60" :src="user.profile_picture">
              {{ user.name?.charAt(0) }}
            </el-avatar>
            <div class="user-details">
              <strong>{{ user.name }}</strong>
              <div class="user-rating">
                <el-tag type="info" size="small">{{ user.rating_count }} 則評價</el-tag>
                <el-tag v-if="user.average_rating > 0" type="warning" size="small" style="margin-left: 5px;">
                  ⭐ {{ user.average_rating }}
                </el-tag>
              </div>
            </div>
            <el-button type="primary" @click="openReviewDialog(user)">
              評價
            </el-button>
          </div>
        </el-card>
      </el-space>
    </el-card>
    
    <!-- 已評價的參與者 -->
    <el-card v-if="reviewedUsers.length > 0" class="review-section" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>已評價</span>
          <el-tag type="success">{{ reviewedUsers.length }} 人</el-tag>
        </div>
      </template>
      
      <el-space direction="vertical" style="width: 100%" :size="15">
        <el-card
          v-for="user in reviewedUsers"
          :key="user.user_id"
          shadow="hover"
          class="user-card"
        >
          <div class="user-info">
            <el-avatar :size="60" :src="user.profile_picture">
              {{ user.name?.charAt(0) }}
            </el-avatar>
            <div class="user-details">
              <strong>{{ user.name }}</strong>
              <div class="user-rating">
                <el-tag type="info" size="small">{{ user.rating_count }} 則評價</el-tag>
                <el-tag v-if="user.average_rating > 0" type="warning" size="small" style="margin-left: 5px;">
                  ⭐ {{ user.average_rating }}
                </el-tag>
              </div>
              <div class="my-review-summary">
                <div v-if="user.my_review" style="margin-bottom: 5px;">
                  <el-rate
                    :model-value="user.my_review.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value} 分"
                    size="small"
                  />
                </div>
                <span class="review-comment">
                  {{ user.my_review.comment }}
                </span>
              </div>
            </div>
            <el-button v-if="canReview" type="info" plain @click="openReviewDialog(user)">
              修改評價
            </el-button>
          </div>
        </el-card>
      </el-space>
    </el-card>
    
    <!-- 暫無參與者 -->
    <el-empty
      v-if="pendingReviews.length === 0 && reviewedUsers.length === 0"
      description="沒有可以評價的參與者"
    />
    
    <!-- 評價對話框 -->
    <el-dialog
      v-model="showReviewDialog"
      :title="isEditing ? '修改評價' : '評價參與者'"
      width="500px"
    >
      <div v-if="currentUser" class="review-dialog-content">
        <div class="review-user-info">
          <el-avatar :size="80" :src="currentUser.profile_picture">
            {{ currentUser.name?.charAt(0) }}
          </el-avatar>
          <div>
            <h3>{{ currentUser.name }}</h3>
            <div style="margin-top: 5px;">
              <el-tag type="info" size="small">{{ currentUser.rating_count }} 則評價</el-tag>
              <el-tag v-if="currentUser.average_rating > 0" type="warning" size="small" style="margin-left: 5px;">
                ⭐ {{ currentUser.average_rating }}
              </el-tag>
            </div>
          </div>
        </div>
        
        <el-form :model="reviewForm" label-width="80px" style="margin-top: 20px">
          <el-form-item label="評分" required>
            <el-rate
              v-model="reviewForm.rating"
              :max="5"
              show-score
              text-color="#ff9900"
              score-template="{value} 分"
            />
            <div style="color: #909399; font-size: 12px; margin-top: 5px;">
              請選擇 1-5 星評分（必填）
            </div>
          </el-form-item>
          <el-form-item label="評價內容" required>
            <el-input
              v-model="reviewForm.comment"
              type="textarea"
              :rows="6"
              placeholder="分享你對這位參與者的評價..."
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <el-button @click="showReviewDialog = false">取消</el-button>
        <el-button
          type="primary"
          :disabled="!reviewForm.rating || reviewForm.rating < 1 || !reviewForm.comment || !reviewForm.comment.trim()"
          :loading="submitting"
          @click="submitReview"
        >
          {{ isEditing ? '更新評價' : '提交評價' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'

const props = defineProps({
  activityId: {
    type: Number,
    required: true
  }
})

const pendingReviews = ref([])
const reviewedUsers = ref([])
const canReview = ref(false)
const showReviewDialog = ref(false)
const currentUser = ref(null)
const submitting = ref(false)

const reviewForm = reactive({
  rating: 0,
  comment: ''
})

const isEditing = computed(() => {
  return currentUser.value?.my_review !== undefined
})

// 載入評價狀態
const loadReviewStatus = async () => {
  try {
    const response = await axios.get(`/activities/${props.activityId}/reviews/my-status`)
    pendingReviews.value = response.data.pending || []
    reviewedUsers.value = response.data.reviewed || []
    canReview.value = response.data.can_review || false
  } catch (error) {
    console.error('載入評價狀態失敗:', error)
    if (error.response?.status !== 403) {
      ElMessage.error(error.response?.data?.error || '載入評價狀態失敗')
    }
  }
}

// 打開評價對話框
const openReviewDialog = (user) => {
  currentUser.value = user
  
  if (user.my_review) {
    // 編輯模式，填入現有評價
    reviewForm.rating = user.my_review.rating || 0
    reviewForm.comment = user.my_review.comment || ''
  } else {
    // 新增模式，清空表單
    reviewForm.rating = 0
    reviewForm.comment = ''
  }
  
  showReviewDialog.value = true
}

// 提交評價
const submitReview = async () => {
  if (!reviewForm.rating || reviewForm.rating < 1 || reviewForm.rating > 5) {
    ElMessage.warning('請選擇 1-5 星評分')
    return
  }
  
  if (!reviewForm.comment || !reviewForm.comment.trim()) {
    ElMessage.warning('請填寫評價內容')
    return
  }
  
  submitting.value = true
  
  try {
    await axios.post(`/activities/${props.activityId}/reviews`, {
      reviewee_id: currentUser.value.user_id,
      rating: reviewForm.rating,
      comment: reviewForm.comment.trim()
    })
    
    ElMessage.success(isEditing.value ? '評價已更新' : '評價已提交')
    showReviewDialog.value = false
    
    // 重新載入評價狀態
    await loadReviewStatus()
  } catch (error) {
    console.error('提交評價失敗:', error)
    ElMessage.error(error.response?.data?.error || '提交評價失敗')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadReviewStatus()
})

// 暴露方法給父組件
defineExpose({
  loadReviewStatus
})
</script>

<style scoped>
.activity-reviews {
  padding: 20px 0;
}

.review-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-card {
  background-color: #f9f9f9;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-count {
  color: #909399;
  font-size: 14px;
}

.my-review-summary {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 8px;
}

.review-comment {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.review-dialog-content {
  padding: 10px 0;
}

.review-user-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.review-user-info h3 {
  margin: 0 0 10px 0;
}

@media (max-width: 768px) {
  .user-info {
    flex-direction: column;
    text-align: center;
  }
  
  .user-details {
    align-items: center;
  }
}
</style>
