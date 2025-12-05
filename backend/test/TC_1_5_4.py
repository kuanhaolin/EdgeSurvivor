"""
TC 1.5.4 - 驗證新密碼欄位
測試說明: 測試重設密碼時新密碼欄位的驗證（必填 + 格式）
密碼規則: 必填 + 至少 6 個字元
"""

import pytest
from models.user import User
from models import db
from blueprints.auth import reset_codes
from datetime import datetime, timedelta

# 測試資料：expected=True 表示通過驗證，False 表示未通過
TEST_DATA = [
    {'password': '', 'expected': False, 'description': '空字串'},
    {'password': '123', 'expected': False, 'description': '少於6字元'},
    {'password': '123456', 'expected': True, 'description': '有效密碼'}
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_reset_password_new_password_validation(client, test_app, test_case):
    """測試重設密碼的新密碼欄位驗證（必填 + 格式）"""
    
    test_email = 'test@test.com'
    test_code = '123456'
    new_password = test_case['password']
    expected = test_case['expected']
    description = test_case['description']
    
    # 先註冊一個用戶並添加驗證碼
    with test_app.app_context():
        user = User(
            name='test',
            email=test_email,
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('oldpassword123')
        db.session.add(user)
        db.session.commit()
        
        # 在 reset_codes 中添加驗證碼
        reset_codes[test_email] = {
            'code': test_code,
            'expires_at': datetime.now() + timedelta(minutes=15)
        }
    
    # 測試重設密碼
    response = client.post('/api/auth/reset-password', json={
        'email': test_email,
        'code': test_code,
        'new_password': new_password
    })
    
    if expected:
        # 有效密碼 - 應該成功
        assert response.status_code == 200, f"{description} 應該返回 200"
        data = response.get_json()
        assert 'message' in data
        assert '成功' in data['message']
        
        # 驗證密碼已更新
        with test_app.app_context():
            user = User.query.filter_by(email=test_email).first()
            assert user.check_password(new_password), "密碼應該已更新"
    else:
        # 無效密碼 - 應該返回錯誤
        assert response.status_code == 400, f"{description} 應該返回 400"
        data = response.get_json()
        assert 'error' in data
