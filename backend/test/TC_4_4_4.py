"""
TC_4.4.4: 費用代墊人欄位驗證 (Backend)
測試說明: 測試代墊人欄位驗證
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_expense_payer_id_validation(client, test_app):
    """驗證代墊人必填"""
    with test_app.app_context():
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant])
        db.session.commit()
        
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
        
        # 測試有效代墊人 ID
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
        
        # 測試另一個有效的參與者 ID
        valid_data2 = valid_data.copy()
        valid_data2['payer_id'] = participant.user_id
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data2
        )
        assert response.status_code == 201
        
        # 測試 null
        null_data = valid_data.copy()
        null_data['payer_id'] = None
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=null_data
        )
        assert response.status_code == 400
        
        # 測試 0
        zero_data = valid_data.copy()
        zero_data['payer_id'] = 0
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=zero_data
        )
        assert response.status_code == 400
        
        # 測試缺少 payer_id 欄位
        missing_data = valid_data.copy()
        del missing_data['payer_id']
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=missing_data
        )
        assert response.status_code == 400
        
        # 測試不存在的 user_id
        invalid_user_data = valid_data.copy()
        invalid_user_data['payer_id'] = 99999
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=invalid_user_data
        )
        assert response.status_code in [400, 404]
