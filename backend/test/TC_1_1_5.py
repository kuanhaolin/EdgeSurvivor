"""
TC 1.1.5: 重複註冊測試
測試使用已存在的電子郵件註冊應該失敗
測試說明：輸入已存在的 Email 註冊, 假設已存在:test@test.com
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestDuplicateRegistration:
    """測試重複註冊驗證"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端並預先註冊 test@test.com"""
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                
                # 預先註冊 test@test.com
                client.post('/api/auth/register', json={
                    'name': 'test',
                    'email': 'test@test.com',
                    'password': '123456'
                })
                
                yield client
                db.drop_all()
    
    # 測試資料：test01@test.com:true, test@test02.com:true, test@test.com:false
    test_data = [
        ('test01@test.com', 201, '不同email成功'),
        ('test@test02.com', 201, '不同email成功'),
        ('test@test.com', 400, '相同email失敗'),
    ]
    
    @pytest.mark.parametrize("email,expected_status,description", test_data)
    def test_duplicate_email_registration(self, client, email, expected_status, description):
        """測試重複email註冊 - 已存在 test@test.com"""
        response = client.post('/api/auth/register', json={
            'name': 'newuser',
            'email': email,
            'password': '123456'
        })
        
        if expected_status == 400:
            # 應該失敗 - 重複的email
            assert response.status_code == 400, f"{description} - {email}"
            data = response.get_json()
            assert 'error' in data, "錯誤回應應該包含 error 欄位"
            assert '已被註冊' in data['error'] or 'already' in data['error'].lower(), "錯誤訊息應該提示email已被註冊"
        else:
            # 應該成功 - 不同的email
            assert response.status_code == 201, f"{description} - {email}"
            data = response.get_json()
            assert 'user' in data, "成功回應應該包含 user 欄位"
            assert 'access_token' in data, "成功回應應該包含 access_token"
            assert 'refresh_token' in data, "成功回應應該包含 refresh_token"