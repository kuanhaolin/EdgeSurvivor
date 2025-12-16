"""
TC_5_5: 刪除費用記錄測試
測試說明: 驗證費用刪除功能的權限控制、錯誤處理和數據更新
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


def test_delete_expense_by_payer_success(client):
    """TC_5_5_1: 測試代墊人成功刪除費用"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        payer = User(name='Payer', email='payer@test.com', gender='female', age=23)
        payer.set_password('password123')
        
        db.session.add_all([creator, payer])
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
            ActivityParticipant(activity_id=activity.activity_id, user_id=payer.user_id, status='approved')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建測試費用記錄
        import json
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=payer.user_id,
            amount=300,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, payer.user_id])
        )
        db.session.add(expense)
        db.session.commit()
        
        expense_id = expense.expense_id
        
        # 生成代墊人的 JWT token
        token = create_access_token(identity=str(payer.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送刪除請求
        response = client.delete(f'/api/expenses/{expense_id}', headers=headers)
        
        # 驗證回應
        assert response.status_code == 200
        data = response.json
        assert '已刪除' in data['message']
        
        # 驗證費用記錄已被刪除
        deleted_expense = Expense.query.get(expense_id)
        assert deleted_expense is None


def test_delete_expense_by_creator_success(client):
    """TC_5_5_2: 測試活動創建者成功刪除費用"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        payer = User(name='Payer', email='payer@test.com', gender='female', age=23)
        payer.set_password('password123')
        
        db.session.add_all([creator, payer])
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
            ActivityParticipant(activity_id=activity.activity_id, user_id=payer.user_id, status='approved')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建測試費用記錄（由非創建者代墊）
        import json
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=payer.user_id,
            amount=500,
            description='午餐費',
            category='food',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, payer.user_id])
        )
        db.session.add(expense)
        db.session.commit()
        
        expense_id = expense.expense_id
        
        # 生成活動創建者的 JWT token
        token = create_access_token(identity=str(creator.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送刪除請求
        response = client.delete(f'/api/expenses/{expense_id}', headers=headers)
        
        # 驗證回應
        assert response.status_code == 200
        data = response.json
        assert '已刪除' in data['message']
        
        # 驗證費用記錄已被刪除
        deleted_expense = Expense.query.get(expense_id)
        assert deleted_expense is None


def test_delete_expense_unauthorized(client):
    """TC_5_5_3: 測試無權限刪除費用（非代墊人也非創建者）"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        payer = User(name='Payer', email='payer@test.com', gender='female', age=23)
        payer.set_password('password123')
        other_user = User(name='Other', email='other@test.com', gender='male', age=24)
        other_user.set_password('password123')
        
        db.session.add_all([creator, payer, other_user])
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
            ActivityParticipant(activity_id=activity.activity_id, user_id=payer.user_id, status='approved'),
            ActivityParticipant(activity_id=activity.activity_id, user_id=other_user.user_id, status='approved')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建測試費用記錄
        import json
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=payer.user_id,
            amount=300,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, payer.user_id, other_user.user_id])
        )
        db.session.add(expense)
        db.session.commit()
        
        expense_id = expense.expense_id
        
        # 生成其他用戶的 JWT token
        token = create_access_token(identity=str(other_user.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送刪除請求
        response = client.delete(f'/api/expenses/{expense_id}', headers=headers)
        
        # 驗證回應
        assert response.status_code == 403
        data = response.json
        assert '無權限' in data['error']
        
        # 驗證費用記錄仍然存在
        existing_expense = Expense.query.get(expense_id)
        assert existing_expense is not None


def test_delete_expense_no_auth(client):
    """TC_5_5_4: 測試未登入用戶無法刪除費用"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        
        db.session.add(creator)
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
        
        # 創建測試費用記錄
        import json
        expense = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=300,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id])
        )
        db.session.add(expense)
        db.session.commit()
        
        expense_id = expense.expense_id
        
        # 發送刪除請求（不帶 token）
        response = client.delete(f'/api/expenses/{expense_id}')
        
        # 驗證回應
        assert response.status_code == 401
        
        # 驗證費用記錄仍然存在
        existing_expense = Expense.query.get(expense_id)
        assert existing_expense is not None


def test_delete_expense_not_found(client):
    """TC_5_5_5: 測試刪除不存在的費用返回 404"""
    with client.application.app_context():
        # 創建測試用戶
        user = User(name='User', email='user@test.com', gender='male', age=25)
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        # 生成 JWT token
        token = create_access_token(identity=str(user.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送刪除請求（不存在的費用 ID）
        response = client.delete('/api/expenses/99999', headers=headers)
        
        # 驗證回應
        assert response.status_code == 404
        data = response.json
        assert '找不到' in data['error']


def test_delete_expense_updates_list(client):
    """TC_5_5_6: 測試刪除後費用清單正確更新"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        
        db.session.add(creator)
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
        participant = ActivityParticipant(
            activity_id=activity.activity_id, 
            user_id=creator.user_id, 
            status='approved'
        )
        db.session.add(participant)
        db.session.commit()
        
        # 創建多筆測試費用記錄
        import json
        expense1 = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=300,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id])
        )
        expense2 = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=500,
            description='午餐費',
            category='food',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id])
        )
        db.session.add_all([expense1, expense2])
        db.session.commit()
        
        expense1_id = expense1.expense_id
        
        # 生成 JWT token
        token = create_access_token(identity=str(creator.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 獲取刪除前的費用清單
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        assert response.status_code == 200
        before_count = len(response.json['expenses'])
        assert before_count == 2
        
        # 刪除第一筆費用
        response = client.delete(f'/api/expenses/{expense1_id}', headers=headers)
        assert response.status_code == 200
        
        # 獲取刪除後的費用清單
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        assert response.status_code == 200
        after_count = len(response.json['expenses'])
        assert after_count == 1
        
        # 驗證剩下的費用是正確的
        remaining_expense = response.json['expenses'][0]
        assert remaining_expense['description'] == '午餐費'
        assert remaining_expense['amount'] == 500


def test_delete_expense_updates_summary(client):
    """TC_5_5_7: 測試刪除後費用統計數據正確更新"""
    with client.application.app_context():
        # 創建測試用戶
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        participant = User(name='Participant', email='p1@test.com', gender='female', age=23)
        participant.set_password('password123')
        
        db.session.add_all([creator, participant])
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
            ActivityParticipant(activity_id=activity.activity_id, user_id=participant.user_id, status='approved')
        ]
        db.session.add_all(participants)
        db.session.commit()
        
        # 創建測試費用記錄（全體分攤）
        import json
        expense1 = Expense(
            activity_id=activity.activity_id,
            payer_id=creator.user_id,
            amount=600,
            description='交通費',
            category='transport',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, participant.user_id])
        )
        expense2 = Expense(
            activity_id=activity.activity_id,
            payer_id=participant.user_id,
            amount=400,
            description='午餐費',
            category='food',
            split_type='all',
            split_method='equal',
            split_participants=json.dumps([creator.user_id, participant.user_id])
        )
        db.session.add_all([expense1, expense2])
        db.session.commit()
        
        expense1_id = expense1.expense_id
        
        # 生成 JWT token
        token = create_access_token(identity=str(creator.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 獲取刪除前的費用摘要
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        assert response.status_code == 200
        before_summary = response.json['summary']
        assert before_summary['total_amount'] == 1000  # 600 + 400
        assert before_summary['participant_count'] == 2
        assert before_summary['per_person'] == 500  # 1000 / 2
        
        # 刪除第一筆費用
        response = client.delete(f'/api/expenses/{expense1_id}', headers=headers)
        assert response.status_code == 200
        
        # 獲取刪除後的費用摘要
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        assert response.status_code == 200
        after_summary = response.json['summary']
        assert after_summary['total_amount'] == 400  # 只剩 400
        assert after_summary['participant_count'] == 2
        assert after_summary['per_person'] == 200  # 400 / 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

