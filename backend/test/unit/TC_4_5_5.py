"""
TC_4.5.5: 刪除費用 (Backend)
測試說明: 測試用戶是否成功刪除費用
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

def test_expense_deletion_success(client, test_app):
    """驗證費用成功刪除"""
    with test_app.app_context():
        # 創建測試用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        payer = User(name='payer', email='payer@test.com', password_hash='hash')
        db.session.add_all([creator, payer])
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
            ActivityParticipant(activity_id=activity_id, user_id=payer.user_id, status='approved', role='participant')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建多筆費用
        expenses = [
            Expense(activity_id=activity_id, payer_id=payer.user_id, amount=500,
                   description='午餐', category='food', split_type='all', is_split=True),
            Expense(activity_id=activity_id, payer_id=creator.user_id, amount=300,
                   description='交通', category='transport', split_type='all', is_split=True),
            Expense(activity_id=activity_id, payer_id=payer.user_id, amount=200,
                   description='門票', category='ticket', split_type='all', is_split=True)
        ]
        db.session.add_all(expenses)
        db.session.commit()
        
        expense_ids = [e.expense_id for e in expenses]
        
        # 測試1: 刪除第一筆費用
        token = create_access_token(identity=str(payer.user_id))
        response = client.delete(
            f'/api/expenses/{expense_ids[0]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == '費用記錄已刪除'
        
        # 驗證資料庫中費用已刪除
        deleted = Expense.query.get(expense_ids[0])
        assert deleted is None
        
        # 測試2: 刪除第二筆費用
        token = create_access_token(identity=str(creator.user_id))
        response = client.delete(
            f'/api/expenses/{expense_ids[1]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 測試3: 驗證刪除後費用清單更新
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        # 應該只剩1筆費用
        assert len(data['expenses']) == 1
        assert data['expenses'][0]['expense_id'] == expense_ids[2]
        
        # 測試4: 刪除不存在的費用
        response = client.delete(
            f'/api/expenses/99999',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert '找不到費用記錄' in data['error']
        
        # 測試5: 刪除最後一筆費用
        response = client.delete(
            f'/api/expenses/{expense_ids[2]}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        
        # 驗證費用清單為空
        response = client.get(
            f'/api/activities/{activity_id}/expenses',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['expenses']) == 0
        assert data['summary']['total_amount'] == 0
