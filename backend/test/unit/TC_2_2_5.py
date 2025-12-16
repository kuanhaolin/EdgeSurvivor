"""
TC 2.2.5: 更新活動資其他必填欄位保持有效
測試說明: 測試更新時必填欄位保持有效
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


def test_update_maintains_required_fields(client, creator_headers):
    """測試更新時必填欄位保持有效"""
    
    # 1. 創建活動
    activity_data = {
        "title": "原始標題",
        "type": "登山",
        "location": "原始地點",
        "start_date": "2025-12-10",
        "max_members": 5
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    # 2. 更新活動（修改標題和地點）
    update_data = {
        "title": "新標題",
        "location": "新地點"
    }
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json=update_data
    )
    assert response.status_code == 200
    
    updated = response.json['activity']
    
    # 3. 驗證所有必填欄位都存在且有效
    assert updated['title'] is not None
    assert updated['title'] != ""
    
    assert updated['category'] is not None
    assert updated['category'] != ""
    
    assert updated['location'] is not None
    assert updated['location'] != ""
    
    assert updated['start_date'] is not None
    
    assert updated['max_participants'] is not None

