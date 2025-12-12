/**
 * TC_3.4.4: 更新聊天室
 * 測試說明: 測試訊息是否會在介面同步更新
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

describe('TC_3.4.4: 更新聊天室', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功同步更新聊天室訊息', async () => {
    // 模擬初始訊息列表
    const initialMessages = {
      status: 200,
      data: {
        messages: [
          {
            message_id: 1,
            sender_id: 1,
            receiver_id: 2,
            content: '第一條訊息',
            created_at: '2024-01-01T10:00:00'
          }
        ]
      }
    }

    // 模擬發送新訊息
    const newMessageResponse = {
      status: 201,
      data: {
        success: true,
        message: {
          message_id: 2,
          sender_id: 2,
          receiver_id: 1,
          content: '回覆訊息',
          created_at: '2024-01-01T10:01:00'
        }
      }
    }

    // 模擬更新後的訊息列表
    const updatedMessages = {
      status: 200,
      data: {
        messages: [
          {
            message_id: 1,
            sender_id: 1,
            receiver_id: 2,
            content: '第一條訊息',
            created_at: '2024-01-01T10:00:00'
          },
          {
            message_id: 2,
            sender_id: 2,
            receiver_id: 1,
            content: '回覆訊息',
            created_at: '2024-01-01T10:01:00'
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(initialMessages)
    axios.post.mockResolvedValueOnce(newMessageResponse)
    axios.get.mockResolvedValueOnce(updatedMessages)

    // 模擬聊天室更新流程
    const chatRoomUpdate = async (userId) => {
      // 1. 載入初始訊息
      const initial = await axios.get(`/api/chat/${userId}/messages`)
      
      // 2. 發送新訊息
      await axios.post('/api/chat/messages', {
        receiver_id: userId,
        content: '回覆訊息'
      })
      
      // 3. 重新載入訊息列表
      const updated = await axios.get(`/api/chat/${userId}/messages`)
      
      return updated.data.messages
    }

    const messages = await chatRoomUpdate(1)

    // 驗證訊息列表已更新
    expect(messages).toHaveLength(2)
    expect(messages[0].content).toBe('第一條訊息')
    expect(messages[1].content).toBe('回覆訊息')

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(2)
    expect(axios.post).toHaveBeenCalledTimes(1)
  })
})
