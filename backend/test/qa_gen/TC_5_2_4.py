"""
TC_5_2_4: 空費用清單測試
測試說明: 驗證活動沒有費用記錄時正確返回空清單
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


def test_get_empty_expense_list(client):
    """測試獲取空費用清單"""
    with client.application.app_context():
        # 創建測試用戶
        user = User(name='TestUser', email='test@test.com', gender='male', age=25)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # 創建測試活動（沒有費用記錄）
        activity = Activity(
            title='無費用活動',
            description='這個活動還沒有任何費用記錄',
            category='travel',
            location='台北',
            date=datetime.utcnow().date(),
            start_date=datetime.utcnow().date(),
            end_date=(datetime.utcnow() + timedelta(days=1)).date(),
            creator_id=user.user_id,
            max_participants=5
        )
        db.session.add(activity)
        db.session.commit()
        
        # 添加用戶為參與者
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=user.user_id,
            status='approved'
        )
        db.session.add(participant)
        db.session.commit()
        
        # 生成 JWT token
        token = create_access_token(identity=str(user.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 發送請求
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        
        # 驗證回應
        assert response.status_code == 200
        data = response.json
        
        # 驗證費用列表為空
        assert 'expenses' in data
        assert isinstance(data['expenses'], list)
        assert len(data['expenses']) == 0
        
        # 驗證摘要資訊存在且為零
        assert 'summary' in data
        assert data['summary']['total_amount'] == 0
        assert data['summary']['participant_count'] == 1
        assert data['summary']['per_person'] == 0


def test_get_expense_list_activity_not_found(client):
    """測試活動不存在時返回 404"""
    with client.application.app_context():
        # 創建測試用戶
        user = User(name='TestUser', email='test@test.com', gender='male', age=25)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # 生成 JWT token
        token = create_access_token(identity=str(user.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 嘗試訪問不存在的活動
        non_existent_activity_id = 99999
        response = client.get(f'/api/activities/{non_existent_activity_id}/expenses', headers=headers)
        
        # 驗證回應 - 應該返回 404 Not Found
        assert response.status_code == 404
        data = response.json
        assert 'error' in data
        assert '找不到活動' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])