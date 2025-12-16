<template>
  <div class="test-dashboard">
    <div class="test-header" style="background: red; color: white; padding: 20px; font-size: 24px;">
      測試頁面 - 如果看到這個就表示基本渲染正常
    </div>
    
    <div style="padding: 20px; background: white;">
      <h1 style="color: black; font-size: 32px;">這是標題</h1>
      <p style="color: black; font-size: 18px;">如果能看到這段文字，表示基本 HTML 沒問題</p>
      
      <button 
        @click="testClick" 
        style="background: blue; color: white; padding: 15px 30px; font-size: 18px; border: none; border-radius: 8px; margin: 10px;"
      >
        點擊測試
      </button>
      
      <div style="margin-top: 20px; padding: 20px; background: #f0f0f0;">
        <h2 style="color: black;">用戶資訊測試</h2>
        <p style="color: black;">用戶名: {{ userName }}</p>
        <p style="color: black;">Token: {{ hasToken ? '存在' : '不存在' }}</p>
      </div>
      
      <!-- Element Plus 測試 -->
      <div style="margin-top: 20px; padding: 20px; background: #e0e0e0;">
        <h2 style="color: black;">Element Plus 元件測試</h2>
        <el-button type="primary" @click="testElClick">Element 按鈕</el-button>
        <el-card style="margin-top: 10px;">
          <p>這是 Element Plus 卡片</p>
        </el-card>
      </div>
      
      <div style="margin-top: 20px; padding: 20px; background: yellow;">
        <p style="color: black; font-weight: bold;">點擊次數: {{ clickCount }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const clickCount = ref(0)
const userName = ref('未載入')
const hasToken = ref(false)

const testClick = () => {
  clickCount.value++
  alert('JavaScript 正常運作！點擊次數: ' + clickCount.value)
}

const testElClick = () => {
  ElMessage.success('Element Plus 正常運作！')
}

onMounted(() => {
  console.log('TestDashboard mounted')
  
  // 檢查 token
  const token = localStorage.getItem('token')
  hasToken.value = !!token
  
  // 檢查用戶
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      userName.value = user.name || user.email || '無名'
    } catch (e) {
      userName.value = '解析失敗'
    }
  }
  
  console.log('Token:', hasToken.value)
  console.log('User:', userName.value)
})
</script>

<style scoped>
.test-dashboard {
  min-height: 100vh;
  background: #cccccc;
}

.test-header {
  position: sticky;
  top: 0;
  z-index: 1000;
}
</style>
