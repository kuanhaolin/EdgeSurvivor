"""
TC 1.1.3: 密碼驗證測試
測試密碼必填及長度限制 (至少6個字元)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestPasswordValidation:
    """測試密碼驗證規則"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    # 共用測試資料
    test_data = [
        ('1', 400, '空字串應該失敗'),
        ('123', 400, '5個字元應該失敗'),
        ('123456', 201, '1個字元應該失敗'),
        ('000000', 201, '6個字元應該成功'),
        ('password', 201, '長密碼應該成功'),
    ]
    
    @pytest.mark.parametrize("password,expected_status,description", test_data)
    def test_password_validation(self, client, password, expected_status, description):
        """測試密碼驗證規則 - 驗證測試資料是否符合密碼規則"""
        response = client.post('/api/auth/register', json={
            'name': 'testuser',
            'email': 'test@test.com',
            'password': password
        })
        # 驗證狀態碼
        assert response.status_code == expected_status, f"{description} - {password}"
        
        # 驗證回應資料內容
        data = response.get_json()
        if expected_status == 400:
            assert 'error' in data, f"錯誤回應應該包含 error 欄位 - {password}"
            assert isinstance(data['error'], str), f"error 應該是字串 - {password}"
        else:
            assert 'user' in data, f"成功回應應該包含 user 欄位 - {password}"
            assert 'access_token' in data, f"成功回應應該包含 access_token 欄位 - {password}"
            assert 'refresh_token' in data, f"成功回應應該包含 refresh_token 欄位 - {password}"
            assert data['user']['name'] == 'testuser', f"用戶名應該正確"
