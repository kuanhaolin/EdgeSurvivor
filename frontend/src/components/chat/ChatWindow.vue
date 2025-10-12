<template>
  <div class="chat-window" v-if="visible">
    <el-card class="chat-card">
      <template #header>
        <div class="chat-header">
          <span>聊天室</span>
          <el-button
            :icon="Close"
            @click="closeChat"
            circle
            size="small"
          />
        </div>
      </template>
      
      <div class="chat-content">
        <div class="messages">
          <!-- 聊天訊息列表 -->
          <div class="message">
            <span>聊天功能開發中...</span>
          </div>
        </div>
        
        <div class="chat-input">
          <el-input
            v-model="newMessage"
            placeholder="輸入訊息..."
            @keyup.enter="sendMessage"
          >
            <template #append>
              <el-button @click="sendMessage">
                發送
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Close } from '@element-plus/icons-vue'

export default {
  name: 'ChatWindow',
  components: {
    Close
  },
  data() {
    return {
      visible: false,
      newMessage: ''
    }
  },
  methods: {
    closeChat() {
      this.visible = false
    },
    sendMessage() {
      if (this.newMessage.trim()) {
        console.log('Send message:', this.newMessage)
        this.newMessage = ''
      }
    }
  }
}
</script>

<style scoped>
.chat-window {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  z-index: 1000;
}

.chat-card {
  max-height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 300px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.message {
  padding: 5px 0;
}

.chat-input {
  margin-top: 10px;
}
</style>