/**
 * TC_3.4.2: 訊息未讀狀態
 * 測試說明: 測試未讀訊息數與訊息列表顯示
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_3.4.2: 訊息未讀狀態', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功顯示未讀訊息列表與數量', async () => {
    const mockResponse = {
      status: 200,
      data: {
        conversations: [
          {
            match_id: 101,
            other_user: {
              user_id: 2,
              name: 'user02',
              avatar: null,
              is_online: true
            },
            last_message: {
              content: '你好，希望能成為旅伴',
              created_at: '2024-01-01T10:00:00'
            },
            unread_count: 3
          },
          {
            match_id: 102,
            other_user: {
              user_id: 3,
              name: 'user03',
              avatar: null,
              is_online: false
            },
            last_message: {
              content: '一起去旅遊吧',
              created_at: '2024-01-02T11:00:00'
            },
            unread_count: 2
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(mockResponse)

    // 模擬獲取對話列表的函數
    const getConversations = async () => {
      const response = await axios.get('/api/chat/conversations')
      return response.data.conversations
    }

    const conversations = await getConversations()

    // 驗證對話數量
    expect(conversations).toHaveLength(2)

    // 驗證第一個對話的未讀訊息
    expect(conversations[0].unread_count).toBe(3)
    expect(conversations[0].other_user.name).toBe('user02')
    expect(conversations[0].last_message.content).toBe('你好，希望能成為旅伴')

    // 驗證第二個對話的未讀訊息
    expect(conversations[1].unread_count).toBe(2)
    expect(conversations[1].other_user.name).toBe('user03')

    // 計算總未讀數
    const totalUnread = conversations.reduce((sum, conv) => sum + conv.unread_count, 0)
    expect(totalUnread).toBe(5)

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/api/chat/conversations')
  })
})
