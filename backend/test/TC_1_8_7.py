"""
TC 1.8.7 - 隱私僅好友可見
測試說明: 測試更新隱私設定，驗證社群資訊是否僅好友可見
測試資料: social_privacy=friends_only
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
            social_privacy='public',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        yield user

def test_privacy_friends_only(client, test_app, test_user):
    """測試隱私設為僅好友可見"""
    # 登入
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']
    
    # 更新社群隱私為僅好友可見
    response = client.put('/api/users/privacy', json={
        'social_privacy': 'friends_only'
    }, headers=get_auth_header(token))
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '隱私設定已更新'
    assert data['social_privacy'] == 'friends_only'
    
    # 驗證資料庫中的資料
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.social_privacy == 'friends_only'
