<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>登入 EdgeSurvivor</h2>
          <p>歡迎回來！請登入您的帳號</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="電子郵件" prop="email">
          <el-input
            v-model="formData.email"
            type="email"
            placeholder="請輸入電子郵件"
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="密碼" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="請輸入密碼"
            show-password
            clearable
            :disabled="loading"
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <!-- 兩步驟驗證碼輸入 -->
        <el-form-item v-if="require2FA" label="兩步驟驗證碼" prop="twoFactorCode">
          <el-input
            v-model="formData.twoFactorCode"
            placeholder="請輸入 6 位數驗證碼"
            maxlength="6"
            clearable
            :disabled="loading"
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <div class="login-options">
          <el-checkbox v-model="formData.rememberMe" :disabled="loading">
            記住我
          </el-checkbox>
          <router-link to="/forgot-password" class="forgot-password">
            忘記密碼？
          </router-link>
        </div>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            native-type="submit"
            style="width: 100%"
          >
            {{ loading ? '登入中...' : (require2FA ? '驗證並登入' : '登入') }}
          </el-button>
        </el-form-item>

        <div class="register-prompt">
          還沒有帳號？
          <router-link to="/register" class="register-link">立即註冊</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

// 表單引用
const formRef = ref(null)
const loading = ref(false)
const require2FA = ref(false)

// 表單資料
const formData = reactive({
  email: '',
  password: '',
  twoFactorCode: '',
  rememberMe: false
})

// 驗證規則
const rules = {
  email: [
    { required: true, message: '請輸入電子郵件', trigger: 'blur' },
    { type: 'email', message: 'Email 格式不正確', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' }
  ],
  twoFactorCode: [
    { 
      validator: (rule, value, callback) => {
        if (require2FA.value && !value) {
          callback(new Error('請輸入兩步驟驗證碼'))
        } else if (require2FA.value && value && !/^\d{6}$/.test(value)) {
          callback(new Error('驗證碼必須是 6 位數字'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 提交處理
const handleSubmit = async () => {
  try {
    // 驗證表單
    const valid = await formRef.value.validate()
    if (!valid) {
      return
    }

    loading.value = true

    // 準備登入憑證
    const credentials = {
      email: formData.email.trim().toLowerCase(),
      password: formData.password
    }

    // 如果需要 2FA 且已輸入驗證碼
    if (require2FA.value && formData.twoFactorCode) {
      credentials.two_factor_code = formData.twoFactorCode
    }

    // 調用 store 的 login action
    const result = await authStore.login(credentials)

    // 檢查是否需要 2FA
    if (result && result.require_2fa) {
      require2FA.value = true
      ElMessage.info('請輸入兩步驟驗證碼')
      return
    }

    // 登入成功（成功訊息和跳轉已由 store 處理）
  } catch (error) {
    // 錯誤處理
    console.error('登入錯誤:', error)
    
    // 特定錯誤訊息已由 store 處理
    // 這裡處理未預期的錯誤
    if (!error.response) {
      ElMessage.error('網路連線失敗，請檢查您的網路')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #667eea;
  font-size: 24px;
  font-weight: 600;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.forgot-password {
  color: #667eea;
  font-size: 14px;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.register-prompt {
  text-align: center;
  margin-top: 16px;
  color: #909399;
  font-size: 14px;
}

.register-link {
  color: #667eea;
  font-weight: 500;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  padding-bottom: 8px;
}

:deep(.el-input__inner) {
  border-radius: 6px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 6px;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: 500;
}

:deep(.el-button--primary:hover) {
  opacity: 0.9;
}

/* 響應式設計 */
@media (max-width: 640px) {
  .login-container {
    padding: 10px;
  }

  .login-card {
    max-width: 100%;
  }

  .card-header h2 {
    font-size: 20px;
  }

  .login-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>