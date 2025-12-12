/**
 * TC_4.4.4: 費用代墊人欄位驗證
 * 測試說明: 測試代墊人欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validatePayerId } from '../src/utils/expenseValidation.js'

describe('TC_4.4.4: 費用代墊人欄位驗證', () => {
  it('驗證代墊人必填', () => {
    // 測試有效代墊人 ID
    const validResult = validatePayerId(1)
    expect(validResult.valid).toBe(true)

    // 測試另一個有效 ID
    const validResult2 = validatePayerId(999)
    expect(validResult2.valid).toBe(true)

    // 測試 null
    const nullResult = validatePayerId(null)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請選擇代墊人')

    // 測試 undefined
    const undefinedResult = validatePayerId(undefined)
    expect(undefinedResult.valid).toBe(false)
    expect(undefinedResult.message).toBe('請選擇代墊人')

    // 測試 0
    const zeroResult = validatePayerId(0)
    expect(zeroResult.valid).toBe(false)
    expect(zeroResult.message).toBe('請選擇代墊人')
  })
})
