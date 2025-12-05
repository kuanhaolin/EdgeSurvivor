"""
TC 1.5.10 - 更改密碼成功流程
測試說明: 測試登入後成功更改密碼的完整流程
"""

import pytest
from models.user import User
from models import db

def test_change_password_success_flow(client, test_app):
    """測試登入後成功更改密碼的完整流程"""
    
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
    
    # 步驟 1: 使用舊密碼登入
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': old_password
    })
    
    assert response.status_code == 200, "舊密碼應該可以登入"
    access_token = response.get_json()['access_token']
    
    # 步驟 2: 更改密碼
    response = client.post('/api/auth/change-password', 
        json={
            'old_password': old_password,
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    assert response.status_code == 200, "更改密碼應該成功"
    data = response.get_json()
    assert 'message' in data
    assert '成功' in data['message']
    
    # 步驟 3: 驗證舊密碼不能登入
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': old_password
    })
    
    assert response.status_code == 401, "舊密碼應該無法登入"
    
    # 步驟 4: 驗證新密碼可以登入
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': new_password
    })
    
    assert response.status_code == 200, "新密碼應該可以登入"
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
