/**
 * TC_4.4.6: 分攤參與者欄位驗證
 * 測試說明: 測試分攤參與者欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateSplitParticipants } from '../src/utils/expenseValidation.js'

describe('TC_4.4.6: 分攤參與者欄位驗證', () => {
  it('驗證分攤參與者', () => {
    const payerId = 1
    
    // 測試 selected 模式 - 有效參與者列表（包含代墊人）
    const validResult = validateSplitParticipants([1, 2, 3], 'selected', payerId)
    expect(validResult.valid).toBe(true)

    // 測試 selected 模式 - 只有代墊人
    const onlyPayerResult = validateSplitParticipants([1], 'selected', payerId)
    expect(onlyPayerResult.valid).toBe(true)

    // 測試 selected 模式 - 空陣列
    const emptyResult = validateSplitParticipants([], 'selected', payerId)
    expect(emptyResult.valid).toBe(false)
    expect(emptyResult.message).toBe('請選擇至少一位參與分攤的人')

    // 測試 selected 模式 - null
    const nullResult = validateSplitParticipants(null, 'selected', payerId)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請選擇至少一位參與分攤的人')

    // 測試 selected 模式 - 不包含代墊人
    const noPayerResult = validateSplitParticipants([2, 3], 'selected', payerId)
    expect(noPayerResult.valid).toBe(false)
    expect(noPayerResult.message).toBe('代墊人必須參與分攤')

    // 測試 selected 模式 - 非陣列
    const notArrayResult = validateSplitParticipants('not-array', 'selected', payerId)
    expect(notArrayResult.valid).toBe(false)
    expect(notArrayResult.message).toBe('請選擇至少一位參與分攤的人')

    // 測試 all 模式 - 不需要驗證參與者（應該 valid）
    const allModeResult = validateSplitParticipants([], 'all', payerId)
    expect(allModeResult.valid).toBe(true)

    // 測試 borrow 模式 - 不需要驗證參與者（應該 valid）
    const borrowModeResult = validateSplitParticipants([], 'borrow', payerId)
    expect(borrowModeResult.valid).toBe(true)
  })
})
