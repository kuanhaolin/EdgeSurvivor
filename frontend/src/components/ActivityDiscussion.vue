<template>
  <div class="discussion-container">
    <el-card class="discussion-card">
      <!-- 訊息列表 -->
      <div class="messages-area" ref="messagesArea">
        <el-empty v-if="discussions.length === 0" description="還沒有討論訊息">
          <el-text type="info">成為第一個發言的人！</el-text>
        </el-empty>
        
        <div
          v-for="msg in discussions"
          :key="msg.discussion_id"
          :class="['message-item', { 'own-message': isOwnMessage(msg) }]"
        >
          <el-avatar :src="msg.user?.avatar" :size="40">
            {{ msg.user?.name?.charAt(0) }}
          </el-avatar>
          
          <div class="message-content">
            <div class="message-header">
              <span class="user-name">{{ msg.user?.name }}</span>
              <span class="message-time">{{ formatTime(msg.created_at) }}</span>
            </div>
            <div class="message-text">{{ msg.message }}</div>
            
            <!-- 刪除按鈕（只有發送者或創建者可以刪除） -->
            <el-button
              v-if="canDelete(msg)"
              type="danger"
              size="small"
              text
              @click="deleteMessage(msg.discussion_id)"
            >
              刪除
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 發送訊息區域 -->
      <div class="send-area">
        <el-input
          v-model="newMessage"
          type="textarea"
          :rows="3"
          placeholder="輸入訊息... (Ctrl+Enter 發送)"
          @keydown.ctrl.enter="sendMessage"
        />
        <el-button
          type="primary"
          :loading="sending"
          :disabled="!newMessage.trim()"
          @click="sendMessage"
        >
          <el-icon><ChatDotRound /></el-icon>
          發送
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ChatDotRound } from '@element-plus/icons-vue'
import axios from '@/utils/axios'
import socketService from '@/services/socket'

const props = defineProps({
  activityId: {
    type: Number,
    required: true
  },
  creatorId: {
    type: Number,
    required: false
  }
})

const discussions = ref([])
const newMessage = ref('')
const sending = ref(false)
const messagesArea = ref(null)
const currentUserId = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.user_id
})

// 載入討論訊息
const loadDiscussions = async () => {
  try {
    const response = await axios.get(`/activities/${props.activityId}/discussions`)
    discussions.value = response.data.discussions || []
    
    // 滾動到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('載入討論失敗:', error)
    if (error.response?.status === 403) {
      ElMessage.error('只有活動參與者才能查看討論')
    } else {
      ElMessage.error('載入討論失敗')
    }
  }
}

// 發送訊息
const sendMessage = async () => {
  if (!newMessage.value.trim()) {
    return
  }
  
  sending.value = true
  try {
    // 優先使用 Socket.IO
    if (socketService.isConnected()) {
      await socketService.sendDiscussion(
        props.activityId,
        currentUserId.value,
        newMessage.value.trim(),
        'text'
      )
      newMessage.value = ''
      // Socket.IO 會通過 new_discussion 事件回傳，不需要重新載入
    } else {
      // 降級到 HTTP API
      await axios.post(`/activities/${props.activityId}/discussions`, {
        message: newMessage.value.trim(),
        message_type: 'text'
      })
      newMessage.value = ''
      await loadDiscussions()
      ElMessage.success('訊息已發送')
    }
  } catch (error) {
    console.error('發送訊息失敗:', error)
    ElMessage.error(error.response?.data?.error || '發送訊息失敗')
  } finally {
    sending.value = false
  }
}

// 刪除訊息
const deleteMessage = async (discussionId) => {
  try {
    await ElMessageBox.confirm('確定要刪除這條訊息嗎？', '確認', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/discussions/${discussionId}`)
    ElMessage.success('訊息已刪除')
    await loadDiscussions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('刪除訊息失敗:', error)
      ElMessage.error(error.response?.data?.error || '刪除訊息失敗')
    }
  }
}

// 判斷是否為自己的訊息
const isOwnMessage = (msg) => {
  return msg.user_id === currentUserId.value
}

// 判斷是否可以刪除
const canDelete = (msg) => {
  return msg.user_id === currentUserId.value || currentUserId.value === props.creatorId
}

// 格式化時間
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  // 小於1分鐘
  if (diff < 60000) {
    return '剛剛'
  }
  
  // 小於1小時
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)} 分鐘前`
  }
  
  // 小於24小時
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)} 小時前`
  }
  
  // 顯示完整日期
  return date.toLocaleString('zh-TW', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 滾動到底部
const scrollToBottom = () => {
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
}

// 組件掛載時載入討論
onMounted(() => {
  loadDiscussions()
  
  // 連線到 Socket.IO (如果還沒連線)
  if (!socketService.isConnected()) {
    socketService.connect()
  }
  
  // 加入活動討論室
  socketService.joinActivityDiscussion(props.activityId, currentUserId.value)
  
  // 監聽新討論訊息
  socketService.onNewDiscussion((discussion) => {
    console.log('收到新討論訊息:', discussion)
    
    // 檢查是否為當前活動的訊息
    if (discussion.activity_id === props.activityId) {
      // 添加到討論列表
      discussions.value.push(discussion)
      
      // 滾動到底部
      nextTick(() => {
        scrollToBottom()
      })
    }
  })
})

// 組件卸載時離開討論室
onUnmounted(() => {
  socketService.leaveActivityDiscussion(props.activityId)
})
</script>

<style scoped>
.discussion-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.discussion-card {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.discussion-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-item.own-message {
  flex-direction: row-reverse;
}

.message-item.own-message .message-content {
  align-items: flex-end;
}

.message-item.own-message .message-text {
  background-color: #409eff;
  color: white;
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
  max-width: 70%;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.user-name {
  font-weight: 600;
  color: #303133;
}

.message-time {
  color: #909399;
  font-size: 11px;
}

.message-text {
  background-color: white;
  padding: 10px 15px;
  border-radius: 8px;
  word-wrap: break-word;
  white-space: pre-wrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  line-height: 1.5;
}

.send-area {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #e4e7ed;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.send-area .el-input {
  flex: 1;
}

.send-area .el-button {
  flex-shrink: 0;
}

/* 滾動條樣式 */
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background-color: #c0c4cc;
}
</style>
