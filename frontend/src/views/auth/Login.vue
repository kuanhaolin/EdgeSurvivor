<template>
  <div class="login">
    <el-card style="max-width: 400px; margin: 50px auto;">
      <template #header>
        <h2>登入</h2>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="Email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item label="密碼">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login">登入</el-button>
          <el-button @click="$router.push('/register')">註冊</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    login() {
      console.log('Login:', this.form)
      // TODO: 實現登入邏輯
    }
  }
}
</script>