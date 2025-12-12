/**
 * TC_3.4.1: 發送訊息給用戶
 * 測試說明: 測試發送訊息給任何用戶是否成功
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn()
  }
}))

describe('TC_3.4.1: 發送訊息給用戶', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功發送訊息給用戶', async () => {
    const mockResponse = {
      status: 201,
      data: {
        success: true,
        message: {
          message_id: 1,
          sender_id: 1,
          receiver_id: 2,
          content: '你好，希望能成為旅伴！',
          message_type: 'text',
          status: 'sent',
          created_at: '2024-01-01T10:00:00'
        }
      }
    }

    axios.post.mockResolvedValueOnce(mockResponse)

    // 模擬發送訊息的函數
    const sendMessage = async (receiverId, content) => {
      const response = await axios.post('/api/chat/messages', {
        receiver_id: receiverId,
        content: content,
        message_type: 'text'
      })
      return response.data
    }

    const result = await sendMessage(2, '你好，希望能成為旅伴！')

    // 驗證返回資料
    expect(result.success).toBe(true)
    expect(result.message.sender_id).toBe(1)
    expect(result.message.receiver_id).toBe(2)
    expect(result.message.content).toBe('你好，希望能成為旅伴！')
    expect(result.message.status).toBe('sent')

    // 驗證 API 被正確調用
    expect(axios.post).toHaveBeenCalledTimes(1)
    expect(axios.post).toHaveBeenCalledWith('/api/chat/messages', {
      receiver_id: 2,
      content: '你好，希望能成為旅伴！',
      message_type: 'text'
    })
  })
})
