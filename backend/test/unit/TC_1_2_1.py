"""
TC 1.2.1: 信箱格式轉換測試
測試 Email 轉換為小寫處理
測試資料: test@test.com, TEST@test.com
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestEmailLowerCase:
    """測試信箱格式轉換為小寫"""
    
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
                
                # 建立測試用戶，透過註冊 API
                client.post('/api/auth/register', json={
                    'name': 'testuser',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                
                yield client
                db.drop_all()
    
    # 測試資料：test@test.com, TEST@test.com
    test_data = [
        ('test@test.com', True, '小寫信箱應該成功登入'),
        ('TEST@test.com', True, '大寫信箱應該轉小寫後成功登入'),
        ('Test@Test.COM', True, '混合大小寫信箱應該轉小寫後成功登入'),
    ]
    
    @pytest.mark.parametrize("email,should_succeed,description", test_data)
    def test_email_lowercase_conversion(self, client, email, should_succeed, description):
        """測試信箱轉換為小寫 - 不同大小寫的信箱應該都能登入同一帳戶"""
        # 嘗試登入
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': '123456'
        })
        
        data = response.get_json()
        
        if should_succeed:
            # 驗證登入成功（可能需要2FA或直接返回token）
            assert response.status_code in [200, 201], f"{description} - 預期成功但失敗了"
            # 如果不需要2FA，應該返回token
            if response.status_code == 200:
                assert 'access_token' in data or 'require_2fa' in data, f"{description} - 應該返回token或2FA要求"
        else:
            # 驗證登入失敗
            assert response.status_code in [400, 401], f"{description} - 預期失敗但成功了"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--no-cov'])
