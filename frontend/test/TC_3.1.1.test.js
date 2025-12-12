/**
 * TC_3.1.1: 依性別搜尋
 * 測試說明: 測試前端性別篩選邏輯（直接引入 matchFilters.js）
 */
import { describe, it, expect } from 'vitest'
import { applyMatchFilters } from '../src/utils/matchFilters.js'

describe('TC_3.1.1: 依性別搜尋', () => {
  it('依性別篩選用戶', () => {
    // 模擬後端返回的推薦用戶列表
    const recommendedMatches = [
      { user_id: 1, name: '用戶1', gender: 'male', age: 25 },
      { user_id: 2, name: '用戶2', gender: 'female', age: 30 },
      { user_id: 3, name: '用戶3', gender: 'male', age: 28 },
      { user_id: 4, name: '用戶4', gender: 'other', age: 35 }
    ]

    // 測試篩選男性
    const maleFilters = { gender: 'male', ageRange: [18, 65], location: '', interests: [], verifiedOnly: false }
    const maleUsers = applyMatchFilters(recommendedMatches, maleFilters)
    expect(maleUsers).toHaveLength(2)
    expect(maleUsers.every(u => u.gender === 'male')).toBe(true)

    // 測試篩選女性
    const femaleFilters = { gender: 'female', ageRange: [18, 65], location: '', interests: [], verifiedOnly: false }
    const femaleUsers = applyMatchFilters(recommendedMatches, femaleFilters)
    expect(femaleUsers).toHaveLength(1)
    expect(femaleUsers[0].gender).toBe('female')

    // 測試篩選其他
    const otherFilters = { gender: 'other', ageRange: [18, 65], location: '', interests: [], verifiedOnly: false }
    const otherUsers = applyMatchFilters(recommendedMatches, otherFilters)
    expect(otherUsers).toHaveLength(1)
    expect(otherUsers[0].gender).toBe('other')

    // 測試不篩選（顯示全部）
    const noFilters = { gender: '', ageRange: [18, 65], location: '', interests: [], verifiedOnly: false }
    const allUsers = applyMatchFilters(recommendedMatches, noFilters)
    expect(allUsers).toHaveLength(4)
  })
})