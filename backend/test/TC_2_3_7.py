"""
TC_2_3_7: 非創建者無法審核
測試說明: 測試非創建者無法審核申請
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_non_creator_cannot_review(client, test_app):
    """測試非創建者無法審核申請"""
    with test_app.app_context():
        # 創建創建者、申請者和另一個普通用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        other_user = User(name='other', email='other@test.com', password_hash='hash')
        db.session.add_all([creator, applicant, other_user])
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
        
        other_user_token = create_access_token(identity=str(other_user.user_id))
        participant_id = participant.participant_id
        activity_id = activity.activity_id
        
        # 非創建者嘗試批准申請（應該失敗）
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers={'Authorization': f'Bearer {other_user_token}'}
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'error' in data
