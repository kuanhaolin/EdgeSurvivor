"""
TC 2.9.3: 無法標記未結束的活動為完成
測試說明: 測試無法標記未結束的活動為 completed
Given: 用戶為活動創建者，但活動 end_date 尚未到
When: 提交 PUT /api/activities/<id> 請求，設定 status='completed'
Then: 回應 400 錯誤，錯誤訊息「活動尚未結束」
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
def ongoing_activity(test_app, creator_user):
    """創建尚未結束的活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='測試活動-進行中',
            category='hiking',
            location='陽明山',
            date=date.today() + timedelta(days=5),
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=7),
            max_participants=10,
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_cannot_mark_ongoing_activity_as_completed(client, creator_headers, ongoing_activity, test_app):
    """測試無法標記未結束的活動為完成"""
    
    # Act
    response = client.put(
        f'/api/activities/{ongoing_activity}',
        headers=creator_headers,
        json={'status': 'completed'}
    )
    
    # Assert
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json
    assert 'error' in data, "Response should contain error message"
    assert '尚未結束' in data['error'] or '未結束' in data['error'], \
        f"Error should mention activity not ended, got: {data['error']}"
    
    # 驗證活動狀態未改變
    with test_app.app_context():
        activity = Activity.query.get(ongoing_activity)
        assert activity.status == 'active', "Activity status should remain active"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
