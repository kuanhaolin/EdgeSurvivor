"""
TC 1.4.2 - 新使用者自動建立帳號
測試說明: 測試帳號是否已建立，已建立不重複建立，未建立則自動建立
測試資料: user01@user01.com:true, user02@user02.com:false
"""

import pytest
from unittest.mock import patch, MagicMock
from models.user import User

# 測試資料
TEST_DATA = [
    {
        'email': 'user01@user01.com',
        'name': 'User01',
        'picture': 'https://example.com/user01.jpg',
        'should_exist': True,  # user01@user01.com 已存在
        'description': '測試已存在的使用者不重複建立'
    },
    {
        'email': 'user02@user02.com',
        'name': 'User02',
        'picture': 'https://example.com/user02.jpg',
        'should_exist': False,  # user02@user02.com 不存在
        'description': '測試新使用者自動建立帳號'
    }
]

@pytest.mark.parametrize('test_case', TEST_DATA)
def test_google_login_user_creation(client, test_app, test_case):
    """測試 Google 登入時的使用者建立邏輯"""
    
    email = test_case['email']
    name = test_case['name']
    picture = test_case['picture']
    should_exist = test_case['should_exist']
    
    # 建立預設測試帳號 user01@user01.com
    with test_app.app_context():
        from models import db
        default_user = User(
            name='User01',
            email='user01@user01.com',
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        db.session.add(default_user)
        db.session.commit()
    
    # 驗證測試前提：檢查帳號是否符合預期狀態
    with test_app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if should_exist:
            assert existing_user is not None, f"測試前提錯誤：{email} 應該已存在但不存在"
            original_user_id = existing_user.user_id
        else:
            assert existing_user is None, f"測試前提錯誤：{email} 應該不存在但已存在"
            original_user_id = None
    
    # Mock Google API
    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {
        'id_token': 'test_id_token'
    }
    
    mock_info_response = MagicMock()
    mock_info_response.status_code = 200
    mock_info_response.json.return_value = {
        'email': email,
        'name': name,
        'picture': picture
    }
    
    with patch('requests.post', return_value=mock_token_response), \
         patch('requests.get', return_value=mock_info_response):
        
        response = client.post('/api/auth/google-code', json={
            'code': 'test_code'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        
        with test_app.app_context():
            from models import db
            user = User.query.filter_by(email=email).first()
            assert user is not None
            assert user.email == email
            assert user.is_verified is True
            assert user.is_active is True
            
            if should_exist:
                # 已存在的使用者：不應重複建立
                user_count = User.query.filter_by(email=email).count()
                assert user_count == 1
                assert user.user_id == original_user_id
                assert data['user']['user_id'] == original_user_id
            else:
                # 新使用者：應成功建立且資料正確
                assert user.name == name
                assert user.profile_picture == picture
                assert data['user']['user_id'] == user.user_id
