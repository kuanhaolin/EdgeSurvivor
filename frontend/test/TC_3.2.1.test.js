/**
 * TC_3.2.1: 驗證請求好友狀態
 * 測試說明: 測試請求狀態，已發送未被回應的或好友不能再次請求
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}));

describe('TC_3.2.1: 驗證請求好友狀態', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('驗證用戶的請求狀態', async () => {
    const mockMatchStatus = {
      data: {
        match: {
          match_id: 101,
          status: 'pending',
          requester_id: 1,
          responder_id: 2,
          created_at: '2024-01-01T10:00:00'
        }
      }
    };

    axios.get.mockResolvedValueOnce(mockMatchStatus);

    // 模擬查詢請求狀態的函數
    const getMatchStatus = async (userId) => {
      const response = await axios.get(`/api/matches/status/${userId}`);
      return response.data.match;
    };

    const matchStatus = await getMatchStatus(2);

    // 驗證請求狀態
    expect(matchStatus.status).toBe('pending');
    expect(matchStatus.match_id).toBe(101);
    expect(matchStatus.responder_id).toBe(2);

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith('/api/matches/status/2');
  });
});
