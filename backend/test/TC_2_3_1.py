"""
TC_2_3_1: 待審核申請管理
測試說明: 測試創建者查看所有待審核申請，驗證創建者是否能查看
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_get_pending_participants(client, test_app):
    """測試創建者查看待審核申請列表"""
    with test_app.app_context():
        # 創建創建者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        db.session.add(creator)
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        
        # 創建者查看待審核列表
        response = client.get(
            f'/api/activities/{activity_id}/participants/pending',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'pending_participants' in data
        assert isinstance(data['pending_participants'], list)
