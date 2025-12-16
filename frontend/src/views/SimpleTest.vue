<template>
  <div style="background: red; color: white; padding: 50px; font-size: 30px; min-height: 100vh;">
    測試成功 - iOS 可以看到這個
    <br><br>
    時間: {{ new Date().toLocaleString() }}
    <br><br>
    <div style="background: blue; padding: 20px; margin-top: 20px;">
      點擊次數: {{ count }}
    </div>
    <button 
      @click="count++" 
      style="background: green; color: white; padding: 20px; font-size: 20px; margin-top: 20px; border: none; border-radius: 10px;"
    >
      點我測試
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>
