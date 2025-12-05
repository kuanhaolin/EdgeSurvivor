/**
 * TC 1.2.2 - 信箱欄位必填測試
 * 測試說明：登入時信箱欄位必填（測試 Login.vue 的 username 驗證規則）
 * 測試資料：test@test.com, test@gmail.com:true
 */

import { describe, it, expect } from 'vitest'
import { createLoginRules } from '@/utils/loginValidationRules'

// 測試資料：test@test.com, test@gmail.com:true
const testCases = [
  { email: '', expected: false },
  { email: 'test@test.com', expected: true },
  { email: 'test@gmail.com', expected: true }
]

describe('TC 1.2.2 - 登入信箱欄位必填', () => {
  
  const rules = createLoginRules()

  it.each(testCases)('$email', ({ email, expected }) => {
    const requiredRule = rules.username.find(r => r.required)
    
    // 模擬 Element Plus 表單驗證邏輯
    let isValid = true
    
    // 如果有 required 規則，執行驗證
    if (requiredRule && requiredRule.required) {
      // Element Plus 的 required 驗證：值不能為空
      if (!email || email.trim() === '') {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
