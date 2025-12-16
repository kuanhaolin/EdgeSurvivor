"""
TC 1.2.6: 帳號是否啟用2FA驗證測試
測試帳號是否啟用2FA驗證，假設test@test.com已啟用, user01@user01.com未啟用
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class Test2FAEnabled:
    """測試2FA啟用狀態"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端並預先設定用戶"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                # 註冊 test@test.com（直接在 DB 設定為啟用 2FA）
                client.post('/api/auth/register', json={
                    'name': 'TestUser',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                user1 = User.query.filter_by(email='test@test.com').first()
                user1.two_factor_enabled = True
                user1.two_factor_secret = 'TESTSECRET123456'
                db.session.commit()
                
                # 註冊 user01@user01.com 但不啟用 2FA
                client.post('/api/auth/register', json={
                    'name': 'User01',
                    'email': 'user01@user01.com',
                    'password': '123456'
                })
                
                yield client
                db.drop_all()
    
    # 共用測試資料
    test_data = [
        ('test@test.com', True, '已啟用2FA'),
        ('user01@user01.com', False, '未啟用2FA'),
    ]
    
    @pytest.mark.parametrize("email,has_2fa,description", test_data)
    def test_2fa_enabled(self, client, email, has_2fa, description):
        """測試2FA啟用狀態 - 直接假設 DB 已設定"""
        # 登入：不帶 two_factor_code
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': '123456'
        })
        data = response.get_json()

        if has_2fa:
            # 啟用 2FA：登入會提示需要驗證碼
            assert response.status_code == 200, f"{description} - 應該返回 200"
            assert data.get('require_2fa') is True, f"{description} - 應該要求 two_factor_code"
        else:
            # 未啟用 2FA：直接成功並返回 access_token
            assert response.status_code == 200, f"{description} - 應該返回 200"
            assert 'access_token' in data, f"{description} - 應該返回 access_token"
            assert not data.get('require_2fa'), f"{description} - 不應要求 two_factor_code"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
