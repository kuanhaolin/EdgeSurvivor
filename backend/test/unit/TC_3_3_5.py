"""
TC_3.3.5: 建立雙向好友關係
測試說明: 測試批准後建立雙向好友關係
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_bidirectional_friendship(client, test_app):
    """測試批准後建立雙向好友關係"""
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
        db.session.add_all([user01, user02])
        db.session.commit()
        
        # user02 發送請求給 user01
        match = Match(
            user_a=user02.user_id,
            user_b=user01.user_id,
            status='pending',
            message='希望能成為旅伴',
            match_date=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        match_id = match.match_id
        
        # user01 接受請求
        token01 = create_access_token(identity=str(user01.user_id))
        response = client.put(
            f'/api/matches/{match_id}/accept',
            headers={'Authorization': f'Bearer {token01}'}
        )
        
        assert response.status_code == 200
        assert Match.query.get(match_id).status == 'accepted'
        
        # 驗證 user01 可以看到 user02 在好友列表中
        response01 = client.get(
            '/api/matches?status=accepted',
            headers={'Authorization': f'Bearer {token01}'}
        )
        assert response01.status_code == 200
        data01 = json.loads(response01.data)
        assert len(data01['matches']) == 1
        assert data01['matches'][0]['requester']['user_id'] == user02.user_id
        
        # 驗證 user02 也可以看到 user01 在好友列表中
        token02 = create_access_token(identity=str(user02.user_id))
        response02 = client.get(
            '/api/matches?status=accepted',
            headers={'Authorization': f'Bearer {token02}'}
        )
        assert response02.status_code == 200
        data02 = json.loads(response02.data)
        assert len(data02['matches']) == 1
        assert data02['matches'][0]['responder']['user_id'] == user01.user_id
