"""
TC 2.9.5: 驗證活動完成後狀態變更
測試說明: 測試活動標記為 completed 後狀態持久化
Given: 活動標記為 completed
When: 查詢活動詳情 GET /api/activities/<id>
Then: 回應中 status='completed'，確認狀態持久化成功
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
def creator_user(test_app):
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
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def ended_activity(test_app, creator_user):
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=date.today() - timedelta(days=2),
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            max_participants=10,
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_completed_status_persists_in_get_request(client, creator_headers, ended_activity, test_app):
    """測試完成狀態在 GET 請求中正確返回"""
    
    # Arrange: 標記為完成
    client.put(
        f'/api/activities/{ended_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Act: 查詢活動詳情
    response = client.get(
        f'/api/activities/{ended_activity}',
        headers=creator_headers
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json
    activity_data = data.get('activity', data)
    assert activity_data.get('status') == 'completed', \
        f"Activity status should be 'completed', got '{activity_data.get('status')}'"


def test_completed_status_in_list_endpoint(client, creator_headers, ended_activity, test_app):
    """測試完成狀態在活動列表中正確顯示"""
    
    # Arrange: 標記為完成
    client.put(
        f'/api/activities/{ended_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Act: 查詢活動列表
    response = client.get(
        '/api/activities?type=created',
        headers=creator_headers
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json
    activities = data.get('activities', [])
    
    # 找到測試活動
    test_activity = next((a for a in activities if a.get('activity_id') == ended_activity), None)
    assert test_activity is not None, "Activity should be in the list"
    assert test_activity.get('status') == 'completed', \
        f"Activity status should be 'completed' in list, got '{test_activity.get('status')}'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
