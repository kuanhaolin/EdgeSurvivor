<template>
  <div class="register-container">
    <!-- 返回首頁按鈕 -->
    <el-button class="back-home-btn" @click="goToHome" circle>
      <el-icon><ArrowLeft /></el-icon>
    </el-button>
    
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2 @click="goToHome" style="cursor: pointer;">註冊新帳號</h2>
          <p>加入 EdgeSurvivor 開始你的旅程</p>
        </div>
      </template>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用戶名" prop="name">
          <el-input
            v-model="registerForm.name"
            placeholder="請輸入用戶名"
          />
        </el-form-item>
        
        <el-form-item label="電子郵件" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="請輸入電子郵件"
          />
        </el-form-item>
        
        <el-form-item label="密碼" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="請輸入密碼（至少6個字元）"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="確認密碼" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="請再次輸入密碼"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            style="width: 100%"
            :loading="loading"
            @click="handleRegister"
          >
            註冊
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <el-button
            style="width: 100%"
            @click="backToLogin"
          >
            返回登入
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)

const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('請再次輸入密碼'))
  } else if (value !== registerForm.password) {
    callback(new Error('兩次輸入密碼不一致'))
  } else {
    callback()
  }
}

const rules = {
  name: [
    { required: true, message: '請輸入用戶名', trigger: 'blur' },
    { min: 2, max: 20, message: '用戶名長度在 2 到 20 個字元', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '請輸入電子郵件', trigger: 'blur' },
    { type: 'email', message: '請輸入正確的電子郵件格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
    { min: 6, message: '密碼長度至少 6 個字元', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const response = await axios.post('/api/auth/register', {
          name: registerForm.name,
          email: registerForm.email,
          password: registerForm.password
        })
        
        ElMessage.success('註冊成功！請登入')
        
        // 跳轉到登入頁
        setTimeout(() => {
          router.push('/login')
        }, 1000)
      } catch (error) {
        console.error('註冊失敗:', error)
        ElMessage.error(
          error.response?.data?.error || '註冊失敗，請稍後再試'
        )
      } finally {
        loading.value = false
      }
    }
  })
}

const backToLogin = () => {
  router.push('/login')
}

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gradient-primary);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

/* 返回首頁按鈕 */
.back-home-btn {
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

.back-home-btn:hover {
  background: white !important;
  transform: translateX(-4px);
  box-shadow: var(--shadow-xl);
}

/* 動態背景粒子效果 */
.register-container::before {
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

.register-container::after {
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

.register-card {
  width: 100%;
  max-width: 480px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-2xl);
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  z-index: 1;
}

.register-card :deep(.el-card__header) {
  background: transparent;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  padding: var(--spacing-xl);
}

.register-card :deep(.el-card__body) {
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
  transition: all var(--transition-base);
}

.card-header h2:hover {
  transform: scale(1.05);
}

.card-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
}

/* 表單樣式 */
.register-card :deep(.el-form-item) {
  margin-bottom: var(--spacing-lg);
}

.register-card :deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
}

.register-card :deep(.el-input__wrapper) {
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all var(--transition-base);
}

.register-card :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.register-card :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
}

/* 按鈕樣式 */
.register-card :deep(.el-button--primary) {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: var(--gradient-primary);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all var(--transition-base);
}

.register-card :deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.register-card :deep(.el-button--primary:active) {
  transform: translateY(0);
}

.register-card :deep(.el-button--default) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: var(--primary-color);
  transition: all var(--transition-base);
}

.register-card :deep(.el-button--default:hover) {
  background: rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

/* 響應式設計 */
@media (max-width: 640px) {
  .register-container {
    padding: var(--spacing-md);
  }
  
  .register-card {
    max-width: 100%;
  }
  
  .register-card :deep(.el-card__header),
  .register-card :deep(.el-card__body) {
    padding: var(--spacing-lg);
  }
  
  .card-header h2 {
    font-size: 28px;
  }
}
</style>
