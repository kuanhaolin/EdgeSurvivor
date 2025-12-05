"""
TC 1.3.3: 2FA 登入驗證碼認證（正確與錯誤）
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
import importlib


class Test2FACodeCorrectVsWrong:
    @pytest.fixture
    def client(self):
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                # 註冊並啟用 2FA 的帳號
                client.post('/api/auth/register', json={'name': 'user01', 'email': 'user1@test.com', 'password': '123456'})
                lr = client.post('/api/auth/login', json={'email': 'user1@test.com', 'password': '123456'})
                token = lr.get_json()['access_token']
                setup = client.post('/api/auth/2fa/setup', headers={'Authorization': f'Bearer {token}'})
                secret = setup.get_json()['secret']
                pyotp = importlib.import_module('pyotp')
                code = pyotp.TOTP(secret).now()
                client.post('/api/auth/2fa/verify', json={'code': code}, headers={'Authorization': f'Bearer {token}'})
                yield client
                db.drop_all()

    # 參數化：正確/錯誤 two_factor_code
    test_data = [
        ('123456', True, '正確驗證碼應成功'),
        ('000000', False, '錯誤驗證碼應失敗')
    ]

    @pytest.mark.parametrize('code_type,expected_success,description', test_data)
    def test_login_with_code(self, client, code_type, expected_success, description):
        # 取 secret 生成碼或使用錯誤碼
        u = User.query.filter_by(email='user1@test.com').first()
        pyotp = importlib.import_module('pyotp')
        code = pyotp.TOTP(u.two_factor_secret).now() if code_type == '123456' else '000000'
        r = client.post('/api/auth/login', json={'email': 'user1@test.com', 'password': '123456', 'two_factor_code': code})
        data = r.get_json()
        if expected_success:
            assert r.status_code == 200, f'{description}，實際 {r.status_code}'
            assert 'access_token' in data
        else:
            assert r.status_code == 401, f'{description}，實際 {r.status_code}'
            assert 'error' in data
