/**
 * TC 1.1.1 - 用戶欄位驗證
 * 測試說明：應該要求用戶名必填，且長度需符合2到20個字元
 * 測試資料：1:false, 0:false, 000000000000000000000:false, user01:true, user02:true
 */

import { describe, it, expect } from 'vitest'
import { createRegisterRules } from '@/utils/registerValidationRules'

describe('TC 1.1.1 - 用戶欄位驗證', () => {
  
  const mockRegisterForm = {
    name: '',
    email: '',
    password: '123456',
    confirmPassword: ''
  }
  const rules = createRegisterRules(mockRegisterForm)

  // 測試資料：1:false, 0:false, 000000000000000000000:false, user01:true, user02:true
  const testCases = [
    { name: '1', expected: false },
    { name: '0', expected: false },
    { name: '0'.repeat(21), expected: false },
    { name: 'user01', expected: true },
    { name: 'user02', expected: true }
  ]

  it.each(testCases)('$name', ({ name, expected }) => {
    const requiredRule = rules.name.find(r => r.required)
    const lengthRule = rules.name.find(r => r.min && r.max)
    
    // 模擬 Element Plus 表單驗證邏輯
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!name || name.trim() === '') {
        isValid = false
      }
    }
    
    // 檢查長度限制
    if (isValid && lengthRule && lengthRule.min && lengthRule.max) {
      if (name.length < lengthRule.min || name.length > lengthRule.max) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
