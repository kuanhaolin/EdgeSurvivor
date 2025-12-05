"""
TC 1.2.2: 信箱欄位必填測試
測試登入時信箱欄位必填且需符合正確格式
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestEmailLoginRequired:
    """測試信箱欄位必填"""
    
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
    
    # 測試資料：空信箱應該失敗，有效信箱應該通過格式驗證
    test_data = [
        ('', False, '空信'),
        ('test@test.com', True, '有效信箱'),
        ('test@gmail.com', True, '有效信箱'),
    ]
    
    @pytest.mark.parametrize("email,should_pass,description", test_data)
    def test_email_required(self, client, email, should_pass, description):
        """測試信箱欄位必填 - 驗證信箱必填"""
        # 嘗試登入
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': '123456'
        })
        
        if should_pass:
            # 有效信箱應該通過格式驗證（可能因用戶不存在返回 401，但不會是 400）
            assert response.status_code != 400, f"{description} - 不應該返回 400 (格式錯誤)"
        else:
            # 空信箱應該返回 400
            assert response.status_code == 400, f"{description} - 應該返回 400"
            data = response.get_json()
            assert 'error' in data, f"{description} - 應該返回錯誤訊息"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
