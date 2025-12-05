"""
TC 1.7.3 - 級聯刪除相關資料
測試說明: 刪除帳號應該清除相關資料（活動參與、媒合記錄等）
"""
import pytest
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.match import Match
from models import db

def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user_with_data(test_app):
    with test_app.app_context():
        # 建立用戶
        user = User(
            name='user',
            email='user@user.com',
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        
        user_id = user.user_id
        
        # 建立另一個用戶
        other_user = User(
            name='other',
            email='other@user.com',
            password_hash='dummy_hash',
            is_verified=True,
            is_active=True
        )
        db.session.add(other_user)
        db.session.commit()
        
        # 建立活動
        from datetime import date
        activity = Activity(
            title='Test Activity',
            date=date(2025, 12, 31),
            location='Test Location',
            creator_id=other_user.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 加入活動參與記錄
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user_id,
            status='joined'
        )
        db.session.add(participant)
        
        # 建立媒合記錄
        match = Match(
            user_a=user_id,
            user_b=other_user.user_id,
            status='accepted'
        )
        db.session.add(match)
        db.session.commit()
        
        yield user_id, activity.activity_id

def test_cascade_delete_related_data(client, test_app, test_user_with_data):
    user_id, activity_id = test_user_with_data
    
    # 登入
    response = client.post('/api/auth/login', json={
        'email': 'user@user.com',
        'password': '123456'
    })
    token = response.get_json()['access_token']
    
    # 確認資料存在
    with test_app.app_context():
        assert ActivityParticipant.query.filter_by(user_id=user_id).count() > 0
        assert Match.query.filter((Match.user_a == user_id) | (Match.user_b == user_id)).count() > 0
    
    # 刪除帳號
    response = client.delete('/api/users/account', json={
        'password': '123456'
    }, headers=get_auth_header(token))
    assert response.status_code == 200
    
    # 驗證相關資料已被刪除
    with test_app.app_context():
        assert ActivityParticipant.query.filter_by(user_id=user_id).count() == 0
        assert Match.query.filter((Match.user_a == user_id) | (Match.user_b == user_id)).count() == 0
        assert User.query.get(user_id) is None
