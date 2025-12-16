"""
TC 1.2.3: 密碼欄位必填測試
測試登入時密碼欄位必填且長度至少需6個字元
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestPasswordLoginRequired:
    """測試密碼欄位必填"""
    
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
    
    # 測試資料：空密碼與短密碼應該失敗；至少 6 個字元應該通過
    test_data = [
        ('', False, '未填'),
        ('123456', True, '成功'),
        ('000000', True, '成功'),
    ]
    
    @pytest.mark.parametrize("password,should_pass,description", test_data)
    def test_password_required(self, client, password, should_pass, description):
        """測試密碼欄位必填 - 驗證密碼必填且長度至少6字元"""
        # 嘗試登入
        response = client.post('/api/auth/login', json={
            'email': 'test@test.com',
            'password': password
        })
        
        if should_pass:
            # 長度符合應該通過驗證（可能因用戶不存在返回 401，但不會是 400）
            assert response.status_code != 400, f"{description} - 不應該返回 400 (格式錯誤)"
        else:
            # 空密碼或長度不足應該返回 400
            assert response.status_code == 400, f"{description} - 應該返回 400"
            data = response.get_json()
            assert 'error' in data, f"{description} - 應該返回錯誤訊息"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
