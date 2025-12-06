"""
TC 2.2.6: 刪除所有相關記錄
測試說明: 測試刪除活動時會級聯刪除相關記錄
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity_participant import ActivityParticipant
from models.activity_discussion import ActivityDiscussion


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


def test_cascade_delete_related_records(client, creator_headers):
    """測試刪除活動會級聯刪除參與者和討論記錄"""
    
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
    
    # 2. 創建討論記錄
    with client.application.app_context():
        creator = User.query.filter_by(email='creator@test.com').first()
        
        discussion = ActivityDiscussion(
            activity_id=activity_id,
            user_id=creator.user_id,
            message="測試討論內容"
        )
        db.session.add(discussion)
        db.session.commit()
        
        # 驗證記錄存在
        participants = ActivityParticipant.query.filter_by(activity_id=activity_id).all()
        discussions = ActivityDiscussion.query.filter_by(activity_id=activity_id).all()
        assert len(participants) >= 1  # 至少有創建者
        assert len(discussions) == 1
    
    # 3. 刪除活動
    response = client.delete(f'/api/activities/{activity_id}',
        headers=creator_headers
    )
    
    assert response.status_code == 200
    
    # 4. 驗證相關記錄已被級聯刪除
    with client.application.app_context():
        participants = ActivityParticipant.query.filter_by(activity_id=activity_id).all()
        discussions = ActivityDiscussion.query.filter_by(activity_id=activity_id).all()
        
        assert len(participants) == 0, "參與者記錄應該被刪除"
        assert len(discussions) == 0, "討論記錄應該被刪除"
