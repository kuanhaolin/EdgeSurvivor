"""
TC 1.5.7 - 驗證碼不能重複使用
測試說明: 測試驗證碼使用後不能重複使用
"""

import pytest
from models.user import User
from models import db
from blueprints.auth import reset_codes
from datetime import datetime, timedelta

def test_reset_password_code_cannot_reuse(client, test_app):
    """測試驗證碼使用後不能重複使用"""
    
    test_email = 'user@user.com'
    test_code = '000000'
    new_password = 'newpassword'
    
    # 建立用戶並添加驗證碼
    with test_app.app_context():
        user = User(
            name='reuse',
            email=test_email,
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('oldpassword')
        db.session.add(user)
        db.session.commit()
        
        # 模擬已發送驗證碼
        reset_codes[test_email] = {
            'code': test_code,
            'expires_at': datetime.now() + timedelta(minutes=15)
        }
    
    # 第一次使用驗證碼（應該成功）
    response = client.post('/api/auth/reset-password', json={
        'email': test_email,
        'code': test_code,
        'new_password': new_password
    })
    
    assert response.status_code == 200, "第一次使用驗證碼應該成功"
    
    # 第二次使用相同驗證碼（應該失敗）
    response = client.post('/api/auth/reset-password', json={
        'email': test_email,
        'code': test_code,
        'new_password': 'anotherpassword'
    })
    
    assert response.status_code == 400, "重複使用驗證碼應該失敗"
    data = response.get_json()
    assert 'error' in data
    assert '無效' in data['error'] or '過期' in data['error']
