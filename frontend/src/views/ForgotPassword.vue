<template>
  <div class="forgot-password-container">
    <!-- 返回登入按鈕 -->
    <el-button class="back-btn" @click="backToLogin" circle>
      <el-icon><ArrowLeft /></el-icon>
    </el-button>
    
    <el-card class="forgot-password-card">
      <template #header>
        <div class="card-header">
          <h2>EdgeSurvivor</h2>
          <p>重設密碼</p>
        </div>
      </template>
      
      <!-- 步驟 1: 輸入電子郵件 -->
      <div v-if="step === 1">
        <el-alert
          title="請輸入您註冊時使用的電子郵件"
          type="info"
          :closable="false"
          style="margin-bottom: 20px;"
        />
        
        <el-form
          ref="emailFormRef"
          :model="emailForm"
          :rules="emailRules"
          label-width="0px"
        >
          <el-form-item prop="email">
            <el-input
              v-model="emailForm.email"
              placeholder="請輸入電子郵件"
              :prefix-icon="Message"
              size="large"
            />
          </el-form-item>
          
          <el-button
            type="primary"
            style="width: 100%"
            :loading="loading"
            @click="sendVerificationCode"
          >
            發送驗證碼
          </el-button>

          <!-- 分隔線 -->
          <el-divider>或</el-divider>

          <el-button
            style="width: 100%; margin-top: 12px;"
            @click="backToLogin"
          >
            返回登入
          </el-button>
        </el-form>
      </div>
      
      <!-- 步驟 2: 輸入驗證碼和新密碼 -->
      <div v-if="step === 2">
        <el-alert
          :title="`驗證碼已發送到 ${emailForm.email}`"
          type="success"
          :closable="false"
          style="margin-bottom: 20px;"
        />
        
        <el-form
          ref="resetFormRef"
          :model="resetForm"
          :rules="resetRules"
          label-width="0px"
        >
          <el-form-item prop="code" style="margin-bottom: 18px;">
            <el-input
              v-model="resetForm.code"
              placeholder="請輸入6位數驗證碼"
              :prefix-icon="Lock"
              maxlength="6"
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="newPassword" style="margin-bottom: 18px;">
            <el-input
              v-model="resetForm.newPassword"
              type="password"
              placeholder="請輸入新密碼（至少6個字元）"
              :prefix-icon="Lock"
              show-password
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="resetForm.confirmPassword"
              type="password"
              placeholder="請再次輸入新密碼"
              :prefix-icon="Lock"
              show-password
              size="large"
            />
          </el-form-item>
          
          <el-button
            type="primary"
            style="width: 100%"
            :loading="loading"
            @click="resetPassword"
          >
            重設密碼
          </el-button>
          
          <!-- 分隔線 -->
          <el-divider>或</el-divider>
          
          <el-button
            style="width: 100%; margin-top: 12px;"
            @click="resendCode"
            :disabled="countdown > 0"
          >
            {{ countdown > 0 ? `重新發送 (${countdown}s)` : '重新發送驗證碼' }}
          </el-button>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Message, Lock } from '@element-plus/icons-vue'
import authAPI from '../api/auth'

const router = useRouter()
const emailFormRef = ref(null)
const resetFormRef = ref(null)
const loading = ref(false)
const step = ref(1)
const countdown = ref(0)
let countdownTimer = null

const emailForm = reactive({
  email: ''
})

const resetForm = reactive({
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const emailRules = {
  email: [
    { required: true, message: '請輸入電子郵件', trigger: 'blur' },
    { type: 'email', message: '請輸入正確的電子郵件格式', trigger: 'blur' }
  ]
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('請再次輸入密碼'))
  } else if (value !== resetForm.newPassword) {
    callback(new Error('兩次輸入密碼不一致'))
  } else {
    callback()
  }
}

const resetRules = {
  code: [
    { required: true, message: '請輸入驗證碼', trigger: 'blur' },
    { len: 6, message: '驗證碼為6位數字', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '請輸入新密碼', trigger: 'blur' },
    { min: 6, message: '密碼長度至少 6 個字元', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 發送驗證碼
const sendVerificationCode = async () => {
  if (!emailFormRef.value) return
  
  await emailFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const response = await authAPI.sendResetCode(emailForm.email)
        
        // 測試用：顯示驗證碼
        if (response.data.code) {
          ElMessage.success(`驗證碼已發送：${response.data.code}（測試模式）`)
        } else {
          ElMessage.success('驗證碼已發送，請檢查您的電子郵件')
        }
        
        step.value = 2
        startCountdown()
      } catch (error) {
        console.error('發送驗證碼失敗:', error)
        ElMessage.error(
          error.response?.data?.error || '發送驗證碼失敗，請稍後再試'
        )
      } finally {
        loading.value = false
      }
    }
  })
}

// 重設密碼
const resetPassword = async () => {
  if (!resetFormRef.value) return
  
  await resetFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await authAPI.resetPassword({
          email: emailForm.email,
          code: resetForm.code,
          new_password: resetForm.newPassword
        })
        
        ElMessage.success('密碼重設成功！請使用新密碼登入')
        
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (error) {
        console.error('重設密碼失敗:', error)
        ElMessage.error(
          error.response?.data?.error || '重設密碼失敗，請檢查驗證碼是否正確'
        )
      } finally {
        loading.value = false
      }
    }
  })
}

// 重新發送驗證碼
const resendCode = async () => {
  loading.value = true
  try {
    const response = await authAPI.sendResetCode(emailForm.email)
    
    // 測試用：顯示驗證碼
    if (response.data.code) {
      ElMessage.success(`驗證碼已重新發送：${response.data.code}（測試模式）`)
    } else {
      ElMessage.success('驗證碼已重新發送')
    }
    
    startCountdown()
  } catch (error) {
    console.error('發送驗證碼失敗:', error)
    ElMessage.error(
      error.response?.data?.error || '發送驗證碼失敗，請稍後再試'
    )
  } finally {
    loading.value = false
  }
}

// 倒數計時
const startCountdown = () => {
  countdown.value = 60
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
    }
  }, 1000)
}

const backToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  min-height: -webkit-fill-available;
  background: var(--gradient-primary);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.back-btn {
  position: fixed;
  top: var(--spacing-lg);
  left: var(--spacing-lg);
  z-index: 100;
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-base);
  color: var(--primary-color) !important;
}

.back-btn:hover {
  background: white !important;
  transform: translateX(-4px);
  box-shadow: var(--shadow-xl);
}

.forgot-password-container::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  top: -100px;
  left: -100px;
  animation: float 20s ease-in-out infinite;
}

.forgot-password-container::after {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  bottom: -50px;
  right: -50px;
  animation: float 15s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(50px, 50px) scale(1.1);
  }
  50% {
    transform: translate(-30px, 80px) scale(0.9);
  }
  75% {
    transform: translate(30px, -50px) scale(1.05);
  }
}

.forgot-password-card {
  width: 100%;
  max-width: 440px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-2xl);
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  z-index: 1;
}

.forgot-password-card :deep(.el-card__header) {
  background: transparent;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  padding: var(--spacing-xl);
}

.forgot-password-card :deep(.el-card__body) {
  padding: var(--spacing-xl);
}

.card-header {
  text-align: center;
  animation: fadeIn 0.8s ease-out 0.2s both;
}

.card-header h2 {
  margin: 0 0 var(--spacing-md) 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
}

.card-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
}

.forgot-password-card :deep(.el-button--primary) {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: var(--gradient-primary);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all var(--transition-base);
}

.forgot-password-card :deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.forgot-password-card :deep(.el-button--default) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: var(--primary-color);
  transition: all var(--transition-base);
}

.forgot-password-card :deep(.el-button--default:hover) {
  background: rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.forgot-password-card :deep(.el-input__wrapper) {
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all var(--transition-base);
}

.forgot-password-card :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.forgot-password-card :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
}

@media (max-width: 640px) {
  .forgot-password-container {
    padding: var(--spacing-md);
  }
  
  .forgot-password-card {
    max-width: 100%;
  }
  
  .forgot-password-card :deep(.el-card__header),
  .forgot-password-card :deep(.el-card__body) {
    padding: var(--spacing-lg);
  }
  
  .card-header h2 {
    font-size: 28px;
  }
}
</style>
