/**
 * 變更密碼表單驗證規則
 * 從 Profile.vue 提取出來，方便測試和重複使用
 */

/**
 * 變更密碼表單驗證規則
 * @param {Object} passwordForm - 密碼表單的 reactive 物件
 */
export const createChangePasswordRules = (passwordForm) => {
  const validateConfirmPassword = (rule, value, callback) => {
    if (value === '') {
      callback(new Error('請再次輸入新密碼'))
    } else if (value !== passwordForm.newPassword) {
      callback(new Error('兩次輸入的密碼不一致'))
    } else {
      callback()
    }
  }

  return {
    currentPassword: [
      { required: true, message: '請輸入目前密碼', trigger: 'blur' },
      { min: 6, message: '密碼長度至少需要 6 個字元', trigger: 'blur' }
    ],
    newPassword: [
      { required: true, message: '請輸入新密碼', trigger: 'blur' },
      { min: 6, message: '密碼長度至少需要 6 個字元', trigger: 'blur' }
    ],
    confirmPassword: [
      { required: true, validator: validateConfirmPassword, trigger: 'blur' }
    ]
  }
}
