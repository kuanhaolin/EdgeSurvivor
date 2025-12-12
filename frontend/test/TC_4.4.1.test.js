/**
 * TC_4.4.1: 費用項目欄位驗證
 * 測試說明: 測試費用項目欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateDescription } from '../src/utils/expenseValidation.js'

describe('TC_4.4.1: 費用項目欄位驗證', () => {
  it('驗證費用項目必填', () => {
    // 測試有效費用項目
    const validDesc = '午餐費用'
    const validResult = validateDescription(validDesc)
    expect(validResult.valid).toBe(true)

    // 測試空字串
    const emptyDesc = ''
    const emptyResult = validateDescription(emptyDesc)
    expect(emptyResult.valid).toBe(false)
    expect(emptyResult.message).toBe('請填寫費用項目')

    // 測試只有空白字符
    const whitespaceDesc = '   '
    const whitespaceResult = validateDescription(whitespaceDesc)
    expect(whitespaceResult.valid).toBe(false)
    expect(whitespaceResult.message).toBe('請填寫費用項目')

    // 測試 null
    const nullDesc = null
    const nullResult = validateDescription(nullDesc)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請填寫費用項目')
  })
})
