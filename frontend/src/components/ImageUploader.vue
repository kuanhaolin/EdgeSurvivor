<template>
  <div class="image-uploader">
    <el-upload
      class="upload-area"
      name="image"
      :action="uploadUrl"
      :headers="uploadHeaders"
      :show-file-list="false"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      :disabled="disabled"
      accept="image/*"
    >
      <div v-if="!imageUrl" class="upload-placeholder">
        <el-icon class="upload-icon"><Plus /></el-icon>
        <div class="upload-text">{{ placeholder }}</div>
      </div>
      <div v-else class="image-preview">
        <el-image :src="imageUrl" fit="cover" />
        <div class="image-actions">
          <el-button
            type="danger"
            size="small"
            circle
            @click.stop="removeImage"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </el-upload>
    
    <div v-if="tip" class="upload-tip">
      <el-text type="info" size="small">{{ tip }}</el-text>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '點擊上傳圖片'
  },
  tip: {
    type: String,
    default: '建議尺寸 800x600，支持 JPG、PNG 格式，大小不超過 2MB'
  },
  maxSize: {
    type: Number,
    default: 2 // MB
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'success', 'error'])

const imageUrl = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 上傳地址（需要實現文件上傳 API）
const uploadUrl = computed(() => {
  // 開發環境使用相對路徑，利用 Vite proxy
  // 生產環境使用環境變量或完整 URL
  if (import.meta.env.DEV) {
    return '/api/upload/image'
  }
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'}/api/upload/image`
})

// 上傳請求頭（需要 JWT token）
const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    'Authorization': `Bearer ${token}`
  }
})

// 上傳前檢查
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < props.maxSize
  
  if (!isImage) {
    ElMessage.error('只能上傳圖片文件!')
    return false
  }
  
  if (!isLt2M) {
    ElMessage.error(`圖片大小不能超過 ${props.maxSize}MB!`)
    return false
  }
  
  return true
}

// 上傳成功
const handleSuccess = (response) => {
  if (response.url) {
    imageUrl.value = response.url
    emit('success', response.url)
    ElMessage.success('上傳成功')
  } else {
    ElMessage.error('上傳失敗：無效的響應')
  }
}

// 上傳失敗
const handleError = (error) => {
  console.error('上傳失敗:', error)
  emit('error', error)
  ElMessage.error('上傳失敗，請重試')
}

// 移除圖片
const removeImage = () => {
  imageUrl.value = ''
  emit('update:modelValue', '')
}
</script>

<style scoped>
.image-uploader {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upload-area {
  width: 100%;
}

.upload-area :deep(.el-upload) {
  width: 100%;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.upload-area :deep(.el-upload:hover) {
  border-color: #409eff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background-color: #fafafa;
}

.upload-icon {
  font-size: 48px;
  color: #8c939d;
  margin-bottom: 10px;
}

.upload-text {
  color: #606266;
  font-size: 14px;
}

.image-preview {
  position: relative;
  width: 100%;
  padding-top: 75%; /* 4:3 比例 */
}

.image-preview .el-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.image-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview:hover .image-actions {
  opacity: 1;
}

.upload-tip {
  text-align: center;
}
</style>
