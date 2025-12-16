"""
TC_3.5.3: 更新好友名單
測試說明: 測試刪除的好友是否還在名單
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_friend_list_updated_after_deletion(client, test_app):
    """測試刪除好友後名單更新"""
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
        
        # 創建兩個好友關係
        match1 = Match(
            user_a=user01.user_id,
            user_b=user02.user_id,
            status='accepted',
            match_date=datetime.utcnow()
        )
        match2 = Match(
            user_a=user01.user_id,
            user_b=user03.user_id,
            status='accepted',
            match_date=datetime.utcnow()
        )
        db.session.add_all([match1, match2])
        db.session.commit()
        
        match1_id = match1.match_id
        
        # 查詢初始好友列表（user01 的好友）
        initial_friends = Match.query.filter(
            ((Match.user_a == user01.user_id) | (Match.user_b == user01.user_id)),
            Match.status == 'accepted'
        ).all()
        
        assert len(initial_friends) == 2
        
        # user01 刪除 user02
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.delete(
            f'/api/matches/{match1_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        
        # 重新查詢好友列表
        updated_friends = Match.query.filter(
            ((Match.user_a == user01.user_id) | (Match.user_b == user01.user_id)),
            Match.status == 'accepted'
        ).all()
        
        # 驗證好友列表已更新（只剩 1 個好友）
        assert len(updated_friends) == 1
        assert updated_friends[0].match_id == match2.match_id
        
        # 驗證 user02 不在好友列表中
        remaining_friend_ids = []
        for match in updated_friends:
            if match.user_a == user01.user_id:
                remaining_friend_ids.append(match.user_b)
            else:
                remaining_friend_ids.append(match.user_a)
        
        assert user02.user_id not in remaining_friend_ids
        assert user03.user_id in remaining_friend_ids
