"""
TC_3.2.6: 更新已發送狀態
測試說明: 測試已發送名單的更新邏輯，取消請求後不會留存紀錄
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
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # User1 發送兩個 pending 請求
            matches = [
                Match(user_a=1, user_b=2, status='pending'),
                Match(user_a=1, user_b=3, status='pending'),
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


def test_update_sent_list_after_cancel(client, auth_headers):
    """測試取消請求後已發送名單會更新（不留存紀錄）"""
    
    # 1. 查看初始已發送名單（應有 2 個）
    response = client.get('/api/matches/sent', headers=auth_headers)
    assert response.status_code == 200
    initial_matches = response.json['matches']
    assert len(initial_matches) == 2
    
    # 2. 取消第一個請求
    first_match_id = initial_matches[0]['match_id']
    response = client.delete(f'/api/matches/{first_match_id}', headers=auth_headers)
    assert response.status_code == 200
    assert '已取消媒合請求' in response.json['message']
    
    # 3. 驗證已發送名單更新（只剩 1 個）
    response = client.get('/api/matches/sent', headers=auth_headers)
    assert response.status_code == 200
    updated_matches = response.json['matches']
    assert len(updated_matches) == 1
    
    # 4. 驗證被取消的請求不在名單中
    remaining_ids = [m['match_id'] for m in updated_matches]
    assert first_match_id not in remaining_ids
    
    # 5. 取消第二個請求
    second_match_id = updated_matches[0]['match_id']
    response = client.delete(f'/api/matches/{second_match_id}', headers=auth_headers)
    assert response.status_code == 200
    
    # 6. 驗證已發送名單為空（所有紀錄都已刪除）
    response = client.get('/api/matches/sent', headers=auth_headers)
    assert response.status_code == 200
    final_matches = response.json['matches']
    assert len(final_matches) == 0
