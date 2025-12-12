"""
TC_3.5.1: 驗證好友狀態
測試說明: 測試是否為好友狀態
"""
import pytest
from flask import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_verify_friend_status(client, test_app):
    """測試驗證是好友狀態"""
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
        
        # 創建好友關係（user01 和 user02 是好友）
        match = Match(
            user_a=user01.user_id,
            user_b=user02.user_id,
            status='accepted',
            match_date=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        # 驗證 user01 和 user02 是好友（status='accepted'）
        friend_match = Match.query.filter(
            ((Match.user_a == user01.user_id) & (Match.user_b == user02.user_id)) |
            ((Match.user_a == user02.user_id) & (Match.user_b == user01.user_id)),
            Match.status == 'accepted'
        ).first()
        
        assert friend_match is not None
        assert friend_match.status == 'accepted'
        assert friend_match.user_a == user01.user_id
        assert friend_match.user_b == user02.user_id
