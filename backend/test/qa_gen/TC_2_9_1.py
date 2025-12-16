"""
TC 2.9.1: 創建者成功標記已結束活動為完成
測試說明: 測試活動創建者可以將已結束的活動標記為 completed
Given: 用戶已登入且為活動創建者，活動 end_date 已過
When: 提交 PUT /api/activities/<id> 請求，設定 status='completed'
Then: 回應 200，活動狀態更新為 completed
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
def ended_activity(test_app, creator_user):
    """創建已結束的測試活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='測試活動-已結束',
            category='hiking',
            location='陽明山',
            date=date.today() - timedelta(days=2),
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            max_participants=10,
            description='這是一個已結束的測試活動',
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_creator_mark_ended_activity_as_completed(client, creator_headers, ended_activity, test_app):
    """測試創建者成功標記已結束活動為完成"""
    
    # Act: 創建者標記活動為完成
    response = client.put(
        f'/api/activities/{ended_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Assert: 回應成功
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
    data = response.json
    assert 'activity' in data or 'message' in data, "Response should contain activity or message"
    
    # 驗證資料庫中的活動狀態已更新
    with test_app.app_context():
        activity = Activity.query.get(ended_activity)
        assert activity is not None, "Activity should exist in database"
        assert activity.status == 'completed', f"Activity status should be 'completed', got '{activity.status}'"


def test_completed_status_persists(client, creator_headers, ended_activity, test_app):
    """測試完成狀態持久化保存"""
    
    # Act: 標記為完成
    client.put(
        f'/api/activities/{ended_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Act: 重新查詢活動
    response = client.get(
        f'/api/activities/{ended_activity}',
        headers=creator_headers
    )
    
    # Assert: 狀態保持為 completed
    assert response.status_code == 200
    data = response.json
    activity_data = data.get('activity', data)
    assert activity_data.get('status') == 'completed', \
        f"Activity status should remain 'completed', got '{activity_data.get('status')}'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
