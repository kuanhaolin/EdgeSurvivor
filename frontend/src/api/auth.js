import api from './index'

const authAPI = {
  // 用戶註冊
  register(userData) {
    return api.post('/auth/register', userData)
  },

  // 用戶登入
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  // 用戶登出
  logout() {
    return api.post('/auth/logout')
  },

  // 刷新令牌
  refreshToken() {
    return api.post('/auth/refresh')
  },

  // 獲取當前用戶資訊
  getCurrentUser() {
    return api.get('/auth/me')
  },

  // 修改密碼
  changePassword(passwords) {
    return api.post('/auth/change-password', passwords)
  },

  // Google 登入
  googleLogin(token) {
    return api.post('/auth/google-login', { token })
  },

  // Google OAuth Code Flow 登入
  googleLoginByCode(code) {
    return api.post('/auth/google-code', { code })
  },

  // 發送重設密碼驗證碼
  sendResetCode(email) {
    return api.post('/auth/forgot-password', { email })
  },

  // 重設密碼
  resetPassword(data) {
    return api.post('/auth/reset-password', data)
  }
}

export default authAPI