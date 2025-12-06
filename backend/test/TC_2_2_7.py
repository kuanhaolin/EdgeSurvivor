"""
TC 2.2.7: 刪除活動
測試說明: 測試活動創建者能刪除活動
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity


@pytest.fixture
def client():
    """建立測試客戶端"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            creator = User(
                name='creator',
                email='creator@test.com',
                gender='male',
                age=25
            )
            creator.set_password('password123')
            
            other_user = User(
                name='other',
                email='other@test.com',
                gender='female',
                age=22
            )
            other_user.set_password('password123')
            
            db.session.add_all([creator, other_user])
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def creator_headers(client):
    """取得創建者的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def other_headers(client):
    """取得其他用戶的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'other@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_delete_activity(client, creator_headers, other_headers):
    """測試刪除活動功能"""
    
    # 1. 創建活動
    activity_data = {
        "title": "測試活動",
        "type": "登山",
        "location": "陽明山",
        "start_date": "2025-12-10",
        "max_members": 5
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    # 2. 測試非創建者無法刪除
    response = client.delete(f'/api/activities/{activity_id}',
        headers=other_headers
    )
    
    assert response.status_code == 403, "非創建者應該無法刪除活動"
    
    # 3. 驗證活動仍然存在
    with client.application.app_context():
        activity = Activity.query.get(activity_id)
        assert activity is not None, "活動應該仍然存在"
    
    # 4. 測試創建者可以刪除
    response = client.delete(f'/api/activities/{activity_id}',
        headers=creator_headers
    )
    
    assert response.status_code == 200, "創建者應該可以刪除活動"
    
    # 5. 驗證活動已被刪除
    with client.application.app_context():
        activity = Activity.query.get(activity_id)
        assert activity is None, "活動應該已被刪除"
    
    # 6. 測試刪除不存在的活動
    response = client.delete(f'/api/activities/99999',
        headers=creator_headers
    )
    
    assert response.status_code == 404, "刪除不存在的活動應該返回 404"
