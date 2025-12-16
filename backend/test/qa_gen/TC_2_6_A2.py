"""
TC_2_6_A2: 後端：成功查看我參加的活動列表（type=joined）
測試說明: 測試用戶可以取得自己參加的所有活動（不包括自己創建的）
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_get_my_joined_activities(client, test_app):
    """測試取得我參加的活動列表"""
    with test_app.app_context():
        # 創建三個用戶
        user1 = User(name='user1', email='user1@test.com', password_hash='hash1')
        user2 = User(name='user2', email='user2@test.com', password_hash='hash2')
        user3 = User(name='user3', email='user3@test.com', password_hash='hash3')
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        
        # user2 創建活動1
        activity1 = Activity(
            title='User2 活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            start_date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=user2.user_id,
            status='active'
        )
        # user3 創建活動2
        activity2 = Activity(
            title='User3 活動',
            category='camping',
            location='合歡山',
            date=datetime.now().date() + timedelta(days=14),
            start_date=datetime.now().date() + timedelta(days=14),
            max_participants=8,
            creator_id=user3.user_id,
            status='active'
        )
        # user1 自己創建活動3（不應該出現在 joined 列表中）
        activity3 = Activity(
            title='User1 自己的活動',
            category='travel',
            location='台南',
            date=datetime.now().date() + timedelta(days=10),
            start_date=datetime.now().date() + timedelta(days=10),
            max_participants=5,
            creator_id=user1.user_id,
            status='active'
        )
        
        db.session.add_all([activity1, activity2, activity3])
        db.session.commit()
        
        # 添加參與者記錄
        # user1 參加 activity1 和 activity2 (已批准)
        participant1 = ActivityParticipant(
            activity_id=activity1.activity_id,
            user_id=user1.user_id,
            status='approved',
            role='participant'
        )
        participant2 = ActivityParticipant(
            activity_id=activity2.activity_id,
            user_id=user1.user_id,
            status='joined',  # 也測試 joined 狀態
            role='participant'
        )
        # user1 是 activity3 的創建者
        participant3 = ActivityParticipant(
            activity_id=activity3.activity_id,
            user_id=user1.user_id,
            status='joined',
            role='creator'  # 創建者，不應該在 joined 列表
        )
        # 創建者本身的參與記錄
        creator1 = ActivityParticipant(
            activity_id=activity1.activity_id,
            user_id=user2.user_id,
            status='joined',
            role='creator'
        )
        creator2 = ActivityParticipant(
            activity_id=activity2.activity_id,
            user_id=user3.user_id,
            status='joined',
            role='creator'
        )
        
        db.session.add_all([participant1, participant2, participant3, creator1, creator2])
        db.session.commit()
        
        # 生成 user1 的 token
        user1_token = create_access_token(identity=str(user1.user_id))
        
        # 請求 user1 參加的活動
        response = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {user1_token}'}
        )
        
        # 驗證回應
        assert response.status_code == 200
        data = response.get_json()
        assert 'activities' in data
        
        activities = data['activities']
        assert len(activities) == 2  # user1 參加了 2 個活動
        
        # 驗證活動內容
        activity_titles = [a['title'] for a in activities]
        assert 'User2 活動' in activity_titles
        assert 'User3 活動' in activity_titles
        assert 'User1 自己的活動' not in activity_titles  # 自己創建的不應該出現
        
        # 驗證回應包含必要欄位
        for activity in activities:
            assert 'activity_id' in activity
            assert 'title' in activity
            assert 'creator' in activity
            assert activity['creator']['user_id'] != user1.user_id  # 創建者不是 user1
            assert 'current_participants' in activity


def test_get_joined_activities_excludes_pending(client, test_app):
    """測試參加的活動列表不包含待審核狀態的活動"""
    with test_app.app_context():
        user = User(name='user', email='user@test.com', password_hash='hash')
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        db.session.add_all([user, creator])
        db.session.commit()
        
        activity = Activity(
            title='測試活動',
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
        
        # user 申請參加但還在待審核狀態
        pending_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user.user_id,
            status='pending',
            role='participant'
        )
        db.session.add(pending_participant)
        db.session.commit()
        
        user_token = create_access_token(identity=str(user.user_id))
        
        response = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['activities']) == 0  # pending 狀態不應該出現


def test_get_joined_activities_excludes_rejected(client, test_app):
    """測試參加的活動列表不包含被拒絕的活動"""
    with test_app.app_context():
        user = User(name='user', email='user@test.com', password_hash='hash')
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        db.session.add_all([user, creator])
        db.session.commit()
        
        activity = Activity(
            title='測試活動',
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
        
        # user 申請被拒絕
        rejected_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user.user_id,
            status='rejected',
            role='participant'
        )
        db.session.add(rejected_participant)
        db.session.commit()
        
        user_token = create_access_token(identity=str(user.user_id))
        
        response = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['activities']) == 0  # rejected 狀態不應該出現
