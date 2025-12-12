/**
 * TC_3.1.4: 依興趣篩選
 * 測試說明: 測試前端興趣篩選邏輯（直接引入 matchFilters.js）
 */
import { describe, it, expect } from 'vitest'
import { applyMatchFilters } from '../src/utils/matchFilters.js'

describe('TC_3.1.4: 依興趣篩選', () => {
  it('依興趣篩選用戶', () => {
    const recommendedMatches = [
      { user_id: 1, name: '用戶1', interests: ['登山', '露營', '攝影'], age: 25 },
      { user_id: 2, name: '用戶2', interests: ['音樂', '電影'], age: 30 },
      { user_id: 3, name: '用戶3', interests: ['登山', '健行'], age: 28 },
      { user_id: 4, name: '用戶4', interests: ['美食', '旅遊'], age: 35 },
      { user_id: 5, name: '用戶5', interests: [], age: 27 }
    ]

    const hikingUsers = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [18, 65], location: '', interests: ['登山'], verifiedOnly: false
    })
    expect(hikingUsers).toHaveLength(2)
    expect(hikingUsers.every(u => u.interests.includes('登山'))).toBe(true)

    const multiInterests = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [18, 65], location: '', interests: ['登山', '音樂'], verifiedOnly: false
    })
    expect(multiInterests).toHaveLength(3)

    const allUsers = applyMatchFilters(recommendedMatches, {
      gender: '', ageRange: [18, 65], location: '', interests: [], verifiedOnly: false
    })
    expect(allUsers).toHaveLength(5)
  })
})
