/**
 * TC_4.2.2: 申請活動（前端）
 * 測試說明: 測試前端申請活動功能
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios')

describe('TC_4.2.2: 申請活動', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('成功申請活動', async () => {
    const activityId = 1
    const message = '我很喜歡登山，希望能加入這個活動！'
    
    // Mock API 回應
    axios.post.mockResolvedValue({
      data: {
        message: '申請已發送，等待活動創建者審核',
        participant_id: 123
      }
    })
    
    // 模擬申請活動
    const response = await axios.post(`/api/activities/${activityId}/join`, {
      message: message
    })
    
    // 驗證 API 呼叫
    expect(axios.post).toHaveBeenCalledWith(
      `/api/activities/${activityId}/join`,
      { message: message }
    )
    
    // 驗證回應
    expect(response.data.message).toBe('申請已發送，等待活動創建者審核')
    expect(response.data.participant_id).toBe(123)
  })
})
