"""
TC 2.8.1: 創建者成功取消活動
測試說明: 測試活動創建者可以將活動狀態設定為 cancelled
Given: 用戶已登入且為活動創建者
When: 提交 PUT /api/activities/<id> 請求，設定 status='cancelled'
Then: 回應 200，活動狀態更新為 cancelled
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
    """建立測試應用程式"""
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
    """建立測試客戶端"""
    return test_app.test_client()


@pytest.fixture
def creator_user(test_app):
    """創建測試用戶（創建者）"""
    with test_app.app_context():
        user = User(
            name='活動創建者',
            email='creator@test.com',
            gender='male',
            age=30
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.user_id


@pytest.fixture
def creator_headers(client, creator_user):
    """取得創建者認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}', 'user_id': creator_user}


@pytest.fixture
def test_activity(test_app, creator_user):
    """創建測試活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='測試活動-取消測試',
            category='hiking',
            location='陽明山',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_participants=10,
            description='這是一個測試用的活動',
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_creator_cancel_activity_success(client, creator_headers, test_activity, test_app):
    """測試創建者成功取消活動"""
    
    # Act: 創建者取消活動
    response = client.put(
        f'/api/activities/{test_activity}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 回應成功
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.json
    assert 'activity' in data or 'message' in data, "Response should contain activity or message"
    
    # 驗證資料庫中的活動狀態已更新
    with test_app.app_context():
        activity = Activity.query.get(test_activity)
        assert activity is not None, "Activity should exist in database"
        assert activity.status == 'cancelled', f"Activity status should be 'cancelled', got '{activity.status}'"


def test_activity_status_persists(client, creator_headers, test_activity, test_app):
    """測試取消狀態持久化保存"""
    
    # Act: 取消活動
    client.put(
        f'/api/activities/{test_activity}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Act: 重新查詢活動
    response = client.get(
        f'/api/activities/{test_activity}',
        headers=creator_headers
    )
    
    # Assert: 狀態保持為 cancelled
    assert response.status_code == 200
    data = response.json
    assert data.get('status') == 'cancelled' or data.get('activity', {}).get('status') == 'cancelled', \
        "Activity status should remain 'cancelled' after retrieval"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
