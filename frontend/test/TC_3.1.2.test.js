/**
 * TC_3.1.2: 依年齡範圍篩選
 * 測試說明: 測試前端年齡範圍篩選邏輯（直接引入 matchFilters.js）
 */
import { describe, it, expect } from 'vitest'
import { applyMatchFilters } from '../src/utils/matchFilters.js'

describe('TC_3.1.2: 依年齡範圍篩選', () => {
  it('依年齡範圍篩選用戶', () => {
    // 模擬後端返回的推薦用戶列表
    const recommendedMatches = [
      { user_id: 1, name: '用戶1', age: 20, gender: 'male' },
      { user_id: 2, name: '用戶2', age: 25, gender: 'female' },
      { user_id: 3, name: '用戶3', age: 35, gender: 'male' },
      { user_id: 4, name: '用戶4', age: 45, gender: 'female' },
      { user_id: 5, name: '用戶5', age: 55, gender: 'other' }
    ]

    // 測試篩選 25-40 歲
    const ageRange1 = applyMatchFilters(recommendedMatches, {
      gender: '',
      ageRange: [25, 40],
      location: '',
      interests: [],
      verifiedOnly: false
    })
    expect(ageRange1).toHaveLength(2)
    expect(ageRange1.every(u => u.age >= 25 && u.age <= 40)).toBe(true)

    // 測試篩選 20-30 歲
    const ageRange2 = applyMatchFilters(recommendedMatches, {
      gender: '',
      ageRange: [20, 30],
      location: '',
      interests: [],
      verifiedOnly: false
    })
    expect(ageRange2).toHaveLength(2)
    expect(ageRange2.every(u => u.age >= 20 && u.age <= 30)).toBe(true)

    // 測試篩選全部年齡 (18-65)
    const allAges = applyMatchFilters(recommendedMatches, {
      gender: '',
      ageRange: [18, 65],
      location: '',
      interests: [],
      verifiedOnly: false
    })
    expect(allAges).toHaveLength(5)
  })
})
