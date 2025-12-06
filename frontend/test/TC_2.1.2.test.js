import { describe, it, expect } from 'vitest'
import { validateDateRange } from '@/utils/activityValidation'

describe('TC_2.1.2 - 開始時間不可早於結束時間', () => {
  // 測試資料: "2025/01/01", "2025/01/02":true, "2026/01/01", "2025/01/01":false
  const testCases = [
    { startDate: '2025/01/01', endDate: '2025/01/02', expected: true },
    { startDate: '2026/01/01', endDate: '2025/01/01', expected: false }
  ]

  it.each(testCases)(
    '$startDate, $endDate',
    ({ startDate, endDate, expected }) => {
      const actual = validateDateRange(startDate, endDate)
      
      // 顯示對比資訊
      // console.log(`\n測試資料: startDate="${startDate}", endDate="${endDate}"`)
      // console.log(`預期結果: ${expected}`)
      // console.log(`實際結果: ${actual}`)
      // console.log(`結果: ${actual === expected ? '✓ 通過' : '✗ 失敗'}`)

      expect(actual).toBe(expected)
    }
  )
})
