"""
TC_4.4.6: 分攤參與者欄位驗證 (Backend)
測試說明: 測試分攤參與者欄位驗證
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_expense_split_participants_validation(client, test_app):
    """驗證分攤參與者（selected模式必填且包含代墊人）"""
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
        
        base_data = {
            'description': '午餐費用',
            'amount': 100,
            'category': 'food',
            'payer_id': payer_id,
            'split_type': 'selected'
        }
        
        # 測試有效參與者列表（包含代墊人）
        valid_data = base_data.copy()
        valid_data['split_participants'] = [creator.user_id, participant.user_id]
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data
        )
        assert response.status_code == 201
        
        # 測試只有代墊人
        only_payer_data = base_data.copy()
        only_payer_data['split_participants'] = [payer_id]
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=only_payer_data
        )
        assert response.status_code == 201
        
        # 測試空陣列
        empty_data = base_data.copy()
        empty_data['split_participants'] = []
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=empty_data
        )
        assert response.status_code == 400
        
        # 測試 null
        null_data = base_data.copy()
        null_data['split_participants'] = None
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=null_data
        )
        assert response.status_code == 400
        
        # 測試不包含代墊人
        no_payer_data = base_data.copy()
        no_payer_data['split_participants'] = [participant.user_id]
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=no_payer_data
        )
        assert response.status_code == 400
        
        # 測試缺少 split_participants 欄位（selected 模式）
        missing_data = base_data.copy()
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=missing_data
        )
        assert response.status_code == 400
        
        # 測試 all 模式不需要驗證參與者（應該成功）
        all_mode_data = {
            'description': '午餐費用',
            'amount': 100,
            'category': 'food',
            'payer_id': payer_id,
            'split_type': 'all'
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=all_mode_data
        )
        assert response.status_code == 201
