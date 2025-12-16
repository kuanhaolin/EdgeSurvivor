"""
TC_3.3.1: 查看待審核邀請
測試說明: 測試查看收到的好友請求名單
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_get_pending_matches(client, test_app):
    """測試取得待審核的好友請求列表"""
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
            message='希望能成為旅伴！',
            match_date=datetime.utcnow()
        )
        match2 = Match(
            user_a=user03.user_id,
            user_b=user01.user_id,
            status='pending',
            message='一起去旅遊吧',
            match_date=datetime.utcnow()
        )
        db.session.add_all([match1, match2])
        db.session.commit()
        
        # 測試 user01 的待審核列表（應有 2 筆）
        token = create_access_token(identity=str(user01.user_id))
        response = client.get(
            '/api/matches/pending',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'matches' in data
        assert len(data['matches']) == 2
        assert data['matches'][0]['requester']['name'] in ['user02', 'user03']
        assert data['matches'][1]['requester']['name'] in ['user02', 'user03']
        
        # 測試 user02 的待審核列表（應為空）
        token2 = create_access_token(identity=str(user02.user_id))
        response2 = client.get(
            '/api/matches/pending',
            headers={'Authorization': f'Bearer {token2}'}
        )
        
        assert response2.status_code == 200
        data2 = json.loads(response2.data)
        assert len(data2['matches']) == 0
