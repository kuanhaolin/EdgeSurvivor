"""
TC 1.1.7: 密碼加密測試
測試密碼存入後端必須加密，驗證密碼不是明文
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


class TestPasswordEncryption:
    """測試密碼加密"""
    
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
    
    # 共用測試資料
    test_data = [
        ('123456', True, '密碼123456應該加密'),
        ('000000', True, '密碼000000應該加密'),
    ]
    
    @pytest.mark.parametrize("password,expected,description", test_data)
    def test_password_encryption(self, client, password, expected, description):
        """測試密碼加密 - 驗證密碼不是明文儲存"""
        # 註冊用戶
        response = client.post('/api/auth/register', json={
            'name': 'TestUser',
            'email': f'test_{password}@test.com',
            'password': password
        })
        
        # 驗證註冊成功
        assert response.status_code == 201, f"{description} - 註冊應該成功"
        
        # 從資料庫取得用戶
        with client.application.app_context():
            user = User.query.filter_by(email=f'test_{password}@test.com').first()
            
            # 驗證密碼不是明文
            assert user.password_hash != password, f"{description} - 密碼不應該是明文"
            
            # 驗證密碼使用加密（pbkdf2 或 scrypt）
            assert user.password_hash.startswith('pbkdf2:') or user.password_hash.startswith('scrypt:'), \
                f"{description} - 密碼應該使用 pbkdf2 或 scrypt 加密"
            
            # 驗證密碼長度足夠（加密後應該很長）
            assert len(user.password_hash) > 50, f"{description} - 加密後密碼應該足夠長"
            
            # 驗證可以用 check_password 驗證
            assert user.check_password(password) == expected, f"{description} - check_password 應該返回 {expected}"
            
            # 驗證錯誤密碼無法通過
            assert user.check_password('wrongpassword') == False, f"{description} - 錯誤密碼應該無法通過驗證"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
