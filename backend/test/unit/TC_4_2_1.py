"""
TC_4.2.1: 驗證活動狀態
測試說明: 測試是否活動狀態為未參與活動與人數未滿
"""
import pytest
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_verify_activity_status(client, test_app):
    """測試驗證活動狀態（未參與且人數未滿）"""
    with test_app.app_context():
        # 創建創建者和申請者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        db.session.add_all([creator, applicant])
        db.session.commit()
        
        # 創建活動（max_participants=5）
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=5,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 創建者自動加入
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        db.session.add(creator_participant)
        db.session.commit()
        
        applicant_token = create_access_token(identity=str(applicant.user_id))
        activity_id = activity.activity_id
        
        # 獲取活動詳情
        response = client.get(
            f'/api/activities/{activity_id}',
            headers={'Authorization': f'Bearer {applicant_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證活動狀態
        assert data['activity']['current_participants'] < data['activity']['max_participants']  # 人數未滿
        assert not activity.is_user_participant(applicant.user_id)  # 申請者未參與
