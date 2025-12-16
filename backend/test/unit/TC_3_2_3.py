"""
TC_3.2.3: 取消好友邀請
測試說明: 測試取消已發送的 pending 請求
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
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            users = [
                User(user_id=1, name='User1', email='user1@test.com', is_active=True),
                User(user_id=2, name='User2', email='user2@test.com', is_active=True),
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # User1 發送 pending 請求給 User2
            match = Match(user_a=1, user_b=2, status='pending')
            db.session.add(match)
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def auth_headers(client):
    response = client.post('/api/auth/login', json={
        'email': 'user1@test.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_cancel_pending_request(client, auth_headers):
    """測試取消已發送的 pending 請求"""
    # 先獲取已發送的請求
    response = client.get('/api/matches/sent', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['matches']) == 1
    
    match_id = response.json['matches'][0]['match_id']
    
    # 取消請求
    response = client.delete(f'/api/matches/{match_id}', headers=auth_headers)
    
    assert response.status_code == 200
    assert '已取消媒合請求' in response.json['message']
    
    # 驗證已刪除
    response = client.get('/api/matches/sent', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['matches']) == 0
