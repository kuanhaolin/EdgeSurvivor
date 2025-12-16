<template>
  <div>
    <NavBarSimple />
    <div style="background: green; color: white; padding: 20px; margin: 10px;">
      簡化版 NavBar 測試成功
    </div>
    <div style="padding: 20px;">
      <el-card style="margin: 10px 0;"><p>測試卡片 1</p></el-card>
      <el-card style="margin: 10px 0;"><p>測試卡片 2</p></el-card>
      <el-button type="primary">測試按鈕</el-button>
    </div>
  </div>
</template>
<script setup>
import NavBarSimple from '@/components/NavBarSimple.vue'
</script>
