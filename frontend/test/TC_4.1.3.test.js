/**
 * TC_4.1.3: 查看我參加的活動
 * 測試說明: 測試我參加的活動清單
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_4.1.3: 查看我參加的活動', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功取得我參加的活動', async () => {
    const mockResponse = {
      status: 200,
      data: {
        activities: [
          {
            activity_id: 3,
            title: '登山活動',
            category: 'hiking',
            location: '陽明山',
            date: '2024-02-01',
            creator_id: 2,
            status: 'active'
          },
          {
            activity_id: 4,
            title: '文化之旅',
            category: 'culture',
            location: '故宮',
            date: '2024-02-05',
            creator_id: 3,
            status: 'active'
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(mockResponse)

    const getJoinedActivities = async () => {
      const response = await axios.get('/api/activities?type=joined')
      return response.data.activities
    }

    const activities = await getJoinedActivities()

    expect(activities).toHaveLength(2)
    activities.forEach(act => {
      expect(act.creator_id).not.toBe(1)
    })

    const titles = activities.map(act => act.title)
    expect(titles).toContain('登山活動')
    expect(titles).toContain('文化之旅')

    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/api/activities?type=joined')
  })
})
