"""
TC_4.4.1: 費用項目欄位驗證 (Backend)
測試說明: 測試費用項目必填驗證
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_expense_description_validation(client, test_app):
    """驗證費用項目必填"""
    with test_app.app_context():
        # 創建測試用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=date.today(),
            max_participants=10,
            status='ongoing',
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 添加參與者
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        participant_record = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([creator_participant, participant_record])
        db.session.commit()
        
        token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        payer_id = creator.user_id
        
        # 測試有效項目描述
        valid_data = {
            'description': '午餐費用',
            'amount': 100,
            'category': 'food',
            'payer_id': payer_id,
            'split_type': 'all'
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data
        )
        assert response.status_code == 201
        
        # 測試空字串
        empty_data = valid_data.copy()
        empty_data['description'] = ''
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=empty_data
        )
        assert response.status_code == 400
        
        # 測試只有空白
        whitespace_data = valid_data.copy()
        whitespace_data['description'] = '   '
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=whitespace_data
        )
        assert response.status_code == 400
        
        # 測試缺少 description 欄位
        missing_data = valid_data.copy()
        del missing_data['description']
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=missing_data
        )
        assert response.status_code == 400
