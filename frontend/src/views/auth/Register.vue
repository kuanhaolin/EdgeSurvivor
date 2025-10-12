<template>
  <div class="register">
    <el-card style="max-width: 400px; margin: 50px auto;">
      <template #header>
        <h2>註冊</h2>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="用戶名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item label="密碼">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="register">註冊</el-button>
          <el-button @click="$router.push('/login')">登入</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      }
    }
  },
  methods: {
    register() {
      console.log('Register:', this.form)
      // TODO: 實現註冊邏輯
    }
  }
}
</script>