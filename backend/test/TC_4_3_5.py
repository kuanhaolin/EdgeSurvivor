"""
TC_4.3.5: 更新評價者評論
測試說明: 測試評價者評論更新
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

def test_update_review(client, test_app):
    """測試更新評價評論和評分"""
    with test_app.app_context():
        # 創建創建者和參與者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant])
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
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 創建者和參與者加入
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        participant_record = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([creator_participant, participant_record])
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        participant_id = participant.user_id
        
        # 第一次提交評價
        response1 = client.post(
            f'/api/activities/{activity_id}/reviews',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={
                'reviewee_id': participant_id,
                'rating': 4,
                'comment': '還不錯的旅伴'
            }
        )
        
        assert response1.status_code == 200
        
        # 驗證原始評價
        review = ActivityReview.query.filter_by(
            activity_id=activity_id,
            reviewer_id=creator.user_id,
            reviewee_id=participant_id
        ).first()
        
        assert review is not None
        assert review.rating == 4
        assert review.comment == '還不錯的旅伴'
        original_created_at = review.created_at
        
        # 更新評價
        response2 = client.post(
            f'/api/activities/{activity_id}/reviews',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={
                'reviewee_id': participant_id,
                'rating': 5,
                'comment': '很棒的旅伴，準時守信，期待下次再一起旅行！'
            }
        )
        
        assert response2.status_code == 200
        data = json.loads(response2.data)
        assert data['message'] == '評價已更新'
        
        # 驗證評價已更新
        db.session.refresh(review)
        assert review.rating == 5
        assert review.comment == '很棒的旅伴，準時守信，期待下次再一起旅行！'
        assert review.created_at == original_created_at  # created_at 不變
        assert review.updated_at > review.created_at  # updated_at 已更新
        
        # 測試再次更新評分和評論
        response3 = client.post(
            f'/api/activities/{activity_id}/reviews',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={
                'reviewee_id': participant_id,
                'rating': 3,
                'comment': '經過相處發現是很棒的旅伴！'
            }
        )
        
        assert response3.status_code == 200
        data3 = json.loads(response3.data)
        assert data3['message'] == '評價已更新'
        
        db.session.refresh(review)
        assert review.rating == 3
        assert review.comment == '經過相處發現是很棒的旅伴！'