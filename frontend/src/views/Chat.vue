<template>
  <div class="chat">
    <NavBar />
    
    <div class="chat-container">
      <el-row :gutter="20" class="chat-row">
        <!-- 聊天列表 -->
        <el-col :xs="24" :md="8" class="chat-list-col" :class="{ 'mobile-hidden': !showChatList && isMobile }">
          <el-card class="chat-list-card">
            <template #header>
              <div class="chat-list-header">
                <span>聊天列表</span>
                <el-badge :value="unreadCount" :hidden="unreadCount === 0" />
              </div>
            </template>
            
            <el-input
              v-model="searchQuery"
              placeholder="搜尋聊天"
              clearable
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
            <el-scrollbar height="calc(100vh - 280px)">
              <div
                v-for="chat in filteredChats"
                :key="chat.id"
                class="chat-item"
                :class="{ active: selectedChat?.id === chat.id }"
                @click="selectChat(chat)"
              >
                <el-badge :value="chat.unreadCount" :hidden="chat.unreadCount === 0">
                  <el-avatar :size="50" :src="chat.avatar" />
                </el-badge>
                <div class="chat-item-content">
                  <div class="chat-item-header">
                    <div class="chat-name-line">
                      <span class="chat-name">{{ chat.name }}</span>
                      <el-tag
                        v-if="!chat.matchId"
                        size="small"
                        type="warning"
                        effect="plain"
                        class="stranger-tag"
                      >
                        陌生
                      </el-tag>
                    </div>
                    <span class="chat-time">{{ chat.lastMessageTime }}</span>
                  </div>
                  <div class="chat-last-message">{{ chat.lastMessage }}</div>
                </div>
              </div>
              
              <el-empty v-if="filteredChats.length === 0" description="沒有聊天記錄" />
            </el-scrollbar>
          </el-card>
        </el-col>
        
        <!-- 聊天窗口 -->
        <el-col :xs="24" :md="16" class="chat-window-col" :class="{ 'mobile-hidden': showChatList && isMobile }">
          <el-card v-if="selectedChat" class="chat-window-card">
            <template #header>
              <div class="chat-window-header">
                <div class="chat-user-info">
                  <el-button 
                    v-if="isMobile" 
                    text 
                    class="back-to-list-btn"
                    @click="showChatList = true"
                  >
                    <el-icon><ArrowLeft /></el-icon>
                  </el-button>
                  <el-avatar :size="40" :src="selectedChat.avatar" />
                  <div class="user-info">
                    <span class="user-name">{{ selectedChat.name }}</span>
                    <span class="user-status" :class="{ online: selectedChat.online }">
                      {{ selectedChat.online ? '在線' : '離線' }}
                    </span>
                  </div>
                </div>
                <el-button-group>
                  <el-button size="small" @click="viewUserProfile">
                    <el-icon><User /></el-icon>
                    查看資料
                  </el-button>
                  <el-button size="small" @click="viewActivityDetails">
                    <el-icon><Calendar /></el-icon>
                    活動詳情
                  </el-button>
                </el-button-group>
              </div>
            </template>
            
            <!-- 陌生訊息提示（非好友對話） -->
            <el-alert
              v-if="selectedChat && !selectedChat.matchId"
              title="陌生訊息"
              type="info"
              :closable="false"
              show-icon
              style="margin-bottom: 10px;"
            >
              此對象尚未成為好友，該對話將歸類為陌生訊息。
            </el-alert>

            <!-- 訊息列表 -->
            <el-scrollbar ref="messageScrollbar" height="calc(100vh - 400px)" class="message-list">
              <div
                v-for="message in messages"
                :key="message.id"
                class="message-item"
                :class="{ 'is-mine': message.isMine }"
              >
                <el-avatar v-if="!message.isMine" :size="35" :src="selectedChat.avatar" />
                <div class="message-content">
                  <div v-if="message.type === 'text'" class="message-bubble">
                    {{ message.content }}
                  </div>
                  <div v-else-if="message.type === 'image'" class="message-image-container">
                    <el-image 
                      :src="message.content" 
                      fit="cover" 
                      :preview-src-list="[message.content]"
                      :initial-index="0"
                      preview-teleported
                      class="message-image"
                    />
                    <el-button
                      size="small"
                      type="primary"
                      class="save-image-btn"
                      @click.stop="saveImage(message.content)"
                    >
                      <el-icon><Download /></el-icon>
                      儲存
                    </el-button>
                  </div>
                  <span class="message-time">{{ message.time }}</span>
                </div>
              </div>
            </el-scrollbar>
            
            <!-- 輸入框 -->
            <div class="message-input-area">
              <el-input
                v-model="messageInput"
                type="textarea"
                :rows="3"
                placeholder="輸入訊息... (Ctrl+Enter 發送)"
                @keydown.ctrl.enter="sendMessage"
              />
              
              <!-- 表情選擇器 -->
              <div v-if="showEmojiPicker" class="emoji-picker">
                <div class="emoji-grid">
                  <span
                    v-for="emoji in emojis"
                    :key="emoji"
                    class="emoji-item"
                    @click="selectEmoji(emoji)"
                  >
                    {{ emoji }}
                  </span>
                </div>
              </div>
              
              <div class="input-actions">
                <el-button-group>
                  <el-button size="small" @click="showEmojiPicker = !showEmojiPicker">
                    <el-icon><ChatDotRound /></el-icon>
                    表情
                  </el-button>
                  <el-button size="small" @click="selectImage">
                    <el-icon><Picture /></el-icon>
                    圖片
                  </el-button>
                </el-button-group>
                <el-button type="primary" @click="sendMessage">
                  發送
                  <el-icon><Promotion /></el-icon>
                </el-button>
              </div>
              
              <!-- 隱藏的文件輸入 -->
              <input
                ref="imageInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleImageSelect"
              />
            </div>
          </el-card>
          
          <!-- 未選擇聊天時的提示 -->
          <el-card v-else class="chat-window-card">
            <el-empty description="請選擇一個聊天開始對話" />
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 共同參與的活動對話框 -->
    <el-dialog
      v-model="showActivityDialog"
      title="共同參與的活動"
      width="600px"
    >
      <el-space direction="vertical" style="width: 100%">
        <el-card
          v-for="activity in sharedActivities"
          :key="activity.activity_id"
          shadow="hover"
          class="activity-card"
          @click="goToActivity(activity.activity_id)"
        >
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <h3>{{ activity.title }}</h3>
              <p style="color: #909399; margin: 5px 0;">
                <el-icon><Calendar /></el-icon>
                {{ activity.date ? new Date(activity.date).toLocaleDateString('zh-TW') : '待定' }}
              </p>
              <p style="color: #909399; margin: 5px 0;">
                <el-icon><Location /></el-icon>
                {{ activity.location }}
              </p>
            </div>
            <el-tag :type="getActivityStatusType(activity.status)">
              {{ getActivityStatusText(activity.status) }}
            </el-tag>
          </div>
        </el-card>
      </el-space>
      
      <template #footer>
        <el-button @click="showActivityDialog = false">關閉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search,
  User,
  Calendar,
  ChatDotRound,
  Picture,
  Promotion,
  Location,
  ArrowLeft,
  Download
} from '@element-plus/icons-vue'
import NavBar from '@/components/NavBar.vue'
import axios from '@/utils/axios'
import socketService from '@/services/socket'

const router = useRouter()
const route = useRoute()

// 手機版顯示控制
const isMobile = ref(false)
const showChatList = ref(true) // 手機版預設顯示聊天列表

// 檢測是否為手機版
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
  // 如果是手機版且沒有選擇聊天，顯示列表
  if (isMobile.value && !selectedChat.value) {
    showChatList.value = true
  }
}

// 搜尋
const searchQuery = ref('')

// 聊天列表
const chats = ref([])

// 已選擇的聊天
const selectedChat = ref(null)

// 訊息列表
const messages = ref([])

// 訊息輸入
const messageInput = ref('')

// 訊息滾動容器
const messageScrollbar = ref(null)

// 載入聊天列表
const loadConversations = async () => {
  try {
    const response = await axios.get('/chat/conversations')
    
    if (response.data && response.data.conversations) {
      chats.value = response.data.conversations.map(conv => {
        console.log('📋 聊天對話:', {
          userId: conv.other_user.user_id,
          name: conv.other_user.name,
          matchId: conv.match_id,
          hasMatch: !!conv.match_id
        })
        
        return {
          id: conv.other_user.user_id,
          matchId: conv.match_id,
          activityId: conv.activity_id,
          name: conv.other_user.name,
          avatar: conv.other_user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          lastMessage: conv.last_message?.content || '開始聊天吧',
          lastMessageTime: conv.last_message ? formatTime(conv.last_message.created_at) : '',
          unreadCount: conv.unread_count || 0,
          online: conv.other_user.is_online || false
        }
      })
    }
  } catch (error) {
    console.error('載入聊天列表失敗:', error)
    if (error.response?.status === 401) {
      ElMessage.error('登入已過期，請重新登入')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
  }
}

// 載入聊天訊息
const loadMessages = async (userId) => {
  try {
    const response = await axios.get(`/chat/${userId}/messages`)
    
    if (response.data && response.data.messages) {
      const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
      messages.value = response.data.messages.map(msg => {
        let content = msg.content
        
        // 如果是圖片訊息且 URL 是相對路徑，轉換為完整 URL
        if (msg.message_type === 'image' && content && !content.startsWith('http')) {
          content = `${window.location.origin}${content}`
        }
        
        return {
          id: msg.message_id,
          type: msg.message_type || 'text',
          content: content,
          time: formatTime(msg.created_at),
          isMine: msg.sender_id === currentUserId
        }
      })
    } else {
      // 沒有訊息記錄時，設為空陣列
      messages.value = []
    }
    
    // 滾動到底部
    nextTick(() => {
      if (messageScrollbar.value) {
        messageScrollbar.value.setScrollTop(999999)
      }
    })
  } catch (error) {
    console.error('載入訊息失敗:', error)
    // 發生錯誤時也設為空陣列，這樣可以開始新聊天
    messages.value = []
  }
}

// 標記與指定用戶的對話為已讀（用於沒有 matchId 的情況，例如尚未成為好友）
const markMessagesAsRead = async (userId) => {
  try {
    await axios.put(`/chat/conversations/${userId}/read`)
    // 無需額外處理，UI 端已在 selectChat 時將未讀數設為 0
  } catch (error) {
    console.error('REST 標記對話已讀失敗:', error)
  }
}

// 格式化時間
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 86400000) { // 24小時內
    return date.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' })
  } else if (diff < 172800000) { // 48小時內
    return '昨天'
  } else {
    return date.toLocaleDateString('zh-TW', { month: '2-digit', day: '2-digit' })
  }
}

// 未讀數量
const unreadCount = computed(() => {
  return chats.value.reduce((sum, chat) => sum + chat.unreadCount, 0)
})

// 過濾後的聊天列表
const filteredChats = computed(() => {
  if (!searchQuery.value) return chats.value
  
  return chats.value.filter(chat =>
    chat.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 選擇聊天
const selectChat = async (chat) => {
  // 如果之前有選擇的聊天，先離開
  if (selectedChat.value && selectedChat.value.matchId) {
    const currentUser = JSON.parse(localStorage.getItem('user'))
    socketService.leaveChat(selectedChat.value.matchId, currentUser.user_id)
  }
  
  selectedChat.value = chat
  // 清除未讀數
  chat.unreadCount = 0
  
  // 手機版：選擇聊天後隱藏列表，顯示聊天窗口
  if (isMobile.value) {
    showChatList.value = false
  }
  
  // 載入訊息
  loadMessages(chat.id)
  
  // 加入新的聊天室（使用 user_id 或 matchId）
  if (socketService.isConnected()) {
    const currentUser = JSON.parse(localStorage.getItem('user'))
    const roomId = chat.matchId || chat.id // 優先使用 matchId，否則使用 user_id
    
    console.log('🔵 準備加入聊天室:', {
      roomId,
      isMatch: !!chat.matchId,
      userId: currentUser.user_id,
      isConnected: socketService.isConnected()
    })
    
    socketService.joinChat(roomId, currentUser.user_id)
    
    // 標記為已讀
    if (chat.matchId) {
      socketService.markAsRead(chat.matchId, currentUser.user_id)
    } else {
      // 對於沒有 matchId 的對話（非好友），通過 REST API 標記已讀
      try {
        await markMessagesAsRead(chat.id)
      } catch (error) {
        console.error('標記訊息為已讀失敗:', error)
      }
    }
  } else {
    console.log('⚠️ Socket.IO 未連線')
  }
}

// 發送訊息
const sendMessage = async () => {
  if (!messageInput.value.trim()) {
    ElMessage.warning('請輸入訊息內容')
    return
  }
  
  if (!selectedChat.value) {
    ElMessage.warning('請選擇聊天對象')
    return
  }
  
  try {
    const currentUser = JSON.parse(localStorage.getItem('user'))
    
    const roomId = selectedChat.value.matchId || selectedChat.value.id
    
    console.log('🔍 檢查發送條件:', {
      isConnected: socketService.isConnected(),
      matchId: selectedChat.value.matchId,
      userId: selectedChat.value.id,
      roomId,
      chatObject: selectedChat.value
    })
    
    // 優先使用 Socket.IO 發送（使用 roomId：matchId 或 userId）
    if (socketService.isConnected()) {
      console.log('🟢 使用 Socket.IO 發送訊息:', {
        roomId,
        isMatch: !!selectedChat.value.matchId,
        content: messageInput.value
      })
      
      const sent = await socketService.sendMessage(
        roomId,
        currentUser.user_id,
        messageInput.value,
        'text'
      )

      console.log('✅ 服務器回應:', sent)

      // Server acknowledged and returned message data (sent)
      // Optimistically add to local message list if not already present.
      if (sent && sent.message_id) {
        const exists = messages.value.some(m => m.id === sent.message_id)
        if (!exists) {
          console.log('📝 樂觀更新：添加訊息到本地列表')
          messages.value.push({
            id: sent.message_id,
            type: sent.message_type || 'text',
            content: sent.content || messageInput.value,
            time: formatTime(sent.timestamp || new Date().toISOString()),
            isMine: true
          })
          
          // 滾動到底部
          nextTick(() => {
            if (messageScrollbar.value) {
              messageScrollbar.value.setScrollTop(999999)
            }
          })
        } else {
          console.log('⚠️ 訊息已存在，跳過添加')
        }
      }

      // 清空輸入框
      messageInput.value = ''
      
    } else {
      // 降級到 HTTP API
      const response = await axios.post('/chat/messages', {
        receiver_id: selectedChat.value.id,
        content: messageInput.value
      })
      
      if (response.data && response.data.message) {
        const newMessage = {
          id: response.data.message.message_id,
          type: 'text',
          content: messageInput.value,
          time: new Date().toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' }),
          isMine: true
        }
        
        messages.value.push(newMessage)
        messageInput.value = ''
        
        // 更新聊天列表中的最後訊息
        const chatIndex = chats.value.findIndex(c => c.id === selectedChat.value.id)
        if (chatIndex !== -1) {
          chats.value[chatIndex].lastMessage = newMessage.content
          chats.value[chatIndex].lastMessageTime = newMessage.time
        }
        
        // 滾動到底部
        nextTick(() => {
          if (messageScrollbar.value) {
            messageScrollbar.value.setScrollTop(999999)
          }
        })
      }
    }
  } catch (error) {
    console.error('發送訊息失敗:', error)
    ElMessage.error('發送訊息失敗')
  }
}

// 組件掛載時載入聊天列表
onMounted(async () => {
  // 檢測螢幕尺寸
  checkMobile()
  window.addEventListener('resize', checkMobile)
  
  await loadConversations()
  
  // 連線到 Socket.IO
  socketService.connect()
  
  // 監聽新訊息
  socketService.onNewMessage((message) => {
    console.log('📨 收到即時訊息:', message)
    console.log('當前聊天室:', selectedChat.value?.matchId, '訊息來自:', message.match_id)

    // 防止重複推入相同 message_id
    if (messages.value.some(m => m.id === message.message_id)) {
      console.log('⚠️ 訊息已存在（去重）:', message.message_id)
      return
    }

    // 如果是當前聊天室的訊息，添加到訊息列表
    if (selectedChat.value && message.match_id === selectedChat.value.matchId) {
      console.log('✅ 添加訊息到當前聊天室')
      const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
      
      // 如果是圖片訊息且 URL 是相對路徑，轉換為完整 URL
      let content = message.content
      if (message.message_type === 'image' && content && !content.startsWith('http')) {
        content = `${window.location.origin}${content}`
      }
      
      messages.value.push({
        id: message.message_id,
        type: message.message_type,
        content: content,
        time: formatTime(message.timestamp),
        isMine: message.sender_id === currentUserId
      })

      // 滾動到底部
      nextTick(() => {
        if (messageScrollbar.value) {
          messageScrollbar.value.setScrollTop(999999)
        }
      })
    } else {
      console.log('ℹ️ 訊息不屬於當前聊天室，僅更新列表')
    }

    // 更新聊天列表中的最後訊息（使用 matchId 或通過 sender_id/receiver_id 查找）
    let chatIndex = chats.value.findIndex(c => c.matchId === message.match_id)
    
    // 如果通過 matchId 找不到，嘗試通過 sender_id 查找（陌生訊息）
    if (chatIndex === -1) {
      const currentUserId = JSON.parse(localStorage.getItem('user')).user_id
      const otherUserId = message.sender_id === currentUserId ? message.receiver_id : message.sender_id
      chatIndex = chats.value.findIndex(c => c.id === otherUserId)
    }
    
    if (chatIndex > -1) {
      chats.value[chatIndex].lastMessage = message.content
      chats.value[chatIndex].lastMessageTime = formatTime(message.timestamp)

      // 如果不是當前聊天，增加未讀數
      const currentRoomId = selectedChat.value?.matchId || selectedChat.value?.id
      const messageRoomId = message.match_id || message.sender_id
      if (!selectedChat.value || currentRoomId !== messageRoomId) {
        chats.value[chatIndex].unreadCount = (chats.value[chatIndex].unreadCount || 0) + 1
      }
    }
  })
  
  // 監聽輸入狀態
  let typingTimeout = null
  socketService.onUserTyping((data) => {
    if (selectedChat.value && data.user_id !== JSON.parse(localStorage.getItem('user')).user_id) {
      // 顯示輸入提示
      console.log('對方正在輸入...', data.is_typing)
      
      if (typingTimeout) {
        clearTimeout(typingTimeout)
      }
      
      if (data.is_typing) {
        typingTimeout = setTimeout(() => {
          // 3秒後自動隱藏
        }, 3000)
      }
    }
  })
  
  // 監聽用戶上線/離線狀態
  socketService.on('user_status_change', (data) => {
    console.log('用戶狀態變更:', data)
    // 更新聊天列表中的在線狀態
    const chatIndex = chats.value.findIndex(c => c.id === data.user_id)
    if (chatIndex > -1) {
      chats.value[chatIndex].online = data.online
    }
    
    // 如果是當前聊天對象，也更新
    if (selectedChat.value && selectedChat.value.id === data.user_id) {
      selectedChat.value.online = data.online
    }
  })
  
  // 如果 URL 中有 userId 參數，自動選擇該用戶
  const userIdParam = route.query.userId
  if (userIdParam) {
    const userId = parseInt(userIdParam)
    
    // 先檢查聊天列表中是否已有該用戶
    let chat = chats.value.find(c => c.id === userId)
    
    if (chat) {
      // 如果已存在，直接選擇
      selectChat(chat)
    } else {
      // 如果不存在，創建新的聊天
      try {
        const response = await axios.get(`/users/${userId}`)
        if (response.data && response.data.user) {
          const user = response.data.user
          chat = {
            id: user.user_id,
            name: user.name,
            avatar: user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
            lastMessage: '開始聊天吧',
            lastMessageTime: '',
            unreadCount: 0,
            online: false
          }
          
          // 添加到聊天列表
          chats.value.unshift(chat)
          
          // 選擇該聊天
          selectChat(chat)
        }
      } catch (error) {
        console.error('載入用戶資料失敗:', error)
        ElMessage.error('無法開始聊天')
      }
    }
  }
})

// 組件卸載時斷開連線
onUnmounted(() => {
  // 移除 resize 監聽器
  window.removeEventListener('resize', checkMobile)
  
  // 如果有選擇的聊天，離開聊天室
  if (selectedChat.value && selectedChat.value.matchId) {
    const currentUser = JSON.parse(localStorage.getItem('user'))
    socketService.leaveChat(selectedChat.value.matchId, currentUser.user_id)
  }
  
  // 斷開 Socket.IO 連線（可選，如果其他頁面也需要則不斷開）
  // socketService.disconnect()
})

// 選擇表情
const showEmojiPicker = ref(false)
const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😊', '😇', 
  '🥰', '😍', '🤩', '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪', '😝', '🤑', '🤗', '🤭', 
  '🤫', '🤔', '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪',
  '👍', '👎', '👌', '✌️', '🤞', '🤟', '🤘', '🤙', '👏', '🙌', '👐', '🤲', '🙏', '✨', '🎉',
  '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗']

const selectEmoji = (emoji) => {
  messageInput.value += emoji
  showEmojiPicker.value = false
}

// 選擇圖片
const imageInput = ref(null)

const selectImage = () => {
  imageInput.value?.click()
}

const handleImageSelect = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    ElMessage.error('請選擇圖片檔案')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('圖片大小不能超過 5MB')
    return
  }

  try {
    // 上傳圖片到服務器
    const formData = new FormData()
    formData.append('image', file)
    
    const response = await axios.post('/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data && response.data.url) {
      // 將相對路徑轉換為完整 URL
      const imageUrl = response.data.url.startsWith('http') 
        ? response.data.url 
        : `${window.location.origin}${response.data.url}`
      
      // 如果已選擇聊天，直接發送圖片
      if (selectedChat.value) {
        await sendImageMessage(imageUrl)
      } else {
        ElMessage.warning('請先選擇聊天對象')
      }
    } else {
      ElMessage.error('圖片上傳失敗')
    }
  } catch (error) {
    console.error('上傳圖片失敗:', error)
    ElMessage.error(error.response?.data?.error || '圖片上傳失敗')
  }
  
  // 清空 input
  event.target.value = ''
}

// 發送圖片訊息
const sendImageMessage = async (imageUrl) => {
  if (!selectedChat.value) {
    ElMessage.warning('請選擇聊天對象')
    return
  }
  
  try {
    const currentUser = JSON.parse(localStorage.getItem('user'))
    const roomId = selectedChat.value.matchId || selectedChat.value.id
    
    // 使用 Socket.IO 發送圖片訊息
    if (socketService.isConnected()) {
      const sent = await socketService.sendMessage(
        roomId,
        currentUser.user_id,
        imageUrl,
        'image'
      )
      
      if (sent && sent.message_id) {
        const exists = messages.value.some(m => m.id === sent.message_id)
        if (!exists) {
          messages.value.push({
            id: sent.message_id,
            type: 'image',
            content: imageUrl,
            time: formatTime(sent.timestamp || new Date().toISOString()),
            isMine: true
          })
          
          // 滾動到底部
          nextTick(() => {
            if (messageScrollbar.value) {
              messageScrollbar.value.setScrollTop(999999)
            }
          })
        }
      }
    } else {
      // 降級到 HTTP API
      const response = await axios.post('/chat/messages', {
        receiver_id: selectedChat.value.id,
        content: imageUrl,
        message_type: 'image'
      })
      
      if (response.data && response.data.message) {
        const newMessage = {
          id: response.data.message.message_id,
          type: 'image',
          content: imageUrl,
          time: new Date().toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' }),
          isMine: true
        }
        
        messages.value.push(newMessage)
        
        // 更新聊天列表中的最後訊息
        const chatIndex = chats.value.findIndex(c => c.id === selectedChat.value.id)
        if (chatIndex !== -1) {
          chats.value[chatIndex].lastMessage = '[圖片]'
          chats.value[chatIndex].lastMessageTime = newMessage.time
        }
        
        // 滾動到底部
        nextTick(() => {
          if (messageScrollbar.value) {
            messageScrollbar.value.setScrollTop(999999)
          }
        })
      }
    }
    
    ElMessage.success('圖片已發送')
  } catch (error) {
    console.error('發送圖片失敗:', error)
    ElMessage.error('發送圖片失敗')
  }
}

// 儲存圖片
const saveImage = async (imageUrl) => {
  try {
    // 如果是相對路徑，轉換為完整 URL
    let fullUrl = imageUrl
    if (imageUrl.startsWith('/')) {
      fullUrl = `${window.location.origin}${imageUrl}`
    }
    
    // 下載圖片
    const response = await fetch(fullUrl)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `image_${Date.now()}.${blob.type.split('/')[1] || 'jpg'}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('圖片已儲存')
  } catch (error) {
    console.error('儲存圖片失敗:', error)
    ElMessage.error('儲存圖片失敗')
  }
}

// 查看用戶資料（導航到公開資料頁面）
const viewUserProfile = () => {
  if (!selectedChat.value) {
    ElMessage.warning('請先選擇聊天對象')
    return
  }

  // 導航到公開用戶資料頁面
  router.push(`/user/${selectedChat.value.id}`)
}

// 查看活動詳情
const showActivityDialog = ref(false)
const sharedActivities = ref([])

const viewActivityDetails = async () => {
  if (!selectedChat.value) {
    ElMessage.warning('請先選擇聊天對象')
    return
  }
  
  try {
    // 首先檢查當前對話是否有關聯活動
    const activityId = selectedChat.value.activityId
    
    if (activityId) {
      // 如果有關聯活動，直接跳轉
      router.push(`/activities/${activityId}`)
      return
    }
    
    // 如果沒有關聯活動，查詢共同參與的活動
    const response = await axios.get(`/chat/shared-activities/${selectedChat.value.id}`)
    
    if (response.data.shared_activities && response.data.shared_activities.length > 0) {
      sharedActivities.value = response.data.shared_activities
      showActivityDialog.value = true
    } else {
      ElMessage.info('您與此用戶沒有共同參與的活動')
    }
  } catch (error) {
    console.error('無法查看活動詳情:', error)
    ElMessage.error('無法查看活動詳情')
  }
}

// 跳轉到活動詳情
const goToActivity = (activityId) => {
  showActivityDialog.value = false
  router.push(`/activities/${activityId}`)
}

// 活動狀態輔助函數
const getActivityStatusType = (status) => {
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

const getActivityStatusText = (status) => {
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
  return texts[status] || status
}
</script>

<style scoped>
.chat {
  min-height: 100vh;
  min-height: -webkit-fill-available;
  background-color: #f5f7fa;
}

.chat-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.chat-row {
  height: calc(100vh - 100px);
  position: relative;
}

.chat-list-card,
.chat-window-card {
  height: 100%;
}

.chat-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  margin-bottom: 15px;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.chat-item:hover {
  background-color: #f5f7fa;
}

.chat-item.active {
  background-color: #ecf5ff;
}

.chat-item-content {
  flex: 1;
  overflow: hidden;
}

.chat-item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.chat-name-line {
  display: flex;
  align-items: center;
  gap: 6px;
}

.chat-name {
  font-weight: bold;
  font-size: 15px;
}

.stranger-tag {
  margin-left: 4px;
}

.chat-time {
  font-size: 12px;
  color: #909399;
}

.chat-last-message {
  font-size: 13px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-window-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: bold;
  font-size: 16px;
}

.user-status {
  font-size: 12px;
  color: #909399;
}

.user-status.online {
  color: #67c23a;
}

.message-list {
  padding: 20px;
}

.message-item {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.message-item.is-mine {
  flex-direction: row-reverse;
}

.message-content {
  display: flex;
  flex-direction: column;
  max-width: 60%;
}

.message-item.is-mine .message-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  word-break: break-word;
}

.message-item.is-mine .message-bubble {
  background-color: #409eff;
  color: #fff;
}

.message-image-container {
  position: relative;
  display: inline-block;
}

.message-image {
  max-width: 300px;
  max-height: 300px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.message-image:hover {
  transform: scale(1.02);
}

.save-image-btn {
  position: absolute;
  bottom: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.message-image-container:hover .save-image-btn {
  opacity: 1;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.message-input-area {
  margin-top: 15px;
  border-top: 1px solid #dcdfe6;
  padding-top: 15px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.emoji-picker {
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.emoji-item {
  font-size: 24px;
  cursor: pointer;
  text-align: center;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.emoji-item:hover {
  background-color: #f5f7fa;
}

.activity-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.activity-card:hover {
  transform: translateY(-2px);
}

.activity-card h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

/* 手機版響應式 */
@media (max-width: 768px) {
  .chat-container {
    padding: 0;
  }
  
  .chat-row {
    height: calc(100vh - 70px);
    margin: 0;
    position: relative;
    overflow: hidden;
  }
  
  .chat-list-col,
  .chat-window-col {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
  }
  
  .chat-list-col.mobile-hidden {
    transform: translateX(-100%);
    z-index: 0;
  }
  
  .chat-window-col.mobile-hidden {
    transform: translateX(100%);
    z-index: 0;
  }
  
  .chat-list-card,
  .chat-window-card {
    border-radius: 0;
    height: 100%;
    box-shadow: none;
  }
  
  .chat-list-card :deep(.el-card__body) {
    padding: 10px;
    height: calc(100% - 60px);
    display: flex;
    flex-direction: column;
  }
  
  .back-to-list-btn {
    margin-right: 8px;
    padding: 8px;
    color: #409eff;
  }
  
  .message-content {
    max-width: 80%;
  }
  
  .chat-window-header {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .chat-user-info {
    flex: 1;
    min-width: 0;
  }
  
  .chat-window-header .el-button-group {
    width: 100%;
    margin-top: 8px;
  }
  
  .chat-window-header .el-button-group .el-button {
    flex: 1;
  }
  
  .message-list {
    height: calc(100vh - 350px) !important;
  }
  
  .chat-item {
    padding: 15px 12px;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .chat-item:active {
    background-color: #f5f7fa;
  }
}
</style>
