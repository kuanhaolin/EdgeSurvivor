"""
TC 2.2.3: 更新活動資訊欄位驗證
測試說明: 測試更新時必填欄位驗證
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


def test_required_fields_validation(client, creator_headers):
    """測試所有必填欄位驗證"""
    
    # 1. 創建活動 - 給所有欄位完整資料
    activity_data = {
        "title": "考試",
        "type": "其他",
        "location": "學校",
        "start_date": "2025-12-10",
        "end_date": "2025-12-10",
        "max_members": 5,
        "description": "考試活動描述"
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"title": ""}
    )
    assert response.status_code == 400, "應該拒絕空標題"
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"type": ""}
    )
    assert response.status_code == 400, "應該拒絕空類型"
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"location": ""}
    )
    assert response.status_code == 400, "應該拒絕空地點"
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"start_date": ""}
    )
    assert response.status_code == 400, "應該拒絕空開始日期"
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={"max_members": 0}
    )
    assert response.status_code == 400, "應該拒絕無效人數"

