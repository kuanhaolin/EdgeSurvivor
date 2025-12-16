"""
TC 1.8.9 - 未登入無法更新資料
測試說明: 測試更新條件，未登入無法透過api進行更新，使用未登入帳號更新姓名
測試資料: user
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

def test_update_without_login(client, test_app, test_user):
    """測試未登入無法更新資料"""
    # 不登入，直接嘗試更新資料
    response = client.put('/api/users/profile', json={
        'name': 'user01'
    })
    
    # 應該返回 401 未授權
    assert response.status_code == 401
    
    # 驗證資料庫中的資料沒有被修改
    with test_app.app_context():
        user = User.query.filter_by(email='user@user.com').first()
        assert user.name == 'user'  # 名稱應該沒有改變