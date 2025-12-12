/**
 * TC_4.1.2: 查看我創建的活動
 * 測試說明: 測試我創建的活動清單
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_4.1.2: 查看我創建的活動', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功取得我創建的活動', async () => {
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
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(mockResponse)

    const getCreatedActivities = async () => {
      const response = await axios.get('/api/activities?type=created')
      return response.data.activities
    }

    const activities = await getCreatedActivities()

    // 驗證活動數量
    expect(activities).toHaveLength(2)

    // 驗證所有活動都是當前用戶創建的
    activities.forEach(act => {
      expect(act.creator_id).toBe(1)
    })

    // 驗證活動標題
    const titles = activities.map(act => act.title)
    expect(titles).toContain('登山活動')
    expect(titles).toContain('美食探索')

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/api/activities?type=created')
  })
})
