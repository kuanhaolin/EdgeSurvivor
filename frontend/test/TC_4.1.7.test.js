/**
 * TC_4.1.7: 依活動狀態篩選
 * 測試說明: 測試狀態篩選（直接使用前端篩選邏輯）
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { statusMatches } from '../src/utils/activityFilters.js'

describe('TC_4.1.7: 依活動狀態篩選', () => {
  let activities

  beforeEach(() => {
    activities = [
      { activity_id: 1, title: '登山健行', category: 'hiking', status: 'active' },
      { activity_id: 2, title: '美食探險', category: 'food', status: 'completed' },
      { activity_id: 3, title: '文化之旅', category: 'culture', status: 'recruiting' },
      { activity_id: 4, title: '溫泉之旅', category: 'leisure', status: 'open' },
      { activity_id: 5, title: '單車遊', category: 'sports', status: 'cancelled' }
    ]
  })

  it('成功篩選活動狀態', () => {
    // 測試 recruiting 狀態（包含 recruiting/active/open）
    const recruitingFiltered = activities.filter(act => statusMatches(act.status, 'recruiting'))
    expect(recruitingFiltered).toHaveLength(3)
    expect(recruitingFiltered[0].activity_id).toBe(1)  // active
    expect(recruitingFiltered[1].activity_id).toBe(3)  // recruiting
    expect(recruitingFiltered[2].activity_id).toBe(4)  // open
    
    // 測試單一狀態
    const completedFiltered = activities.filter(act => statusMatches(act.status, 'completed'))
    expect(completedFiltered).toHaveLength(1)
    expect(completedFiltered[0].status).toBe('completed')
  })
})
