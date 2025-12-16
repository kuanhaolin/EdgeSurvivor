"""
TC 1.2.7: JWT Token 正確生成測試
測試登入成功後應該返回access_token和refresh_token，驗證token都不為空
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from flask_jwt_extended import decode_token


class TestJWTTokenGeneration:
    """測試JWT Token生成"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端並預先註冊用戶"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                
                # 預先註冊 test@test.com
                client.post('/api/auth/register', json={
                    'name': 'TestUser1',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                
                # 不註冊 user01@user01.com，保留為未註冊用戶以驗證不產生 token
                
                yield client
                db.drop_all()
    
    # 共用測試資料：(email, password, expected_success, description)
    test_data = [
        ('test@test.com', '123456', True, '已註冊用戶應該生成 token'),
        ('user01@user01.com', 'wrongpassword', False, '未註冊或錯誤憑證不應該生成 token'),
    ]
    
    @pytest.mark.parametrize("email,password,expected_success,description", test_data)
    def test_jwt_token_generation(self, client, email, password, expected_success, description):
        """測試JWT Token生成 - 驗證登入成功後返回token"""
        # 嘗試登入
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })
        data = response.get_json()
        
        if expected_success:
            # 正確密碼/已註冊：登入成功並返回 token，且不為空
            assert response.status_code == 200, f"{description} - 預期成功(200)，實際 {response.status_code}"
            
            # 驗證 access_token 存在且不為空
            assert 'access_token' in data, f"{description} - 應該包含 access_token"
            assert data['access_token'], f"{description} - access_token 不應該為空"
            assert len(data['access_token']) > 0, f"{description} - access_token 長度應該大於 0"
            
            # 驗證 refresh_token 存在且不為空
            assert 'refresh_token' in data, f"{description} - 應該包含 refresh_token"
            assert data['refresh_token'], f"{description} - refresh_token 不應該為空"
            assert len(data['refresh_token']) > 0, f"{description} - refresh_token 長度應該大於 0"
            
            # 驗證可以解析 access_token
            with client.application.app_context():
                decoded = decode_token(data['access_token'])
                assert 'sub' in decoded, f"{description} - token 應該包含 sub (user_id)"
                
                # 驗證 token 中的 user_id 正確
                user = User.query.filter_by(email=email).first()
                assert decoded['sub'] == str(user.user_id), f"{description} - token 中的 user_id 應該正確"
            
            # 驗證可以用 access_token 訪問受保護的端點
            headers = {'Authorization': f'Bearer {data["access_token"]}'}
            me_response = client.get('/api/auth/me', headers=headers)
            assert me_response.status_code == 200, f"{description} - 應該可以用 token 訪問 /me"
            me_data = me_response.get_json()
            assert me_data['user']['email'] == email, f"{description} - /me 應該返回正確的用戶信息"
        else:
            # 未註冊或錯誤密碼：不應生成 token
            assert response.status_code == 401, f"{description} - 預期失敗(401)，實際 {response.status_code}"
            assert 'error' in data, f"{description} - 應該返回錯誤訊息"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
