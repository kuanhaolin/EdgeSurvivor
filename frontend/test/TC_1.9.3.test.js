/**
 * TC 1.9.3 - 連結 LINE 並生成 QR Code
 * 測試說明: 測試 LINE ID 連結功能和 QR Code 生成
 * 測試資料: user01
 */

import { describe, it, expect, vi } from 'vitest'
import { generateLineQRCode } from '../src/utils/lineQRCode.js'

// Mock document.createElement 和相關 DOM 操作
const mockImage = {
  src: '',
  alt: '',
  style: {}
}

const mockContainer = {
  innerHTML: '',
  appendChild: vi.fn()
}

global.document = {
  createElement: vi.fn((tag) => {
    if (tag === 'img') {
      return mockImage
    }
    return {}
  })
}

describe('TC_1.9.3: 連結LINE', () => {
  it('user01', () => {
    const lineId = 'user01'
    const result = generateLineQRCode(lineId, mockContainer)

    // 驗證是否成功
    expect(result.success).toBe(true)
    
    // 驗證生成的 URL
    expect(result.lineUrl).toBe('https://line.me/ti/p/user01')
    expect(result.qrCodeUrl).toContain('https://api.qrserver.com/v1/create-qr-code/')
    expect(result.qrCodeUrl).toContain('size=200x200')
  })
})
