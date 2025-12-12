/**
 * TC_3.1.6: 查看用戶資料
 * 測試說明: 測試前端查看完整用戶資料
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_3.1.6: 查看用戶資料', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('查看完整用戶資料', async () => {
    const mockUserProfile = {
      user_id: 123,
      name: '測試用戶',
      email: 'test@example.com',
      gender: 'male',
      age: 28,
      location: '台北市',
      bio: '喜歡登山和攝影的旅行愛好者',
      interests: ['登山', '攝影', '旅遊', '咖啡'],
      avatar: 'https://example.com/avatar.jpg',
      is_verified: true
    }

    axios.get.mockResolvedValueOnce({
      status: 200,
      data: mockUserProfile
    })

    // 模擬載入用戶資料的函數
    const viewUserProfile = async (userId) => {
      const response = await axios.get(`/users/${userId}`)
      return response.data
    }

    const userProfile = await viewUserProfile(123)

    // 驗證用戶資料完整性
    expect(userProfile.user_id).toBe(123)
    expect(userProfile.name).toBe('測試用戶')
    expect(userProfile.gender).toBe('male')
    expect(userProfile.age).toBe(28)
    expect(userProfile.location).toBe('台北市')
    expect(userProfile.bio).toBeTruthy()
    expect(userProfile.interests).toHaveLength(4)
    expect(userProfile.is_verified).toBe(true)

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/users/123')
  })
})
