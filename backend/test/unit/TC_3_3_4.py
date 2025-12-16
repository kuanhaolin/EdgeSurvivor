"""
TC_3.3.4: 拒絕好友請求
測試說明: 測試拒絕好友邀請
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from datetime import datetime


def test_reject_match_success(client, test_app):
    """測試成功拒絕好友請求"""
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
        
        # user01 拒絕請求
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.put(
            f'/api/matches/{match_id}/reject',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == '已拒絕媒合請求'
        assert data['match']['status'] == 'rejected'
        
        # 驗證資料庫中的狀態已更新為 rejected
        updated_match = Match.query.get(match_id)
        assert updated_match.status == 'rejected'
