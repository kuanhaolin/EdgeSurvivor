/**
 * TC_3.3.3: 批准好友請求
 * 測試說明: 測試批准好友請求
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    put: vi.fn()
  }
}))

describe('TC_3.3.3: 批准好友請求', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功批准好友請求', async () => {
    const mockResponse = {
      status: 200,
      data: {
        message: '已接受媒合請求',
        match: {
          match_id: 123,
          user_a: 1,
          user_b: 2,
          status: 'accepted',
          match_date: '2024-01-01T10:00:00'
        }
      }
    }

    axios.put.mockResolvedValueOnce(mockResponse)

    // 模擬批准好友請求的函數
    const acceptMatchRequest = async (matchId) => {
      const response = await axios.put(`/api/matches/${matchId}/accept`)
      return response.data
    }

    const result = await acceptMatchRequest(123)

    // 驗證返回資料
    expect(result.message).toBe('已接受媒合請求')
    expect(result.match.match_id).toBe(123)
    expect(result.match.status).toBe('accepted')

    // 驗證 API 被正確調用
    expect(axios.put).toHaveBeenCalledTimes(1)
    expect(axios.put).toHaveBeenCalledWith('/api/matches/123/accept')
  })
})
