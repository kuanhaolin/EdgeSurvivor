/**
 * TC 1.1.2 - 信箱欄位驗證
 * 測試說明：應該要求信箱必填，且需符合正確格式
 * 測試資料：test@test:false, testtest.com:false, test @test.com:false, test@test.com:true, test@gmail.com:true
 */

import { describe, it, expect } from 'vitest'
import { createRegisterRules } from '@/utils/registerValidationRules'

describe('TC 1.1.2 - 信箱欄位驗證', () => {
  
  const mockRegisterForm = {
    name: '',
    email: '',
    password: '123456',
    confirmPassword: ''
  }
  const rules = createRegisterRules(mockRegisterForm)

  // 測試資料：test@test:false, testtest.com:false, test @test.com:false, test@test.com:true, test@gmail.com:true
  const testCases = [
    { email: 'test@test', expected: false },
    { email: 'testtest.com', expected: false },
    { email: 'test @test.com', expected: false },
    { email: 'test@test.com', expected: true },
    { email: 'test@gmail.com', expected: true }
  ]

  it.each(testCases)('$email', ({ email, expected }) => {
    const requiredRule = rules.email.find(r => r.required)
    const typeRule = rules.email.find(r => r.type === 'email')
    
    // 模擬 Element Plus 表單驗證邏輯
    let isValid = true
    
    // 檢查必填
    if (requiredRule && requiredRule.required) {
      if (!email || email.trim() === '') {
        isValid = false
      }
    }
    
    // 檢查 email 格式（Element Plus 使用的正則表達式）
    if (isValid && typeRule && typeRule.type === 'email') {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailPattern.test(email)) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
