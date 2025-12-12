"""
TC_4.1.2: 查看我創建的活動
測試說明: 測試我創建的活動清單
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from datetime import datetime, timedelta


def test_get_created_activities(client, test_app):
    """測試查看我創建的活動"""
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
        
        # user02 創建活動3（不應該出現在 user01 的列表中）
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
        
        # user01 查詢創建的活動（type=created）
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.get(
            '/api/activities?type=created',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 應該只返回 user01 創建的活動（2個）
        assert 'activities' in data
        assert len(data['activities']) == 2
        
        # 驗證活動標題
        activity_titles = [act['title'] for act in data['activities']]
        assert '登山活動' in activity_titles
        assert '美食探索' in activity_titles
        assert '文化之旅' not in activity_titles
        
        # 驗證都是 user01 創建的
        for activity in data['activities']:
            assert activity['creator_id'] == user01.user_id
