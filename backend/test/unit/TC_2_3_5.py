"""
TC_2_3_5: 批准後人數增加
測試說明: 測試驗證人數變化，批准後活動參與人數+1
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_participant_count_increase_after_approval(client, test_app):
    """測試批准後活動參與人數增加"""
    with test_app.app_context():
        # 創建創建者和申請者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        db.session.add_all([creator, applicant])
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
        db.session.commit()
        
        # 創建待審核申請
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=applicant.user_id,
            status='pending',
            role='participant'
        )
        db.session.add(participant)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        participant_id = participant.participant_id
        activity_id = activity.activity_id
        
        # 批准申請前的人數是 0（只有創建者，但創建者不計入 pending）
        count_before = 0
        
        # 批准申請
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證人數增加到 1
        assert data['current_participants'] == count_before + 1
