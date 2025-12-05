"""
TC 1.4.5 - Google 登入返回 JWT Token
測試說明: Google 登入成功後應該返回有效的 JWT access_token
測試資料: 驗證 token 存在且不為空
"""

import pytest
from unittest.mock import patch, MagicMock

def test_google_login_returns_access_token(client, test_app):
    """測試 Google 登入成功後返回 access_token"""
    
    test_email = 'user@user.com'
    
    # Mock Google API
    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {
        'id_token': 'test_id_token'
    }
    
    mock_info_response = MagicMock()
    mock_info_response.status_code = 200
    mock_info_response.json.return_value = {
        'email': test_email,
        'name': 'Token Test User',
        'picture': 'https://example.com/token.jpg'
    }
    
    with patch('requests.post', return_value=mock_token_response), \
         patch('requests.get', return_value=mock_info_response):
        
        response = client.post('/api/auth/google-code', json={
            'code': 'test_code'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        
        # 驗證返回 access_token
        assert 'access_token' in data, "應該包含 access_token"
        access_token = data['access_token']
        assert access_token is not None, "access_token 不應該為 None"
        assert len(access_token) > 0, "access_token 長度應該大於 0"
        
        # 驗證返回 user 資訊
        assert 'user' in data, "應該包含 user 資訊"
        assert data['user']['email'] == test_email
