"""
TC_4.2.5: 更新我的活動清單
測試說明: 測試申請活動後，我的活動清單是否正確更新
"""
import pytest
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_update_my_activities_after_apply(client, test_app):
    """測試申請活動後更新我的活動清單"""
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
        
        applicant_token = create_access_token(identity=str(applicant.user_id))
        activity_id = activity.activity_id
        
        # 申請前：檢查我創建的活動列表（應為空）
        response_created_before = client.get(
            '/api/activities?type=created',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response_created_before.status_code == 200
        data_created_before = json.loads(response_created_before.data)
        assert len(data_created_before['activities']) == 0
        
        # 申請前：檢查我參加的活動列表（應為空）
        response_joined_before = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response_joined_before.status_code == 200
        data_joined_before = json.loads(response_joined_before.data)
        assert len(data_joined_before['activities']) == 0
        
        # 申請活動
        response_apply = client.post(
            f'/api/activities/{activity_id}/join',
            headers={'Authorization': f'Bearer {applicant_token}'},
            json={'message': '我想參加這個活動！'}
        )
        
        assert response_apply.status_code == 200
        
        # 申請後：驗證用戶已是參與者（pending狀態）
        assert activity.is_user_participant(applicant.user_id)
        
        # 驗證申請記錄
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=applicant.user_id
        ).first()
        
        assert participant is not None
        assert participant.status == 'pending'
        assert participant.role == 'participant'
        
        # 批准申請
        creator_token = create_access_token(identity=str(creator.user_id))
        participant_id = participant.participant_id
        
        response_approve = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response_approve.status_code == 200
        
        # 批准後：檢查我參加的活動列表（應包含該活動）
        response_joined_after = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response_joined_after.status_code == 200
        data_joined_after = json.loads(response_joined_after.data)
        assert len(data_joined_after['activities']) == 1
        assert data_joined_after['activities'][0]['activity_id'] == activity_id
        
        # 驗證申請狀態已更新為approved
        db.session.refresh(participant)
        assert participant.status == 'approved'
