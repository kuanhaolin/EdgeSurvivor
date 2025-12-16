"""
TC_2_5_A4: 測試無法重複處理已審核申請
測試說明: 嘗試重複批准/拒絕已處理的申請時應返回400錯誤
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_cannot_reprocess_approved_application(client, test_app):
    """測試無法重複處理已批准的申請"""
    with test_app.app_context():
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        db.session.add_all([creator, applicant])
        db.session.commit()
        
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
        
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=applicant.user_id,
            status='approved',  # 已批准
            role='participant'
        )
        db.session.add(participant)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        participant_id = participant.participant_id
        
        # 嘗試再次批准已批准的申請
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '已處理' in data['error'] or 'processed' in data['error'].lower()

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v', '--no-cov'])
