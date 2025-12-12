/**
 * TC_4.1.4: 查看探索活動
 * 測試說明: 測試探索活動清單
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('TC_4.1.4: 查看探索活動', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功取得探索活動', async () => {
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
            creator_id: 2,
            status: 'active'
          },
          {
            activity_id: 3,
            title: '文化之旅',
            category: 'culture',
            location: '故宮',
            date: '2024-02-10',
            creator_id: 3,
            status: 'active'
          }
        ]
      }
    }

    axios.get.mockResolvedValueOnce(mockResponse)

    const getExploreActivities = async () => {
      const response = await axios.get('/api/activities')
      return response.data.activities
    }

    const activities = await getExploreActivities()

    expect(activities).toHaveLength(3)

    const creatorIds = [...new Set(activities.map(act => act.creator_id))]
    expect(creatorIds.length).toBeGreaterThanOrEqual(2)

    const titles = activities.map(act => act.title)
    expect(titles).toContain('登山活動')
    expect(titles).toContain('美食探索')
    expect(titles).toContain('文化之旅')

    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith('/api/activities')
  })
})
