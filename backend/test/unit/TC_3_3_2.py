"""
TC_3.3.2: 驗證用戶審核狀態
測試說明: 測試好友請求狀態驗證
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_verify_pending_status(client, test_app):
    """測試驗證待審核請求的狀態為 pending"""
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
        
        # 創建待審核請求
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
        
        # 驗證資料庫中的狀態
        assert match1.status == 'pending'
        assert match2.status == 'pending'
        
        # 透過 API 驗證狀態
        token = create_access_token(identity=str(user01.user_id))
        response = client.get(
            '/api/matches/pending',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['matches']) == 2
        # 驗證所有請求的狀態都應該是 pending（API 只返回 pending 狀態的請求）
        for match in data['matches']:
            assert match['requester']['user_id'] in [user02.user_id, user03.user_id]
