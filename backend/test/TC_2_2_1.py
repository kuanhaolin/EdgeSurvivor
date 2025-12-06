"""
TC 2.2.1: 創建者可以編輯活動
測試說明: 測試活動創建者能編輯活動
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
            
            # 創建測試用戶（創建者）
            creator = User(
                name='user',
                email='user@user.com',
                gender='male',
                age=25
            )
            creator.set_password('password')
            db.session.add(creator)
            
            # 創建另一個用戶（非創建者）
            other_user = User(
                name='other',
                email='other@other.com',
                gender='female',
                age=23
            )
            other_user.set_password('password')
            db.session.add(other_user)
            
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


@pytest.fixture
def other_headers(client):
    """取得其他用戶的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'other@other.com',
        'password': 'password'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_creator_can_edit_activity(client, creator_headers):
    """測試創建者可以編輯活動"""
    
    # 1. 創建活動
    activity_data = {
        "title": "原始標題",
        "type": "其他",
        "location": "中央大學",
        "start_date": "2025-12-10",
        "max_members": 5,
        "description": "原始描述"
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    print(f"\n[建立活動] 預期: 201, 實際: {response.status_code}")
    assert response.status_code == 201
    activity_id = response.json['activity']['activity_id']
    
    # 2. 創建者編輯活動
    update_data = {
        "title": "更新後標題",
        "description": "更新後描述"
    }
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=creator_headers,
        json=update_data
    )
    
    expected_status = 200
    actual_status = response.status_code
    assert actual_status == expected_status
    
    # 3. 驗證更新內容
    updated_activity = response.json['activity']
    assert updated_activity['title'] == "更新後標題"
    assert updated_activity['description'] == "更新後描述"

def test_non_creator_cannot_edit_activity(client, creator_headers, other_headers):
    """測試非創建者不能編輯活動"""
    
    # 1. 創建者建立活動
    activity_data = {
        "title": "測試活動",
        "type": "其他",
        "location": "中央大學",
        "start_date": "2025-12-10",
        "max_members": 5
    }
    
    response = client.post('/api/activities',
        headers=creator_headers,
        json=activity_data
    )
    
    activity_id = response.json['activity']['activity_id']
    
    # 2. 其他用戶嘗試編輯
    update_data = {
        "title": "嘗試更新"
    }
    
    response = client.put(f'/api/activities/{activity_id}',
        headers=other_headers,
        json=update_data
    )
    
    expected_status = 403
    actual_status = response.status_code
    assert actual_status == expected_status
    assert '無權限' in response.json.get('error', '')
