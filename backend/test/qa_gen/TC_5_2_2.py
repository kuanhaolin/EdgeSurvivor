"""
TC_5_2_2: 非參與者無權限測試
測試說明: 驗證非活動參與者無法查看費用清單
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


def test_get_expense_list_unauthorized(client):
    """測試非參與者無權限查看費用清單"""
    with client.application.app_context():
        # 創建活動創建者
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        
        # 創建非參與者
        outsider = User(name='Outsider', email='outsider@test.com', gender='female', age=23)
        outsider.set_password('password123')
        
        db.session.add_all([creator, outsider])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='私密活動',
            description='測試用私密活動',
            category='travel',
            location='台北',
            date=datetime.utcnow().date(),
            start_date=datetime.utcnow().date(),
            end_date=(datetime.utcnow() + timedelta(days=1)).date(),
            creator_id=creator.user_id,
            max_participants=5
        )
        db.session.add(activity)
        db.session.commit()
        
        # 只添加創建者為參與者
        participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=creator.user_id,
            status='approved'
        )
        db.session.add(participant)
        db.session.commit()
        
        # 使用非參與者的 token
        token = create_access_token(identity=str(outsider.user_id))
        headers = {'Authorization': f'Bearer {token}'}
        
        # 嘗試訪問費用清單
        response = client.get(f'/api/activities/{activity.activity_id}/expenses', headers=headers)
        
        # 驗證回應 - 應該返回 403 Forbidden
        assert response.status_code == 403
        data = response.json
        assert 'error' in data
        assert '只有活動參與者可以查看費用' in data['error']


def test_get_expense_list_no_auth(client):
    """測試未登入用戶無法查看費用清單"""
    with client.application.app_context():
        # 創建活動
        creator = User(name='Creator', email='creator@test.com', gender='male', age=25)
        creator.set_password('password123')
        db.session.add(creator)
        db.session.commit()
        
        activity = Activity(
            title='測試活動',
            description='測試用活動',
            category='travel',
            location='台北',
            date=datetime.utcnow().date(),
            start_date=datetime.utcnow().date(),
            end_date=datetime.utcnow().date(),
            creator_id=creator.user_id,
            max_participants=5
        )
        db.session.add(activity)
        db.session.commit()
        
        # 不提供 token 直接訪問
        response = client.get(f'/api/activities/{activity.activity_id}/expenses')
        
        # 驗證回應 - 應該返回 401 Unauthorized
        assert response.status_code == 401


if __name__ == '__main__':
    pytest.main([__file__, '-v'])