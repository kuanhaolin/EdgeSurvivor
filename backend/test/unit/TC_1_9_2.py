"""
TC 1.9.2 - 連結 Facebook
測試說明: 連結 Facebook 帳號，測試是否能成功儲存連結
測試資料: https://facebook.com/user01
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

def test_link_facebook(client, test_app, test_user):
    """測試連結 Facebook 帳號"""
    # 登入
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']
    
    # 更新社群連結 (Facebook)
    facebook_url = 'https://facebook.com/user01'
    response = client.put('/api/users/profile', json={
        'social_links': {
            'facebook': facebook_url
        }
    }, headers=get_auth_header(token))
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '個人資料更新成功'
    
    # 驗證社群連結已儲存
    assert 'social_links' in data['user']
    assert data['user']['social_links']['facebook'] == facebook_url
    
    # 驗證資料庫中的資料
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.facebook_url == facebook_url
