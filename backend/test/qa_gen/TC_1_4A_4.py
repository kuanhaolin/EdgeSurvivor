"""
TC 1.4A.4 - 2FA TOTP 驗證窗口測試
測試說明: 測試 TOTP 驗證碼的時間窗口（valid_window=1）
測試資料: 模擬不同時間點的驗證碼
"""

import pytest
import sys
import os
import pyotp
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class Test2FAValidWindow:
    """測試 2FA TOTP 驗證窗口"""
    
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
    
    def test_current_code_is_valid(self, client):
        """測試當前時間的驗證碼應該有效"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'window1@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        secret = setup_response.get_json()['secret']
        
        # 2. 生成當前時間的驗證碼
        totp = pyotp.TOTP(secret)
        current_code = totp.now()
        
        # 3. 驗證
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': current_code}
        )
        
        assert verify_response.status_code == 200
        print(f"✓ 當前驗證碼 {current_code} 通過驗證")
    
    def test_previous_code_is_valid_with_window(self, client):
        """測試前一個時間窗口的驗證碼應該有效（valid_window=1）"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'window2@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        secret = setup_response.get_json()['secret']
        
        # 2. 生成前一個時間窗口的驗證碼
        totp = pyotp.TOTP(secret)
        # 使用 for_time 取得 30 秒前的驗證碼
        import datetime
        past_time = datetime.datetime.now() - datetime.timedelta(seconds=30)
        previous_code = totp.at(past_time)
        
        # 3. 驗證（應該因為 valid_window=1 而通過）
        verify_response = client.post('/api/auth/2fa/verify',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'code': previous_code}
        )
        
        # valid_window=1 允許前後各 1 個窗口（30秒），所以前一個應該有效
        assert verify_response.status_code == 200
        print(f"✓ 前一個窗口的驗證碼 {previous_code} 通過驗證（valid_window=1）")
    
    def test_code_format_validation(self, client):
        """測試驗證碼格式驗證"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'format@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        # 2. 測試各種格式的驗證碼
        test_cases = [
            ('12345', '5位數應該失敗'),
            ('1234567', '7位數應該失敗'),
            ('abcdef', '非數字應該失敗'),
            ('123 456', '包含空格應該失敗'),
        ]
        
        for code, description in test_cases:
            verify_response = client.post('/api/auth/2fa/verify',
                headers={'Authorization': f'Bearer {access_token}'},
                json={'code': code}
            )
            
            # 應該返回 400（格式錯誤或驗證失敗）
            assert verify_response.status_code == 400
            print(f"✓ {description}: {code}")
    
    def test_totp_secret_format(self, client):
        """測試生成的 secret 符合 Base32 格式"""
        # 1. 註冊並設定 2FA
        register_response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'secretformat@test.com',
            'password': 'Password123'
        })
        access_token = register_response.get_json()['access_token']
        
        setup_response = client.post('/api/auth/2fa/setup',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        secret = setup_response.get_json()['secret']
        
        # 2. 驗證 secret 可以被 pyotp 使用
        try:
            totp = pyotp.TOTP(secret)
            code = totp.now()
            assert len(code) == 6
            assert code.isdigit()
            print(f"✓ Secret 格式正確，可生成 6 位數驗證碼: {code}")
        except Exception as e:
            pytest.fail(f"Secret 格式無效: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--no-cov'])
