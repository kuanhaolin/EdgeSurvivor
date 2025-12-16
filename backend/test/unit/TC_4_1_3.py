"""
TC_4.1.3: 查看我參加的活動
測試說明: 測試我參加的活動清單
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from datetime import datetime, timedelta


def test_get_joined_activities(client, test_app):
    """測試查看我參加的活動"""
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
        
        # user02 創建活動1
        activity1 = Activity(
            title='登山活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=5,
            creator_id=user02.user_id,
            status='active'
        )
        
        # user02 創建活動2
        activity2 = Activity(
            title='美食探索',
            category='food',
            location='台北',
            date=datetime.now().date() + timedelta(days=10),
            max_participants=3,
            creator_id=user02.user_id,
            status='active'
        )
        
        # user01 創建活動3（不應該出現在參加列表中）
        activity3 = Activity(
            title='文化之旅',
            category='culture',
            location='故宮',
            date=datetime.now().date() + timedelta(days=5),
            max_participants=4,
            creator_id=user01.user_id,
            status='active'
        )
        
        db.session.add_all([activity1, activity2, activity3])
        db.session.commit()
        
        # user01 參加 activity1 和 activity2
        participant1 = ActivityParticipant(
            activity_id=activity1.activity_id,
            user_id=user01.user_id,
            status='approved',
            role='participant'
        )
        participant2 = ActivityParticipant(
            activity_id=activity2.activity_id,
            user_id=user01.user_id,
            status='approved',
            role='participant'
        )
        
        # user01 作為 activity3 的創建者
        participant3 = ActivityParticipant(
            activity_id=activity3.activity_id,
            user_id=user01.user_id,
            status='joined',
            role='creator'
        )
        
        db.session.add_all([participant1, participant2, participant3])
        db.session.commit()
        
        # user01 查詢參加的活動（type=joined）
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.get(
            '/api/activities?type=joined',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 應該只返回 user01 參加的活動（2個），不包含創建的
        assert 'activities' in data
        assert len(data['activities']) == 2
        
        # 驗證活動標題
        activity_titles = [act['title'] for act in data['activities']]
        assert '登山活動' in activity_titles
        assert '美食探索' in activity_titles
        assert '文化之旅' not in activity_titles
        
        # 驗證都不是 user01 創建的
        for activity in data['activities']:
            assert activity['creator_id'] != user01.user_id
