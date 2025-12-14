"""
TC_3.1.8: 排除自己與好友名單
測試說明: 測試推薦配對列表是否正確排除自己、已配對用戶、待處理配對
測試資料:
  - 登入用戶: user1
  - 其他用戶: user2(已配對), user3(待處理), user4(正常), user5(正常)
結果: 推薦列表只包含 user4 和 user5
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
                User(user_id=1, name='User1', email='user1@test.com', gender='male', age=25, is_active=True),
                User(user_id=2, name='User2', email='user2@test.com', gender='female', age=26, is_active=True),
                User(user_id=3, name='User3', email='user3@test.com', gender='female', age=27, is_active=True),
                User(user_id=4, name='User4', email='user4@test.com', gender='male', age=28, is_active=True),
                User(user_id=5, name='User5', email='user5@test.com', gender='female', age=29, is_active=True),
            ]
            
            for user in users:
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            
            # 創建配對關係
            # User1 已配對 User2 (accepted)
            match1 = Match(user_a=1, user_b=2, status='accepted')
            db.session.add(match1)
            
            # User1 發送配對請求給 User3 (pending)
            match2 = Match(user_a=1, user_b=3, status='pending')
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


def test_exclude_self_and_friends_list(client, auth_headers):
    """測試排除交友名單：自己、已配對好友、待處理配對"""
    response = client.get('/api/matches/recommended', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'matches' in data
    
    matches = data['matches']
    user_ids = [match['user_id'] for match in matches]
    
    # 測試情境：
    # User1 (自己) - 排除
    # User2 (已配對好友 accepted) - 排除  
    # User3 (待處理配對 pending) - 排除
    # User4 (正常用戶) - 應出現
    # User5 (正常用戶) - 應出現
    
    excluded = [1, 2, 3]  # 排除：自己、好友、待處理
    included = [4, 5]     # 應出現：正常用戶
    
    for uid in excluded:
        assert uid not in user_ids, f"User{uid} 應被排除"
    
    for uid in included:
        assert uid in user_ids, f"User{uid} 應該出現"
    
    assert len(user_ids) == 2
