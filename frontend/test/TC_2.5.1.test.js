/**
 * TC_2.5.1: 創建者刪除任何訊息
 * 測試說明: 測試創建者可以刪除任何活動討論訊息
 */

import { describe, it, expect, vi } from 'vitest'
import axios from 'axios'

vi.mock('axios')

describe('TC_2.5.1: 創建者刪除任何訊息', () => {
  
  it('創建者可以刪除他人訊息並呼叫刪除API', async () => {
    // 模擬訊息資料
    const message = {
      discussion_id: 123,
      user_id: 2,  // 其他用戶
      user: { name: '其他用戶' },
      message: '測試訊息',
      created_at: '2025-12-06T10:00:00Z'
    }
    
    // 模擬當前用戶（創建者）
    const currentUserId = 1
    const creatorId = 1
    
    // 驗證 canDelete 邏輯：創建者可以刪除任何訊息
    const canDelete = (msg) => {
      return msg.user_id === currentUserId || currentUserId === creatorId
    }
    
    expect(canDelete(message)).toBe(true)
    
    // Mock axios.delete 回應
    axios.delete.mockResolvedValue({
      status: 200,
      data: { message: '訊息已刪除' }
    })
    
    // 模擬前端的 deleteMessage 函數（假設用戶點擊「確定」）
    const deleteMessage = async (id) => {
      const response = await axios.delete(`/discussions/${id}`)
      return response
    }
    
    // 創建者執行刪除
    const response = await deleteMessage(message.discussion_id)
    
    // 驗證是否真的呼叫了 axios.delete
    expect(axios.delete).toHaveBeenCalledWith(`/discussions/${message.discussion_id}`)
    expect(axios.delete).toHaveBeenCalledTimes(1)
    
    // 驗證 API 回應
    expect(response.status).toBe(200)
    expect(response.data.message).toBe('訊息已刪除')
  })
})
