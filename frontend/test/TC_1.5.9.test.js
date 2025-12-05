/**
 * TC 1.5.9 - 已登入使用者變更密碼新密碼欄位驗證
 * 測試說明：測試登入狀態下變更密碼，新密碼欄位驗證
 * 測試資料：" ":false, "123":false, "123456":true
 * 規則來源：Profile.vue 的 changePassword 函數中的驗證邏輯
 */

import { describe, it, expect } from 'vitest'
import { createChangePasswordRules } from '@/utils/changePasswordValidationRules'

describe('TC 1.5.9 - 已登入使用者變更密碼新密碼欄位驗證', () => {
  
  const passwordForm = { newPassword: '' }
  const rules = createChangePasswordRules(passwordForm)

  // 測試資料：" ":false, "123":false, "123456":true
  const testCases = [
    { password: ' ', expected: false, description: '空字串' },
    { password: '123', expected: false, description: '少於6字元' },
    { password: '123456', expected: true, description: '有效密碼(6字元)' }
  ]

  it.each(testCases)('$password', ({ password, expected }) => {
    const requiredRule = rules.newPassword.find(r => r.required)
    const minRule = rules.newPassword.find(r => r.min)
    
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!password || password.trim() === '') {
        isValid = false
      }
    }
    
    // 檢查最小長度
    if (isValid && minRule && minRule.min) {
      if (password.length < minRule.min) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
