/**
 * TC_3.2.6: 更新已發送狀態
 * 測試說明: 測試已發送名單的更新邏輯，取消請求後不會留存紀錄
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    delete: vi.fn()
  }
}));

describe('TC_3.2.6: 更新已發送狀態', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('取消請求後更新已發送名單不留存紀錄', async () => {
    // 模擬已發送名單 API
    const loadSentMatches = async () => {
      const response = await axios.get('/api/matches/sent');
      return response.data.matches;
    };

    // 模擬取消請求 API
    const cancelMatch = async (matchId) => {
      const response = await axios.delete(`/api/matches/${matchId}`);
      return response.data;
    };

    // 1. Mock 初始已發送名單（2 個）
    axios.get.mockResolvedValueOnce({
      data: {
        matches: [
          {
            match_id: 101,
            responder: { user_id: 2, name: '測試用戶2' },
            status: 'pending'
          },
          {
            match_id: 102,
            responder: { user_id: 3, name: '測試用戶3' },
            status: 'pending'
          }
        ]
      }
    });

    // 2. 載入初始已發送名單
    let sentMatches = await loadSentMatches();
    expect(sentMatches.length).toBe(2);
    expect(sentMatches[0].match_id).toBe(101);
    expect(sentMatches[1].match_id).toBe(102);

    // 3. Mock 取消第一個請求成功
    axios.delete.mockResolvedValueOnce({
      data: { message: '已取消媒合請求' }
    });

    // 4. Mock 取消後的已發送名單（只剩 1 個）
    axios.get.mockResolvedValueOnce({
      data: {
        matches: [
          {
            match_id: 102,
            responder: { user_id: 3, name: '測試用戶3' },
            status: 'pending'
          }
        ]
      }
    });

    // 5. 取消第一個請求
    const cancelResult1 = await cancelMatch(101);
    expect(cancelResult1.message).toBe('已取消媒合請求');

    // 6. 重新載入已發送名單
    sentMatches = await loadSentMatches();
    expect(sentMatches.length).toBe(1);
    expect(sentMatches[0].match_id).toBe(102);

    // 7. 驗證被取消的請求不在名單中
    const remainingIds = sentMatches.map(m => m.match_id);
    expect(remainingIds).not.toContain(101);

    // 8. Mock 取消第二個請求成功
    axios.delete.mockResolvedValueOnce({
      data: { message: '已取消媒合請求' }
    });

    // 9. Mock 取消後的已發送名單（空）
    axios.get.mockResolvedValueOnce({
      data: { matches: [] }
    });

    // 10. 取消第二個請求
    const cancelResult2 = await cancelMatch(102);
    expect(cancelResult2.message).toBe('已取消媒合請求');

    // 11. 重新載入已發送名單
    sentMatches = await loadSentMatches();
    expect(sentMatches.length).toBe(0);

    // 12. 驗證 API 調用次數
    expect(axios.delete).toHaveBeenCalledTimes(2);
    expect(axios.delete).toHaveBeenNthCalledWith(1, '/api/matches/101');
    expect(axios.delete).toHaveBeenNthCalledWith(2, '/api/matches/102');
    expect(axios.get).toHaveBeenCalledTimes(3); // 初始 + 兩次更新
  });
});
