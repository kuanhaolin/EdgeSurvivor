"""
TC_2_6_2: 刪除後重新計算分攤
測試說明: 測試刪除費用後重新計算每人應付
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.expense import Expense
from models.activity_participant import ActivityParticipant
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_recalculate_after_delete(client, test_app):
    """測試刪除費用後重新計算分攤"""
    with test_app.app_context():
        # 創建創建者和參與者
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        participant = User(name='participant', email='participant@test.com', password_hash='hash')
        db.session.add_all([creator, participant])
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
        db.session.flush()
        
        # 添加參與者
        creator_part = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='joined',
            role='creator'
        )
        participant_part = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=participant.user_id,
            status='approved',
            role='participant'
        )
        db.session.add_all([creator_part, participant_part])
        db.session.commit()
        
        # 創建者新增費用（2人平分100元，每人50元）
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=100.0,
            description='測試費用',
            split_type='equal'
        )
        db.session.add(expense)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        activity_id = activity.activity_id
        expense_id = expense.expense_id
        
        # 查看刪除前的結算
        response_before = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        assert response_before.status_code == 200
        
        # 刪除費用
        response_delete = client.delete(
            f'/api/expenses/{expense_id}',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        assert response_delete.status_code == 200
        
        # 查看刪除後的結算（應該沒有欠款）
        response_after = client.get(
            f'/api/activities/{activity_id}/expenses/settlement',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response_after.status_code == 200
        data = json.loads(response_after.data)
        
        # 驗證刪除後沒有費用或結算為0
        if 'settlements' in data:
            assert len(data['settlements']) == 0 or all(s['amount'] == 0 for s in data['settlements'])
