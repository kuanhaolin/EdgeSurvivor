"""
TC 1.2.5: 密碼登入驗證測試
測試應為已註冊信箱與密碼且需經過加密比對，假設已建立test@test.com密碼為123456
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestPasswordLoginValidation:
    """測試密碼登入驗證"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端並預先註冊 test@test.com"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                
                # 預先註冊 test@test.com，密碼為 123456
                client.post('/api/auth/register', json={
                    'name': 'TestUser',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                
                yield client
                db.drop_all()
    
    # 共用測試資料
    test_data = [
        ('000000', False, '錯誤密碼 000000 應該失敗'),
        ('123123', False, '錯誤密碼 123123 應該失敗'),
        ('123456', True, '正確密碼 123456 應該成功'),
    ]
    
    @pytest.mark.parametrize("password,expected,description", test_data)
    def test_password_login_validation(self, client, password, expected, description):
        """測試密碼登入驗證 - 驗證密碼是否正確且經過加密比對"""
        # 嘗試登入
        response = client.post('/api/auth/login', json={
            'email': 'test@test.com',
            'password': password
        })
        
        if expected:
            # 正確密碼應該登入成功
            assert response.status_code == 200, f"{description} - 應該返回 200"
            data = response.get_json()
            assert 'access_token' in data, f"{description} - 應該返回 access_token"
            assert 'refresh_token' in data, f"{description} - 應該返回 refresh_token"
            assert 'user' in data, f"{description} - 應該返回 user 資訊"
        else:
            # 錯誤密碼應該失敗
            assert response.status_code == 401, f"{description} - 應該返回 401"
            data = response.get_json()
            assert 'error' in data, f"{description} - 應該返回錯誤訊息"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
