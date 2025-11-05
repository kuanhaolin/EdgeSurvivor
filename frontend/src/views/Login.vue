<template>
  <div class="login-container">
    <!-- 返回首頁按鈕 -->
    <el-button class="back-home-btn" @click="goToHome" circle>
      <el-icon><ArrowLeft /></el-icon>
    </el-button>
    
    <el-card class="login-card">
      <template #header>
                <div class="card-header">
          <h2>EdgeSurvivor</h2>
          <p>邊緣人神器 - 旅伴交友平台</p>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-width="0px"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="請輸入帳號或電子郵件"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="請輸入密碼"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <!-- 兩步驟驗證碼 -->
        <el-form-item v-if="require2FA" prop="twoFactorCode">
          <el-input
            v-model="loginForm.twoFactorCode"
            placeholder="請輸入 6 位數驗證碼"
            maxlength="6"
            style="text-align: center; letter-spacing: 2px;"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
          <div style="margin-top: 8px; color: #909399; font-size: 12px;">
            請打開驗證器 App 查看驗證碼
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            {{ require2FA ? '驗證並登入' : '登入' }}
          </el-button>
        </el-form-item>

        <!-- 忘記密碼連結 -->
        <div style="text-align: right; margin-bottom: 20px;">
          <el-link type="primary" @click="handleForgotPassword">忘記密碼？</el-link>
        </div>
        
        <!-- 分隔線 -->
        <el-divider>或</el-divider>
        
        <!-- Google 登入按鈕 -->
        <el-form-item>
          <el-button
            style="width: 100%"
            :loading="googleLoading"
            @click="handleGoogleLogin"
            class="google-login-btn"
          >
            <svg v-if="!googleLoading" class="google-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            使用 Google 登入
        </el-button>
        </el-form-item>
        
        <el-form-item>
          <el-button
            style="width: 100%"
            @click="handleRegister"
          >
            註冊新帳號
          </el-button>
        </el-form-item>
        
        <!-- 隱藏的 Google 按鈕用於觸發 OAuth -->
        <div id="google-signin-button-hidden" style="position: absolute; width: 1px; height: 1px; overflow: hidden; opacity: 0; pointer-events: none;"></div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, ArrowLeft } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import authAPI from '../api/auth'

const router = useRouter()
const authStore = useAuthStore()
const loginFormRef = ref(null)
const loading = ref(false)
const googleLoading = ref(false)

const require2FA = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  twoFactorCode: ''
})

const rules = {
  username: [
    { required: true, message: '請輸入帳號或電子郵件', trigger: 'blur' },
    { type: 'email', message: 'Email 格式不正確', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' }
  ],
  twoFactorCode: [
    { 
      validator: (rule, value, callback) => {
        if (require2FA.value && !value) {
          callback(new Error('請輸入驗證碼'))
        } else if (require2FA.value && value && !/^\d{6}$/.test(value)) {
          callback(new Error('驗證碼必須為 6 位數字'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 驗證表單
    const valid = await loginFormRef.value.validate()
    if (!valid) {
      return
    }

    loading.value = true

    // 準備登入憑證
    const credentials = {
      email: loginForm.username.trim().toLowerCase(),
      password: loginForm.password
    }

    // 如果需要兩步驟驗證，加入驗證碼
    if (require2FA.value && loginForm.twoFactorCode) {
      credentials.two_factor_code = loginForm.twoFactorCode
    }

    // 調用 auth store 的 login action
    const result = await authStore.login(credentials)

    // 檢查是否需要兩步驟驗證
    if (result && result.require_2fa) {
      require2FA.value = true
      ElMessage.info('請輸入兩步驟驗證碼')
      return
    }

    // 登入成功（成功訊息和跳轉已由 store 處理）
  } catch (error) {
    console.error('登入失敗:', error)
    
    // 特定錯誤訊息已由 store 處理
    // 這裡處理未預期的錯誤
    if (!error.response) {
      ElMessage.error('網路連線失敗，請檢查您的網路')
    }
  } finally {
    loading.value = false
  }
}

// Google 登入功能
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '你的Google Client ID'

// 手動觸發 Google 登入
const handleGoogleLogin = () => {
  googleLoading.value = true
  
  // 找到隱藏的 Google 按鈕並點擊
  const hiddenButton = document.querySelector('#google-signin-button-hidden div[role="button"]')
  if (hiddenButton) {
    hiddenButton.click()
  } else {
    ElMessage.error('Google 登入服務未就緒，請稍後再試')
    googleLoading.value = false
  }
}

// Google 登入回調函數
const handleGoogleCallback = async (response) => {
  try {
    if (response.credential) {
      console.log('收到 Google ID Token')

      // 呼叫後端 Google 登入 API（直接傳 token 字串）
      const result = await authAPI.googleLogin(response.credential)

      console.log('Google 登入後端回應:', result.data)

      if (result.data.access_token) {
        // 使用 auth store 統一管理 token 和用戶資訊
        authStore.setToken(result.data.access_token, null)
        authStore.setUser(result.data.user)

        console.log('Token 已設置:', localStorage.getItem('access_token'))
        console.log('用戶已設置:', result.data.user)

        ElMessage.success('Google 登入成功！')

        // 跳轉到控制台
        setTimeout(() => {
          console.log('準備導航到 /dashboard')
          router.push('/dashboard').then(() => {
            console.log('成功導航到 /dashboard')
          }).catch(err => {
            console.error('導航失敗:', err)
          })
        }, 100)
      } else {
        ElMessage.error('Google 登入失敗：未收到 access token')
      }
    }
  } catch (error) {
    console.error('Google 登入失敗:', error)
    ElMessage.error(
      error.response?.data?.msg || error.response?.data?.error || 'Google 登入失敗，請稍後再試'
    )
  } finally {
    googleLoading.value = false
  }
}

  // 載入 Google Identity Services 並渲染按鈕
onMounted(() => {
  // 確保 Google API 已載入並初始化
  const initGoogle = () => {
    if (window.google) {
      console.log('Google Identity Services 已載入')
      
      // 初始化 Google Identity Services
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleCallback,
        auto_select: false
      })
      
      // 渲染隱藏的 Google 按鈕供點擊觸發
      window.google.accounts.id.renderButton(
        document.getElementById('google-signin-button-hidden'),
        {
          type: 'standard',
          size: 'large',
          width: 400
        }
      )
      
      console.log('Google Identity Services 初始化完成')
    } else {
      // 如果還沒載入，100ms 後重試
      setTimeout(initGoogle, 100)
    }
  }
  
  initGoogle()
})

const handleRegister = () => {
  router.push('/register')
}

const handleForgotPassword = () => {
  router.push('/forgot-password')
}

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.login-container {
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
.login-container::before {
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

.login-container::after {
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

.login-card {
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

.login-card :deep(.el-card__header) {
  background: transparent;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  padding: var(--spacing-xl);
}

.login-card :deep(.el-card__body) {
  padding: var(--spacing-xl);
}

.card-header {
  text-align: center;
  animation: fadeIn 0.8s ease-out 0.2s both;
}

.card-header h2 {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.15;        /* 控制行內行距 */
  margin-bottom: 10px;      /* 控制和下一行 <p> 的距離 */
  letter-spacing: -1px;
  /* 漸層文字相關屬性保留 */
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
}

/* 表單樣式 */
.login-card :deep(.el-form-item) {
  margin-bottom: var(--spacing-lg);
}

.login-card :deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
}

.login-card :deep(.el-input__wrapper) {
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all var(--transition-base);
}

.login-card :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.login-card :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
}

/* 按鈕樣式 */
.login-card :deep(.el-button--primary) {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: var(--gradient-primary);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all var(--transition-base);
}

.login-card :deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.login-card :deep(.el-button--primary:active) {
  transform: translateY(0);
}

.login-card :deep(.el-button--default) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: var(--primary-color);
  transition: all var(--transition-base);
}

.login-card :deep(.el-button--default:hover) {
  background: rgba(102, 126, 234, 0.15);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

/* Google 登入按鈕樣式 */
.google-login-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: white !important;
  border: 1px solid #dadce0 !important;
  color: #3c4043 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all var(--transition-base);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.google-login-btn:hover {
  background: #f8f9fa !important;
  border-color: #d2d3d4 !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.google-login-btn:active {
  background: #f1f3f4 !important;
  transform: translateY(0);
}

.google-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* 測試帳號區域 */
.test-accounts {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  text-align: center;
  animation: fadeIn 1s ease-out 0.4s both;
}

.test-accounts p {
  font-size: 13px;
  color: var(--text-secondary);
  background: rgba(102, 126, 234, 0.05);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  display: inline-block;
}

.test-accounts :deep(.el-divider__text) {
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-weight: 500;
}

/* 響應式設計 */
@media (max-width: 640px) {
  .login-container {
    padding: var(--spacing-md);
  }
  
  .login-card {
    max-width: 100%;
  }
  
  .login-card :deep(.el-card__header),
  .login-card :deep(.el-card__body) {
    padding: var(--spacing-lg);
  }
  
  .card-header h2 {
    font-size: 28px;
  }
}
</style>
