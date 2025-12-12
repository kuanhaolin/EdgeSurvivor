/**
 * TC_4.3.2: 驗證互評（前端）
 * 測試說明: 測試前端互評評分功能，rating 必填
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateRating } from '../src/utils/reviewValidation.js'

describe('TC_4.3.2: 驗證互評', () => {
  it('驗證評分必填', () => {
    // 測試有效評分
    const validRating = 5
    const validResult = validateRating(validRating)
    expect(validResult.valid).toBe(true)

    // 測試缺少評分
    const missingRating = null
    const missingResult = validateRating(missingRating)
    expect(missingResult.valid).toBe(false)
    expect(missingResult.message).toBe('請選擇 1-5 星評分')

    // 測試評分小於1
    const lowRating = 0
    const lowResult = validateRating(lowRating)
    expect(lowResult.valid).toBe(false)
    expect(lowResult.message).toBe('請選擇 1-5 星評分')

    // 測試評分大於5
    const highRating = 6
    const highResult = validateRating(highRating)
    expect(highResult.valid).toBe(false)
    expect(highResult.message).toBe('請選擇 1-5 星評分')
  })
})
