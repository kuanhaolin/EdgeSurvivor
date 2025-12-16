"""
TC_3.2.2: 發送好友請求
測試說明: 測試發送好友請求功能
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


def test_send_friend_request(client, auth_headers):
    """測試發送好友請求"""
    response = client.post('/api/matches',
        headers=auth_headers,
        json={'responder_id': 2, 'message': '想跟你一起旅行'}
    )
    
    assert response.status_code == 201
    assert '媒合請求已發送' in response.json['message']
    assert 'match' in response.json
    assert response.json['match']['status'] == 'pending'
