/**
 * TC 1.2.3 - 密碼欄位必填測試
 * 測試說明：登入時密碼欄位必填且長度至少需6個字元（測試 Login.vue 的 password 驗證規則）
 * 測試資料：123:false, 123456:true, 000000:true
 */

import { describe, it, expect } from 'vitest'
import { createLoginRules } from '@/utils/loginValidationRules'

// 測試資料：123:false, 123456:true, 000000:true
const testCases = [
  { password: '123', expected: false },
  { password: '123456', expected: true },
  { password: '000000', expected: true }
]

describe('TC 1.2.3 - 登入密碼欄位必填', () => {
  
  const rules = createLoginRules()

  it.each(testCases)('$password', ({ password, expected }) => {
    const requiredRule = rules.password.find(r => r.required)
    const minRule = rules.password.find(r => r.min)

    // 模擬 Element Plus 表單驗證邏輯
    let isValid = true
    
    // 如果有 required 規則，執行必填驗證
    if (requiredRule && requiredRule.required) {
      if (!password || password.trim() === '') {
        isValid = false
      }
    }
    
    // 如果通過必填驗證，且有 min 規則，執行最小長度驗證
    if (isValid && minRule && minRule.min) {
      if (password.length < minRule.min) {
        isValid = false
      }
    }
    
    expect(isValid).toBe(expected)
  })
})
