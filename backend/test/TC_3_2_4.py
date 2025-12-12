"""
TC_3.2.4: 更新交友名單
測試說明: 測試推薦交友名單的更新邏輯
  - 已發送請求的用戶 → 不顯示
  - 已配對的用戶 → 不顯示
  - 被拒絕的用戶 → 重新顯示在名單上
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
                User(user_id=2, name='User2', email='user2@test.com', is_active=True),  # pending - 不顯示
                User(user_id=3, name='User3', email='user3@test.com', is_active=True),  # accepted - 不顯示
                User(user_id=4, name='User4', email='user4@test.com', is_active=True),  # rejected - 顯示
                User(user_id=5, name='User5', email='user5@test.com', is_active=True),  # 無關係 - 顯示
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # User1 的配對狀態
            matches = [
                Match(user_a=1, user_b=2, status='pending'),   # 已發送請求 - 排除
                Match(user_a=1, user_b=3, status='accepted'),  # 已配對 - 排除
                Match(user_a=1, user_b=4, status='rejected'),  # 被拒絕 - 應顯示
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


def test_friend_list_updates_correctly(client, auth_headers):
    """測試交友名單更新邏輯"""
    response = client.get('/api/matches/recommended', headers=auth_headers)
    
    assert response.status_code == 200
    matches = response.json['matches']
    user_ids = [m['user_id'] for m in matches]
    
    # 驗證：不包含自己
    assert 1 not in user_ids
    
    # 驗證：不包含已發送請求的 User2 (pending)
    assert 2 not in user_ids, "pending 狀態不應顯示"
    
    # 驗證：不包含已配對的 User3 (accepted)
    assert 3 not in user_ids, "accepted 狀態不應顯示"
    
    # 驗證：包含被拒絕的 User4 (rejected) - 重新顯示
    assert 4 in user_ids, "rejected 狀態應重新顯示"
    
    # 驗證：包含無關係的 User5
    assert 5 in user_ids, "無關係用戶應顯示"
