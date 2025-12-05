"""
TC 1.3.4: 停用 2FA（disable）
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
import importlib


class TestDisable2FA:
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

    def test_disable_2fa_via_api(self, client):
        # 先登入 user1；若要求 2FA，帶入正確驗證碼以取得 token
        u = User.query.filter_by(email='user1@test.com').first()
        pyotp = importlib.import_module('pyotp')
        code = pyotp.TOTP(u.two_factor_secret).now()
        lr = client.post('/api/auth/login', json={'email': 'user1@test.com', 'password': '123456', 'two_factor_code': code})
        data_login = lr.get_json()
        assert lr.status_code == 200 and 'access_token' in data_login
        token = data_login['access_token']

        # 使用當前碼停用 2FA
        code = pyotp.TOTP(u.two_factor_secret).now()
        disable = client.post('/api/auth/2fa/disable', json={'code': code}, headers={'Authorization': f'Bearer {token}'})
        assert disable.status_code == 200

        # 再次查詢確認 two_factor_enabled 已停用
        u2 = User.query.filter_by(email='user1@test.com').first()
        assert u2.two_factor_enabled is False
