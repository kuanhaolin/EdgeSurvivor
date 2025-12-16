"""
TC_4.1.4: 查看探索活動
測試說明: 測試探索活動清單（所有活動）
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.activity import Activity
from datetime import datetime, timedelta


def test_get_explore_activities(client, test_app):
    """測試查看探索活動（所有活動）"""
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
        
        # 創建不同用戶的活動
        activity1 = Activity(
            title='登山活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=5,
            creator_id=user01.user_id,
            status='active'
        )
        
        activity2 = Activity(
            title='美食探索',
            category='food',
            location='台北',
            date=datetime.now().date() + timedelta(days=10),
            max_participants=3,
            creator_id=user02.user_id,
            status='active'
        )
        
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
        
        # user01 查詢探索活動（不指定 type，返回所有）
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
        
        # 驗證有不同創建者的活動
        creator_ids = set([act['creator_id'] for act in data['activities']])
        assert len(creator_ids) >= 2  # 至少有2個不同的創建者
