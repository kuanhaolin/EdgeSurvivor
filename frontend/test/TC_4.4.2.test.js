/**
 * TC_4.4.2: 費用金額欄位驗證
 * 測試說明: 測試金額欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateAmount } from '../src/utils/expenseValidation.js'

describe('TC_4.4.2: 費用金額欄位驗證', () => {
  it('驗證金額必填', () => {
    // 測試有效金額
    const validAmount = 100
    const validResult = validateAmount(validAmount)
    expect(validResult.valid).toBe(true)

    // 測試0金額
    const zeroAmount = 0
    const zeroResult = validateAmount(zeroAmount)
    expect(zeroResult.valid).toBe(false)
    expect(zeroResult.message).toBe('請輸入有效金額')

    // 測試負金額
    const negativeAmount = -50
    const negativeResult = validateAmount(negativeAmount)
    expect(negativeResult.valid).toBe(false)
    expect(negativeResult.message).toBe('請輸入有效金額')

    // 測試 null
    const nullAmount = null
    const nullResult = validateAmount(nullAmount)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請輸入有效金額')
  })
})
