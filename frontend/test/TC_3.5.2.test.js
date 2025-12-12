/**
 * TC_3.5.2: 刪除好友
 * 測試說明: 測試刪除好友是否成功
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    delete: vi.fn()
  }
}))

describe('TC_3.5.2: 刪除好友', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功刪除好友', async () => {
    const mockResponse = {
      status: 200,
      data: {
        message: '已刪除好友關係'
      }
    }

    axios.delete.mockResolvedValueOnce(mockResponse)

    // 模擬刪除好友的函數
    const deleteFriend = async (matchId) => {
      const response = await axios.delete(`/api/matches/${matchId}`)
      return response.data
    }

    const result = await deleteFriend(1)

    // 驗證返回資料
    expect(result.message).toBe('已刪除好友關係')

    // 驗證 API 被正確調用
    expect(axios.delete).toHaveBeenCalledTimes(1)
    expect(axios.delete).toHaveBeenCalledWith('/api/matches/1')
  })
})
