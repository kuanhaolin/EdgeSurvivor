<template>
  <div class="navbar">
    <div class="navbar-brand">
      <el-button text @click="$router.push('/')">
        <span class="logo">EdgeSurvivor</span>
      </el-button>
    </div>
    
    <div class="navbar-nav">
      <el-menu
        mode="horizontal"
        :default-active="$route.path"
        class="navbar-menu"
        router
      >
        <el-menu-item index="/dashboard">控制台</el-menu-item>
        <el-menu-item index="/activities">活動</el-menu-item>
        <el-menu-item index="/matches">交友</el-menu-item>
        <el-menu-item index="/chat">
          聊天
          <el-badge 
            v-if="unreadCount > 0" 
            :value="unreadCount" 
            :max="99"
            class="chat-badge"
          />
        </el-menu-item>
      </el-menu>
    </div>
    
    <div class="navbar-actions">
      <el-dropdown>
        <span class="user-dropdown">
          <el-avatar :size="30" :src="userAvatar" icon="UserFilled" />
          <span class="username">{{ userName }}</span>
          <el-icon><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="$router.push('/profile')">
              個人資料
            </el-dropdown-item>
            <el-dropdown-item divided @click="logout">
              登出
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UserFilled, ArrowDown } from '@element-plus/icons-vue'
import axios from '@/utils/axios'
import socketService from '@/services/socket'

const router = useRouter()

// 未讀訊息數量
const unreadCount = ref(0)

// 獲取用戶信息
const user = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

// 用戶名顯示邏輯
const userName = computed(() => {
  if (!user.value) return '訪客'
  
  // 優先使用名字
  if (user.value.name && user.value.name !== '用戶') {
    return user.value.name
  }
  
  // 從 email 提取
  if (user.value.email) {
    return user.value.email.split('@')[0]
  }
  
  return '旅行者'
})

// 用戶頭像
const userAvatar = computed(() => {
  return user.value?.profile_picture || user.value?.avatar || null
})

// 登出
const logout = async () => {
  try {
    await ElMessageBox.confirm(
      '確定要登出嗎？',
      '提示',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 斷開 Socket.IO 連線
    try {
      socketService.disconnect()
    } catch (error) {
      console.warn('Socket 斷線失敗:', error)
    }
    
    // 清除本地存儲的 token 和用戶資料
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    
    ElMessage.success('登出成功')
    
    // 跳轉到登入頁面
    router.push('/login')
  } catch (error) {
    // 用戶取消登出
    console.log('用戶取消登出')
  }
}

// 載入未讀訊息數量
const loadUnreadCount = async () => {
  try {
    const response = await axios.get('/chat/unread-count')
    if (response.data) {
      unreadCount.value = response.data.unread_count || 0
    }
  } catch (error) {
    console.error('載入未讀數失敗:', error)
  }
}

// 監聽新訊息事件
const setupMessageListener = () => {
  try {
    socketService.onNewMessage((message) => {
      // 如果不是我發送的訊息，增加未讀數
      const currentUserId = user.value?.user_id
      if (message.sender_id !== currentUserId) {
        unreadCount.value++
        
        // 顯示桌面通知 (如果已授權且支援)
        try {
          if (typeof Notification !== 'undefined' && Notification.permission === 'granted') {
            new Notification('新訊息', {
              body: message.content,
              icon: message.sender_avatar || '/logo.png'
            })
          }
        } catch (error) {
          console.warn('通知顯示失敗:', error)
        }
      }
    })
    
    // 監聽訊息已讀事件
    socketService.onMessagesRead(() => {
      // 重新載入未讀數
      loadUnreadCount()
    })
  } catch (error) {
    console.warn('設置訊息監聽失敗:', error)
  }
}

// 組件掛載時
onMounted(() => {
  // 載入未讀數
  loadUnreadCount()
  
  // 使用 try-catch 包裝 Socket.IO 連線，避免 iOS 初始化失敗
  try {
    if (!socketService.isConnected()) {
      socketService.connect()
    }
    setupMessageListener()
  } catch (error) {
    console.warn('Socket.IO 連線失敗 (可能是 iOS):', error)
    // 即使 Socket 失敗，NavBar 也要正常顯示
  }
  
  // 請求桌面通知權限 - iOS Safari 不支援，需要檢查
  try {
    if (typeof Notification !== 'undefined' && Notification.permission === 'default') {
      Notification.requestPermission()
    }
  } catch (error) {
    console.warn('通知權限不支援:', error)
  }
  
  // 每30秒刷新一次未讀數
  const interval = setInterval(loadUnreadCount, 30000)
  
  // 清理定時器
  return () => clearInterval(interval)
})

</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 70px;
  padding: 0 var(--spacing-xl);
  padding-top: env(safe-area-inset-top); /* iOS 安全區域 */
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.9) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky);
  transition: all var(--transition-base);
  /* iOS 修復 */
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.navbar-brand .logo {
  font-size: 24px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.navbar-brand .logo:hover {
  transform: scale(1.05);
  filter: brightness(1.2);
}

.navbar-nav {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
  margin: 0 var(--spacing-lg);
}

.navbar-menu {
  border-bottom: none !important;
  background: transparent !important;
  width: 100%;
}

.navbar-menu .el-menu-item {
  font-weight: 500;
  font-size: 15px;
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  margin: 0 var(--spacing-xs);
  transition: all var(--transition-base);
  position: relative;
  padding: 0 16px !important;
}

.navbar-menu .el-menu-item::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 3px;
  background: var(--gradient-primary);
  border-radius: 3px 3px 0 0;
  transition: width 0.3s ease;
}

.navbar-menu .el-menu-item:hover {
  background: rgba(102, 126, 234, 0.08) !important;
  color: var(--primary-color);
  transform: translateY(-2px);
}

.navbar-menu .el-menu-item:hover::before {
  width: 60%;
}

.navbar-menu .el-menu-item.is-active {
  background: rgba(102, 126, 234, 0.1) !important;
  color: var(--primary-color) !important;
  font-weight: 600;
}

.navbar-menu .el-menu-item.is-active::before {
  width: 80%;
}

.navbar-menu .el-menu-item.is-active::after {
  display: none;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.user-dropdown:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-badge {
  margin-left: var(--spacing-sm);
  position: relative;
  animation: pulse 2s ease-in-out infinite;
}

.chat-badge :deep(.el-badge__content) {
  background: linear-gradient(135deg, #f56c6c, #ef4444);
  border: 2px solid white;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.4);
}

/* 主題切換按鈕 */
.theme-toggle {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: rgba(102, 126, 234, 0.1);
  transition: all var(--transition-base);
  border: none;
  color: var(--primary-color);
}

.theme-toggle:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: rotate(180deg);
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .navbar {
    padding: 0 var(--spacing-md);
  }
  
  .navbar-nav {
    margin: 0 var(--spacing-sm);
  }
  
  .username {
    display: none;
  }
}

@media (max-width: 768px) {
  .navbar {
    height: 60px;
    min-height: calc(60px + env(safe-area-inset-top)); /* iOS 安全區域 */
    padding: 0 var(--spacing-sm);
    padding-top: env(safe-area-inset-top);
    flex-wrap: nowrap;
  }
  
  .navbar-brand .logo {
    font-size: 16px;
  }
  
  .navbar-menu .el-menu-item {
    font-size: 12px;
    padding: 0 8px !important;
    margin: 0 1px;
    min-width: auto;
  }
  
  .navbar-nav {
    margin: 0;
    flex: 1;
    min-width: 0;
  }
  
  .user-dropdown {
    padding: var(--spacing-xs);
    min-width: 40px;
  }
  
  .el-avatar {
    width: 28px !important;
    height: 28px !important;
  }
}

/* 動畫效果 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>