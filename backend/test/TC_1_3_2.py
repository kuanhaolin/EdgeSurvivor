"""
TC 1.3.2: 2FA 登入需要驗證碼（未帶 two_factor_code 時）
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
import importlib


class Test2FALoginFlow:
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
                # 註冊三個帳號：user01 啟用 2FA；user02/user03 不啟用
                client.post('/api/auth/register', json={
                    'name': 'user01',
                    'email': 'user01@user01.com',
                    'password': '123456'
                })
                # 登入取得 token
                lr = client.post('/api/auth/login', json={'email': 'user01@user01.com', 'password': '123456'})
                token = lr.get_json()['access_token']
                # setup + verify 啟用 2FA
                setup = client.post('/api/auth/2fa/setup', headers={'Authorization': f'Bearer {token}'})
                secret = setup.get_json()['secret']
                pyotp = importlib.import_module('pyotp')
                code = pyotp.TOTP(secret).now()
                client.post('/api/auth/2fa/verify', json={'code': code}, headers={'Authorization': f'Bearer {token}'})
                yield client
                db.drop_all()

    # 測試資料：user01 啟用 2FA，其餘未啟用
    login_cases = [
        ('user01@user01.com', True, 'user01 已啟用 2FA 應要求驗證碼')
    ]

    @pytest.mark.parametrize('email,requires_code,description', login_cases)
    def test_login_require_2fa_behavior(self, client, email, requires_code, description):
        r = client.post('/api/auth/login', json={'email': email, 'password': '123456'})
        data = r.get_json()
        assert r.status_code == 200, f"{description} - 狀態碼應為 200，實際 {r.status_code}"
        if requires_code:
            assert data.get('require_2fa') is True, f"{description} - 應提示 require_2fa"
        else:
            assert 'access_token' in data, f"{description} - 應直接返回 access_token"
            assert not data.get('require_2fa'), f"{description} - 不應提示 require_2fa"

    # 僅測試未帶驗證碼時的 require_2fa 行為；正確/錯誤碼移至 TC_1_3_3.py
