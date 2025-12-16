"""
TC_4.5.1: 結算計算邏輯 (Backend)
測試說明: 測試全體平攤的結算計算，包含所有分攤項目
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

def test_settlement_calculation_logic(client, test_app):
    """驗證結算計算邏輯"""
    with test_app.app_context():
        # 創建測試用戶
        alice = User(name='Alice', email='alice@test.com', password_hash='hash')
        bob = User(name='Bob', email='bob@test.com', password_hash='hash')
        charlie = User(name='Charlie', email='charlie@test.com', password_hash='hash')
        db.session.add_all([alice, bob, charlie])
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
            ActivityParticipant(activity_id=activity_id, user_id=bob.user_id, status='approved', role='participant'),
            ActivityParticipant(activity_id=activity_id, user_id=charlie.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 場景1: 單筆全體平攤
        # Alice 付 300，三人平分，每人應付 100
        expense1 = Expense(
            activity_id=activity_id,
            payer_id=alice.user_id,
            amount=300,
            description='午餐',
            category='food',
            split_type='all',
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
        
        # 驗證總金額
        assert data['total_amount'] == 300.0
        assert data['participant_count'] == 3
        
        # 驗證結算清單
        # Bob 和 Charlie 各欠 Alice 100
        assert len(data['settlements']) == 2
        settlement_map = {s['from_user_id']: s for s in data['settlements']}
        
        assert bob.user_id in settlement_map
        assert settlement_map[bob.user_id]['to_user_id'] == alice.user_id
        assert settlement_map[bob.user_id]['amount'] == 100.0
        
        assert charlie.user_id in settlement_map
        assert settlement_map[charlie.user_id]['to_user_id'] == alice.user_id
        assert settlement_map[charlie.user_id]['amount'] == 100.0
        
        # 場景2: 多筆全體平攤
        # Bob 付 600，Charlie 付 300
        # 總計：Alice 付 300, Bob 付 600, Charlie 付 300 = 1200
        # 每人應付：400
        # Alice 應收 100 (300 - 400 = -100)
        # Bob 應收 200 (600 - 400 = 200)
        # Charlie 應收 100 (300 - 400 = -100)
        expense2 = Expense(
            activity_id=activity_id,
            payer_id=bob.user_id,
            amount=600,
            description='交通',
            category='transport',
            split_type='all',
            is_split=True,
            split_participants=json.dumps([alice.user_id, bob.user_id, charlie.user_id])
        )
        expense3 = Expense(
            activity_id=activity_id,
            payer_id=charlie.user_id,
            amount=300,
            description='門票',
            category='ticket',
            split_type='all',
            is_split=True,
            split_participants=json.dumps([alice.user_id, bob.user_id, charlie.user_id])
        )
        db.session.add_all([expense2, expense3])
        db.session.commit()
        
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證總金額
        assert data['total_amount'] == 1200.0
        
        # 驗證結算清單
        # Alice 欠 Bob 100
        # Charlie 欠 Bob 100
        assert len(data['settlements']) == 2
        
        settlements_list = data['settlements']
        alice_settlement = next((s for s in settlements_list if s['from_user_id'] == alice.user_id), None)
        charlie_settlement = next((s for s in settlements_list if s['from_user_id'] == charlie.user_id), None)
        
        assert alice_settlement is not None
        assert alice_settlement['to_user_id'] == bob.user_id
        assert alice_settlement['amount'] == 100.0
        
        assert charlie_settlement is not None
        assert charlie_settlement['to_user_id'] == bob.user_id
        assert charlie_settlement['amount'] == 100.0
        
        # 場景3: 指定分攤
        # 清空之前的費用
        Expense.query.filter_by(activity_id=activity_id).delete()
        db.session.commit()
        
        # Alice 付 600，只有 Alice 和 Bob 分攤
        # 每人應付 300
        # Bob 欠 Alice 300
        expense4 = Expense(
            activity_id=activity_id,
            payer_id=alice.user_id,
            amount=600,
            description='住宿',
            category='accommodation',
            split_type='selected',
            is_split=True,
            split_participants=json.dumps([alice.user_id, bob.user_id])
        )
        db.session.add(expense4)
        db.session.commit()
        
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 驗證總金額
        assert data['total_amount'] == 600.0
        
        # 驗證結算清單：只有 Bob 欠 Alice
        assert len(data['settlements']) == 1
        assert data['settlements'][0]['from_user_id'] == bob.user_id
        assert data['settlements'][0]['to_user_id'] == alice.user_id
        assert data['settlements'][0]['amount'] == 300.0
        
        # 場景4: 借款記錄
        # 清空之前的費用
        Expense.query.filter_by(activity_id=activity_id).delete()
        db.session.commit()
        
        # Alice 借給 Bob 500
        expense5 = Expense(
            activity_id=activity_id,
            payer_id=alice.user_id,
            amount=500,
            description='借款',
            category='other',
            split_type='borrow',
            is_split=False,
            borrower_id=bob.user_id
        )
        db.session.add(expense5)
        db.session.commit()
        
        response = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 借款不計入 total_amount
        assert data['total_amount'] == 0.0
        
        # 驗證結算清單：Bob 欠 Alice 500
        assert len(data['settlements']) == 1
        assert data['settlements'][0]['from_user_id'] == bob.user_id
        assert data['settlements'][0]['to_user_id'] == alice.user_id
        assert data['settlements'][0]['amount'] == 500.0
