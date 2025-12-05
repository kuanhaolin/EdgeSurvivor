/**
 * 註冊表單驗證規則
 * 從 Register.vue 提取出來，方便測試和重複使用
 */

/**
 * 確認密碼驗證器
 * @param {Object} registerForm - 註冊表單資料
 */
export const createPasswordValidator = (registerForm) => {
  return (rule, value, callback) => {
    if (value === '') {
      callback(new Error('請再次輸入密碼'))
    } else if (value !== registerForm.password) {
      callback(new Error('兩次輸入密碼不一致'))
    } else {
      callback()
    }
  }
}

/**
 * 註冊表單驗證規則
 * @param {Object} registerForm - 註冊表單資料（用於 confirmPassword 驗證）
 */
export const createRegisterRules = (registerForm) => {
  return {
    name: [
      { required: true, message: '請輸入用戶名', trigger: 'blur' },
      { min: 2, max: 20, message: '用戶名長度在 2 到 20 個字元', trigger: 'blur' }
    ],
    email: [
      { required: true, message: '請輸入電子郵件', trigger: 'blur' },
      { type: 'email', message: '請輸入正確的電子郵件格式', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '請輸入密碼', trigger: 'blur' },
      { min: 6, message: '密碼長度至少 6 個字元', trigger: 'blur' }
    ],
    confirmPassword: [
      { required: true, validator: createPasswordValidator(registerForm), trigger: 'blur' }
    ]
  }
}
