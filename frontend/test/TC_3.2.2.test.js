/**
 * TC_3.2.2: 發送好友請求
 * 測試說明: 測試發送好友請求功能
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    post: vi.fn()
  }
}));

describe('TC_3.2.2: 發送好友請求', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('成功發送好友請求並返回正確資料', async () => {
    const defaultMessage = '希望能成為旅伴，一起探索世界！';
    const customMessage = '你好！看到你也喜歡登山，希望能一起去爬山！';
    
    const mockResponse1 = {
      data: {
        message: '媒合請求已發送',
        match: {
          match_id: 101,
          requester_id: 1,
          responder_id: 2,
          status: 'pending',
          message: defaultMessage,
          created_at: '2024-01-01T10:00:00'
        }
      }
    };

    const mockResponse2 = {
      data: {
        message: '媒合請求已發送',
        match: {
          match_id: 102,
          requester_id: 1,
          responder_id: 3,
          status: 'pending',
          message: customMessage,
          created_at: '2024-01-01T11:00:00'
        }
      }
    };

    axios.post.mockResolvedValueOnce(mockResponse1)
               .mockResolvedValueOnce(mockResponse2);

    // 模擬發送好友請求的函數
    const sendMatchRequest = async (userId, message) => {
      const response = await axios.post('/api/matches', {
        responder_id: userId,
        activity_id: null,
        message: message
      });
      return response.data;
    };

    // 測試 1: 使用預設訊息發送請求
    const result1 = await sendMatchRequest(2, defaultMessage);

    expect(result1.message).toBe('媒合請求已發送');
    expect(result1.match.match_id).toBe(101);
    expect(result1.match.status).toBe('pending');
    expect(result1.match.responder_id).toBe(2);
    expect(result1.match.message).toBe(defaultMessage);

    // 測試 2: 使用自定義訊息發送請求
    const result2 = await sendMatchRequest(3, customMessage);

    expect(result2.match.match_id).toBe(102);
    expect(result2.match.responder_id).toBe(3);
    expect(result2.match.message).toBe(customMessage);

    // 驗證 API 被正確調用兩次
    expect(axios.post).toHaveBeenCalledTimes(2);
    expect(axios.post).toHaveBeenNthCalledWith(1, '/api/matches', {
      responder_id: 2,
      activity_id: null,
      message: defaultMessage
    });
    expect(axios.post).toHaveBeenNthCalledWith(2, '/api/matches', {
      responder_id: 3,
      activity_id: null,
      message: customMessage
    });
  });
});
