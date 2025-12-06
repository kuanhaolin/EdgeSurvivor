"""
TC_2_4_3: 創建者無法移除自己
測試說明: 測試創建者移除自己是否成功
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_creator_cannot_remove_self(client, test_app):
    """測試創建者無法移除自己"""
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
        db.session.flush()
        
        # 創建者加入
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        db.session.add(creator_participant)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        creator_participant_id = creator_participant.participant_id
        
        # 創建者嘗試移除自己（應該失敗）
        response = client.delete(
            f'/api/activities/{activity_id}/participants/{creator_participant_id}',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '不能移除自己' in data['error'] or 'cannot remove' in data['error'].lower()
