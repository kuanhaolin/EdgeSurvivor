# 9. Socket.IO 整合 (services/socket.js)

```javascript
import { io } from 'socket.io-client'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { ElNotification } from 'element-plus'

class SocketService {
  constructor() {
    this.socket = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
  }

  /**
   * 連接到 Socket.IO 伺服器
   */
  connect() {
    const authStore = useAuthStore()
    
    if (!authStore.accessToken) {
      console.warn('無法連接 Socket: 缺少認證 Token')
      return
    }

    const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'

    this.socket = io(socketUrl, {
      auth: {
        token: authStore.accessToken
      },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: this.maxReconnectAttempts
    })

    this.setupEventHandlers()
  }

  /**
   * 設置事件處理器
   */
  setupEventHandlers() {
    const appStore = useAppStore()

    // 連接成功
    this.socket.on('connect', () => {
      console.log('Socket 已連接:', this.socket.id)
      this.reconnectAttempts = 0
    })

    // 連接錯誤
    this.socket.on('connect_error', (error) => {
      console.error('Socket 連接錯誤:', error)
      this.reconnectAttempts++

      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        ElNotification({
          title: '連線失敗',
          message: '無法連接到伺服器，請稍後再試',
          type: 'error'
        })
      }
    })

    // 斷開連接
    this.socket.on('disconnect', (reason) => {
      console.log('Socket 已斷開:', reason)
      
      if (reason === 'io server disconnect') {
        // 伺服器主動斷開，需要手動重連
        this.socket.connect()
      }
    })

    // 重連
    this.socket.on('reconnect', (attemptNumber) => {
      console.log('Socket 重連成功:', attemptNumber)
      ElNotification({
        title: '連線恢復',
        message: '已重新連接到伺服器',
        type: 'success'
      })
    })

    // 新訊息通知
    this.socket.on('new_message', (data) => {
      console.log('收到新訊息:', data)
      appStore.addNotification({
        type: 'message',
        title: '新訊息',
        message: `${data.sender_name}: ${data.message}`,
        data: data
      })
    })

    // 活動更新通知
    this.socket.on('activity_update', (data) => {
      console.log('活動更新:', data)
      appStore.addNotification({
        type: 'activity',
        title: '活動更新',
        message: data.message,
        data: data
      })
    })
  }

  /**
   * 加入聊天室
   */
  joinRoom(roomId) {
    if (!this.socket) {
      console.warn('Socket 未連接')
      return
    }

    this.socket.emit('join', { room: roomId })
    console.log('加入聊天室:', roomId)
  }

  /**
   * 離開聊天室
   */
  leaveRoom(roomId) {
    if (!this.socket) return

    this.socket.emit('leave', { room: roomId })
    console.log('離開聊天室:', roomId)
  }

  /**
   * 發送訊息
   */
  sendMessage(roomId, message) {
    if (!this.socket) {
      console.warn('Socket 未連接')
      return
    }

    return new Promise((resolve, reject) => {
      this.socket.emit('send_message', {
        room: roomId,
        message: message
      }, (response) => {
        if (response.success) {
          resolve(response)
        } else {
          reject(new Error(response.error || '發送失敗'))
        }
      })
    })
  }

  /**
   * 監聽事件
   */
  on(event, callback) {
    if (!this.socket) return

    this.socket.on(event, callback)
  }

  /**
   * 移除事件監聽
   */
  off(event, callback) {
    if (!this.socket) return

    this.socket.off(event, callback)
  }

  /**
   * 斷開連接
   */
  disconnect() {
    if (!this.socket) return

    this.socket.disconnect()
    this.socket = null
    console.log('Socket 已手動斷開')
  }

  /**
   * 檢查連接狀態
   */
  isConnected() {
    return this.socket && this.socket.connected
  }
}

// 導出單例
export default new SocketService()
```

---
