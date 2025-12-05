/**
 * TC 1.1.3 - 密碼欄位驗證
 * 測試說明：應該要求密碼必填，且長度至少需6個字元
 * 測試資料：1:false, 123:false, 123456:true, 000000:true, password:true
 */

import { describe, it, expect } from 'vitest'
import { createRegisterRules } from '@/utils/registerValidationRules'

describe('TC 1.1.3 - 密碼欄位驗證', () => {
  
  const mockRegisterForm = {
    name: '',
    email: '',
    password: '123456',
    confirmPassword: ''
  }
  const rules = createRegisterRules(mockRegisterForm)

  // 測試資料：1:false, 123:false, 123456:true, 000000:true, password:true
  const testCases = [
    { password: '1', expected: false },
    { password: '123', expected: false },
    { password: '123456', expected: true },
    { password: '000000', expected: true },
    { password: 'password', expected: true }
  ]

  it.each(testCases)('$password', ({ password, expected }) => {
    const requiredRule = rules.password.find(r => r.required)
    const minRule = rules.password.find(r => r.min)
    
    // 模擬 Element Plus 表單驗證邏輯
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
