"""
TC 1.4A.3 - 2FA 資料庫狀態測試
測試說明: 測試 2FA 啟用後資料庫狀態是否正確更新
測試資料: 啟用 2FA 的用戶
"""

import pytest
import sys
import os
import pyotp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class Test2FADatabaseState:
    """測試 2FA 資料庫狀態"""
    
    @pytest.fixture
    def test_app(self):
        """建立測試應用"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, test_app):
        """建立測試客戶端"""
        return test_app.test_client()
    
    def test_two_factor_secret_saved_after_setup(self, client, test_app):
        """測試 setup 後 secret 應儲存到資料庫"""
        # 1. 註冊用戶
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'dbtest1@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        user_id = register_response.get_json()['user']['user_id']
        
        # 2. 設定 2FA
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        secret = setup_response.get_json()['secret']
        
        # 3. 檢查資料庫
        with test_app.app_context():
            user = User.query.get(user_id)
            assert user.two_factor_secret == secret
            assert user.two_factor_enabled is False  # 尚未驗證，所以還是 False
            
            print(f"✓ Secret 已儲存到資料庫: {user.two_factor_secret}")
            print(f"✓ two_factor_enabled 狀態: {user.two_factor_enabled} (尚未驗證)")
    
    def test_two_factor_enabled_after_verify(self, client, test_app):
        """測試 verify 成功後 two_factor_enabled 應為 True"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'dbtest2@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        user_id = register_response.get_json()['user']['user_id']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        secret = setup_response.get_json()['secret']
        
        # 2. 生成驗證碼並驗證
        totp = pyotp.TOTP(secret)
        valid_code = totp.now()
        
        client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': valid_code}
        )
        
        # 3. 檢查資料庫狀態
        with test_app.app_context():
            user = User.query.get(user_id)
            assert user.two_factor_enabled is True
            assert user.two_factor_secret == secret
            
            print(f"✓ two_factor_enabled 已更新為 True")
            print(f"✓ Secret 保留: {user.two_factor_secret}")
    
    def test_verify_failure_does_not_enable_2fa(self, client, test_app):
        """測試驗證失敗不應啟用 2FA"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'dbtest3@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        user_id = register_response.get_json()['user']['user_id']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        # 2. 使用錯誤的驗證碼
        client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': '000000'}
        )
        
        # 3. 檢查資料庫狀態
        with test_app.app_context():
            user = User.query.get(user_id)
            assert user.two_factor_enabled is False
            
            print(f"✓ 驗證失敗後 two_factor_enabled 仍為 False")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--no-cov'])
