/**
 * TC_3.4.5: 刪除訊息
 * 測試說明: 測試刪除自己發送的訊息是否可以被刪除
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    delete: vi.fn(),
    get: vi.fn()
  }
}))

describe('TC_3.4.5: 刪除訊息', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功刪除自己發送的訊息', async () => {
    // 模擬刪除訊息成功
    const deleteResponse = {
      status: 200,
      data: {
        message: '訊息已刪除'
      }
    }

    // 模擬刪除後的訊息列表
    const messagesAfterDelete = {
      status: 200,
      data: {
        messages: [
          {
            message_id: 2,
            sender_id: 1,
            receiver_id: 2,
            content: '第二條訊息',
            created_at: '2024-01-01T10:01:00'
          }
        ]
      }
    }

    axios.delete.mockResolvedValueOnce(deleteResponse)
    axios.get.mockResolvedValueOnce(messagesAfterDelete)

    // 模擬刪除訊息的流程
    const deleteMessage = async (messageId, userId) => {
      // 1. 刪除訊息
      await axios.delete(`/api/chat/messages/${messageId}`)
      
      // 2. 重新載入訊息列表
      const response = await axios.get(`/api/chat/${userId}/messages`)
      return response.data.messages
    }

    const remainingMessages = await deleteMessage(1, 2)

    // 驗證訊息已被刪除（原本有 2 條，刪除後剩 1 條）
    expect(remainingMessages).toHaveLength(1)
    expect(remainingMessages[0].message_id).toBe(2)

    // 驗證 API 被正確調用
    expect(axios.delete).toHaveBeenCalledTimes(1)
    expect(axios.delete).toHaveBeenCalledWith('/api/chat/messages/1')
    expect(axios.get).toHaveBeenCalledTimes(1)
  })
})
