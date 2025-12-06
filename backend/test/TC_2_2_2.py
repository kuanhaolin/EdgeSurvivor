"""
TC 2.2.2: 創建者更新活動資訊
測試說明: 測試活動創建者能更新活動資訊
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


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
                name='user',
                email='user@user.com',
                gender='male',
                age=25
            )
            creator.set_password('password')
            db.session.add(creator)
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def creator_headers(client):
    """取得創建者的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': 'password'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_update_activity_info(client, creator_headers):
    """測試更新活動的所有欄位"""
    
    # 1. 創建活動
    activity_data = {
        "title": "原始活動",
        "type": "登山",
        "location": "陽明山",
        "start_date": "2025-12-10",
        "end_date": "2025-12-10",
        "start_time": "09:00",
        "end_time": "17:00",
        "max_members": 5,
        "description": "原始描述",
        "status": "open"
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    # 2. 更新所有欄位
    update_data = {
        "title": "更新的活動名稱",
        "type": "露營",
        "location": "武陵農場",
        "start_date": "2025-12-15",
        "end_date": "2025-12-16",
        "start_time": "10:00",
        "end_time": "18:00",
        "max_members": 8,
        "description": "更新後的描述內容",
        "status": "confirmed"
    }
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json=update_data
    )
    
    expected_status = 200
    actual_status = response.status_code
    assert actual_status == expected_status
    
    # 3. 驗證所有欄位都已更新
    updated = response.json['activity']
    
    assert updated['title'] == update_data['title']
    assert updated['category'] == update_data['type']
    assert updated['location'] == update_data['location']
    assert updated['start_date'] == update_data['start_date']
    assert updated['end_date'] == update_data['end_date']
    assert updated['max_participants'] == update_data['max_members']
    assert updated['description'] == update_data['description']
    assert updated['status'] == update_data['status']