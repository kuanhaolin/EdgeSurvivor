"""
TC_3.3.7: 更新好友名單
測試說明: 測試批准後好友名單會更新
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_update_friends_list(client, test_app):
    """測試批准後好友名單會更新"""
    with test_app.app_context():
        # 創建測試用戶
        user01 = User(
            name='user01',
            email='user01@example.com',
            password_hash='hash1',
            gender='male',
            age=25
        )
        user02 = User(
            name='user02',
            email='user02@example.com',
            password_hash='hash2',
            gender='female',
            age=28
        )
        user03 = User(
            name='user03',
            email='user03@example.com',
            password_hash='hash3',
            gender='male',
            age=30
        )
        db.session.add_all([user01, user02, user03])
        db.session.commit()
        
        # user02 和 user03 發送請求給 user01
        match1 = Match(
            user_a=user02.user_id,
            user_b=user01.user_id,
            status='pending',
            message='請求1',
            match_date=datetime.utcnow()
        )
        match2 = Match(
            user_a=user03.user_id,
            user_b=user01.user_id,
            status='pending',
            message='請求2',
            match_date=datetime.utcnow()
        )
        db.session.add_all([match1, match2])
        db.session.commit()
        
        token = create_access_token(identity=str(user01.user_id))
        
        # 驗證好友名單為空
        response = client.get(
            '/api/matches?status=accepted',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['matches']) == 0
        
        # 接受 match1
        client.put(
            f'/api/matches/{match1.match_id}/accept',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # 驗證好友名單有 1 筆
        response = client.get(
            '/api/matches?status=accepted',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['matches']) == 1
        assert data['matches'][0]['requester']['user_id'] == user02.user_id
        
        # 接受 match2
        client.put(
            f'/api/matches/{match2.match_id}/accept',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # 驗證好友名單有 2 筆
        response = client.get(
            '/api/matches?status=accepted',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['matches']) == 2
        friend_ids = [m['requester']['user_id'] for m in data['matches']]
        assert user02.user_id in friend_ids
        assert user03.user_id in friend_ids
