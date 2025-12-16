"""
TC 2.7.A3: 必填欄位驗證（title, type, location 為空返回 400）
測試編輯活動時必填欄位不能為空
Given: 用戶已登入且為活動創建者
When: 提交編輯請求但必填欄位為空
Then: 回應 400 Bad Request，顯示欄位驗證錯誤
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


@pytest.fixture
def test_activity(test_app, auth_headers):
    """創建測試活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='測試活動',
            category='hiking',
            location='測試地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_empty_title_validation(client, auth_headers, test_activity):
    """測試標題為空時返回 400"""
    response = client.put(
        f'/api/activities/{test_activity}',
        json={'title': ''},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert '標題' in data['error']


def test_empty_type_validation(client, auth_headers, test_activity):
    """測試類型為空時返回 400"""
    response = client.put(
        f'/api/activities/{test_activity}',
        json={'type': ''},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert '類型' in data['error']


def test_empty_location_validation(client, auth_headers, test_activity):
    """測試地點為空時返回 400"""
    response = client.put(
        f'/api/activities/{test_activity}',
        json={'location': ''},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert '地點' in data['error']


def test_whitespace_only_title(client, auth_headers, test_activity):
    """測試標題只有空白字元時返回 400"""
    response = client.put(
        f'/api/activities/{test_activity}',
        json={'title': '   '},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert '標題' in data['error']


def test_invalid_max_members(client, auth_headers, test_activity):
    """測試最大人數小於等於 0 時返回 400"""
    response = client.put(
        f'/api/activities/{test_activity}',
        json={'max_members': 0},
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert '最大人數' in data['error'] or '人數' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
