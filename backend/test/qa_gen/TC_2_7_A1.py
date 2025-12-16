"""
TC 2.7.A1: 創建者成功編輯活動所有欄位
測試創建者可以成功編輯活動的所有欄位（標題、類型、地點、日期、時間、人數、描述）
Given: 用戶已登入且為活動創建者
When: 提交編輯活動請求，修改所有欄位
Then: 回應 200，活動資料已更新
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
    """創建測試用戶"""
    with test_app.app_context():
        user = User(
            name='Test Creator',
            email='creator@test.com',
            gender='male',
            age=25
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.user_id


@pytest.fixture
def auth_headers(client, auth_user):
    """取得認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}', 'user_id': auth_user}


def test_creator_update_activity_success(client, auth_headers, test_app):
    """測試創建者成功編輯活動所有欄位"""
    
    with test_app.app_context():
        # Arrange: 創建測試活動
        activity = Activity(
            creator_id=auth_headers['user_id'],
            title='原標題',
            category='hiking',
            location='原地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_participants=10,
            description='原描述'
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # Act: 更新活動所有欄位
    update_data = {
        'title': '新標題 - 更新後',
        'type': 'camping',
        'location': '新地點 - 陽明山',
        'start_date': (date.today() + timedelta(days=14)).isoformat(),
        'end_date': (date.today() + timedelta(days=16)).isoformat(),
        'start_time': '10:00',
        'end_time': '18:00',
        'max_members': 20,
        'description': '新描述 - 這是一個很棒的露營活動'
    }
    
    response = client.put(
        f'/api/activities/{activity_id}',
        json=update_data,
        headers={'Authorization': auth_headers['Authorization']}
    )
    
    # Assert: 驗證回應
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '活動更新成功'
    assert data['activity']['title'] == '新標題 - 更新後'
    assert data['activity']['category'] == 'camping'
    assert data['activity']['location'] == '新地點 - 陽明山'
    assert data['activity']['max_participants'] == 20
    assert data['activity']['description'] == '新描述 - 這是一個很棒的露營活動'
    
    # 驗證資料庫已更新
    with test_app.app_context():
        updated_activity = Activity.query.get(activity_id)
        assert updated_activity.title == '新標題 - 更新後'
        assert updated_activity.category == 'camping'
        assert updated_activity.date == date.today() + timedelta(days=14)
        assert updated_activity.start_date == date.today() + timedelta(days=14)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
