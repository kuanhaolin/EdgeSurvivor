"""
TC 2.7.A5: 已開始活動無法修改日期和地點（返回 400）
測試已開始的活動不能修改關鍵資訊（日期、地點）
Given: 用戶已登入且為活動創建者，活動已開始（start_date < today）
When: 嘗試修改活動的日期或地點
Then: 回應 400 Bad Request，顯示已開始活動限制錯誤
注意: 此功能目前未實作，測試將會失敗直到實作 AC 5
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
def auth_user(test_app):
    with test_app.app_context():
        user = User(
            name='Test User',
            email='test@test.com',
            gender='male',
            age=25
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.user_id


@pytest.fixture
def auth_headers(client, auth_user):
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}', 'user_id': auth_user}


@pytest.mark.skip(reason="AC 5 功能尚未實作 - 已開始活動限制")
def test_cannot_modify_started_activity_location(client, auth_headers, test_app):
    """測試無法修改已開始活動的地點"""
    
    with test_app.app_context():
        # Arrange: 創建已開始的活動（昨天開始）
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='已開始的活動',
            category='hiking',
            location='原地點',
            date=date.today() - timedelta(days=1),
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 嘗試修改地點
    response = client.put(
        f'/api/activities/{activity_id}',
        json={'location': '新地點'},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該返回 400
    assert response.status_code == 400
    data = response.get_json()
    assert '已開始' in data['error'] or '不能修改' in data['error']


@pytest.mark.skip(reason="AC 5 功能尚未實作 - 已開始活動限制")
def test_cannot_modify_started_activity_dates(client, auth_headers, test_app):
    """測試無法修改已開始活動的日期"""
    
    with test_app.app_context():
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='已開始的活動',
            category='camping',
            location='測試地點',
            date=date.today() - timedelta(days=2),
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=1),
            max_participants=15
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 嘗試修改開始日期
    response = client.put(
        f'/api/activities/{activity_id}',
        json={'start_date': (date.today() + timedelta(days=5)).isoformat()},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該返回 400
    assert response.status_code == 400
    data = response.get_json()
    assert '已開始' in data['error'] or '日期' in data['error']


@pytest.mark.skip(reason="AC 5 功能尚未實作 - 已開始活動限制")
def test_can_modify_started_activity_other_fields(client, auth_headers, test_app):
    """測試可以修改已開始活動的其他欄位（標題、描述）"""
    
    with test_app.app_context():
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='已開始的活動',
            category='hiking',
            location='測試地點',
            date=date.today() - timedelta(days=1),
            start_date=date.today() - timedelta(days=1),
            max_participants=10,
            description='原描述'
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 修改標題和描述（非關鍵資訊）
    response = client.put(
        f'/api/activities/{activity_id}',
        json={
            'title': '更新的標題',
            'description': '更新的描述'
        },
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該成功
    assert response.status_code == 200
    data = response.get_json()
    assert data['activity']['title'] == '更新的標題'


def test_can_modify_future_activity_freely(client, auth_headers, test_app):
    """測試未開始的活動可以自由修改所有欄位"""
    
    with test_app.app_context():
        # Arrange: 創建未來的活動
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='未來的活動',
            category='hiking',
            location='原地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 修改日期和地點
    response = client.put(
        f'/api/activities/{activity_id}',
        json={
            'location': '新地點',
            'start_date': (date.today() + timedelta(days=14)).isoformat(),
            'end_date': (date.today() + timedelta(days=15)).isoformat()
        },
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該成功
    assert response.status_code == 200
    data = response.get_json()
    assert data['activity']['location'] == '新地點'


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-k', 'not skip'])
