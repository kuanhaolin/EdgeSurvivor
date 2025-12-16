"""
TC_2_4_4: 非創建者無法移除他人
測試說明: 測試一般參與者移除其他人是否成功
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_non_creator_cannot_remove_others(client, test_app):
    """測試非創建者無法移除其他參與者"""
    with test_app.app_context():
        # 創建創建者和兩個參與者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant1 = User(name='participant1', email='participant1@test.com', password_hash='hash')
        participant2 = User(name='participant2', email='participant2@test.com', password_hash='hash')
        db.session.add_all([creator, participant1, participant2])
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
        
        # 添加參與者1（已批准）
        participant1_record = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant1.user_id,
            status='approved',
            role='participant'
        )
        # 添加參與者2（已批准）
        participant2_record = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant2.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([participant1_record, participant2_record])
        db.session.commit()
        
        participant1_token = create_access_token(identity=str(participant1.user_id))
        activity_id = activity.activity_id
        participant2_id = participant2_record.participant_id
        
        # 參與者1嘗試移除參與者2（應該失敗）
        response = client.delete(
            f'/api/activities/{activity_id}/participants/{participant2_id}',
            headers={'Authorization': f'Bearer {participant1_token}'}
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'error' in data
        assert '創建者' in data['error'] or 'creator' in data['error'].lower()
