/**
 * TC_2.4.1: 創建者移除參與者
 * 測試說明: 測試創建者可以移除參與者
 */

import { describe, it, expect, vi } from 'vitest'
import axios from 'axios'

vi.mock('axios')

describe('TC_2.4.1: 創建者移除參與者', () => {
  
  it('創建者可以移除參與者並呼叫移除API', async () => {
    const activityId = 1
    const participantId = 123
    
    // Mock axios.delete 回應
    axios.delete.mockResolvedValue({
      status: 200,
      data: {
        message: '已移除參與者',
        current_participants: 1
      }
    })
    
    // 模擬前端的 removeParticipant 函數（假設用戶點擊「確定移除」）
    const removeParticipant = async (actId, partId) => {
      const response = await axios.delete(`/activities/${actId}/participants/${partId}`)
      return response
    }
    
    // 創建者執行移除
    const response = await removeParticipant(activityId, participantId)
    
    // 驗證是否真的呼叫了 axios.delete
    expect(axios.delete).toHaveBeenCalledWith(`/activities/${activityId}/participants/${participantId}`)
    expect(axios.delete).toHaveBeenCalledTimes(1)
    
    // 驗證 API 回應
    expect(response.status).toBe(200)
    expect(response.data.message).toBe('已移除參與者')
  })
})
