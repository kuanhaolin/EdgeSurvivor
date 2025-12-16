"""
TC_4.4.8: 費用新增 (Backend)
測試說明: 測試用戶是否成功新增費用
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

def test_expense_creation_success(client, test_app):
    """驗證費用成功新增"""
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
        
        # 測試全體分攤費用
        all_split_data = {
            'description': '交通費',
            'amount': 600,
            'category': 'transport',
            'payer_id': creator.user_id,
            'split_type': 'all'
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=all_split_data
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == '費用記錄已創建'
        assert 'expense' in data
        expense = data['expense']
        assert expense['description'] == '交通費'
        assert float(expense['amount']) == 600.0
        assert expense['category'] == 'transport'
        assert expense['payer_id'] == creator.user_id
        assert expense['split_type'] == 'all'
        
        # 測試指定分攤費用
        selected_split_data = {
            'description': '晚餐',
            'amount': 450,
            'category': 'food',
            'payer_id': creator.user_id,
            'split_type': 'selected',
            'split_participants': [creator.user_id, participant1.user_id]
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=selected_split_data
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        expense = data['expense']
        assert expense['split_type'] == 'selected'
        assert set(json.loads(expense['split_participants'])) == {creator.user_id, participant1.user_id}
        
        # 測試借款費用
        borrow_data = {
            'description': '緊急藥品',
            'amount': 150,
            'category': 'other',
            'payer_id': creator.user_id,
            'split_type': 'borrow',
            'borrower_id': participant2.user_id
        }
        response = client.post(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'},
            json=borrow_data
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        expense = data['expense']
        assert expense['split_type'] == 'borrow'
        assert expense['borrower_id'] == participant2.user_id
        
        # 驗證資料庫中的費用記錄
        expenses = Expense.query.filter_by(activity_id=activity_id).all()
        assert len(expenses) == 3
        
        descriptions = [e.description for e in expenses]
        assert '交通費' in descriptions
        assert '晚餐' in descriptions
        assert '緊急藥品' in descriptions
