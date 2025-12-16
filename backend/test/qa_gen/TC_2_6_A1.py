"""
TC_2_6_A1: 後端：成功查看我創建的活動列表（type=created）
測試說明: 測試用戶可以取得自己創建的所有活動
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_get_my_created_activities(client, test_app):
    """測試取得我創建的活動列表"""
    with test_app.app_context():
        # 創建兩個用戶
        user1 = User(name='user1', email='user1@test.com', password_hash='hash1')
        user2 = User(name='user2', email='user2@test.com', password_hash='hash2')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # user1 創建兩個活動
        activity1 = Activity(
            title='User1 活動1',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            start_date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=user1.user_id,
            status='active'
        )
        activity2 = Activity(
            title='User1 活動2',
            category='camping',
            location='合歡山',
            date=datetime.now().date() + timedelta(days=14),
            start_date=datetime.now().date() + timedelta(days=14),
            max_participants=8,
            creator_id=user1.user_id,
            status='active'
        )
        
        # user2 也創建一個活動（不應該在 user1 的列表中）
        activity3 = Activity(
            title='User2 活動',
            category='travel',
            location='台南',
            date=datetime.now().date() + timedelta(days=10),
            start_date=datetime.now().date() + timedelta(days=10),
            max_participants=5,
            creator_id=user2.user_id,
            status='active'
        )
        
        db.session.add_all([activity1, activity2, activity3])
        db.session.commit()
        
        # 為每個活動添加創建者為參與者
        for activity in [activity1, activity2, activity3]:
            participant = ActivityParticipant(
                activity_id=activity.activity_id,
                user_id=activity.creator_id,
                status='joined',
                role='creator'
            )
            db.session.add(participant)
        db.session.commit()
        
        # 生成 user1 的 token
        user1_token = create_access_token(identity=str(user1.user_id))
        
        # 請求 user1 創建的活動
        response = client.get(
            '/api/activities?type=created',
            headers={'Authorization': f'Bearer {user1_token}'}
        )
        
        # 驗證回應
        assert response.status_code == 200
        data = response.get_json()
        assert 'activities' in data
        
        activities = data['activities']
        assert len(activities) == 2  # user1 創建了 2 個活動
        
        # 驗證所有活動都是 user1 創建的
        activity_titles = [a['title'] for a in activities]
        assert 'User1 活動1' in activity_titles
        assert 'User1 活動2' in activity_titles
        assert 'User2 活動' not in activity_titles  # user2 的活動不應該出現
        
        # 驗證回應包含必要欄位
        for activity in activities:
            assert 'activity_id' in activity
            assert 'title' in activity
            assert 'creator' in activity
            assert activity['creator']['user_id'] == user1.user_id
            assert 'current_participants' in activity
            assert activity['current_participants'] == 1  # 只有創建者


def test_get_created_activities_empty(client, test_app):
    """測試沒有創建活動時返回空列表"""
    with test_app.app_context():
        user = User(name='newuser', email='newuser@test.com', password_hash='hash')
        db.session.add(user)
        db.session.commit()
        
        user_token = create_access_token(identity=str(user.user_id))
        
        response = client.get(
            '/api/activities?type=created',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'activities' in data
        assert len(data['activities']) == 0


def test_get_created_activities_with_pending_count(client, test_app):
    """測試創建的活動包含待審核數量"""
    with test_app.app_context():
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        applicant = User(name='applicant', email='applicant@test.com', password_hash='hash')
        db.session.add_all([creator, applicant])
        db.session.commit()
        
        activity = Activity(
            title='待審核活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            start_date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id,
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        
        # 創建者參與
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        # 申請者待審核
        applicant_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=applicant.user_id,
            status='pending',
            role='participant'
        )
        db.session.add_all([creator_participant, applicant_participant])
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        
        response = client.get(
            '/api/activities?type=created',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        activities = data['activities']
        assert len(activities) == 1
        assert activities[0]['pending_count'] == 1  # 有 1 個待審核申請
