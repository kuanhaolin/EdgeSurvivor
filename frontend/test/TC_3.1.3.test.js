/**
 * TC_3.1.3: 依地區篩選
 * 測試說明: 測試前端地區篩選邏輯（直接引入 matchFilters.js）
 */
import { describe, it, expect } from 'vitest'
import { applyMatchFilters } from '../src/utils/matchFilters.js'

describe('TC_3.1.3: 依地區篩選', () => {
  it('依地區篩選用戶', () => {
    const recommendedMatches = [
      { user_id: 1, name: '用戶1', location: '台北市', age: 25 },
      { user_id: 2, name: '用戶2', location: '新北市', age: 30 },
      { user_id: 3, name: '用戶3', location: '台中市', age: 28 },
      { user_id: 4, name: '用戶4', location: '高雄市', age: 35 },
      { user_id: 5, name: '用戶5', location: '台北市中山區', age: 27 }
    ]

    const taipeiUsers = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [, ], location: '台北', interests: [], verifiedOnly: false
    })
    expect(taipeiUsers).toHaveLength(2)
    expect(taipeiUsers.every(u => u.location.includes('台北'))).toBe(true)

    const taichungUsers = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [, ], location: '台中', interests: [], verifiedOnly: false
    })
    expect(taichungUsers).toHaveLength(1)
    expect(taichungUsers[0].location).toBe('台中市')

    const allUsers = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [, ], location: '', interests: [], verifiedOnly: false
    })
    expect(allUsers).toHaveLength(5)
  })
})
