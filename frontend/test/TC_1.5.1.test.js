/**
 * TC 1.5.1 - 驗證 Email 欄位（忘記密碼）
 * 測試說明：測試忘記密碼的 email 欄位是否正確
 * 測試資料：" ":false, "123@":false, "user@user.com":true
 * 規則來源：ForgotPassword.vue 的 emailRules
 */

import { describe, it, expect } from 'vitest'
import { createEmailRules } from '@/utils/forgotPasswordValidationRules'

describe('TC 1.5.1 - 驗證 Email 欄位', () => {
  
  const rules = createEmailRules()

  // 測試資料：" ":false, "123@":false, "user@user.com":true
  const testCases = [
    { email: ' ', expected: false, description: '空字串' },
    { email: '123@', expected: false, description: '不完整email' },
    { email: 'user@user.com', expected: true, description: '有效email' }
  ]

  it.each(testCases)('$email', ({ email, expected }) => {
    const requiredRule = rules.email.find(r => r.required)
    const typeRule = rules.email.find(r => r.type === 'email')
    
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!email || email.trim() === '') {
        isValid = false
      }
    }
    
    // 檢查 email 格式
    if (isValid && typeRule && typeRule.type === 'email') {
      // Element Plus 的 email 驗證使用簡單的正則表達式
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailPattern.test(email)) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
