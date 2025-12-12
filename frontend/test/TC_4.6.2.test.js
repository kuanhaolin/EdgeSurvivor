/**
 * TC_4.6.2: 活動照片上傳 - 前端檔案格式與大小驗證（單一測試）
 * 覆蓋情境：
 * - 合法圖片（類型 image/* 且 <=2MB）
 * - 非圖片類型
 * - 超過 2MB
 * - 未選擇檔案
 */
import { describe, it, expect } from 'vitest'
import { validateImageFile } from '../src/utils/imageValidation.js'

const mockFile = (name, size, type) => ({ name, size, type })

describe('TC_4.6.2: 活動照片上傳檔案驗證', () => {
  it('成功驗證檔案格式規範', () => {
    // 合法：image/jpeg, 1MB
    const valid = validateImageFile(mockFile('ok.jpg', 1 * 1024 * 1024, 'image/jpeg'))
    expect(valid.valid).toBe(true)
    expect(valid.error).toBeNull()

    // 非圖片：application/pdf
    const notImage = validateImageFile(mockFile('bad.pdf', 1000, 'application/pdf'))
    expect(notImage.valid).toBe(false)
    expect(notImage.error).toBe('請選擇圖片檔案')

    // 超過 2MB：image/png 3MB
    const tooLarge = validateImageFile(mockFile('large.png', 3 * 1024 * 1024, 'image/png'))
    expect(tooLarge.valid).toBe(false)
    expect(tooLarge.error).toBe('圖片大小不能超過 2MB')

    // 未選擇檔案
    const noFile = validateImageFile(null)
    expect(noFile.valid).toBe(false)
    expect(noFile.error).toBe('請選擇文件')
  })
})
