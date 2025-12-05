"""
TC 1.5.12 - 更改密碼後更新 Token
測試說明: 測試更改密碼後應返回新的 JWT token
"""

import pytest
from models.user import User
from models import db

def test_change_password_updates_token(client, test_app):
    """測試更改密碼後更新 Token"""
    
    test_email = 'user@user.com'
    old_password = 'oldpassword'
    new_password = 'newpassword'
    
    # 建立用戶
    with test_app.app_context():
        user = User(
            name='user',
            email=test_email,
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password(old_password)
        db.session.add(user)
        db.session.commit()
    
    # 步驟 1: 登入取得第一個 token
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': old_password
    })
    
    assert response.status_code == 200
    old_access_token = response.get_json()['access_token']
    
    # 步驟 2: 使用舊 token 更改密碼
    response = client.post('/api/auth/change-password', 
        json={
            'old_password': old_password,
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {old_access_token}'}
    )
    
    assert response.status_code == 200, "更改密碼應該成功"
    
    # 步驟 3: 使用新密碼重新登入，取得新 token
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': new_password
    })
    
    assert response.status_code == 200, "新密碼應該可以登入"
    new_access_token = response.get_json()['access_token']
    
    # 驗證新舊 token 不同
    assert new_access_token != old_access_token, "新 token 應該與舊 token 不同"
