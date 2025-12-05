/**
 * TC 1.3.5 - 驗證碼欄位驗證
 * 測試說明: 測試驗證碼欄位的長度與格式驗證
 * 測試資料: 123456:true, " ":false, "123":false
 */

import { describe, it, expect } from 'vitest'
import { createLoginRules } from '../src/utils/loginValidationRules.js'

// Helper to run Element Plus style rule validators
function runValidator(validator, value) {
  return new Promise((resolve) => {
    validator({}, value, (err) => resolve(err))
  })
}

// 測試資料: 123456:true, " ":false, "123":false
const testCases = [
  { code: '123456', expected: true },
  { code: ' ', expected: false },
  { code: '123', expected: false }
]

describe('TC_1.3.5: 驗證碼欄位驗證', () => {
  const rules = createLoginRules({ value: true })
  const validator = rules.twoFactorCode[0].validator

  it.each(testCases)('$code', async ({ code, expected }) => {
    const err = await runValidator(validator, code)
    
    if (expected) {
      expect(err).toBeUndefined()
    } else {
      expect(err).toBeDefined()
      expect(err?.message).toBeTruthy()
    }
  })
})
