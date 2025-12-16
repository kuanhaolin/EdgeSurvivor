"""
TC 1.3.1: 啟用 2FA（setup + verify）
使用真後端 API：/api/auth/2fa/setup 與 /api/auth/2fa/verify
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
import importlib


class TestEnable2FA:
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
                # 註冊帳號
                client.post('/api/auth/register', json={
                    'name': 'user01',
                    'email': 'user01@user01.com',
                    'password': '123456'
                })
                yield client
                db.drop_all()

    def test_enable_2fa_via_api(self, client):
        # 先登入取得 token
        resp = client.post('/api/auth/login', json={'email': 'user01@user01.com', 'password': '123456'})
        assert resp.status_code == 200
        token = resp.get_json()['access_token']

        # 呼叫 setup 取得 secret
        setup = client.post('/api/auth/2fa/setup', headers={'Authorization': f'Bearer {token}'})
        assert setup.status_code == 200
        secret = setup.get_json().get('secret')
        assert secret

        # 生成 TOTP 並 verify
        pyotp = importlib.import_module('pyotp')
        code = pyotp.TOTP(secret).now()
        verify = client.post('/api/auth/2fa/verify', json={'code': code}, headers={'Authorization': f'Bearer {token}'})
        assert verify.status_code == 200
