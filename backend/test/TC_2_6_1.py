"""
TC_2_6_1: 創建者刪除任何費用項目
測試說明: 測試創建者可以刪除任何費用項目
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.expense import Expense
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_creator_can_delete_any_expense(client, test_app):
    """測試創建者可以刪除任何人的費用項目"""
    with test_app.app_context():
        # 創建創建者和其他用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        other_user = User(name='other', email='other@test.com', password_hash='hash')
        db.session.add_all([creator, other_user])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 其他用戶新增費用
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=other_user.user_id,
            amount=100.0,
            description='測試費用',
            split_type='equal'
        )
        db.session.add(expense)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        expense_id = expense.expense_id
        
        # 創建者刪除其他用戶的費用
        response = client.delete(
            f'/api/expenses/{expense_id}',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert '已刪除' in data['message'] or 'deleted' in data['message'].lower()
