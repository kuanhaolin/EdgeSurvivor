"""
TC_4.5.3: 驗證用戶狀態 (Backend)
測試說明: 測試用戶是否為活動參與者，驗證結算查看權限
"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.expense import Expense
from app import db

def test_settlement_permission(client, test_app):
    """驗證結算查看權限"""
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
        participants = [
            ActivityParticipant(activity_id=activity_id, user_id=creator.user_id, status='joined', role='creator'),
            ActivityParticipant(activity_id=activity_id, user_id=participant.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 添加一筆費用
        expense = Expense(
            activity_id=activity_id,
            payer_id=creator.user_id,
            amount=300,
            description='午餐',
            category='food',
            split_type='all',
            is_split=True
        )
        db.session.add(expense)
        db.session.commit()
        
        # 測試1: 創建者可以查看結算
        token = create_access_token(identity=str(creator.user_id))
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'settlements' in data
        assert 'total_amount' in data
        
        # 測試2: 參與者可以查看結算
        token = create_access_token(identity=str(participant.user_id))
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'settlements' in data
        
        # 測試3: 非參與者不能查看結算
        token = create_access_token(identity=str(non_participant.user_id))
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 403
        data = json.loads(response.data)
        assert '只有活動參與者可以查看結算' in data['error']
        
        # 測試4: 不存在的活動返回404
        token = create_access_token(identity=str(creator.user_id))
        response = client.get(
            f'/api/activities/99999/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert '找不到活動' in data['error']
