<template>
  <div class="not-found">
    <h1>404 - 頁面未找到</h1>
    <p>抱歉，您要找的頁面不存在。</p>
    <el-button @click="$router.push('/')">回到首頁</el-button>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>