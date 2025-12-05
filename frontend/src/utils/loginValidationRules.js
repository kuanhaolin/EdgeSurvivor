/**
 * 登入表單驗證規則
 * 從 Login.vue 提取出來，方便測試和重複使用
 */

/**
 * 登入表單驗證規則
 * @param {Object} require2FA - 是否需要兩步驟驗證的 ref
 */
export const createLoginRules = (require2FA) => {
  return {
    username: [
      { required: true, message: '請輸入帳號或電子郵件', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '請輸入密碼', trigger: 'blur' },
      { min: 6, message: '密碼長度至少 6 個字元', trigger: 'blur' }
    ],
    twoFactorCode: [
      { 
        validator: (rule, value, callback) => {
          if (require2FA?.value && !value) {
            callback(new Error('請輸入驗證碼'))
          } else if (require2FA?.value && value.length !== 6) {
            callback(new Error('驗證碼必須為 6 位數'))
          } else {
            callback()
          }
        },
        trigger: 'blur'
      }
    ]
  }
}
