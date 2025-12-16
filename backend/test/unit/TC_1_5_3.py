"""
TC 1.5.3 - 驗證驗證碼欄位
測試說明: 測試重設密碼時驗證碼欄位的必填驗證
注意: 後端目前只驗證必填，不驗證格式（長度、數字）
"""

import pytest

# 測試資料：expected=True 表示通過必填驗證，False 表示未通過
TEST_DATA = [
    {'code': '', 'expected': False, 'description': '空字串'},
    {'code': '123456', 'expected': True, 'description': '有值'}
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_reset_password_code_field_validation(client, test_case):
    """測試重設密碼的驗證碼欄位格式驗證"""
    
    test_email = 'test@test.com'
    code = test_case['code']
    expected_valid = test_case['expected']
    description = test_case['description']
    
    # 直接呼叫 reset-password API，測試驗證碼欄位驗證
    response = client.post('/api/auth/reset-password', json={
        'email': test_email,
        'code': code,
        'new_password': 'newpass123'
    })
    
    data = response.get_json()
    error_msg = data.get('error', '')
    
    # 判斷格式是否有效（根據錯誤訊息）
    # 格式無效 → 錯誤訊息包含「必填」
    # 格式有效 → 錯誤訊息是「無效」或「過期」(表示通過格式驗證，但驗證碼不存在)
    is_format_valid = '必填' not in error_msg
    
    # 比較預期與實際
    assert is_format_valid == expected_valid, (
        f"{description} 失敗:\n"
        f"  預期格式有效: {expected_valid}\n"
        f"  實際格式有效: {is_format_valid}\n"
        f"  錯誤訊息: {error_msg}"
    )


