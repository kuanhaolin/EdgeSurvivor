import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    isLoading: false,
    showChat: false,
    notifications: []
  }),
  
  actions: {
    setLoading(loading) {
      this.isLoading = loading
    },
    
    toggleChat() {
      this.showChat = !this.showChat
    },
    
    showChatWindow() {
      this.showChat = true
    },
    
    hideChatWindow() {
      this.showChat = false
    },
    
    addNotification(notification) {
      this.notifications.push({
        id: Date.now(),
        ...notification
      })
    },
    
    removeNotification(id) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index > -1) {
        this.notifications.splice(index, 1)
      }
    },
    
    clearNotifications() {
      this.notifications = []
    }
  }
})