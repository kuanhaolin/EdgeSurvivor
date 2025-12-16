"""
TC 1.7.2 - 成功刪除帳號
測試說明: 測試成功刪除自己的帳號，驗證能否登入
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

def test_delete_account_success(client, test_app, test_user):
    # 登入取得 token
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']

    # 刪除帳號
    response = client.delete('/api/users/account', json={
        'password': '123456'
    }, headers=get_auth_header(token))
    assert response.status_code == 200
    assert response.get_json()['message'] == '帳號已刪除'
    
    # 驗證無法再登入（應該返回 401 或 404）
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code in [401, 404]
