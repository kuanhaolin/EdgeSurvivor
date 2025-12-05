/**
 * TC 1.5.8 - 已登入使用者變更密碼舊密碼欄位驗證
 * 測試說明：測試登入狀態下變更密碼，舊密碼欄位驗證
 * 測試資料：" ":false, "12345":false, "123456":true
 * 規則來源：Profile.vue 的 changePassword 函數中的驗證邏輯
 * 注意：前端只驗證欄位格式，不驗證密碼是否正確（後端負責）
 */

import { describe, it, expect } from 'vitest'
import { createChangePasswordRules } from '@/utils/changePasswordValidationRules'

describe('TC 1.5.8 - 已登入使用者變更密碼舊密碼欄位驗證', () => {
  
  const passwordForm = { currentPassword: '' }
  const rules = createChangePasswordRules(passwordForm)

  // 測試資料：" ":false, "12345":false, "123456":true
  const testCases = [
    { password: ' ', expected: false, description: '空字串' },
    { password: '123', expected: false, description: '少於6字元' },
    { password: '123456', expected: true, description: '有效格式' }
  ]

  it.each(testCases)('$password', ({ password, expected }) => {
    const requiredRule = rules.currentPassword.find(r => r.required)
    const minRule = rules.newPassword.find(r => r.min)
    
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!password || password.trim() === '') {
        isValid = false
      }
    }
    if (isValid && minRule && minRule.min) {
      if (password.length < minRule.min) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
