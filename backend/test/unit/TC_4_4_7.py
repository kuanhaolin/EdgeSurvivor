"""
TC_4.4.7: 驗證用戶狀態 (Backend)
測試說明: 測試用戶是否為活動參與者
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from app import db

def test_expense_user_participant_status(client, test_app):
    """驗證只有活動參與者可以添加費用"""
    with test_app.app_context():
        # 創建測試用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        non_participant = User(name='outsider', email='outsider@test.com', password_hash='hash')
        db.session.add_all([creator, participant, non_participant])
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
        
        activity_id = activity.activity_id
        
        # 添加參與者
        creator_participant = ActivityParticipant(
            activity_id=activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        participant_record = ActivityParticipant(
            activity_id=activity_id,
            user_id=participant.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([creator_participant, participant_record])
        db.session.commit()
        
        # 準備有效的費用資料
        valid_data = {
            'description': '午餐',
            'amount': 300,
            'category': 'food',
            'payer_id': creator.user_id,
            'split_type': 'all'
        }
        
        # 測試創建者可以添加費用
        token = create_access_token(identity=str(creator.user_id))
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == '費用記錄已創建'
        
        # 測試參與者可以添加費用
        valid_data['payer_id'] = participant.user_id
        token = create_access_token(identity=str(participant.user_id))
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data
        )
        assert response.status_code == 201
        
        # 測試非參與者不能添加費用
        token = create_access_token(identity=str(non_participant.user_id))
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=valid_data
        )
        assert response.status_code == 403
        data = json.loads(response.data)
        assert '只有活動參與者可以添加費用' in data['error']
