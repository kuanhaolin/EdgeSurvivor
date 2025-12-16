"""
TC 1.4A.2 - 2FA Verify 端點測試
測試說明: 測試使用正確/錯誤驗證碼呼叫 /api/auth/2fa/verify
測試資料: 已設定 2FA secret 的用戶
"""

import pytest
import sys
import os
import pyotp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class Test2FAVerify:
    """測試 2FA Verify 端點"""
    
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
    
    def test_2fa_verify_success(self, client):
        """測試使用正確驗證碼應成功啟用 2FA"""
        # 1. 註冊用戶
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'verify2fa@test.com',
            'password': 'Password123'
        })
        assert register_response.status_code == 201
        access_token = register_response.get_json()['access_token']
        
        # 2. 設定 2FA
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        assert setup_response.status_code == 200
        secret = setup_response.get_json()['secret']
        
        # 3. 生成有效的 TOTP 驗證碼
        totp = pyotp.TOTP(secret)
        valid_code = totp.now()
        
        # 4. 驗證碼確認
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': valid_code}
        )
        
        # 5. 驗證響應
        assert verify_response.status_code == 200
        data = verify_response.get_json()
        assert data['success'] is True
        assert '已啟用' in data['message']
        
        print(f"✓ 使用驗證碼 {valid_code} 成功啟用 2FA")
        print(f"✓ 響應訊息: {data['message']}")
    
    def test_2fa_verify_wrong_code(self, client):
        """測試使用錯誤驗證碼應返回 400"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'wrongcode@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        assert setup_response.status_code == 200
        
        # 2. 使用錯誤的驗證碼
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': '000000'}  # 錯誤的驗證碼
        )
        
        # 3. 驗證響應
        assert verify_response.status_code == 400
        data = verify_response.get_json()
        assert data['success'] is False
        assert '錯誤' in data['error']
        
        print(f"✓ 錯誤驗證碼被正確拒絕")
        print(f"✓ 錯誤訊息: {data['error']}")
    
    def test_2fa_verify_without_setup(self, client):
        """測試未先呼叫 setup 就驗證應返回 400"""
        # 1. 只註冊，不設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'nosetup@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        # 2. 直接嘗試驗證
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': '123456'}
        )
        
        # 3. 驗證響應
        assert verify_response.status_code == 400
        data = verify_response.get_json()
        assert 'error' in data
        assert '設定' in data['error']
        
        print(f"✓ 未設定就驗證被正確拒絕")
        print(f"✓ 錯誤訊息: {data['error']}")
    
    def test_2fa_verify_missing_code(self, client):
        """測試未提供驗證碼應返回 400"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'nocode@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        # 2. 不提供 code 欄位
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={}
        )
        
        # 3. 驗證響應
        assert verify_response.status_code == 400
        data = verify_response.get_json()
        assert 'error' in data
        
        print(f"✓ 缺少驗證碼被正確拒絕")
        print(f"✓ 錯誤訊息: {data['error']}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--no-cov'])
