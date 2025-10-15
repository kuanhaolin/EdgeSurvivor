/**
 * Socket.IO 客戶端服務
 * 處理與後端的即時通訊連線
 */
import { io } from 'socket.io-client'
import { ElMessage } from 'element-plus'

class SocketService {
  constructor() {
    this.socket = null
    this.connected = false
    this.listeners = new Map()
  }

  /**
   * 連線到 Socket.IO 伺服器
   */
  connect() {
    if (this.connected) {
      console.log('Socket.IO 已連線')
      return
    }

    // 從 localStorage 獲取 token
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('無法連線 Socket.IO: 缺少認證 token')
      return
    }

    // 在 Docker 環境中使用相對路徑，讓 Vite proxy 處理
    // 在生產環境使用當前 origin
    const SOCKET_URL = import.meta.env.DEV 
      ? window.location.origin  // 使用當前 origin，讓 proxy 轉發
      : window.location.origin

    console.log('正在連線到 Socket.IO...', SOCKET_URL)

    this.socket = io(SOCKET_URL, {
      auth: {
        token: token
      },
      path: '/socket.io',  // 明確指定 Socket.IO 路徑
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    })

    // 連線成功
    this.socket.on('connect', () => {
      this.connected = true
      console.log('✅ Socket.IO 連線成功', this.socket.id)
      // 靜默連線，不顯示提示
    })

    // 連線錯誤
    this.socket.on('connect_error', (error) => {
      console.error('❌ Socket.IO 連線錯誤:', error)
      this.connected = false
      // 靜默處理，不顯示錯誤提示
    })

    // 斷線
    this.socket.on('disconnect', (reason) => {
      this.connected = false
      console.log('Socket.IO 已斷線:', reason)
      
      if (reason === 'io server disconnect') {
        // 伺服器主動斷線，需要手動重連
        this.socket.connect()
      }
    })

    // 重新連線
    this.socket.on('reconnect', (attemptNumber) => {
      this.connected = true
      console.log('Socket.IO 重新連線成功', attemptNumber)
      // 靜默重連，不顯示提示
    })

    // 重新連線失敗
    this.socket.on('reconnect_failed', () => {
      console.error('Socket.IO 重新連線失敗')
      // 僅在控制台記錄，不打擾用戶
    })

    // 用戶上線/離線事件
    this.socket.on('user_online', (data) => {
      console.log('用戶上線:', data.user_id)
      this.emit('user_status_change', { user_id: data.user_id, online: true })
    })

    this.socket.on('user_offline', (data) => {
      console.log('用戶離線:', data.user_id)
      this.emit('user_status_change', { user_id: data.user_id, online: false })
    })
  }

  /**
   * 斷開連線
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.connected = false
      console.log('Socket.IO 已手動斷線')
    }
  }

  /**
   * 加入聊天室
   */
  joinChat(matchId, userId) {
    if (!this.socket || !this.connected) {
      console.error('Socket.IO 未連線')
      return
    }

    console.log(`加入聊天室: chat_${matchId}`)
    
    this.socket.emit('join_chat', {
      match_id: matchId,
      user_id: userId
    }, (response) => {
      if (response?.error) {
        console.error('加入聊天室失敗:', response.error)
        ElMessage.error('加入聊天室失敗')
      } else {
        console.log('成功加入聊天室:', response)
      }
    })
  }

  /**
   * 離開聊天室
   */
  leaveChat(matchId, userId) {
    if (!this.socket || !this.connected) return

    console.log(`離開聊天室: chat_${matchId}`)
    
    this.socket.emit('leave_chat', {
      match_id: matchId,
      user_id: userId
    })
  }

  /**
   * 發送聊天訊息
   */
  sendMessage(matchId, senderId, content, messageType = 'text') {
    if (!this.socket || !this.connected) {
      console.error('Socket.IO 未連線，無法發送訊息')
      return Promise.reject(new Error('Socket.IO 未連線'))
    }

    return new Promise((resolve, reject) => {
      this.socket.emit('send_message', {
        match_id: matchId,
        sender_id: senderId,
        content: content,
        message_type: messageType
      }, (response) => {
        if (response?.error) {
          console.error('發送訊息失敗:', response.error)
          reject(new Error(response.error))
        } else {
          console.log('訊息發送成功:', response)
          resolve(response.message)
        }
      })
    })
  }

  /**
   * 監聽新訊息
   */
  onNewMessage(callback) {
    if (!this.socket) return

    this.socket.on('new_message', (message) => {
      console.log('收到新訊息:', message)
      callback(message)
    })
  }

  /**
   * 發送輸入狀態
   */
  sendTyping(matchId, userId, isTyping) {
    if (!this.socket || !this.connected) return

    this.socket.emit('typing', {
      match_id: matchId,
      user_id: userId,
      is_typing: isTyping
    })
  }

  /**
   * 監聽輸入狀態
   */
  onUserTyping(callback) {
    if (!this.socket) return

    this.socket.on('user_typing', (data) => {
      callback(data)
    })
  }

  /**
   * 加入活動討論室
   */
  joinActivityDiscussion(activityId, userId) {
    if (!this.socket || !this.connected) {
      console.error('Socket.IO 未連線')
      return
    }

    console.log(`加入活動討論室: activity_${activityId}`)
    
    this.socket.emit('join_activity_discussion', {
      activity_id: activityId,
      user_id: userId
    }, (response) => {
      if (response?.error) {
        console.error('加入活動討論室失敗:', response.error)
      } else {
        console.log('成功加入活動討論室:', response)
      }
    })
  }

  /**
   * 離開活動討論室
   */
  leaveActivityDiscussion(activityId) {
    if (!this.socket || !this.connected) return

    console.log(`離開活動討論室: activity_${activityId}`)
    
    this.socket.emit('leave_activity_discussion', {
      activity_id: activityId
    })
  }

  /**
   * 發送活動討論訊息
   */
  sendDiscussion(activityId, userId, message, messageType = 'text') {
    if (!this.socket || !this.connected) {
      console.error('Socket.IO 未連線，無法發送討論')
      return Promise.reject(new Error('Socket.IO 未連線'))
    }

    return new Promise((resolve, reject) => {
      this.socket.emit('send_discussion', {
        activity_id: activityId,
        user_id: userId,
        message: message,
        message_type: messageType
      }, (response) => {
        if (response?.error) {
          console.error('發送討論訊息失敗:', response.error)
          reject(new Error(response.error))
        } else {
          console.log('討論訊息發送成功:', response)
          resolve(response.discussion)
        }
      })
    })
  }

  /**
   * 監聽新討論訊息
   */
  onNewDiscussion(callback) {
    if (!this.socket) return

    this.socket.on('new_discussion', (discussion) => {
      console.log('收到新討論訊息:', discussion)
      callback(discussion)
    })
  }

  /**
   * 標記訊息為已讀
   */
  markAsRead(matchId, userId) {
    if (!this.socket || !this.connected) return

    this.socket.emit('mark_as_read', {
      match_id: matchId,
      user_id: userId
    }, (response) => {
      if (response?.error) {
        console.error('標記已讀失敗:', response.error)
      } else {
        console.log('訊息已標記為已讀')
      }
    })
  }

  /**
   * 監聽訊息已讀事件
   */
  onMessagesRead(callback) {
    if (!this.socket) return

    this.socket.on('messages_read', (data) => {
      console.log('對方已讀訊息:', data)
      callback(data)
    })
  }

  /**
   * 獲取在線用戶列表
   */
  getOnlineUsers() {
    if (!this.socket || !this.connected) {
      return Promise.resolve({ online_users: [] })
    }

    return new Promise((resolve) => {
      this.socket.emit('get_online_users', {}, (response) => {
        resolve(response)
      })
    })
  }

  /**
   * 自定義事件監聽器
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  /**
   * 移除事件監聽器
   */
  off(event, callback) {
    if (!this.listeners.has(event)) return

    const callbacks = this.listeners.get(event)
    const index = callbacks.indexOf(callback)
    if (index > -1) {
      callbacks.splice(index, 1)
    }
  }

  /**
   * 觸發自定義事件
   */
  emit(event, data) {
    if (!this.listeners.has(event)) return

    const callbacks = this.listeners.get(event)
    callbacks.forEach(callback => callback(data))
  }

  /**
   * 檢查連線狀態
   */
  isConnected() {
    return this.connected
  }
}

// 單例模式
const socketService = new SocketService()

export default socketService
