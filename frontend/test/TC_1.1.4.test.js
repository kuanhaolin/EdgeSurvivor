/**
 * TC 1.1.4 - 確認密碼欄位驗證
 * 測試說明：應該要求確認密碼必填，且需與密碼欄位相同
 * 假設密碼為123456，測試資料：012345:false, 111111:false, 123456:true
 */

import { describe, it, expect } from 'vitest'
import { createRegisterRules } from '@/utils/registerValidationRules'

describe('TC 1.1.4 - 確認密碼欄位驗證', () => {
  
  // 測試資料：假設密碼為 123456
  const mockPassword = '123456'
  
  // 測試資料：012345:false, 111111:false, 123456:true
  const testCases = [
    { confirmPassword: '012345', expected: false },
    { confirmPassword: '111111', expected: false },
    { confirmPassword: '123456', expected: true }
  ]

  it.each(testCases)('$confirmPassword', async ({ confirmPassword, expected }) => {
    const mockRegisterForm = {
      name: '',
      email: '',
      password: mockPassword,
      confirmPassword: confirmPassword
    }
    const rules = createRegisterRules(mockRegisterForm)
    const validatorRule = rules.confirmPassword.find(r => r.validator)
    
    // 模擬 Element Plus 表單驗證邏輯
    let isValid = true
    
    // 使用前端的 validator 規則驗證
    if (validatorRule && validatorRule.validator) {
      await new Promise((resolve) => {
        validatorRule.validator(null, confirmPassword, (error) => {
          if (error) {
            isValid = false
          }
          resolve()
        })
      })
    }
    
    expect(isValid).toBe(expected)
  })
})
