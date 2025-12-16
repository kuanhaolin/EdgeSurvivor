"""
TC_4.4.9: 更新費用清單 (Backend)
測試說明: 測試費用清單是否正確
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

def test_expense_list_retrieval(client, test_app):
    """驗證費用清單正確更新和返回"""
    with test_app.app_context():
        # 創建測試用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant1 = User(name='participant1', email='p1@test.com', password_hash='hash')
        participant2 = User(name='participant2', email='p2@test.com', password_hash='hash')
        db.session.add_all([creator, participant1, participant2])
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
            ActivityParticipant(activity_id=activity_id, user_id=participant1.user_id, status='approved', role='participant'),
            ActivityParticipant(activity_id=activity_id, user_id=participant2.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        token = create_access_token(identity=str(creator.user_id))
        
        # 測試初始費用清單為空
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'expenses' in data
        assert len(data['expenses']) == 0
        assert 'summary' in data
        assert data['summary']['total_amount'] == 0
        assert data['summary']['participant_count'] == 3
        
        # 添加第一筆費用（全體分攤）
        expense1_data = {
            'description': '交通費',
            'amount': 600,
            'category': 'transport',
            'payer_id': creator.user_id,
            'split_type': 'all'
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=expense1_data
        )
        assert response.status_code == 201
        
        # 檢查費用清單已更新
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 1
        assert data['expenses'][0]['description'] == '交通費'
        assert float(data['expenses'][0]['amount']) == 600.0
        assert data['summary']['total_amount'] == 600.0
        assert data['summary']['per_person'] == 200.0  # 600 / 3
        
        # 添加第二筆費用（指定分攤）
        expense2_data = {
            'description': '午餐',
            'amount': 450,
            'category': 'food',
            'payer_id': participant1.user_id,
            'split_type': 'selected',
            'split_participants': [creator.user_id, participant1.user_id]
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=expense2_data
        )
        assert response.status_code == 201
        
        # 添加第三筆費用（借款）
        expense3_data = {
            'description': '雨衣',
            'amount': 100,
            'category': 'other',
            'payer_id': creator.user_id,
            'split_type': 'borrow',
            'borrower_id': participant2.user_id
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=expense3_data
        )
        assert response.status_code == 201
        
        # 檢查完整費用清單
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 3
        
        # 驗證費用詳情
        descriptions = [e['description'] for e in data['expenses']]
        assert '交通費' in descriptions
        assert '午餐' in descriptions
        assert '雨衣' in descriptions
        
        # 驗證總金額（只計算全體分攤的費用）
        assert data['summary']['total_amount'] == 600.0  # 只有交通費是全體分攤
        assert data['summary']['participant_count'] == 3
        assert data['summary']['per_person'] == 200.0
        
        # 驗證各種分攤類型都存在
        split_types = [e['split_type'] for e in data['expenses']]
        assert 'all' in split_types
        assert 'selected' in split_types
        assert 'borrow' in split_types
        
        # 測試非參與者無法查看費用清單
        non_participant = User(name='outsider', email='outsider@test.com', password_hash='hash')
        db.session.add(non_participant)
        db.session.commit()
        
        outsider_token = create_access_token(identity=str(non_participant.user_id))
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {outsider_token}'}
        )
        assert response.status_code == 403
        data = json.loads(response.data)
        assert '只有活動參與者可以查看費用' in data['error']
