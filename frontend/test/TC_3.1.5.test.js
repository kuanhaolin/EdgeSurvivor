/**
 * TC_3.1.5: 重置篩選
 * 測試說明: 測試篩選重置功能
 */
import { describe, it, expect } from 'vitest'
import { getDefaultFilters } from '../src/utils/matchFilters.js'

describe('TC_3.1.5: 重置篩選', () => {
  it('重置所有篩選條件', () => {
    let filters = {
      gender: 'male',
      ageRange: [25, 35],
      location: '台北',
      interests: ['登山', '露營'],
      verifiedOnly: true
    }

    // 模擬重置篩選功能
    filters = getDefaultFilters()

    // 驗證所有篩選條件都恢復為預設值
    expect(filters.gender).toBe('')
    expect(filters.ageRange).toEqual([20, 40])
    expect(filters.location).toBe('')
    expect(filters.interests).toEqual([])
    expect(filters.verifiedOnly).toBe(false)
  })
})
