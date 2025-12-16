"""
TC 1.1.2: 電子郵件驗證測試
測試電子郵件必填及格式驗證
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestEmailValidation:
    """測試電子郵件驗證規則"""
    
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
        ('test@test', 400, '域名問題'),
        ('testtest.com', 400, '＠問題'),
        ('test @test.com', 400, '空格問題'),
        ('test@test.com', 201, '完整'),
        ('test@gmail.com', 201, '完整'),
    ]
    
    @pytest.mark.parametrize("email,expected_status,description", test_data)
    def test_email_validation(self, client, email, expected_status, description):
        """測試電子郵件驗證規則 - 驗證測試資料是否符合email格式規則"""
        response = client.post('/api/auth/register', json={
            'name': 'testuser',
            'email': email,
            'password': '123456'
        })
        # 驗證狀態碼
        assert response.status_code == expected_status, f"{description} - {email}"
        
        # 驗證回應資料內容
        data = response.get_json()
        if expected_status == 400:
            assert 'error' in data, f"錯誤回應應該包含 error 欄位 - {email}"
            assert isinstance(data['error'], str), f"error 應該是字串 - {email}"
        else:
            assert 'user' in data, f"成功回應應該包含 user 欄位 - {email}"
            assert 'access_token' in data, f"成功回應應該包含 access_token 欄位 - {email}"
            assert 'refresh_token' in data, f"成功回應應該包含 refresh_token 欄位 - {email}"
            assert data['user']['email'] == email, f"email 應該是 {email}"
            assert data['user']['name'] == 'testuser', f"用戶名應該正確 - {email}"
