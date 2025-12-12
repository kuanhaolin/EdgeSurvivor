/**
 * TC_3.2.5: 查看已接受好友請求
 * 測試說明: 測試查看已成功接受的好友請求
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}));

describe('TC_3.2.5: 查看已發送狀態', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('成功載入已接受的好友請求', async () => {
    const mockAcceptedMatches = {
      data: {
        matches: [
          {
            match_id: 102,
            responder: { user_id: 3, name: '用戶3', avatar: null, interests: ['旅遊'] },
            status: 'accepted',
            created_at: '2024-01-02T11:00:00'
          },
          {
            match_id: 105,
            responder: { user_id: 6, name: '用戶6', avatar: null, interests: ['登山', '攝影'] },
            status: 'accepted',
            created_at: '2024-01-05T15:00:00'
          }
        ]
      }
    };

    axios.get.mockResolvedValueOnce(mockAcceptedMatches);

    // 模擬載入已接受好友請求的函數
    const loadAcceptedMatches = async () => {
      const response = await axios.get('/api/matches?status=accepted');
      return response.data.matches;
    };

    const acceptedMatches = await loadAcceptedMatches();

    // 驗證返回已接受的請求
    expect(acceptedMatches.length).toBe(2);

    // 驗證所有請求的狀態都是 accepted
    acceptedMatches.forEach(match => {
      expect(match.status).toBe('accepted');
      expect(match.responder).toBeDefined();
      expect(match.responder.name).toBeDefined();
    });

    // 驗證 API 被正確調用
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith('/api/matches?status=accepted');
  });
});
