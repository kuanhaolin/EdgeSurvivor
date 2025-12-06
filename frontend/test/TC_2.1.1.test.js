import { describe, it, expect } from 'vitest'
import { validateActivityForm } from '@/utils/activityValidation'

describe('TC_2.1.1 - 活動欄位必填驗證', () => {
  // 測試資料: "期末考", "其他", "中央大學", "2025/12/10", "2025/12/10", "", "5", "":true
  // "放寒假", "", "", "", "", "", "", "":false
  // "開學", "其他", "", "", "", "", "", "":false
  const testCases = [
    { title: '期末考', type: '其他', location: '中央大學', startDate: '2025/12/10', endDate: '2025/12/10', description: '', maxMembers: '5', expected: true },
    { title: '放寒假', type: '', location: '', startDate: '', endDate: '', description: '', maxMembers: '', expected: false },
    { title: '開學', type: '其他', location: '', startDate: '', endDate: '', description: '', maxMembers: '', expected: false }
  ]

  it.each(testCases)(
    '$title, $type, $location, $startDate, $endDate',
    ({ title, type, location, startDate, endDate, description, maxMembers, expected }) => {
      const dateRange = startDate && endDate ? [startDate, endDate] : []
      const activityForm = {
        title,
        type,
        location,
        dateRange,
        description,
        maxMembers
      }

      const actual = validateActivityForm(activityForm)
      
      // 顯示對比資訊
      // console.log(`\n測試資料: title="${title}", type="${type}", location="${location}", startDate="${startDate}", endDate="${endDate}"`)
      // console.log(`預期結果: ${expected}`)
      // console.log(`實際結果: ${actual}`)
      // console.log(`結果: ${actual === expected ? '✓ 通過' : '✗ 失敗'}`)

      expect(actual).toBe(expected)
    }
  )
})
