"""
TC_4.3.3: 更新評價者平均分數
測試說明: 測試評價者平均分數
"""
import pytest
import json
from datetime import datetime, timedelta, date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.activity_review import ActivityReview
from app import db

def test_update_average_rating(client, test_app):
    """測試更新被評價者的平均分數"""
    with test_app.app_context():
        # 創建三個用戶
        reviewer1 = User(name='reviewer1', email='reviewer1@test.com', password_hash='hash')
        reviewer2 = User(name='reviewer2', email='reviewer2@test.com', password_hash='hash')
        reviewee = User(name='reviewee', email='reviewee@test.com', password_hash='hash', average_rating=0.0, rating_count=0)
        db.session.add_all([reviewer1, reviewer2, reviewee])
        db.session.commit()
        
        # 創建已完成的活動
        yesterday = date.today() - timedelta(days=1)
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=yesterday,
            end_date=yesterday,
            max_participants=10,
            status='completed',
            creator_id=reviewer1.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 三個用戶都加入活動
        participants = [
            ActivityParticipant(activity_id=activity.activity_id, user_id=reviewer1.user_id, status='joined', role='creator'),
            ActivityParticipant(activity_id=activity.activity_id, user_id=reviewer2.user_id, status='approved', role='participant'),
            ActivityParticipant(activity_id=activity.activity_id, user_id=reviewee.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 驗證初始平均分數
        assert reviewee.average_rating == 0.0
        assert reviewee.rating_count == 0
        
        # Reviewer1 給 Reviewee 5分
        reviewer1_token = create_access_token(identity=str(reviewer1.user_id))
        response1 = client.post(
            f'/api/activities/{activity.activity_id}/reviews',
            headers={'Authorization': f'Bearer {reviewer1_token}'},
            json={
                'reviewee_id': reviewee.user_id,
                'rating': 5,
                'comment': '很棒！'
            }
        )
        assert response1.status_code == 200
        
        # 驗證平均分數更新（5分）
        db.session.refresh(reviewee)
        assert reviewee.rating_count == 1
        assert reviewee.average_rating == 5.0
        
        # Reviewer2 給 Reviewee 3分
        reviewer2_token = create_access_token(identity=str(reviewer2.user_id))
        response2 = client.post(
            f'/api/activities/{activity.activity_id}/reviews',
            headers={'Authorization': f'Bearer {reviewer2_token}'},
            json={
                'reviewee_id': reviewee.user_id,
                'rating': 3,
                'comment': '還可以'
            }
        )
        assert response2.status_code == 200
        
        # 驗證平均分數更新（(5+3)/2 = 4.0）
        db.session.refresh(reviewee)
        assert reviewee.rating_count == 2
        assert reviewee.average_rating == 4.0
