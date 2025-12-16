"""
TC 1.8.4 - 更新地區
測試說明: 測試更新地區，以選單進行，驗證是否更新資訊
測試資料: 台灣
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
            location='香港',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        yield user

def test_update_location(client, test_app, test_user):
    """測試更新地區"""
    # 登入
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']
    
    # 更新地區為台灣
    response = client.put('/api/users/profile', json={
        'location': '台灣'
    }, headers=get_auth_header(token))
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '個人資料更新成功'
    assert data['user']['location'] == '台灣'
    
    # 驗證資料庫中的資料
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.location == '台灣'
