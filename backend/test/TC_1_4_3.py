"""
TC 1.4.3 - 現有使用者直接登入
測試說明: 已存在的 Google 帳號應該直接登入，不重複建立
測試資料: google_user@gmail.com 登入兩次
"""

import pytest
from unittest.mock import patch, MagicMock
from models.user import User

def test_google_login_existing_user_twice(client, test_app):
    """測試同一個 Google 使用者登入兩次，不重複建立帳號"""
    
    test_email = 'user@user.com'
    
    # Mock Google API 回應
    def create_mock_responses():
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {
            'id_token': 'test_id_token'
        }
        
        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            'email': test_email,
            'name': 'Google User',
            'picture': 'https://example.com/google_user.jpg'
        }
        return mock_token_response, mock_info_response
    
    # 第一次登入
    with patch('requests.post') as mock_post, \
         patch('requests.get') as mock_get:
        
        mock_token, mock_info = create_mock_responses()
        mock_post.return_value = mock_token
        mock_get.return_value = mock_info
        
        response1 = client.post('/api/auth/google-code', json={
            'code': 'first_login_code'
        })
        
        assert response1.status_code == 200
        data1 = response1.get_json()
        first_user_id = data1['user']['user_id']
        first_token = data1['access_token']
        
        # 驗證第一次登入建立了使用者
        with test_app.app_context():
            user = User.query.filter_by(email=test_email).first()
            assert user is not None
            assert user.user_id == first_user_id
            user_count_after_first = User.query.filter_by(email=test_email).count()
            assert user_count_after_first == 1
    
    # 第二次登入（同一個 Google 帳號）
    with patch('requests.post') as mock_post, \
         patch('requests.get') as mock_get:
        
        mock_token, mock_info = create_mock_responses()
        mock_post.return_value = mock_token
        mock_get.return_value = mock_info
        
        response2 = client.post('/api/auth/google-code', json={
            'code': 'second_login_code'
        })
        
        assert response2.status_code == 200
        data2 = response2.get_json()
        second_user_id = data2['user']['user_id']
        second_token = data2['access_token']
        
        # 驗證 user_id 相同（沒有重複建立）
        assert first_user_id == second_user_id
        
        # 驗證資料庫中沒有重複建立
        with test_app.app_context():
            user_count_after_second = User.query.filter_by(email=test_email).count()
            assert user_count_after_second == 1
            
            # 驗證使用者資料一致
            user = User.query.filter_by(email=test_email).first()
            assert user.user_id == first_user_id
            assert user.email == test_email
            
        # 驗證兩次登入都返回有效但不同的 JWT token
        assert first_token is not None
        assert second_token is not None
        assert first_token != second_token
