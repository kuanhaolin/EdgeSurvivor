"""
TC_2_3_6: 達到人數上限自動拒絕
測試說明: 測試人數已滿時自動拒絕新申請
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_reject_when_full(client, test_app):
    """測試人數已滿時無法批准新申請"""
    with test_app.app_context():
        # 創建創建者和兩個申請者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant1 = User(name='applicant1', email='applicant1@test.com', password_hash='hash')
        applicant2 = User(name='applicant2', email='applicant2@test.com', password_hash='hash')
        db.session.add_all([creator, applicant1, applicant2])
        db.session.commit()
        
        # 創建人數上限為 2 的活動（創建者 + 1 個參與者就滿了）
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=2,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.flush()
        
        # 創建者自動加入為參與者
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        db.session.add(creator_participant)
        db.session.commit()
        
        # 創建兩個待審核申請
        participant1 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=applicant1.user_id,
            status='pending',
            role='participant'
        )
        participant2 = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=applicant2.user_id,
            status='pending',
            role='participant'
        )
        db.session.add_all([participant1, participant2])
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        participant1_id = participant1.participant_id
        participant2_id = participant2.participant_id
        activity_id = activity.activity_id
        
        # 批准第一個申請（活動變滿）
        response1 = client.post(
            f'/api/activities/{activity_id}/participants/{participant1_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        assert response1.status_code == 200
        
        # 嘗試批准第二個申請（應該失敗，因為人數已滿）
        response2 = client.post(
            f'/api/activities/{activity_id}/participants/{participant2_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response2.status_code == 400
        data2 = json.loads(response2.data)
        assert '已滿' in data2['error'] or 'full' in data2['error'].lower()
