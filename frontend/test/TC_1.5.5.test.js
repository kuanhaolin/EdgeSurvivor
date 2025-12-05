/**
 * TC 1.5.5 - 確認新密碼欄位驗證（忘記密碼）
 * 測試說明：測試確認新密碼欄位是否正確且需與新密碼相同
 * 測試資料：假設新密碼為 "123456"，測試 " ":false, "123":false, "123456":true
 * 規則來源：ForgotPassword.vue 的 resetRules.confirmPassword
 */

import { describe, it, expect } from 'vitest'
import { createResetRules } from '@/utils/forgotPasswordValidationRules'

describe('TC 1.5.5 - 確認新密碼欄位驗證', () => {
  
  const newPassword = '123456'
  const resetForm = { newPassword }
  const rules = createResetRules(resetForm)

  // 測試資料：假設新密碼為 "123456"，測試 " ":false, "123":false, "123456":true
  const testCases = [
    { confirmPassword: ' ', expected: false, description: '空字串' },
    { confirmPassword: '123', expected: false, description: '與新密碼不一致' },
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
