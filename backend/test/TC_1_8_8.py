"""
TC 1.8.8 - 更新大頭照
測試說明: 測試上傳照片，驗證是否更新
測試資料: photo.jpg (模擬)
"""

import pytest
import io
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

def test_upload_avatar(client, test_app, test_user):
    """測試上傳頭像"""
    # 登入
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']
    
    # 創建假圖片文件
    fake_image = io.BytesIO(b'fake image content')
    fake_image.name = 'photo.jpg'
    
    # 上傳圖片
    response = client.post('/api/upload/image', 
        data={'image': (fake_image, 'photo.jpg')},
        headers=get_auth_header(token),
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'url' in data
    assert data['message'] == '上傳成功'
    
    avatar_url = data['url']
    
    # 更新個人資料中的頭像
    response = client.put('/api/users/profile', json={
        'profile_picture': avatar_url
    }, headers=get_auth_header(token))
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '個人資料更新成功'
    assert data['user']['profile_picture'] == avatar_url
    
    # 驗證資料庫中的資料
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.profile_picture == avatar_url
