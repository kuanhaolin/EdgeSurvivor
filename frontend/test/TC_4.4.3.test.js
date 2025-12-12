/**
 * TC_4.4.3: 費用類別欄位驗證
 * 測試說明: 測試類別欄位驗證
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateCategory } from '../src/utils/expenseValidation.js'

describe('TC_4.4.3: 費用類別欄位驗證', () => {
  it('驗證類別必填且為有效選項', () => {
    // 測試有效類別 - transport
    const transportResult = validateCategory('transport')
    expect(transportResult.valid).toBe(true)

    // 測試有效類別 - accommodation
    const accommodationResult = validateCategory('accommodation')
    expect(accommodationResult.valid).toBe(true)

    // 測試有效類別 - food
    const foodResult = validateCategory('food')
    expect(foodResult.valid).toBe(true)

    // 測試有效類別 - ticket
    const ticketResult = validateCategory('ticket')
    expect(ticketResult.valid).toBe(true)

    // 測試有效類別 - other
    const otherResult = validateCategory('other')
    expect(otherResult.valid).toBe(true)

    // 測試無效類別
    const invalidResult = validateCategory('invalid_category')
    expect(invalidResult.valid).toBe(false)
    expect(invalidResult.message).toBe('請選擇有效的類別')

    // 測試空字串
    const emptyResult = validateCategory('')
    expect(emptyResult.valid).toBe(false)
    expect(emptyResult.message).toBe('請選擇有效的類別')

    // 測試 null
    const nullResult = validateCategory(null)
    expect(nullResult.valid).toBe(false)
    expect(nullResult.message).toBe('請選擇有效的類別')
  })
})
