"""
TC 1.5.2 - 發送重設密碼 Email
測試說明: 測試發送重設密碼驗證碼功能
測試資料: 已註冊用戶 test@test.com
"""

import pytest
from models.user import User
from models import db

test_email = 'user@user.com'

def test_send_reset_password_code(client, test_app):
    """測試發送重設密碼驗證碼"""
    
    # 先註冊一個用戶
    with test_app.app_context():
        user = User(
            name='user',
            email=test_email,
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
    
    # 發送重設密碼驗證碼
    response = client.post('/api/auth/forgot-password', json={
        'email': test_email
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert '驗證碼' in data['message']
    
    # 在開發環境下，應該返回驗證碼（用於測試）
    # 如果有返回 code，驗證格式
    if 'code' in data:
        assert len(data['code']) == 6
        assert data['code'].isdigit()
