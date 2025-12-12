/**
 * TC_4.3.4: 驗證評價內容
 * 測試說明: 測試評價者評價內容，必填
 * 直接使用前端驗證邏輯
 */
import { describe, it, expect } from 'vitest'
import { validateComment } from '../src/utils/reviewValidation.js'

describe('TC_4.3.4: 驗證評價內容', () => {
  it('驗證評論內容必填', () => {
    // 測試有效評論
    const validComment = '很棒的旅伴，準時守信，期待下次再一起旅行！'
    const validResult = validateComment(validComment)
    expect(validResult.valid).toBe(true)

    // 測試空字串
    const emptyComment = ''
    const emptyResult = validateComment(emptyComment)
    expect(emptyResult.valid).toBe(false)
    expect(emptyResult.message).toBe('請填寫評價內容')

    // 測試只有空白字符
    const whitespaceComment = '   '
    const whitespaceResult = validateComment(whitespaceComment)
    expect(whitespaceResult.valid).toBe(false)
    expect(whitespaceResult.message).toBe('請填寫評價內容')
  })
})