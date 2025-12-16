"""
TC 1.7.1 - 刪除帳號密碼驗證
測試說明: 測試刪除帳號時的密碼驗證
測試資料: 654321:false, 123456:true
"""

import pytest
from models.user import User
from models import db

def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user(test_app):
    with test_app.app_context():
        user = User(
            name='user',
            email='user@user.com',
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        yield user

# 測試資料
TEST_DATA = [
    {'password': '654321', 'expected': False, 'description': '錯誤密碼'},
    {'password': '123456', 'expected': True, 'description': '正確密碼'}
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_delete_account_password_validation(client, test_app, test_user, test_case):
    password = test_case['password']
    expected = test_case['expected']
    description = test_case['description']
    
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']

    response = client.delete('/api/users/account', json={
        'password': password
    }, headers=get_auth_header(token))
    
    if expected:
        # 正確密碼 - 應該成功
        assert response.status_code == 200, f"{description} 應該返回 200"
        assert response.get_json()['message'] == '帳號已刪除'
    else:
        # 錯誤密碼 - 應該失敗
        assert response.status_code == 400, f"{description} 應該返回 400"
        assert '密碼錯誤' in response.get_json()['error']

