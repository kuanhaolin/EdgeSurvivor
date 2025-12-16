"""
TC 1.1.1: 用戶名驗證測試
測試用戶名必填及長度限制 (2-20字元)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestUsernameValidation:
    """測試用戶名驗證規則"""
    
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
        ('1', 400, '1個字元應該失敗'),
        ('0', 400, '1個字元應該失敗'),
        ('000000000000000000000', 400, '21個字元應該失敗'),
        ('user01', 201, 'user01應該成功'),
        ('user02', 201, 'user02應該成功'),
    ]
    
    @pytest.mark.parametrize("name,expected_status,description", test_data)
    def test_username_validation(self, client, name, expected_status, description):
        """測試用戶名驗證規則 - 驗證測試資料是否符合用戶名規則"""
        response = client.post('/api/auth/register', json={
            'name': name,
            'email': f'{name if name else "test"}@test.com',
            'password': '123456'
        })
        # 驗證狀態碼
        assert response.status_code == expected_status, f"{description} - {name}"
        
        # 驗證回應資料內容
        data = response.get_json()
        if expected_status == 400:
            assert 'error' in data, f"錯誤回應應該包含 error 欄位 - {name}"
            assert isinstance(data['error'], str), f"error 應該是字串 - {name}"
        else:
            assert 'user' in data, f"成功回應應該包含 user 欄位 - {name}"
            assert 'access_token' in data, f"成功回應應該包含 access_token 欄位 - {name}"
            assert 'refresh_token' in data, f"成功回應應該包含 refresh_token 欄位 - {name}"
            assert data['user']['name'] == name, f"用戶名應該是 {name}"
            assert data['user']['email'] == f'{name}@test.com', f"email 應該正確 - {name}"