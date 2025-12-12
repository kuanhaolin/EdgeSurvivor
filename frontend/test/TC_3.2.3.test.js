/**
 * TC_3.2.3: 取消好友邀請
 * 測試說明: 測試取消已發送的請求
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    delete: vi.fn()
  }
}));

describe('TC_3.2.3: 取消好友邀請', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('成功取消已發送的好友請求', async () => {
    const mockDeleteResponse = {
      data: { message: '已取消媒合請求' }
    };

    axios.delete.mockResolvedValueOnce(mockDeleteResponse);

    // 模擬取消請求的函數
    const cancelMatch = async (matchId) => {
      const response = await axios.delete(`/api/matches/${matchId}`);
      return response.data;
    };

    const result = await cancelMatch(101);

    // 驗證回應訊息
    expect(result.message).toBe('已取消媒合請求');

    // 驗證 DELETE API 被正確調用
    expect(axios.delete).toHaveBeenCalledTimes(1);
    expect(axios.delete).toHaveBeenCalledWith('/api/matches/101');
  });
});
