"""
TC_4.1.1: 查看用戶所有活動
測試說明: 測試我的所有活動清單
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from datetime import datetime, timedelta


def test_get_all_user_activities(client, test_app):
    """測試查看用戶所有活動"""
    with test_app.app_context():
        # 創建測試用戶
        user01 = User(
            name='user01',
            email='user01@example.com',
            password_hash='hash1',
            gender='male',
            age=25
        )
        user02 = User(
            name='user02',
            email='user02@example.com',
            password_hash='hash2',
            gender='female',
            age=28
        )
        db.session.add_all([user01, user02])
        db.session.commit()
        
        # user01 創建活動1
        activity1 = Activity(
            title='登山活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=5,
            creator_id=user01.user_id,
            status='active'
        )
        
        # user01 創建活動2
        activity2 = Activity(
            title='美食探索',
            category='food',
            location='台北',
            date=datetime.now().date() + timedelta(days=10),
            max_participants=3,
            creator_id=user01.user_id,
            status='active'
        )
        
        # user02 創建活動3
        activity3 = Activity(
            title='文化之旅',
            category='culture',
            location='故宮',
            date=datetime.now().date() + timedelta(days=5),
            max_participants=4,
            creator_id=user02.user_id,
            status='active'
        )
        
        db.session.add_all([activity1, activity2, activity3])
        db.session.commit()
        
        # 添加創建者為參與者
        participant1 = ActivityParticipant(
            activity_id=activity1.activity_id,
            user_id=user01.user_id,
            status='joined',
            role='creator'
        )
        participant2 = ActivityParticipant(
            activity_id=activity2.activity_id,
            user_id=user01.user_id,
            status='joined',
            role='creator'
        )
        participant3 = ActivityParticipant(
            activity_id=activity3.activity_id,
            user_id=user02.user_id,
            status='joined',
            role='creator'
        )
        
        # user01 參加 activity3
        participant4 = ActivityParticipant(
            activity_id=activity3.activity_id,
            user_id=user01.user_id,
            status='approved',
            role='participant'
        )
        
        db.session.add_all([participant1, participant2, participant3, participant4])
        db.session.commit()
        
        # user01 查詢所有活動（不指定 type 參數）
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.get(
            '/api/activities',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 應該返回所有活動（3個）
        assert 'activities' in data
        assert len(data['activities']) == 3
        
        # 驗證活動標題
        activity_titles = [act['title'] for act in data['activities']]
        assert '登山活動' in activity_titles
        assert '美食探索' in activity_titles
        assert '文化之旅' in activity_titles
