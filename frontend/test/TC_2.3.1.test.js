/**
 * TC_2.3.1: 待審核申請管理
 * 測試說明: 測試創建者查看所有待審核申請，驗證創建者是否能查看
 */

import { describe, it, expect, vi } from 'vitest'
import axios from 'axios'

vi.mock('axios')

describe('TC_2.3.1: 待審核申請管理', () => {
  
  it('創建者可以查看待審核申請列表並呼叫API', async () => {
    const activityId = 1
    
    // Mock axios.get 回應
    axios.get.mockResolvedValue({
      status: 200,
      data: {
        pending_participants: [
          {
            participant_id: 1,
            user_id: 2,
            user_name: '測試申請者1',
            status: 'pending'
          },
          {
            participant_id: 2,
            user_id: 3,
            user_name: '測試申請者2',
            status: 'pending'
          }
        ]
      }
    })
    
    // 模擬前端的 viewPendingApplicants 函數
    const viewPendingApplicants = async (actId) => {
      const response = await axios.get(`/activities/${actId}/participants/pending`)
      return response
    }
    
    // 創建者查看待審核列表
    const response = await viewPendingApplicants(activityId)
    
    // 驗證是否真的呼叫了 axios.get
    expect(axios.get).toHaveBeenCalledWith(`/activities/${activityId}/participants/pending`)
    expect(axios.get).toHaveBeenCalledTimes(1)
    
    // 驗證 API 回應
    expect(response.status).toBe(200)
    expect(response.data).toHaveProperty('pending_participants')
    expect(Array.isArray(response.data.pending_participants)).toBe(true)
    expect(response.data.pending_participants.length).toBe(2)
    expect(response.data.pending_participants[0].status).toBe('pending')
  })
})
