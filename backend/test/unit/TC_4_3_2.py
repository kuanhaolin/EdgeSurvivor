"""
TC_4.3.2: 驗證互評評分
測試說明: 測試互評評分，必填
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

def test_submit_review_rating_validation(client, test_app):
    """測試提交互評評分必填驗證"""
    with test_app.app_context():
        # 創建創建者和參與者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant])
        db.session.commit()
        
        # 創建已完成的活動（結束日期為昨天）
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
        
        # 創建者自動加入
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        # 參與者加入
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
        
        # 提交評價（包含必填的rating）
        response = client.post(
            f'/api/activities/{activity_id}/reviews',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={
                'reviewee_id': participant_id,
                'rating': 5,  # 必填
                'comment': '很棒的旅伴！'
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == '評價已提交'
        assert 'review' in data
        
        # 驗證評價已創建
        review = ActivityReview.query.filter_by(
            activity_id=activity_id,
            reviewer_id=creator.user_id,
            reviewee_id=participant_id
        ).first()
        
        assert review is not None
        assert review.rating == 5
        assert review.comment == '很棒的旅伴！'
        
        # 測試提交評價但缺少rating
        response2 = client.post(
            f'/api/activities/{activity_id}/reviews',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={
                'reviewee_id': participant_id,
                'comment': '很棒的旅伴！'
                # 缺少rating
            }
        )
        
        assert response2.status_code == 400
        data2 = json.loads(response2.data)
        assert 'error' in data2
        assert '評分' in data2['error'] or 'rating' in data2['error'].lower()

