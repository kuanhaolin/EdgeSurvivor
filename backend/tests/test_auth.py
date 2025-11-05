"""
測試使用者認證 API

測試範圍：
- 使用者註冊
- 使用者登入
- JWT Token 驗證
"""

import pytest
from models.user import User


class TestUserAuthentication:
    """使用者認證測試類"""
    
    def test_user_registration(self, client, session):
        """測試使用者註冊"""
        # 準備測試資料
        user_data = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'name': 'New User',
            'gender': 'female',
            'age': 28
        }
        
        # 發送註冊請求
        response = client.post('/api/auth/register', json=user_data)
        
        # 驗證回應
        assert response.status_code == 201
        data = response.get_json()
        
        # 驗證回應包含正確的欄位
        assert 'message' in data
        assert data['message'] == '註冊成功'
        assert 'user' in data
        assert 'access_token' in data
        assert 'refresh_token' in data
        
        # 驗證 user 物件
        user_data_response = data['user']
        assert user_data_response['email'] == user_data['email']
        assert user_data_response['name'] == user_data['name']
        assert user_data_response['gender'] == user_data['gender']
        assert user_data_response['age'] == user_data['age']
        
        # 驗證資料庫中的使用者
        user = session.query(User).filter_by(email=user_data['email']).first()
        assert user is not None
        assert user.name == user_data['name']
        assert user.check_password(user_data['password'])  # 密碼應該被加密
    
    def test_user_registration_duplicate_email(self, client, sample_user):
        """測試重複 email 註冊應該失敗"""
        user_data = {
            'email': 'test@example.com',  # 已存在的 email
            'password': 'password123',
            'name': 'Duplicate User'
        }
        
        response = client.post('/api/auth/register', json=user_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_user_login_success(self, client, sample_user):
        """測試成功登入"""
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == login_data['email']
        assert 'message' in data
        assert data['message'] == '登入成功'
    
    def test_user_login_wrong_password(self, client, sample_user):
        """測試錯誤密碼登入應該失敗"""
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert '電子郵件或密碼錯誤' in data['error']
    
    def test_user_login_nonexistent_email(self, client):
        """測試不存在的 email 登入應該失敗"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert '電子郵件或密碼錯誤' in data['error']
    
    def test_user_login_inactive_account(self, client, session):
        """測試停用帳號無法登入"""
        # 創建一個停用的使用者
        from models.user import User
        inactive_user = User(
            email='inactive@example.com',
            name='Inactive User',
            is_active=False
        )
        inactive_user.set_password('testpass123')
        session.add(inactive_user)
        session.commit()
        
        # 嘗試登入
        login_data = {
            'email': 'inactive@example.com',
            'password': 'testpass123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert '帳號已被停用' in data['error']
    
    def test_user_login_updates_last_seen(self, client, sample_user, session):
        """測試登入成功後更新 last_seen"""
        from datetime import datetime
        
        # 記錄原始的 last_seen 時間
        original_last_seen = sample_user.last_seen
        
        # 登入
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        
        # 刷新 sample_user 以獲取最新資料
        session.refresh(sample_user)
        
        # 驗證 last_seen 已更新
        assert sample_user.last_seen is not None
        if original_last_seen:
            assert sample_user.last_seen > original_last_seen
    
    def test_user_login_missing_credentials(self, client):
        """測試缺少登入憑證"""
        # 缺少密碼
        response = client.post('/api/auth/login', json={'email': 'test@example.com'})
        assert response.status_code == 400
        
        # 缺少 email
        response = client.post('/api/auth/login', json={'password': 'testpass123'})
        assert response.status_code == 400
        
        # 空資料
        response = client.post('/api/auth/login', json={})
        assert response.status_code == 400
    
    def test_protected_route_without_token(self, client):
        """測試無 token 存取受保護路由應該失敗"""
        response = client.get('/api/users/profile')
        
        assert response.status_code == 401
    
    def test_protected_route_with_valid_token(self, client, auth_headers):
        """測試有效 token 存取受保護路由"""
        response = client.get('/api/users/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert 'email' in data['user']
    
    def test_password_hashing(self, session):
        """測試密碼加密"""
        user = User(
            email='hashtest@example.com',
            name='Hash Test'
        )
        plain_password = 'mypassword123'
        user.set_password(plain_password)
        
        # 密碼不應該以明文儲存
        assert user.password_hash != plain_password
        
        # 應該能夠驗證正確的密碼
        assert user.check_password(plain_password)
        
        # 應該拒絕錯誤的密碼
        assert not user.check_password('wrongpassword')


class TestJWTToken:
    """JWT Token 測試類"""
    
    def test_refresh_token(self, client, sample_user):
        """測試刷新 token"""
        # 先登入取得 refresh token
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # 使用 refresh token 取得新的 access token
        refresh_response = client.post('/api/auth/refresh', 
            headers={'Authorization': f'Bearer {refresh_token}'})
        
        assert refresh_response.status_code == 200
        data = refresh_response.get_json()
        assert 'access_token' in data
    
    def test_logout(self, client, auth_headers):
        """測試登出"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data


# 執行測試的說明
"""
執行所有測試：
    pytest

執行特定檔案：
    pytest tests/test_auth.py

執行特定測試類：
    pytest tests/test_auth.py::TestUserAuthentication

執行特定測試：
    pytest tests/test_auth.py::TestUserAuthentication::test_user_registration

顯示詳細輸出：
    pytest -v

顯示 print 輸出：
    pytest -s

產生覆蓋率報告：
    pytest --cov=. --cov-report=html
"""
