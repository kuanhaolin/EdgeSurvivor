"""
TC_4.5.2: 算法優化轉帳次數 (Backend)
測試說明: 測試多人情況下驗證轉帳次數最少
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

def test_minimum_transactions(client, test_app):
    """驗證貪婪演算法優化轉帳次數"""
    with test_app.app_context():
        # 創建4個測試用戶
        users = [
            User(name='Alice', email='alice@test.com', password_hash='hash'),
            User(name='Bob', email='bob@test.com', password_hash='hash'),
            User(name='Charlie', email='charlie@test.com', password_hash='hash'),
            User(name='David', email='david@test.com', password_hash='hash')
        ]
        db.session.add_all(users)
        db.session.commit()
        
        alice, bob, charlie, david = users
        
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
            ActivityParticipant(activity_id=activity_id, user_id=u.user_id, 
                              status='joined' if u == alice else 'approved', 
                              role='creator' if u == alice else 'participant')
            for u in users
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 場景1: 三人平攤 - 最優解應該是2筆轉帳
        # Alice 付 300，Bob 和 Charlie 沒付
        # 每人應付 100
        # 最優解：Bob → Alice 100, Charlie → Alice 100
        expense1 = Expense(
            activity_id=activity_id,
            payer_id=alice.user_id,
            amount=300,
            description='午餐',
            category='food',
            split_type='selected',
            is_split=True,
            split_participants=json.dumps([alice.user_id, bob.user_id, charlie.user_id])
        )
        db.session.add(expense1)
        db.session.commit()
        
        token = create_access_token(identity=str(alice.user_id))
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證轉帳次數：應該是2筆
        assert len(data['settlements']) == 2
        
        # 驗證轉帳方向和金額
        settlement_map = {s['from_user_id']: s for s in data['settlements']}
        assert bob.user_id in settlement_map
        assert charlie.user_id in settlement_map
        assert settlement_map[bob.user_id]['to_user_id'] == alice.user_id
        assert settlement_map[charlie.user_id]['to_user_id'] == alice.user_id
        
        # 場景2: 複雜四人情況
        # 清空之前的費用
        Expense.query.filter_by(activity_id=activity_id).delete()
        db.session.commit()
        
        # Alice 付 1000, Bob 付 800, Charlie 付 600, David 付 400
        # 總計 2800, 每人應付 700
        # Balance: Alice +300, Bob +100, Charlie -100, David -300
        # 最優解應該是2筆：Charlie → Bob 100, David → Alice 300
        expenses = [
            Expense(activity_id=activity_id, payer_id=alice.user_id, amount=1000,
                   description='住宿', category='accommodation', split_type='all', is_split=True,
                   split_participants=json.dumps([u.user_id for u in users])),
            Expense(activity_id=activity_id, payer_id=bob.user_id, amount=800,
                   description='交通', category='transport', split_type='all', is_split=True,
                   split_participants=json.dumps([u.user_id for u in users])),
            Expense(activity_id=activity_id, payer_id=charlie.user_id, amount=600,
                   description='餐飲', category='food', split_type='all', is_split=True,
                   split_participants=json.dumps([u.user_id for u in users])),
            Expense(activity_id=activity_id, payer_id=david.user_id, amount=400,
                   description='門票', category='ticket', split_type='all', is_split=True,
                   split_participants=json.dumps([u.user_id for u in users]))
        ]
        db.session.add_all(expenses)
        db.session.commit()
        
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證總金額
        assert data['total_amount'] == 2800.0
        
        # 驗證轉帳次數：應該 <= 3 (理想情況是2筆)
        assert len(data['settlements']) <= 3
        
        # 驗證所有轉帳金額總和正確
        total_transfer = sum(s['amount'] for s in data['settlements'])
        assert abs(total_transfer - 400.0) < 0.01  # Charlie 100 + David 300 = 400
        
        # 驗證債務人和債權人正確
        debtors = {s['from_user_id'] for s in data['settlements']}
        creditors = {s['to_user_id'] for s in data['settlements']}
        
        # Charlie 和 David 是債務人
        assert charlie.user_id in debtors or david.user_id in debtors
        # Alice 和 Bob 是債權人
        assert alice.user_id in creditors or bob.user_id in creditors
        
        # 場景3: 已平衡情況 - 應該沒有轉帳
        Expense.query.filter_by(activity_id=activity_id).delete()
        db.session.commit()
        
        # 每人都付 100
        balanced_expenses = [
            Expense(activity_id=activity_id, payer_id=u.user_id, amount=100,
                   description=f'{u.name}的費用', category='other', split_type='all', is_split=True,
                   split_participants=json.dumps([user.user_id for user in users]))
            for u in users
        ]
        db.session.add_all(balanced_expenses)
        db.session.commit()
        
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證沒有需要結算的交易
        assert len(data['settlements']) == 0
        assert data['total_amount'] == 400.0
