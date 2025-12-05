/**
 * 忘記密碼表單驗證規則
 * 從 ForgotPassword.vue 提取出來，方便測試和重複使用
 */

/**
 * Email 表單驗證規則
 */
export const createEmailRules = () => {
  return {
    email: [
      { required: true, message: '請輸入電子郵件', trigger: 'blur' },
      { type: 'email', message: '請輸入正確的電子郵件格式', trigger: 'blur' }
    ]
  }
}

/**
 * 重設密碼表單驗證規則
 * @param {Object} resetForm - 重設密碼表單的 reactive 物件
 */
export const createResetRules = (resetForm) => {
  const validateConfirmPassword = (rule, value, callback) => {
    if (value === '') {
      callback(new Error('請再次輸入密碼'))
    } else if (value !== resetForm.newPassword) {
      callback(new Error('兩次輸入密碼不一致'))
    } else {
      callback()
    }
  }

  return {
    code: [
      { required: true, message: '請輸入驗證碼', trigger: 'blur' },
      { len: 6, message: '驗證碼為6位數字', trigger: 'blur' }
    ],
    newPassword: [
      { required: true, message: '請輸入新密碼', trigger: 'blur' },
      { min: 6, message: '密碼長度至少 6 個字元', trigger: 'blur' }
    ],
    confirmPassword: [
      { required: true, validator: validateConfirmPassword, trigger: 'blur' }
    ]
  }
}
