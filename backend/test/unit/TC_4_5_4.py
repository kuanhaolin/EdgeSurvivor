"""
TC_4.5.4: 驗證費用的編輯權 (Backend)
測試說明: 測試費用明細的編輯權，驗證自己新增的資訊
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

def test_expense_edit_permission(client, test_app):
    """驗證費用編輯權限（透過刪除功能測試）"""
    with test_app.app_context():
        # 創建測試用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        payer = User(name='payer', email='payer@test.com', password_hash='hash')
        other_user = User(name='other', email='other@test.com', password_hash='hash')
        db.session.add_all([creator, payer, other_user])
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
            ActivityParticipant(activity_id=activity_id, user_id=payer.user_id, status='approved', role='participant'),
            ActivityParticipant(activity_id=activity_id, user_id=other_user.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # payer 新增費用
        expense_by_payer = Expense(
            activity_id=activity_id,
            payer_id=payer.user_id,
            amount=500,
            description='午餐',
            category='food',
            split_type='all',
            is_split=True
        )
        db.session.add(expense_by_payer)
        db.session.commit()
        expense_id = expense_by_payer.expense_id
        
        # 測試1: 費用新增者（payer）有編輯權
        token = create_access_token(identity=str(payer.user_id))
        # 驗證可以查看費用清單
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 1
        assert data['expenses'][0]['payer_id'] == payer.user_id
        
        # 驗證可以刪除自己的費用（編輯權的一種體現）
        response = client.delete(
            f'/api/expenses/{expense_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 創建另一筆費用
        expense_by_creator = Expense(
            activity_id=activity_id,
            payer_id=creator.user_id,
            amount=300,
            description='交通',
            category='transport',
            split_type='all',
            is_split=True
        )
        db.session.add(expense_by_creator)
        db.session.commit()
        expense2_id = expense_by_creator.expense_id
        
        # 測試2: 活動創建者對所有費用有編輯權
        token = create_access_token(identity=str(creator.user_id))
        response = client.delete(
            f'/api/expenses/{expense2_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 創建第三筆費用
        expense3 = Expense(
            activity_id=activity_id,
            payer_id=payer.user_id,
            amount=200,
            description='門票',
            category='ticket',
            split_type='all',
            is_split=True
        )
        db.session.add(expense3)
        db.session.commit()
        expense3_id = expense3.expense_id
        
        # 測試3: 其他參與者對他人費用沒有編輯權
        token = create_access_token(identity=str(other_user.user_id))
        response = client.delete(
            f'/api/expenses/{expense3_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 403
        data = json.loads(response.data)
        assert '無權限' in data['error']
        
        # 驗證費用未被刪除
        existing = Expense.query.get(expense3_id)
        assert existing is not None
