"""
TC_3.5.2: 刪除好友
測試說明: 測試刪除好友是否成功
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_delete_friend_success(client, test_app):
    """測試成功刪除好友"""
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
        
        # 創建好友關係
        match = Match(
            user_a=user01.user_id,
            user_b=user02.user_id,
            status='accepted',
            match_date=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        match_id = match.match_id
        
        # user01 刪除好友
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.delete(
            f'/api/matches/{match_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert '已刪除好友關係' in data['message']
        
        # 驗證好友關係已被刪除
        deleted_match = Match.query.get(match_id)
        assert deleted_match is None
