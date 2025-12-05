/**
 * TC 1.5.3 - 驗證驗證碼欄位
 * 測試說明：測試重設密碼的驗證碼欄位格式
 * 測試資料：" ":false, "123":false, "123456":true
 * 規則來源：ForgotPassword.vue 的 resetRules.code
 */

import { describe, it, expect } from 'vitest'
import { createResetRules } from '@/utils/forgotPasswordValidationRules'

describe('TC 1.5.3 - 驗證驗證碼欄位', () => {
  
  const resetForm = { newPassword: '' }
  const rules = createResetRules(resetForm)

  // 測試資料：" ":false, "123":false, "123456":true
  const testCases = [
    { code: ' ', expected: false, description: '空字串' },
    { code: '123', expected: false, description: '少於6位數' },
    { code: '123456', expected: true, description: '正確的6位數' }
  ]

  it.each(testCases)('$code', ({ code, expected }) => {
    const requiredRule = rules.code.find(r => r.required)
    const lenRule = rules.code.find(r => r.len)
    
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!code || code.trim() === '') {
        isValid = false
      }
    }
    
    // 檢查長度
    if (isValid && lenRule && lenRule.len) {
      if (code.length !== lenRule.len) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
