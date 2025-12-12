/**
 * TC_4.4.5: 分攤方式欄位驗證
 * 測試說明: 測試分攤方式欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateSplitType } from '../src/utils/expenseValidation.js'

describe('TC_4.4.5: 分攤方式欄位驗證', () => {
  it('驗證分攤方式必填且為有效選項', () => {
    // 測試有效分攤方式 - all
    const allResult = validateSplitType('all')
    expect(allResult.valid).toBe(true)

    // 測試有效分攤方式 - selected
    const selectedResult = validateSplitType('selected')
    expect(selectedResult.valid).toBe(true)

    // 測試有效分攤方式 - borrow
    const borrowResult = validateSplitType('borrow')
    expect(borrowResult.valid).toBe(true)

    // 測試無效分攤方式
    const invalidResult = validateSplitType('invalid_type')
    expect(invalidResult.valid).toBe(false)
    expect(invalidResult.message).toBe('請選擇有效的分攤方式')

    // 測試空字串
    const emptyResult = validateSplitType('')
    expect(emptyResult.valid).toBe(false)
    expect(emptyResult.message).toBe('請選擇有效的分攤方式')

    // 測試 null
    const nullResult = validateSplitType(null)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請選擇有效的分攤方式')

    // 測試 undefined
    const undefinedResult = validateSplitType(undefined)
    expect(undefinedResult.valid).toBe(false)
    expect(undefinedResult.message).toBe('請選擇有效的分攤方式')
  })
})
