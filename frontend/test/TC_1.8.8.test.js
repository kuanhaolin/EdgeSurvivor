/**
 * TC 1.8.8 - 更新大頭照
 * 測試說明: 測試上傳照片功能，驗證文件類型、大小限制和上傳流程
 * 測試資料: over2mb.jpg:false, paper.pdf:false, 1.5mb.jpg:true
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { isImageFile, isValidImageSize, validateImageFile, IMAGE_MAX_SIZE } from '../src/utils/imageValidation.js'

// Mock File API
class MockFile {
  constructor(content, name, options = {}) {
    this.content = content
    this.name = name
    this.type = options.type || 'image/jpeg'
    this.size = options.size || content.length
  }
}

// Mock fetch
global.fetch = vi.fn()

// Mock localStorage
const mockLocalStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}
global.localStorage = mockLocalStorage

// 測試資料: over2mb.jpg:false, paper.pdf:false, 1.5mb.jpg:true
const testCases = [
  { 
    filename: 'over2mb.jpg', 
    type: 'image/jpeg', 
    size: 3 * 1024 * 1024, // 3MB (超過 2MB)
    expected: false,
    description: '超過2MB'
  },
  { 
    filename: 'paper.pdf', 
    type: 'application/pdf', 
    size: 1024,
    expected: false,
    description: '非圖片文件'
  },
  { 
    filename: '1.5mb.jpg', 
    type: 'image/jpeg', 
    size: 1.5 * 1024 * 1024, // 1.5MB
    expected: true,
    description: '有效的圖片文件'
  }
]

describe('TC_1.8.8: 更新大頭照', () => {
  it.each(testCases)('$filename', ({ filename, type, size, expected }) => {
    const file = new MockFile('x'.repeat(size), filename, {
      type: type,
      size: size
    })

    const validation = validateImageFile(file)
    
    // 驗證結果是否符合預期
    expect(validation.valid).toBe(expected)
    
    if (expected) {
      // 預期通過：錯誤訊息應為 null
      expect(validation.error).toBe(null)
    } else {
      // 預期失敗：應有錯誤訊息
      expect(validation.error).toBeTruthy()
    }
  })
})
