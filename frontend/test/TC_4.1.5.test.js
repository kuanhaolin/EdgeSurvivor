/**
 * TC_4.1.5: 依活動關鍵字篩選
 * 測試說明: 測試關鍵字篩選（直接使用前端篩選邏輯）
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { textMatches } from '../src/utils/activityFilters.js'

describe('TC_4.1.5: 依活動關鍵字篩選', () => {
  let activities

  beforeEach(() => {
    activities = [
      { 
        activity_id: 1, 
        title: '陽明山登山健行', 
        category: 'hiking', 
        location: '陽明山',
        description: '探索陽明山美景',
        creatorName: '小明'
      },
      { 
        activity_id: 2, 
        title: '夜市美食探險', 
        category: 'food', 
        location: '士林夜市',
        description: '品嚐台北美食',
        creatorName: '小華'
      },
      { 
        activity_id: 3, 
        title: '溫泉之旅', 
        category: 'leisure', 
        location: '陽明山',
        description: '放鬆身心的溫泉體驗',
        creatorName: '小美'
      }
    ]
  })

  it('成功篩選包含關鍵字的活動', () => {
    const searchQuery = '陽明山'
    const filtered = activities.filter(act => textMatches(act, searchQuery))

    expect(filtered).toHaveLength(2)
    expect(filtered[0].activity_id).toBe(1)
    expect(filtered[1].activity_id).toBe(3)
  })
})
