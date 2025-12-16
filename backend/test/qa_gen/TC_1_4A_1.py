"""
TC 1.4A.1 - 2FA Setup 端點測試
測試說明: 測試使用有效 JWT 呼叫 /api/auth/2fa/setup 應返回 secret 和 qr_code_url
測試資料: 已登入的用戶
"""

import pytest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class Test2FASetup:
    """測試 2FA Setup 端點"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    def test_2fa_setup_success(self, client):
        """測試成功設定 2FA - 應返回 secret 和 qr_code_url"""
        # 1. 先註冊用戶
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test2fa@test.com',
            'password': 'Password123'
        })
        assert register_response.status_code == 201
        
        # 2. 取得 access token
        data = register_response.get_json()
        access_token = data['access_token']
        
        # 3. 呼叫 2FA setup 端點
        response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        # 4. 驗證響應
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'secret' in data
        assert 'qr_code_url' in data
        
        # 5. 驗證 secret 格式（base32，通常 16 或 32 字元）
        secret = data['secret']
        assert len(secret) >= 16
        assert re.match(r'^[A-Z2-7]+$', secret), 'Secret 應該是有效的 base32 字串'
        
        # 6. 驗證 qr_code_url 格式
        qr_url = data['qr_code_url']
        assert qr_url.startswith('otpauth://totp/EdgeSurvivor:')
        assert f'test2fa@test.com' in qr_url
        assert f'secret={secret}' in qr_url
        assert 'issuer=EdgeSurvivor' in qr_url
        
        print(f"✓ Secret: {secret}")
        print(f"✓ QR Code URL: {qr_url}")
    
    def test_2fa_setup_without_auth(self, client):
        """測試未登入呼叫 setup 應返回 401"""
        response = client.post('/api/auth/2fa/setup')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'msg' in data or 'message' in data
        
        msg = data.get('msg') or data.get('message')
        print(f"✓ 未認證請求被正確拒絕: {msg}")
    
    def test_2fa_setup_with_invalid_token(self, client):
        """測試使用無效 token 應返回 422 或 401"""
        response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': 'Bearer invalid_token_12345'}
        )
        
        assert response.status_code in [401, 422]
        
        print(f"✓ 無效 token 被正確拒絕: {response.status_code}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--no-cov'])
