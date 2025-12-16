"""
TC 2.7.A6: 不存在的活動返回 404
測試嘗試編輯不存在的活動時返回 404
Given: 用戶已登入
When: 嘗試編輯不存在的活動
Then: 回應 404 Not Found，顯示活動不存在錯誤
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


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
def auth_headers(client, test_app):
    """創建用戶並取得認證 token"""
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
    
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_update_nonexistent_activity(client, auth_headers):
    """測試編輯不存在的活動返回 404"""
    
    # Act: 嘗試編輯一個不存在的活動 ID（例如 99999）
    nonexistent_id = 99999
    update_data = {
        'title': '新標題',
        'type': 'hiking',
        'location': '新地點'
    }
    
    response = client.put(
        f'/api/activities/{nonexistent_id}',
        json=update_data,
        headers=auth_headers
    )
    
    # Assert: 驗證回應 404
    assert response.status_code == 404
    data = response.get_json()
    assert '找不到' in data['error'] or '不存在' in data['error'] or 'not found' in data['error'].lower()


def test_update_with_invalid_activity_id(client, auth_headers):
    """測試使用無效的活動 ID 格式"""
    
    # Act: 使用 0 作為 ID
    response = client.put(
        '/api/activities/0',
        json={'title': '新標題'},
        headers=auth_headers
    )
    
    # Assert: 應該返回 404
    assert response.status_code == 404


def test_update_deleted_activity(client, auth_headers, test_app):
    """測試編輯已刪除的活動（如果資料庫中不存在）"""
    from models.activity import Activity
    from datetime import date, timedelta
    
    with test_app.app_context():
        # 先創建活動
        response = client.post('/api/auth/login', json={
            'email': 'test@test.com',
            'password': 'password123'
        })
        user_id = response.json.get('user_id', 1)
        
        activity = Activity(
            creator_id=user_id,
            title='將被刪除的活動',
            category='hiking',
            location='測試地點',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            max_participants=10
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
        
        # 刪除活動
        db.session.delete(activity)
        db.session.commit()
    
    # Act: 嘗試編輯已刪除的活動
    response = client.put(
        f'/api/activities/{activity_id}',
        json={'title': '嘗試更新'},
        headers=auth_headers
    )
    
    # Assert: 應該返回 404
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
