"""
TC 1.5.8 - 驗證舊密碼欄位（登入後更改密碼）
測試說明: 測試登入後更改密碼時舊密碼欄位的驗證
測試資料: None:false, "":false, "wrongpass":false, "correctpass":true
"""

import pytest
from models.user import User
from models import db

# 測試資料
TEST_DATA = [
    {'old_password': '', 'expected': False, 'description': '空字串'},
    {'old_password': 'fakepassword', 'expected': False, 'description': '錯誤舊密碼'},
    {'old_password': 'oldpassword', 'expected': True, 'description': '正確舊密碼'}
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_change_password_old_password_validation(client, test_app, test_case):
    """測試登入後更改密碼的舊密碼欄位驗證"""
    
    test_email = 'test@test.com'
    correct_old_password = 'oldpassword'
    new_password = 'newpassword'
    old_password = test_case['old_password']
    expected = test_case['expected']
    description = test_case['description']
    
    # 建立用戶並登入
    with test_app.app_context():
        user = User(
            name='user',
            email=test_email,
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password(correct_old_password)
        db.session.add(user)
        db.session.commit()
    
    # 登入取得 JWT token
    response = client.post('/api/auth/login', json={
        'email': test_email,
        'password': correct_old_password
    })
    
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    
    # 測試更改密碼
    response = client.post('/api/auth/change-password', 
        json={
            'old_password': old_password,
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if expected:
        # 正確的舊密碼 - 應該成功
        assert response.status_code == 200, f"{description} 應該返回 200"
        data = response.get_json()
        assert 'message' in data
        assert '成功' in data['message']
    else:
        # 無效的舊密碼 - 應該返回錯誤
        assert response.status_code == 400, f"{description} 應該返回 400"
        data = response.get_json()
        assert 'error' in data
