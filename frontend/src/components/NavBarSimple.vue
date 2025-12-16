<template>
  <div style="background: #409EFF; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 20px; font-weight: bold;">EdgeSurvivor</div>
    <div style="display: flex; gap: 15px;">
      <button @click="$router.push('/dashboard')" style="background: white; color: #409EFF; border: none; padding: 8px 15px; border-radius: 5px;">控制台</button>
      <button @click="$router.push('/activities')" style="background: white; color: #409EFF; border: none; padding: 8px 15px; border-radius: 5px;">活動</button>
      <button @click="logout" style="background: #F56C6C; color: white; border: none; padding: 8px 15px; border-radius: 5px;">登出</button>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>
