"""
TC_4.4.5: 分攤方式欄位驗證 (Backend)
測試說明: 測試分攤方式欄位驗證
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_expense_split_type_validation(client, test_app):
    """驗證分攤方式必填且為有效選項"""
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
            'payer_id': payer_id
        }
        
        # 測試 all 分攤方式
        all_data = base_data.copy()
        all_data['split_type'] = 'all'
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=all_data
        )
        assert response.status_code == 201
        
        # 測試 selected 分攤方式
        selected_data = base_data.copy()
        selected_data['split_type'] = 'selected'
        selected_data['split_participants'] = [payer_id]
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=selected_data
        )
        assert response.status_code == 201
        
        # 測試 borrow 分攤方式
        borrow_data = base_data.copy()
        borrow_data['split_type'] = 'borrow'
        borrow_data['borrower_id'] = participant.user_id
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=borrow_data
        )
        assert response.status_code == 201
        
        # 測試無效分攤方式
        invalid_data = base_data.copy()
        invalid_data['split_type'] = 'invalid_type'
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=invalid_data
        )
        assert response.status_code == 400
        
        # 測試空字串
        empty_data = base_data.copy()
        empty_data['split_type'] = ''
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=empty_data
        )
        assert response.status_code == 400
        
        # 測試缺少 split_type 欄位
        missing_data = base_data.copy()
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=missing_data
        )
        assert response.status_code == 400
