"""
TC_5_2_1: 成功獲取活動費用清單
測試說明: 驗證活動參與者可以成功獲取費用清單及摘要資訊
"""
import pytest
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.expense import Expense
from flask_jwt_extended import create_access_token


@pytest.fixture
def client():
    """建立測試客戶端"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_get_expense_list_success(client):
    """測試成功獲取費用清單"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        participant1 = User(name='Participant1', email='p1@test.com', gender='female', age=23)
        participant1.set_password('password123')
        participant2 = User(name='Participant2', email='p2@test.com', gender='male', age=27)
        participant2.set_password('password123')
        
        db.session.add_all([creator, participant1, participant2])
        db.session.commit()
        
        # 創建測試活動
        activity = Activity(
            title='測試活動',
            description='測試用活動',
            category='travel',
            location='台北',
            date=datetime.utcnow().date(),
            start_date=datetime.utcnow().date(),
            end_date=(datetime.utcnow() + timedelta(days=2)).date(),
            creator_id=creator.user_id,
            max_participants=5
        )
        db.session.add(activity)
        db.session.commit()
        
        # 添加參與者
        participants = [
            ActivityParticipant(activity_id=activity.activity_id, user_id=creator.user_id, status='approved'),
            ActivityParticipant(activity_id=activity.activity_id, user_id=participant1.user_id, status='approved'),
            ActivityParticipant(activity_id=activity.activity_id, user_id=participant2.user_id, status='approved')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建測試費用記錄
        import json
        expense1 = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=300,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, participant1.user_id, participant2.user_id])
        )
        expense2 = Expense(
            activity_id=activity.activity_id,
            payer_id=participant1.user_id,
            amount=600,
            description='午餐費',
            category='food',
            split_type='selected',
            split_method='equal',
            split_participants=json.dumps([participant1.user_id, participant2.user_id])
        )
        expense3 = Expense(
            activity_id=activity.activity_id,
            payer_id=participant2.user_id,
            amount=200,
            description='借款',
            category='other',
            split_type='borrow',
            borrower_id=creator.user_id
        )
        db.session.add_all([expense1, expense2, expense3])
        db.session.commit()
        
        # 生成 JWT token
        token = create_access_token(identity=str(creator.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送請求
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        
        # 驗證回應
        assert response.status_code == 200
        data = response.json
        
        # 驗證費用列表
        assert 'expenses' in data
        assert len(data['expenses']) == 3
        
        # 驗證第一筆費用資料結構
        expense = data['expenses'][0]
        assert 'expense_id' in expense
        assert 'payer' in expense
        assert 'description' in expense
        assert 'amount' in expense
        assert 'category' in expense
        assert 'split_type' in expense
        assert 'created_at' in expense
        
        # 驗證支付者資訊
        assert expense['payer']['name'] is not None
        
        # 驗證摘要資訊
        assert 'summary' in data
        assert 'total_amount' in data['summary']
        assert 'participant_count' in data['summary']
        assert 'per_person' in data['summary']
        
        # 驗證摘要計算（只計算 split_type='all' 的費用）
        assert data['summary']['total_amount'] == 300
        assert data['summary']['participant_count'] == 3
        assert data['summary']['per_person'] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])