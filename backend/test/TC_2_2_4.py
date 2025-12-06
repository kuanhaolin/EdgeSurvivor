"""
TC 2.2.4: 更新活動資訊部分其他欄位不變
測試說明: 測試部分欄位更新，其他欄位不變
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
                name='creator',
                email='creator@test.com',
                gender='male',
                age=25
            )
            creator.set_password('password123')
            db.session.add(creator)
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


def test_update_partial_field_keeps_others_unchanged(client, creator_headers):
    """測試只更新標題，其他欄位保持不變"""
    
    # 1. 創建活動
    activity_data = {
        "title": "原始標題",
        "type": "登山",
        "location": "陽明山",
        "start_date": "2025-12-10",
        "max_members": 5,
        "description": "原始描述"
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    # 2. 只更新標題
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"title": "更新後的標題"}
    )
    
    assert response.status_code == 200
    updated = response.json['activity']
    
    # 3. 驗證標題已更新，其他欄位不變
    assert updated['title'] == "更新後的標題"
    assert updated['category'] == "登山"
    assert updated['location'] == "陽明山"
    assert updated['description'] == "原始描述"
    assert updated['max_participants'] == 5
