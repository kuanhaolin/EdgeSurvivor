"""
TC 2.9.4: 已完成活動可重複標記為完成（冪等性）
測試說明: 測試已完成的活動可以重複標記為 completed
Given: 活動已標記為 completed
When: 再次提交 PUT /api/activities/<id> 請求，設定 status='completed'
Then: 回應 200，操作成功且狀態保持為 completed
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
def completed_activity(test_app, creator_user):
    """創建已完成的活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='測試活動-已完成',
            category='hiking',
            location='陽明山',
            date=date.today() - timedelta(days=2),
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            max_participants=10,
            status='completed'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_idempotent_mark_completed(client, creator_headers, completed_activity, test_app):
    """測試重複標記為完成是冪等的"""
    
    # Act: 再次標記為完成
    response = client.put(
        f'/api/activities/{completed_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Assert: 操作成功
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # 驗證狀態保持為 completed
    with test_app.app_context():
        activity = Activity.query.get(completed_activity)
        assert activity.status == 'completed', "Activity should remain completed"


def test_multiple_mark_completed_operations(client, creator_headers, completed_activity, test_app):
    """測試多次標記為完成操作"""
    
    # 執行 3 次標記操作
    for i in range(3):
        response = client.put(
            f'/api/activities/{completed_activity}',
            headers=creator_headers,
            json={'status': 'completed'}
        )
        assert response.status_code == 200, f"Operation {i+1} should succeed"
    
    # 驗證狀態依然為 completed
    with test_app.app_context():
        activity = Activity.query.get(completed_activity)
        assert activity.status == 'completed', "Status should still be completed after multiple operations"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
