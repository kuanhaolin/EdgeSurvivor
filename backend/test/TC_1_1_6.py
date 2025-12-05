"""
TC 1.1.6: 成功註冊測試
測試使用有效資料註冊應該成功並返回正確的資料
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db


class TestSuccessfulRegistration:
    """測試成功註冊流程"""
    
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
    
    # 測試資料
    test_data = [
        ('user01', 'user01@user01.com', '111111', 201, '完整資料成功'),
        ('user02', 'user02@user02.com', '222222', 201, '完整資料成功'),
        ('', 'user03@user03.com', '333333', 400, '缺用戶名'),
        ('user04', '', '444444', 400, '缺email'),
    ]
    
    @pytest.mark.parametrize("name,email,password,expected_status,description", test_data)
    def test_successful_registration(self, client, name, email, password, expected_status, description):
        """測試註冊驗證"""
        response = client.post('/api/auth/register', json={
            'name': name,
            'email': email,
            'password': password
        })
        
        assert response.status_code == expected_status, f"{description} - name:{name}, email:{email}, password:{password}"
        
        data = response.get_json()
        if expected_status == 400:
            assert 'error' in data, "錯誤回應應該包含 error 欄位"
            assert isinstance(data['error'], str), "error 應該是字串"
        else:
            assert 'user' in data, "成功回應應該包含 user 欄位"
            assert 'access_token' in data, "成功回應應該包含 access_token"
            assert 'refresh_token' in data, "成功回應應該包含 refresh_token"
            assert 'message' in data, "成功回應應該包含 message"
            assert data['user']['name'] == name, f"用戶名應該是 {name}"
            assert data['user']['email'] == email, f"email 應該是 {email}"
            assert 'user_id' in data['user'], "應該包含 user_id"
            assert 'password' not in data['user'], "不應該返回密碼"
