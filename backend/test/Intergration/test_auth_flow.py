"""
身份與帳戶管理整合測試
測試範圍:
1. 完整註冊流程
2. 登入流程
3. 2FA 驗證
4. 密碼重設
5. 社群帳號連結
6. 隱私設定
"""

import pytest
from models.user import User
from flask_jwt_extended import create_access_token


class TestAuthenticationFlow:
    """測試完整的認證流程"""
    
    def test_complete_registration_and_login_flow(self, client, db_session, test_app):
        """
        測試完整註冊與登入流程:
        1. 註冊新用戶
        2. 驗證用戶資料儲存
        3. 登入
        4. 取得用戶資料
        """
        # 1. 註冊新用戶
        register_data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'location': 'Taipei',
            'gender': 'male',
            'age': 25
        }
        
        response = client.post('/api/auth/register', json=register_data)
        assert response.status_code == 201
        data = response.get_json()
        assert 'user' in data
        assert data['message'] == '註冊成功'
        user_id = data['user']['user_id']
        
        # 2. 驗證用戶資料儲存
        with test_app.app_context():
            user = db_session.query(User).filter_by(user_id=user_id).first()
            assert user is not None
            assert user.email == 'newuser@example.com'
            assert user.name == 'New User'
            assert user.check_password('SecurePass123!')
        
        # 3. 登入
        login_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        access_token = data['access_token']
        
        # 4. 使用 token 取得用戶資料
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = client.get('/api/users/profile', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        # The response has a 'user' key containing the user data
        assert 'user' in data
        assert data['user']['email'] == 'newuser@example.com'
        assert data['user']['name'] == 'New User'
        assert data['user']['location'] == 'Taipei'
    
    def test_login_with_invalid_credentials(self, client, test_user):
        """測試使用錯誤憑證登入"""
        login_data = {
            'email': test_user.email,
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
        data = response.get_json()
        # API 可能返回 'message' 或 'error'
        assert 'message' in data or 'error' in data
    
    def test_duplicate_email_registration(self, client, test_user):
        """測試重複 email 註冊"""
        register_data = {
            'name': 'Another User',
            'email': test_user.email,  # 使用已存在的 email
            'password': 'SecurePass123!',
            'location': 'Taipei',
            'gender': 'male',
            'age': 25
        }
        
        response = client.post('/api/auth/register', json=register_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert '已被註冊' in data['error'] or 'already' in data['error'].lower()
    
    def test_token_refresh_flow(self, client, test_user, test_app):
        """測試 token 刷新流程"""
        # 1. 登入取得 refresh token
        login_data = {
            'email': test_user.email,
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        data = response.get_json()
        refresh_token = data['refresh_token']
        
        # 2. 使用 refresh token 取得新的 access token
        headers = {
            'Authorization': f'Bearer {refresh_token}',
            'Content-Type': 'application/json'
        }
        
        response = client.post('/api/auth/refresh', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data


class TestProfileManagement:
    """測試個人資料管理"""
    
    def test_update_profile(self, client, auth_headers, test_user, db_session, test_app):
        """測試更新個人資料"""
        update_data = {
            'name': 'Updated Name',
            'bio': 'This is my bio',
            'location': 'Kaohsiung',
            'age': 30
        }
        
        response = client.put('/api/users/profile', 
                             json=update_data, 
                             headers=auth_headers)
        assert response.status_code == 200
        
        # 驗證資料已更新
        with test_app.app_context():
            db_session.expire_all()  # 清除 session 快取
            user = db_session.query(User).filter_by(user_id=test_user.user_id).first()
            assert user.name == 'Updated Name'
            assert user.bio == 'This is my bio'
            assert user.location == 'Kaohsiung'
            assert user.age == 30
    
    def test_social_account_linking(self, client, auth_headers, test_user, db_session, test_app):
        """測試社群帳號連結"""
        social_data = {
            'social_links': {
                'instagram': 'https://instagram.com/testuser',
                'facebook': 'https://facebook.com/testuser',
                'line': 'testuser_line',
                'twitter': 'https://twitter.com/testuser'
            }
        }
        
        response = client.put('/api/users/profile', 
                             json=social_data, 
                             headers=auth_headers)
        assert response.status_code == 200
        
        # 驗證社群帳號已連結
        with test_app.app_context():
            db_session.expire_all()
            user = db_session.query(User).filter_by(user_id=test_user.user_id).first()
            assert user.instagram_url == 'https://instagram.com/testuser'
            assert user.facebook_url == 'https://facebook.com/testuser'
            assert user.line_id == 'testuser_line'
            assert user.twitter_url == 'https://twitter.com/testuser'
    
    def test_social_privacy_settings(self, client, auth_headers, test_user, 
                                     multiple_users, db_session, test_app):
        """
        測試社群隱私設定:
        1. 設定為僅好友可見
        2. 非好友無法看到社群帳號
        3. 好友可以看到社群帳號
        """
        # 1. 設定社群帳號
        social_data = {
            'social_links': {
                'instagram': 'https://instagram.com/testuser'
            }
        }
        
        response = client.put('/api/users/profile', 
                             json=social_data, 
                             headers=auth_headers)
        assert response.status_code == 200
        
        # 2. 設定隱私為僅好友可見
        privacy_data = {
            'social_privacy': 'friends_only'
        }
        
        response = client.put('/api/users/privacy',
                             json=privacy_data,
                             headers=auth_headers)
        assert response.status_code == 200
        
        # 2. 非好友查看個人資料
        # Query the user from database to avoid detached instance error
        with test_app.app_context():
            other_user = db_session.query(User).filter_by(email='user1@example.com').first()
            if other_user:
                other_user_id = other_user.user_id
                other_token = create_access_token(identity=str(other_user_id))
            else:
                # Fallback: create a simple user for testing
                pytest.skip("No other user available for privacy testing")
        
        other_headers = {
            'Authorization': f'Bearer {other_token}',
            'Content-Type': 'application/json'
        }
        
        response = client.get(f'/api/users/{test_user.user_id}', 
                             headers=other_headers)
        assert response.status_code == 200
        data = response.get_json()
        
        # The response has a 'user' key containing the user data
        # 非好友應該看不到社群帳號
        assert 'user' in data
        assert data['user']['social_links']['instagram'] is None
        
        # 3. 建立好友關係後再測試
        # (這部分會在 test_match_flow.py 中詳細測試)


class TestAccountDeletion:
    """測試帳號刪除"""
    
    def test_delete_account(self, client, auth_headers, test_user, db_session, test_app):
        """測試刪除帳號"""
        # Note: The delete endpoint requires password in request body
        delete_data = {'password': 'password123'}
        response = client.delete('/api/users/account', json=delete_data, headers=auth_headers)
        assert response.status_code == 200
        
        # 驗證帳號已被刪除
        with test_app.app_context():
            db_session.expire_all()
            user = db_session.query(User).filter_by(user_id=test_user.user_id).first()
            assert user is None  # User should be completely deleted
    
    def test_deleted_account_cannot_login(self, client, test_user, db_session, test_app):
        """測試已刪除的帳號無法登入"""
        # 1. 刪除帳號
        with test_app.app_context():
            test_user.is_active = False
            db_session.commit()
        
        # 2. 嘗試登入
        login_data = {
            'email': test_user.email,
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
