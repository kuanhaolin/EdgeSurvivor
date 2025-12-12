/**
 * TC_4.1.6: 依活動類型篩選
 * 測試說明: 測試類型篩選（直接使用前端篩選邏輯）
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { typeMatches } from '../src/utils/activityFilters.js'

describe('TC_4.1.6: 依活動類型篩選', () => {
  let activities

  beforeEach(() => {
    activities = [
      { activity_id: 1, title: '登山健行', type: 'hiking', status: 'active' },
      { activity_id: 2, title: '美食探險', type: 'food', status: 'active' },
      { activity_id: 3, title: '文化之旅', type: 'travel', status: 'active' },
      { activity_id: 4, title: '登高望遠', type: 'hiking', status: 'active' }
    ]
  })

  it('成功篩選指定類型的活動', () => {
    const filterType = 'hiking'
    const filtered = activities.filter(act => typeMatches(act.type, filterType))

    expect(filtered).toHaveLength(2)
    expect(filtered[0].activity_id).toBe(1)
    expect(filtered[1].activity_id).toBe(4)
    filtered.forEach(act => expect(act.type).toBe('hiking'))
  })
})
