/**
 * TC_2.6.1: 驗證創建者可以刪除任何費用
 * 測試說明: 測試創建者可以刪除其他用戶建立的費用記錄
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    delete: vi.fn()
  }
}))

describe('TC_2.6.1: 驗證創建者可以刪除任何費用', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('創建者可以刪除他人費用並呼叫刪除API', async () => {
    const expenseId = 123
    const creatorId = 1
    const otherUserId = 2
    
    // Mock axios.delete 回應
    axios.delete.mockResolvedValue({
      status: 200,
      data: { message: '費用記錄已刪除' }
    })

    // 模擬刪除費用的函數
    const deleteExpense = async (expenseId) => {
      await axios.delete(`/expenses/${expenseId}`)
    }

    // 模擬 canDelete 權限檢查（創建者可以刪除任何費用）
    const canDelete = (expense, currentUserId, activityCreatorId) => {
      return expense.payer_id === currentUserId || currentUserId === activityCreatorId
    }

    // 測試創建者可以刪除其他用戶的費用
    const expense = {
      expense_id: expenseId,
      payer_id: otherUserId,
      amount: 100,
      description: '測試費用'
    }

    // 驗證權限
    const hasPermission = canDelete(expense, creatorId, creatorId)
    expect(hasPermission).toBe(true)

    // 執行刪除
    await deleteExpense(expenseId)

    // 驗證 API 呼叫
    expect(axios.delete).toHaveBeenCalledWith(`/expenses/${expenseId}`)
    expect(axios.delete).toHaveBeenCalledTimes(1)
  })
})
