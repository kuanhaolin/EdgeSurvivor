"""
TC 1.5.1 - 驗證 Email 欄位
測試說明: 測試忘記密碼時的 email 欄位驗證
測試資料: " ":false, "123@":false, "user@user.com":true
"""

import pytest

# 測試資料
TEST_DATA = [
    {'email': ' ', 'expected': False, 'description': '空字串'},
    {'email': '123@', 'expected': False, 'description': '不完整email'},
    {'email': 'user@user.com', 'expected': True, 'description': '有效email'}
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_forgot_password_email_validation(client, test_app, test_case):
    """測試忘記密碼的 email 欄位驗證"""
    
    email = test_case['email']
    expected = test_case['expected']
    description = test_case['description']
    
    response = client.post('/api/auth/forgot-password', json={
        'email': email
    })
    
    if expected:
        # 有效 email - 應該成功（即使用戶不存在也返回 200）
        assert response.status_code == 200, f"{description} 應該返回 200"
        data = response.get_json()
        assert 'message' in data
    else:
        # 無效 email - 應該返回錯誤
        assert response.status_code == 400, f"{description} 應該返回 400"
        data = response.get_json()
        assert 'error' in data
