"""
TC 2.7.A2: 非創建者無法編輯活動（403）
測試非創建者嘗試編輯活動時被拒絕
Given: 用戶已登入但不是活動創建者
When: 嘗試編輯他人創建的活動
Then: 回應 403 Forbidden，顯示無權限錯誤
"""

import pytest
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity


@pytest.fixture
def test_app():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def setup_users(test_app):
    """創建兩個測試用戶"""
    with test_app.app_context():
        # 創建者
        creator = User(
            name='Creator',
            email='creator@test.com',
            gender='male',
            age=30
        )
        creator.set_password('password123')
        db.session.add(creator)
        
        # 其他用戶
        other_user = User(
            name='Other User',
            email='other@test.com',
            gender='female',
            age=25
        )
        other_user.set_password('password123')
        db.session.add(other_user)
        
        db.session.commit()
        return {'creator_id': creator.user_id, 'other_id': other_user.user_id}


@pytest.fixture
def other_user_headers(client):
    """取得非創建者的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'other@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_non_creator_cannot_update_activity(client, setup_users, other_user_headers, test_app):
    """測試非創建者無法編輯活動（403）"""
    
    with test_app.app_context():
        # Arrange: 由創建者創建活動
        activity = Activity(
            creator_id=setup_users['creator_id'],
            title='創建者的活動',
            category='hiking',
            location='陽明山',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            max_participants=15
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 其他用戶嘗試更新活動
    update_data = {
        'title': '被修改的標題',
        'location': '被修改的地點'
    }
    
    response = client.put(
        f'/api/activities/{activity_id}',
        json=update_data,
        headers=other_user_headers
    )
    
    # Assert: 驗證回應 403
    assert response.status_code == 403
    data = response.get_json()
    assert '無權限' in data['error'] or '權限' in data['error']
    
    # 驗證資料庫未被修改
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        assert activity.title == '創建者的活動'
        assert activity.location == '陽明山'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
