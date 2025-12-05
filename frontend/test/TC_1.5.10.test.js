/**
 * TC 1.5.10 - 已登入使用者變更密碼確認密碼欄位驗證
 * 測試說明：測試登入狀態下變更密碼，確認新密碼欄位驗證
 * 測試資料：假設新密碼為 "123456"，測試 " ":false, "654321":false, "123456":true
 * 規則來源：Profile.vue 的 changePassword 函數中的驗證邏輯
 */

import { describe, it, expect } from 'vitest'
import { createChangePasswordRules } from '@/utils/changePasswordValidationRules'

describe('TC 1.5.10 - 已登入使用者變更密碼確認密碼欄位驗證', () => {
  
  const newPassword = '123456'
  const passwordForm = { newPassword }
  const rules = createChangePasswordRules(passwordForm)

  // 測試資料：" ":false, "654321":false, "123456":true
  const testCases = [
    { confirmPassword: ' ', expected: false, description: '空字串' },
    { confirmPassword: '654321', expected: false, description: '與新密碼不一致' },
    { confirmPassword: '123456', expected: true, description: '與新密碼一致' }
  ]

  it.each(testCases)('$confirmPassword', ({ confirmPassword, expected }) => {
    const validatorRule = rules.confirmPassword.find(r => r.validator)
    
    let isValid = true
    
    if (validatorRule && validatorRule.validator) {
      // 模擬 Element Plus 的 validator callback
      validatorRule.validator(null, confirmPassword, (error) => {
        if (error) {
          isValid = false
        }
      })
    }
    
    expect(isValid).toBe(expected)
  })
})
