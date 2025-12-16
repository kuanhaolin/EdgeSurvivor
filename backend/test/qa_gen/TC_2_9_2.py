"""
TC 2.9.2: 非創建者無法標記活動為完成
測試說明: 測試非創建者無法標記活動為 completed
Given: 用戶已登入但不是活動創建者
When: 提交 PUT /api/activities/<id> 請求，設定 status='completed'
Then: 回應 403 錯誤，錯誤訊息「無權限修改此活動」
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
def other_user(test_app):
    with test_app.app_context():
        user = User(
            name='其他用戶',
            email='other@test.com',
            gender='female',
            age=25
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.user_id


@pytest.fixture
def other_headers(client, other_user):
    response = client.post('/api/auth/login', json={
        'email': 'other@test.com',
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


def test_non_creator_cannot_mark_completed(client, other_headers, ended_activity, test_app):
    """測試非創建者無法標記活動為完成"""
    
    # Act
    response = client.put(
        f'/api/activities/{ended_activity}',
        headers=other_headers,
        json={'status': 'completed'}
    )
    
    # Assert
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    data = response.json
    assert 'error' in data, "Response should contain error message"
    assert '無權限' in data['error'], f"Error message should mention permission, got: {data['error']}"
    
    # 驗證活動狀態未改變
    with test_app.app_context():
        activity = Activity.query.get(ended_activity)
        assert activity.status == 'active', "Activity status should remain unchanged"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
