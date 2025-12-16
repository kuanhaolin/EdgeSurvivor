"""
TC_4.2.2: 申請活動
測試說明: 測試申請活動
"""
import pytest
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_apply_activity(client, test_app):
    """測試申請活動並附上自我介紹"""
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
        
        # 申請活動
        response = client.post(
            f'/api/activities/{activity_id}/join',
            headers={'Authorization': f'Bearer {applicant_token}'},
            json={'message': '我很喜歡登山，希望能加入這個活動！'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == '申請已發送，等待活動創建者審核'
        assert 'participant_id' in data
        
        # 驗證記錄已創建
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=applicant.user_id
        ).first()
        
        assert participant is not None
        assert participant.status == 'pending'
        assert participant.message == '我很喜歡登山，希望能加入這個活動！'
