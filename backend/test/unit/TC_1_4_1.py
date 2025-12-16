"""
TC 1.4.1 - Google Code 驗證成功
測試說明: 使用有效的 Google authorization code 應該能成功交換 token 並登入
測試資料: Mock Google API 返回有效的 id_token 和 userinfo
"""

import pytest
from unittest.mock import patch, MagicMock

def test_google_code_login_success(client, test_app):
    """測試 Google Code 登入成功流程"""
    
    # Mock Google OAuth token exchange
    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {
        'id_token': 'mock_id_token_12345',
        'access_token': 'mock_google_access_token'
    }
    
    # Mock Google tokeninfo API
    mock_info_response = MagicMock()
    mock_info_response.status_code = 200
    mock_info_response.json.return_value = {
        'email': 'test@gmail.com',
        'name': 'Test',
        'picture': 'https://example.com/photo.jpg',
        'email_verified': True
    }
    
    with patch('requests.post', return_value=mock_token_response), \
         patch('requests.get', return_value=mock_info_response):
        
        response = client.post('/api/auth/google-code', json={
            'code': 'valid_google_code'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        
        # 驗證返回 access_token
        assert 'access_token' in data
        assert data['access_token'] is not None
        
        # 驗證返回 user 資訊
        assert 'user' in data
        assert data['user']['email'] == 'test@gmail.com'
        assert data['user']['name'] == 'Test'
        assert data['user']['profile_picture'] == 'https://example.com/photo.jpg'

def test_google_code_login_missing_code(client):
    """測試缺少 authorization code 時返回錯誤"""
    
    response = client.post('/api/auth/google-code', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'msg' in data
    assert 'Missing authorization code' in data['msg']
