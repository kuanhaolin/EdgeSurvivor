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
            class="google-login-btn" 
            style="width: 100%" 
            @click="handleGoogleCodeLogin"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" style="margin-right: 8px;">
              <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
              <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
              <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.951H.957C.348 6.173 0 7.55 0 9s.348 2.827.957 4.049l3.007-2.342z"/>
              <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.951L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z"/>
            </svg>
            使用 Google 登入
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <el-button
            class="register-btn"
            style="width: 100%"
            @click="handleRegister"
          >
            註冊新帳號
          </el-button>
        </el-form-item>
        
  <!-- 移除隱藏按鈕，改以可見官方按鈕提高穩定性 -->
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, ArrowLeft } from '@element-plus/icons-vue'
import axios from 'axios'
import authAPI from '../api/auth'
import { createLoginRules } from '../utils/loginValidationRules'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const gisReady = ref(false)
let gisInitStarted = false
let codeClient = null

const require2FA = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  twoFactorCode: ''
})

const rules = createLoginRules(require2FA)

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const loginData = {
          email: loginForm.username,
          password: loginForm.password
        }
        
        // 如果需要兩步驟驗證，加入驗證碼
        if (require2FA.value && loginForm.twoFactorCode) {
          loginData.two_factor_code = loginForm.twoFactorCode
        }
        
        const response = await axios.post('/api/auth/login', loginData)
        
        // 檢查是否需要兩步驟驗證
        if (response.data.require_2fa) {
          require2FA.value = true
          ElMessage.info('請輸入兩步驟驗證碼')
          return
        }
        
        if (response.data.access_token) {
          // 儲存 token
          localStorage.setItem('token', response.data.access_token)
          localStorage.setItem('user', JSON.stringify(response.data.user))
          
          ElMessage.success('登入成功！')
          
          // 跳轉到控制台
          setTimeout(() => {
            router.push('/dashboard')
          }, 500)
        }
      } catch (error) {
        console.error('登入失敗:', error)
        ElMessage.error(
          error.response?.data?.error || '登入失敗，請檢查帳號密碼'
        )
      } finally {
        loading.value = false
      }
    }
  })
}

// Google 登入功能
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '你的Google Client ID'

// Debug: 檢查 Client ID
console.log('VITE_GOOGLE_CLIENT_ID:', import.meta.env.VITE_GOOGLE_CLIENT_ID)
console.log('GOOGLE_CLIENT_ID:', GOOGLE_CLIENT_ID)

// 移除 One Tap 觸發流程，改用 Code Flow 的自訂按鈕

// 自訂按鈕：使用 OAuth Code Flow 以確保「使用者手勢」且可自訂外觀
const handleGoogleCodeLogin = () => {
  if (!window.google || !gisReady.value || !codeClient) {
    ElMessage.info('Google 登入服務準備中，請稍後再試')
    return
  }
  try {
    codeClient.requestCode()
  } catch (e) {
    console.error('請求 Google 授權碼失敗:', e)
    ElMessage.error('無法啟動 Google 授權流程，請稍後再試')
  }
}

// 移除 ID Token 直接登入回調（改用 Code Flow）

  // 載入 Google Identity Services 並渲染按鈕
onMounted(() => {
  // 確保 Google API 已載入並初始化
  const initGoogle = () => {
    if (window.google && !gisInitStarted) {
      gisInitStarted = true
      console.log('Google Identity Services 已載入')
      console.log('使用的 Client ID:', GOOGLE_CLIENT_ID)
      
      // 初始化 OAuth Code Flow 用的 code client（供自訂樣式的按鈕使用）
      try {
        codeClient = window.google.accounts.oauth2.initCodeClient({
          client_id: GOOGLE_CLIENT_ID,
          scope: 'openid email profile',
          ux_mode: 'popup',
          callback: async (resp) => {
            try {
              if (resp && resp.code) {
                const result = await authAPI.googleLoginByCode(resp.code)
                if (result.data?.access_token) {
                  localStorage.setItem('token', result.data.access_token)
                  localStorage.setItem('user', JSON.stringify(result.data.user))
                  ElMessage.success('Google 登入成功！')
                  setTimeout(() => router.push('/dashboard'), 300)
                } else {
                  ElMessage.error(result.data?.msg || 'Google 登入失敗，請稍後再試')
                }
              } else {
                ElMessage.info('未取得 Google 授權碼，請重試')
              }
            } catch (err) {
              console.error('Google Code Flow 後端交換失敗:', err)
              ElMessage.error(err.response?.data?.msg || 'Google 登入失敗，請稍後再試')
            }
          }
        })
      } catch (e) {
        console.error('初始化 Google Code Client 失敗:', e)
      }
      
      console.log('Google Code Client 初始化完成')
      gisReady.value = true
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
  min-height: -webkit-fill-available;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: var(--spacing-lg);
  padding-bottom: calc(var(--spacing-lg) + env(safe-area-inset-bottom));
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  top: -200px;
  right: -200px;
  animation: pulse 8s ease-in-out infinite;
  filter: blur(60px);
}

.login-container::after {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(240, 147, 251, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  bottom: -150px;
  left: -150px;
  animation: pulse 10s ease-in-out infinite reverse;
  filter: blur(80px);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.back-home-btn {
  position: fixed;
  top: var(--spacing-lg);
  left: var(--spacing-lg);
  z-index: 100;
  width: 52px;
  height: 52px;
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--primary-color) !important;
}

.back-home-btn:hover {
  background: white !important;
  transform: translateX(-6px) scale(1.05);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
  border-color: var(--primary-color) !important;
}

.login-card {
  width: 100%;
  max-width: 460px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.5);
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  z-index: 1;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card :deep(.el-card__header) {
  background: linear-gradient(180deg, rgba(102, 126, 234, 0.03) 0%, transparent 100%);
  border-bottom: 2px solid rgba(102, 126, 234, 0.08);
  padding: 32px;
}

.login-card :deep(.el-card__body) {
  padding: 36px;
}

.card-header {
  text-align: center;
  animation: fadeIn 0.8s ease-out 0.2s both;
  padding-top: 8px;
}

.card-header h2 {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: 12px;
  letter-spacing: -1.5px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(102, 126, 234, 0.1);
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header p {
  margin: 0;
  color: #666;
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.login-card :deep(.el-form-item) {
  margin-bottom: 24px;
  animation: slideInLeft 0.5s ease-out backwards;
}

.login-card :deep(.el-form-item:nth-child(1)) {
  animation-delay: 0.1s;
}

.login-card :deep(.el-form-item:nth-child(2)) {
  animation-delay: 0.2s;
}

.login-card :deep(.el-form-item:nth-child(3)) {
  animation-delay: 0.3s;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-card :deep(.el-form-item__label) {
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.login-card :deep(.el-input__wrapper) {
  padding: 14px 18px;
  border-radius: 12px;
  border: 2px solid #e8ecf4;
  background: #fafbfc;
  box-shadow: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-card :deep(.el-input__wrapper:hover) {
  background: white;
  border-color: #d1d9e6;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.12);
}

.login-card :deep(.el-input__wrapper.is-focus) {
  background: white;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.12), 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.login-card :deep(.el-input__inner) {
  font-size: 15px;
  color: #2c3e50;
  font-weight: 500;
}

.login-card :deep(.el-input__prefix) {
  color: #667eea;
}

.login-card :deep(.el-button--primary) {
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.login-card :deep(.el-button--primary::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.login-card :deep(.el-button--primary:hover) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45);
}

.login-card :deep(.el-button--primary:hover::before) {
  left: 100%;
}

.login-card :deep(.el-button--primary:active) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35);
}

.login-card :deep(.el-divider) {
  margin: 28px 0;
}

.login-card :deep(.el-divider__text) {
  background: white;
  color: #999;
  font-size: 14px;
  font-weight: 500;
  padding: 0 16px;
}

.login-card :deep(.el-link) {
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s;
}

.login-card :deep(.el-link:hover) {
  transform: translateX(2px);
}

.google-login-btn {
  height: 52px;
  font-size: 15px;
  font-weight: 500;
  background: white !important;
  color: #3c4043 !important;
  border: 2px solid #e8ecf4 !important;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

.google-login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(66, 133, 244, 0.05) 0%, rgba(234, 67, 53, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.google-login-btn:hover {
  background: white !important;
  border-color: #4285f4 !important;
  box-shadow: 0 6px 16px rgba(66, 133, 244, 0.2);
  transform: translateY(-3px);
}

.google-login-btn:hover::before {
  opacity: 1;
}

.google-login-btn svg {
  transition: transform 0.3s;
}

.google-login-btn:hover svg {
  transform: scale(1.1);
}

.register-btn {
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(240, 147, 251, 0.08) 100%) !important;
  color: #667eea !important;
  border: 2px solid #667eea !important;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.register-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.5s, height 0.5s;
}

.register-btn:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%) !important;
  border-color: #764ba2 !important;
  color: #764ba2 !important;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
  transform: translateY(-3px);
}

.register-btn:hover::before {
  width: 300px;
  height: 300px;
}

.register-btn:active {
  transform: translateY(-1px);
}

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
