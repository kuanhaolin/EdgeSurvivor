/**
 * TC_3.1.7: 用戶最小資料測試
 * 測試說明: 測試系統處理最小必要資料的能力（邊界測試）
 */
import { describe, it, expect } from 'vitest'
import { applyMatchFilters } from '@/utils/matchFilters'

describe('TC_3.1.7: 用戶最小資料測試', () => {
  it('處理最小資料用戶', () => {
    const minimalUsers = [
      // 完全最小資料：只有必填欄位
      {
        user_id: 1,
        name: '最小用戶A',
        email: 'minimal_a@example.com',
        bio: null,
        interests: [],
        location: null,
        age: null,
        gender: null,
        is_verified: false
      },
      // 空字串資料
      {
        user_id: 2,
        name: '最小用戶B',
        email: 'minimal_b@example.com',
        bio: '',
        interests: [],
        location: '',
        age: undefined,
        gender: '',
        is_verified: false
      },
      // 有效資料
      {
        user_id: 3,
        name: '完整用戶',
        email: 'complete@example.com',
        bio: '自我介紹',
        interests: ['登山'],
        location: '台北市',
        age: 28,
        gender: 'male',
        is_verified: true
      }
    ]

    const filters = {
      gender: '',
      ageRange: [20, 40],
      location: '',
      interests: [],
      verifiedOnly: false
    }

    const result = applyMatchFilters(minimalUsers, filters)

    // 驗證系統不會因為 null/undefined/空值而出錯
    expect(result).toBeDefined()
    expect(Array.isArray(result)).toBe(true)
    // null/undefined 的 age 不會被篩選，只有有效 age 才會檢查範圍
    expect(result).toHaveLength(3)
  })
})
