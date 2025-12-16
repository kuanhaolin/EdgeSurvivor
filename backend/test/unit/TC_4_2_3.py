"""
TC_4.2.3: 驗證申請狀態
測試說明: 測試活動申請狀態
"""
import pytest
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_verify_application_status(client, test_app):
    """測試驗證申請狀態為pending"""
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
            role='participant',
            message='我很愛登山'
        )
        db.session.add(participant)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        
        # 創建者查看待審核列表
        response = client.get(
            f'/api/activities/{activity_id}/participants/pending',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['pending_participants']) == 1
        assert data['pending_participants'][0]['user_id'] == applicant.user_id
        assert data['pending_participants'][0]['message'] == '我很愛登山'
        
        # 驗證申請狀態
        assert participant.status == 'pending'
