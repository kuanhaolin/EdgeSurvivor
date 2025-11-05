<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>註冊 EdgeSurvivor</h2>
          <p>加入我們，找到你的旅伴！</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="80px"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <!-- 基本資訊 -->
        <h3 class="section-title">基本資訊</h3>
        
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="請輸入您的姓名"
            clearable
          />
        </el-form-item>

        <el-form-item label="Email" prop="email">
          <el-input
            v-model="formData.email"
            type="email"
            placeholder="請輸入您的 Email"
            clearable
          />
        </el-form-item>

        <el-form-item label="密碼" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="至少 6 個字元"
            show-password
            clearable
          />
        </el-form-item>

        <!-- 個人資料 (選填) -->
        <h3 class="section-title">個人資料 (選填)</h3>

        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="性別" prop="gender">
              <el-select v-model="formData.gender" placeholder="請選擇性別" clearable>
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="年齡" prop="age">
              <el-input-number
                v-model="formData.age"
                :min="18"
                :max="100"
                placeholder="年齡"
                controls-position="right"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="地點" prop="location">
          <el-input
            v-model="formData.location"
            placeholder="例如：台北市"
            clearable
          />
        </el-form-item>

        <el-form-item label="個人簡介" prop="bio">
          <el-input
            v-model="formData.bio"
            type="textarea"
            :rows="3"
            placeholder="簡單介紹一下自己..."
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="隱私設定" prop="privacy_setting">
          <el-select v-model="formData.privacy_setting" placeholder="選擇隱私設定">
            <el-option label="公開" value="public" />
            <el-option label="私密" value="private" />
          </el-select>
        </el-form-item>

        <!-- 按鈕 -->
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            native-type="submit"
            style="width: 100%"
          >
            {{ loading ? '註冊中...' : '註冊' }}
          </el-button>
        </el-form-item>

        <div class="login-link">
          已有帳號？
          <router-link to="/login">立即登入</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

// 表單引用
const formRef = ref(null)
const loading = ref(false)

// 表單資料
const formData = reactive({
  name: '',
  email: '',
  password: '',
  gender: '',
  age: null,
  location: '',
  bio: '',
  privacy_setting: 'public'
})

// 驗證規則
const rules = {
  name: [
    { required: true, message: '請輸入姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名長度應在 2-50 字元之間', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '請輸入 Email', trigger: 'blur' },
    { type: 'email', message: 'Email 格式不正確', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
    { min: 6, message: '密碼長度至少需要 6 個字元', trigger: 'blur' }
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

    // 準備提交資料 (過濾空值)
    const submitData = {}
    Object.keys(formData).forEach(key => {
      if (formData[key] !== '' && formData[key] !== null && formData[key] !== undefined) {
        submitData[key] = formData[key]
      }
    })

    // 調用 store 的 register action
    await authStore.register(submitData)

    // 成功訊息已由 store 處理
    // 路由跳轉已由 store 處理
  } catch (error) {
    // 錯誤處理
    if (error.response?.data?.error) {
      const errorMsg = error.response.data.error
      
      // 根據錯誤類型顯示特定訊息
      if (errorMsg.includes('已被註冊') || errorMsg.includes('already')) {
        ElMessage.error('此電子郵件已被註冊')
      } else if (errorMsg.includes('格式') || errorMsg.includes('invalid')) {
        ElMessage.error('電子郵件格式不正確')
      } else if (errorMsg.includes('密碼') || errorMsg.includes('password')) {
        ElMessage.error('密碼長度至少需要 6 個字元')
      } else {
        ElMessage.error(errorMsg)
      }
    } else {
      // 已由 store 處理
      console.error('註冊失敗:', error)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 600px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #667eea;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 20px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #f0f0f0;
}

.section-title:first-of-type {
  margin-top: 0;
}

.login-link {
  text-align: center;
  margin-top: 16px;
  color: #909399;
  font-size: 14px;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
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
  .register-container {
    padding: 10px;
  }

  .register-card {
    max-width: 100%;
  }

  :deep(.el-form-item__label) {
    padding-bottom: 4px;
  }
}
</style>
