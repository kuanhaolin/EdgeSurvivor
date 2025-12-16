"""
TC 1.5.6 - 使用驗證碼重設密碼
測試說明: 測試使用驗證碼重設密碼功能
"""

import pytest
from models.user import User
from models import db
from blueprints.auth import reset_codes
from datetime import datetime, timedelta

def test_reset_password_with_valid_code(client, test_app):
    """測試使用有效驗證碼重設密碼"""
    
    test_email = 'user@user.com'
    test_code = '123456'
    old_password = 'oldpassword'
    new_password = 'newpassword'
    
    # 建立用戶並添加驗證碼
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
        
        # 模擬已發送驗證碼
        reset_codes[test_email] = {
            'code': test_code,
            'expires_at': datetime.now() + timedelta(minutes=15)
        }
    
    # 使用驗證碼重設密碼
    response = client.post('/api/auth/reset-password', json={
        'email': test_email,
        'code': test_code,
        'new_password': new_password
    })
    
    assert response.status_code == 200, "重設密碼應該成功"
    data = response.get_json()
    assert 'message' in data
    assert '成功' in data['message']
    
    # 驗證驗證碼已被刪除
    with test_app.app_context():
        assert test_email not in reset_codes, "已使用的驗證碼應該被刪除"
    
    # 驗證新密碼可以登入
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': new_password
    })
    
    assert response.status_code == 200, "新密碼應該可以登入"
    data = response.get_json()
    assert 'access_token' in data
