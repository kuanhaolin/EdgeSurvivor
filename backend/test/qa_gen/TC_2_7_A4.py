"""
TC 2.7.A4: 日期範圍驗證（start_date > end_date 返回 400）
測試編輯活動時開始日期不能晚於結束日期
Given: 用戶已登入且為活動創建者
When: 提交編輯請求但開始日期晚於結束日期
Then: 回應 400 Bad Request，顯示日期範圍錯誤
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


def test_start_date_after_end_date(client, auth_headers, test_app):
    """測試開始日期晚於結束日期時返回 400"""
    
    with test_app.app_context():
        # Arrange: 創建測試活動
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='測試活動',
            category='hiking',
            location='測試地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=10),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 嘗試將開始日期設為晚於結束日期
    update_data = {
        'start_date': (date.today() + timedelta(days=20)).isoformat(),
        'end_date': (date.today() + timedelta(days=15)).isoformat()
    }
    
    response = client.put(
        f'/api/activities/{activity_id}',
        json=update_data,
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 驗證回應 400
    assert response.status_code == 400
    data = response.get_json()
    assert 'date' in data['error'].lower() or '日期' in data['error']


def test_valid_date_range(client, auth_headers, test_app):
    """測試有效的日期範圍（開始日期等於結束日期）"""
    
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
        activity_id = activity.activity_id
    
    # Act: 設定開始日期等於結束日期（單日活動）
    same_date = (date.today() + timedelta(days=14)).isoformat()
    update_data = {
        'start_date': same_date,
        'end_date': same_date
    }
    
    response = client.put(
        f'/api/activities/{activity_id}',
        json=update_data,
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該成功（開始日期等於結束日期是允許的）
    assert response.status_code == 200


def test_valid_multi_day_activity(client, auth_headers, test_app):
    """測試有效的多日活動（開始日期早於結束日期）"""
    
    with test_app.app_context():
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='測試活動',
            category='camping',
            location='測試地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 設定三天的活動
    update_data = {
        'start_date': (date.today() + timedelta(days=20)).isoformat(),
        'end_date': (date.today() + timedelta(days=22)).isoformat()
    }
    
    response = client.put(
        f'/api/activities/{activity_id}',
        json=update_data,
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 應該成功
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '活動更新成功'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
