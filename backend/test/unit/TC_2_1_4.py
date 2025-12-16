"""
TC 2.1.4: 建立者自動成為參與者
測試說明: 測試建立活動後創建者自動新增為參與者
測試資料: user
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant


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
            
            # 創建測試用戶
            user = User(
                name='user',
                email='user@user.com',
                gender='male',
                age=25
            )
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def auth_headers(client):
    """取得認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': 'password'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_creator_auto_added_as_participant(client, auth_headers):
    """測試建立活動後創建者自動成為參與者"""
    
    # 準備活動資料
    activity_data = {
        "title": "測試活動",
        "type": "其他",
        "location": "中央大學",
        "start_date": "2025-12-10",
        "end_date": "2025-12-10",
        "max_members": 5
    }
    
    # 建立活動
    response = client.post('/api/activities',
        headers=auth_headers,
        json=activity_data
    )
    
    assert response.status_code == 201
    
    # 取得活動 ID
    data = response.get_json()
    activity_id = data['activity']['activity_id']
    
    # 查詢資料庫確認創建者已被新增為參與者
    with client.application.app_context():
        # 取得測試用戶 ID
        user = User.query.filter_by(email='user@user.com').first()
        user_id = user.user_id
        
        # 查詢參與者記錄
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=user_id
        ).first()
        
        # 驗證參與者記錄存在
        assert participant is not None, "創建者應該自動被新增為參與者"
        
        # 驗證參與者狀態
        expected_status = 'joined'
        actual_status = participant.status
        assert actual_status == expected_status, f"參與者狀態應為 'joined'，實際為 '{actual_status}'"
        
        # 驗證參與者角色
        expected_role = 'creator'
        actual_role = participant.role
        assert actual_role == expected_role, f"參與者角色應為 'creator'，實際為 '{actual_role}'"
