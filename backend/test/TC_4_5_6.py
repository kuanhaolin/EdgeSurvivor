"""
TC_4.5.6: 更新費用明細清單 (Backend)
測試說明: 測試費用明細清單是否正確（包含刪除後的更新）
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

def test_expense_list_update_after_deletion(client, test_app):
    """驗證刪除費用後清單和結算正確更新"""
    with test_app.app_context():
        # 創建測試用戶
        alice = User(name='Alice', email='alice@test.com', password_hash='hash')
        bob = User(name='Bob', email='bob@test.com', password_hash='hash')
        db.session.add_all([alice, bob])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=date.today(),
            max_participants=10,
            status='ongoing',
            creator_id=alice.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        activity_id = activity.activity_id
        
        # 添加參與者
        participants = [
            ActivityParticipant(activity_id=activity_id, user_id=alice.user_id, status='joined', role='creator'),
            ActivityParticipant(activity_id=activity_id, user_id=bob.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建3筆費用
        # Alice 付 600, Bob 付 400
        # 總計 1000, 每人應付 500
        # Alice 應收 100, Bob 應付 100
        expenses = [
            Expense(activity_id=activity_id, payer_id=alice.user_id, amount=300,
                   description='午餐', category='food', split_type='all', is_split=True),
            Expense(activity_id=activity_id, payer_id=alice.user_id, amount=300,
                   description='交通', category='transport', split_type='all', is_split=True),
            Expense(activity_id=activity_id, payer_id=bob.user_id, amount=400,
                   description='門票', category='ticket', split_type='all', is_split=True)
        ]
        db.session.add_all(expenses)
        db.session.commit()
        
        expense_ids = [e.expense_id for e in expenses]
        token = create_access_token(identity=str(alice.user_id))
        
        # 驗證初始狀態
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 3
        assert data['summary']['total_amount'] == 1000.0
        
        # 驗證初始結算：Bob 欠 Alice 100
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['settlements']) == 1
        assert data['settlements'][0]['from_user_id'] == bob.user_id
        assert data['settlements'][0]['to_user_id'] == alice.user_id
        assert data['settlements'][0]['amount'] == 100.0
        
        # 刪除 Alice 的一筆費用（300元）
        response = client.delete(
            f'/api/expenses/{expense_ids[0]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 驗證費用清單更新
        # 剩下：Alice 300, Bob 400 = 700
        # 每人應付 350
        # Alice 應付 50, Bob 應收 50
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 2
        assert data['summary']['total_amount'] == 700.0
        
        # 驗證結算更新：Alice 欠 Bob 50
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['settlements']) == 1
        assert data['settlements'][0]['from_user_id'] == alice.user_id
        assert data['settlements'][0]['to_user_id'] == bob.user_id
        assert data['settlements'][0]['amount'] == 50.0
        
        # 再刪除 Bob 的費用
        response = client.delete(
            f'/api/expenses/{expense_ids[2]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 驗證結算：只剩 Alice 付 300, 每人 150
        # Bob 欠 Alice 150
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['settlements']) == 1
        assert data['settlements'][0]['from_user_id'] == bob.user_id
        assert data['settlements'][0]['amount'] == 150.0
        
        # 刪除最後一筆費用
        response = client.delete(
            f'/api/expenses/{expense_ids[1]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 驗證結算清空
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['settlements']) == 0
        assert data['total_amount'] == 0.0
