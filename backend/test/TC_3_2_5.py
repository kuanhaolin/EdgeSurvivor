"""
TC_3.2.5: 查看已發送狀態
測試說明: 測試查看已發送請求的所有狀態（包含所有紀錄）
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
                User(user_id=3, name='User3', email='user3@test.com', is_active=True),
                User(user_id=4, name='User4', email='user4@test.com', is_active=True),
                User(user_id=5, name='User5', email='user5@test.com', is_active=True),
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # User1 發送的請求（不同狀態）
            matches = [
                Match(user_a=1, user_b=2, status='pending'),   # 待處理
                Match(user_a=1, user_b=3, status='pending'),   # 待處理
                Match(user_a=1, user_b=4, status='accepted'),  # 已接受
                Match(user_a=1, user_b=5, status='rejected'),  # 已拒絕
            ]
            
            for match in matches:
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


def test_view_all_sent_requests(client, auth_headers):
    """測試查看已發送請求的所有狀態（包含所有紀錄）"""
    response = client.get('/api/matches/sent', headers=auth_headers)
    
    assert response.status_code == 200
    all_matches = response.json['matches']
    
    # 驗證回傳所有紀錄（4個：pending x2, accepted x1, rejected x1）
    assert len(all_matches) == 4
    
    # 驗證包含所有狀態
    statuses = [m['status'] for m in all_matches]
    assert 'pending' in statuses
    assert 'accepted' in statuses
    assert 'rejected' in statuses
    
    # 驗證每個請求都有接收者資訊
    for match in all_matches:
        assert 'responder' in match
        assert 'user_id' in match['responder']
        assert 'name' in match['responder']