"""
TC 1.8.10 - 無效 Token 無法更新資料
測試說明: 測試使用無效 token 無法透過 API 進行更新
測試資料: invalid_token
"""

import pytest
from models.user import User
from models import db

@pytest.fixture
def test_user(test_app):
    with test_app.app_context():
        user = User(
            name='user',
            email='user@user.com',
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        yield user

def test_update_with_invalid_token(client, test_app, test_user):
    """測試使用無效 token 無法更新資料"""
    # 使用無效的 token
    response = client.put('/api/users/profile', json={
        'name': 'user01'
    }, headers={'Authorization': 'Bearer invalid_token_here'})
    
    # 應該返回 401 或 422
    assert response.status_code in [401, 422]
    
    # 驗證資料庫中的資料沒有被修改
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.name == 'user'  # 名稱應該沒有改變
