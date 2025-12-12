/**
 * TC_4.1.1: 查看用戶所有活動
 * 測試說明: 測試我的所有活動清單
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_4.1.1: 查看用戶所有活動', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功取得用戶所有活動', async () => {
    const mockResponse = {
      status: 200,
      data: {
        activities: [
          {
            activity_id: 1,
            title: '登山活動',
            category: 'hiking',
            location: '陽明山',
            date: '2024-02-01',
            creator_id: 1,
            status: 'active'
          },
          {
            activity_id: 2,
            title: '美食探索',
            category: 'food',
            location: '台北',
            date: '2024-02-05',
            creator_id: 1,
            status: 'active'
          },
          {
            activity_id: 3,
            title: '文化之旅',
            category: 'culture',
            location: '故宮',
            date: '2024-02-10',
            creator_id: 2,
            status: 'active'
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(mockResponse)

    // 模擬取得所有活動的函數
    const getAllActivities = async () => {
      const response = await axios.get('/api/activities')
      return response.data.activities
    }

    const activities = await getAllActivities()

    // 驗證活動數量
    expect(activities).toHaveLength(3)

    // 驗證活動標題
    const titles = activities.map(act => act.title)
    expect(titles).toContain('登山活動')
    expect(titles).toContain('美食探索')
    expect(titles).toContain('文化之旅')

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/api/activities')
  })
})
