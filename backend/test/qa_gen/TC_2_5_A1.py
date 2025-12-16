"""
TC_2_5_A1: 測試活動參與人數上限檢查
測試說明: 驗證當活動已滿時無法批准新申請
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_cannot_approve_when_activity_full(client, test_app):
    """測試活動已滿時無法批准新申請"""
    with test_app.app_context():
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        user1 = User(name='user1', email='user1@test.com', password_hash='hash')
        user2 = User(name='user2', email='user2@test.com', password_hash='hash')
        user3 = User(name='user3', email='user3@test.com', password_hash='hash')
        db.session.add_all([creator, user1, user2, user3])
        db.session.commit()
        
        # 創建最多2人參加的活動
        activity = Activity(
            title='小型活動',
            category='hiking',
            location='測試地點',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=2,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 創建者自動加入，佔1個位置
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='approved',
            role='creator'
        )
        db.session.add(creator_participant)
        db.session.commit()
        
        # user1 已批准，佔第2個位置（活動已滿）
        participant1 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user1.user_id,
            status='approved',
            role='participant'
        )
        db.session.add(participant1)
        db.session.commit()
        
        # user2 pending狀態
        participant2 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user2.user_id,
            status='pending',
            role='participant'
        )
        db.session.add(participant2)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        participant_id = participant2.participant_id
        
        # 嘗試批准 user2 申請（活動已滿）
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '已滿' in data['error'] or 'full' in data['error'].lower()

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v', '--no-cov'])
