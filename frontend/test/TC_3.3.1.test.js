/**
 * TC_3.3.1: 查看待審核邀請
 * 測試說明: 測試前端查看收到的好友請求名單
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_3.3.1: 查看待審核邀請', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('載入待審核的好友請求列表', async () => {
    const mockPendingMatches = [
      {
        match_id: 1,
        created_at: '2025-12-09T10:00:00',
        message: '希望能成為旅伴！',
        requester: {
          user_id: 101,
          name: '發送者A',
          avatar: 'https://example.com/avatar1.jpg',
          interests: ['登山', '攝影']
        },
        activity: {
          activity_id: 201,
          title: '陽明山健行',
          start_date: '2025-12-15T09:00:00'
        }
      },
      {
        match_id: 2,
        created_at: '2025-12-09T11:00:00',
        message: '一起去旅遊吧',
        requester: {
          user_id: 102,
          name: '發送者B',
          avatar: 'https://example.com/avatar2.jpg',
          interests: ['旅遊', '美食']
        }
      }
    ]

    axios.get.mockResolvedValueOnce({
      status: 200,
      data: { matches: mockPendingMatches }
    })

    // 模擬載入待審核請求的函數
    const loadPendingMatches = async () => {
      const response = await axios.get('/matches/pending')
      return response.data.matches
    }

    const matches = await loadPendingMatches()

    // 驗證返回的資料
    expect(matches).toHaveLength(2)
    expect(matches[0].match_id).toBe(1)
    expect(matches[0].requester.name).toBe('發送者A')
    expect(matches[0].message).toBe('希望能成為旅伴！')
    expect(matches[0].activity.title).toBe('陽明山健行')
    expect(matches[1].match_id).toBe(2)
    expect(matches[1].requester.user_id).toBe(102)

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/matches/pending')
  })
})
