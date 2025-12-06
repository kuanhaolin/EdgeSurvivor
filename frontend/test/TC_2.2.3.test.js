import { describe, it, expect } from 'vitest'
import { validateActivityUpdateForm } from '@/utils/activityValidation'

describe('TC_2.2.3: 活動更新欄位驗證測試', () => {
  it('dateRange: null', () => {
    const editForm = {
      title: '測試活動',
      category: 'hiking',
      location: '陽明山',
      dateRange: null,
      max_participants: 10
    }
    
    const result = validateActivityUpdateForm(editForm)
    expect(result.valid).toBe(false)
    expect(result.error).toBe('請選擇活動日期')
  })

  it('title: null', () => {
    const editForm = {
      title: '',
      category: 'hiking',
      location: '陽明山',
      dateRange: [new Date('2025-12-15'), new Date('2025-12-16')],
      max_participants: 10
    }
    
    const result = validateActivityUpdateForm(editForm)
    expect(result.valid).toBe(false)
    expect(result.error).toBe('活動名稱不能為空')
  })

  it('category: null', () => {
    const editForm = {
      title: '測試活動',
      category: '',
      location: '陽明山',
      dateRange: [new Date('2025-12-15'), new Date('2025-12-16')],
      max_participants: 10
    }
    
    const result = validateActivityUpdateForm(editForm)
    expect(result.valid).toBe(false)
    expect(result.error).toBe('活動類型不能為空')
  })

  it('location: null', () => {
    const editForm = {
      title: '測試活動',
      category: 'hiking',
      location: '',
      dateRange: [new Date('2025-12-15'), new Date('2025-12-16')],
      max_participants: 10
    }
    
    const result = validateActivityUpdateForm(editForm)
    expect(result.valid).toBe(false)
    expect(result.error).toBe('地點不能為空')
  })

  it('participants: 0, 1', () => {
    const testCases = [
      { max_participants: 0 },
      { max_participants: 1 }
    ]
    
    testCases.forEach(({ max_participants }) => {
      const editForm = {
        title: '測試活動',
        category: 'hiking',
        location: '陽明山',
        dateRange: [new Date('2025-12-15'), new Date('2025-12-16')],
        max_participants
      }
      
      const result = validateActivityUpdateForm(editForm)
      expect(result.valid).toBe(false)
      expect(result.error).toBe('人數必須含2人以上')
    })
  })
})
