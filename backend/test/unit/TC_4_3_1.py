"""
TC_4.3.1: 活動狀態驗證
測試說明: 測試活動結束和標示已完成狀態
"""
import pytest
import json
from datetime import datetime, timedelta, date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_activity_completed_status(client, test_app):
    """測試活動標示為已完成狀態"""
    with test_app.app_context():
        # 創建創建者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        db.session.add(creator)
        db.session.commit()
        
        # 創建活動（結束日期為昨天）
        yesterday = date.today() - timedelta(days=1)
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=yesterday,
            end_date=yesterday,
            max_participants=10,
            status='active',  # 初始狀態為active
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        
        # 驗證初始狀態
        assert activity.status == 'active'
        assert activity.end_date == yesterday
        
        # 創建者將活動標示為已完成
        response = client.put(
            f'/api/activities/{activity_id}',
            headers={'Authorization': f'Bearer {creator_token}'},
            json={'status': 'completed'}
        )
        
        assert response.status_code == 200
        
        # 驗證狀態已更新為completed
        db.session.refresh(activity)
        assert activity.status == 'completed'
        
        # 驗證結束日期已過
        today = date.today()
        assert activity.end_date < today or activity.end_date == yesterday
