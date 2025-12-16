"""
TC_3.2.1: 驗證好友請求狀態
測試說明: 測試驗證請求狀態（已發送、已是好友 = 不可再發送）
測試資料:
  - User1 已發送請求給 User2 (pending) - 不可再發送
  - User1 已是 User3 的好友 (accepted) - 不可再發送
  - User1 未與 User4 有任何關係 - 可發送
結果: 正確驗證請求狀態
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.match import Match


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
            
            # 創建測試用戶
            users = [
                User(user_id=1, name='User1', email='user1@test.com', is_active=True),
                User(user_id=2, name='User2', email='user2@test.com', is_active=True),
                User(user_id=3, name='User3', email='user3@test.com', is_active=True),
                User(user_id=4, name='User4', email='user4@test.com', is_active=True),
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # User1 已發送請求給 User2 (pending)
            match1 = Match(user_a=1, user_b=2, status='pending')
            db.session.add(match1)
            
            # User1 已是 User3 的好友 (accepted)
            match2 = Match(user_a=1, user_b=3, status='accepted')
            db.session.add(match2)
            
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def auth_headers(client):
    """取得 User1 的認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'user1@test.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_validate_friend_request_status(client, auth_headers):
    """測試驗證好友請求狀態"""
    
    # 1. 不可再發送：已有 pending 請求
    response = client.post('/api/matches', 
        headers=auth_headers,
        json={'responder_id': 2}
    )
    assert response.status_code == 400
    assert '已發送過交友請求' in response.json['error']
    
    # 2. 不可再發送：已經是好友
    response = client.post('/api/matches',
        headers=auth_headers,
        json={'responder_id': 3}
    )
    assert response.status_code == 400
    assert '已經是好友' in response.json['error']
    
    # 3. 可以發送：無任何關係
    response = client.post('/api/matches',
        headers=auth_headers,
        json={'responder_id': 4}
    )
    assert response.status_code == 201
    assert '媒合請求已發送' in response.json['message']
