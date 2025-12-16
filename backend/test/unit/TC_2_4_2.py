"""
TC_2_4_2: 移除後更新參與者人數
測試說明: 測試移除後更新參與者人數
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_participant_count_decreases_after_removal(client, test_app):
    """測試移除參與者後人數減少"""
    with test_app.app_context():
        # 創建創建者和參與者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant_user = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant_user])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.flush()
        
        # 創建者加入
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        db.session.add(creator_participant)
        db.session.commit()
        
        # 添加參與者（已批准狀態）
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant_user.user_id,
            status='approved',
            role='participant'
        )
        db.session.add(participant)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        participant_id = participant.participant_id
        
        # 移除前人數應為 2（創建者 + 參與者）
        count_before = activity.get_participant_count()
        assert count_before == 2
        
        # 創建者移除參與者
        response = client.delete(
            f'/api/activities/{activity_id}/participants/{participant_id}',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 移除後人數應為 1（只剩創建者）
        assert data['current_participants'] == 1
