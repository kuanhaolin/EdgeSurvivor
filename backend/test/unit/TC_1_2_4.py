"""
TC 1.2.4: 信箱登入驗證測試
測試應為已註冊信箱，假設已建立test@test.com
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestEmailLoginValidation:
    """測試信箱登入驗證"""
    
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
                
                # 預先註冊 test@test.com
                client.post('/api/auth/register', json={
                    'name': 'TestUser',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                
                yield client
                db.drop_all()
    
    # 共用測試資料
    test_data = [
        ('test@test.com', True, 'test@test.com 通過'),
        ('user01@user01.com', False, 'user01@user01.com 未註冊'),
        ('user02@user02.com', False, 'user02@user02.com 未註冊'),
    ]
    
    @pytest.mark.parametrize("email,should_exist,description", test_data)
    def test_email_login_validation(self, client, email, should_exist, description):
        """測試信箱登入驗證 - 僅註冊信箱應成功，未註冊信箱應失敗"""
        # 嘗試登入（密碼固定為註冊時的 '123456'）
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': '123456'
        })

        if should_exist:
            # 已註冊的信箱 + 正確密碼 應該成功
            assert response.status_code == 200, f"{description} - 已註冊信箱應該成功登入(200)，實際 {response.status_code}"
            data = response.get_json()
            assert 'access_token' in data, f"{description} - 登入成功應返回 access_token"
        else:
            # 未註冊的信箱應該失敗（帳密錯誤）
            assert response.status_code == 401, f"{description} - 未註冊信箱應該返回 401，實際 {response.status_code}"
            data = response.get_json()
            assert 'error' in data, f"{description} - 應該返回錯誤訊息"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
