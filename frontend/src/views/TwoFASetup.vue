<template>
  <div class="twofa-setup">
    <h2>兩步驟驗證設定</h2>
    <div v-if="loading">載入中...</div>
    <div v-else>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="qrCodeUrl">
        <canvas ref="qrCanvas"></canvas>
        <p class="secret">備用密鑰：<code>{{ secret }}</code></p>
      </div>
      <div class="verify">
        <label>輸入驗證碼：</label>
        <input v-model="code" maxlength="6" placeholder="6位數驗證碼" />
        <button @click="verify">啟用 2FA</button>
      </div>
      <div v-if="message" class="message">{{ message }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import QRCode from 'qrcode'
import api from '../utils/axios.js'

const loading = ref(true)
const error = ref('')
const message = ref('')
const qrCanvas = ref(null)
const qrCodeUrl = ref('')
const secret = ref('')
const code = ref('')

onMounted(async () => {
  try {
    loading.value = true
    const resp = await api.post('/api/auth/2fa/setup')
    qrCodeUrl.value = resp.data.qr_code_url
    secret.value = resp.data.secret
    if (qrCanvas.value && qrCodeUrl.value) {
      await QRCode.toCanvas(qrCanvas.value, qrCodeUrl.value, { width: 220 })
    }
  } catch (e) {
    error.value = '取得 2FA 設定失敗'
  } finally {
    loading.value = false
  }
})

async function verify() {
  message.value = ''
  error.value = ''
  if (!code.value || code.value.length !== 6) {
    error.value = '請輸入 6 位數驗證碼'
    return
  }
  try {
    const resp = await api.post('/api/auth/2fa/verify', { code: code.value })
    if (resp.data?.success || resp.status === 200) {
      message.value = '兩步驟驗證已啟用'
    } else {
      error.value = resp.data?.error || '驗證失敗'
    }
  } catch (e) {
    error.value = '驗證失敗'
  }
}
</script>

<style scoped>
.twofa-setup { max-width: 360px; }
.error { color: #c00; margin-top: 8px; }
.message { color: #0a0; margin-top: 8px; }
.secret { margin-top: 8px; }
.verify { margin-top: 12px; display: flex; gap: 8px; align-items: center; }
input { padding: 6px 8px; }
button { padding: 6px 10px; }
</style>
