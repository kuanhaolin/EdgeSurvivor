"""
TC_3.4.4: 更新聊天室
測試說明: 測試訊息是否會在介面同步更新
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage
from datetime import datetime


def test_chat_room_update(client, test_app):
    """測試聊天室訊息同步更新"""
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
        
        # 創建媒合關係
        match = Match(
            user_a=user01.user_id,
            user_b=user02.user_id,
            status='accepted',
            match_date=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        # user01 發送第一條訊息
        token1 = create_access_token(identity=str(user01.user_id))
        
        response1 = client.post(
            '/api/chat/messages',
            headers={'Authorization': f'Bearer {token1}'},
            json={
                'receiver_id': user02.user_id,
                'content': '第一條訊息',
                'message_type': 'text'
            }
        )
        assert response1.status_code == 201
        
        # user02 查詢訊息列表（應該看到 user01 的訊息）
        token2 = create_access_token(identity=str(user02.user_id))
        
        response2 = client.get(
            f'/api/chat/{user01.user_id}/messages',
            headers={'Authorization': f'Bearer {token2}'}
        )
        
        assert response2.status_code == 200
        data = json.loads(response2.data)
        assert len(data['messages']) == 1
        assert data['messages'][0]['content'] == '第一條訊息'
        assert data['messages'][0]['sender_id'] == user01.user_id
        
        # user02 發送回覆
        response3 = client.post(
            '/api/chat/messages',
            headers={'Authorization': f'Bearer {token2}'},
            json={
                'receiver_id': user01.user_id,
                'content': '回覆訊息',
                'message_type': 'text'
            }
        )
        assert response3.status_code == 201
        
        # user01 查詢更新後的訊息列表（應該看到兩條訊息）
        response4 = client.get(
            f'/api/chat/{user02.user_id}/messages',
            headers={'Authorization': f'Bearer {token1}'}
        )
        
        assert response4.status_code == 200
        data2 = json.loads(response4.data)
        assert len(data2['messages']) == 2
        assert data2['messages'][0]['content'] == '第一條訊息'
        assert data2['messages'][1]['content'] == '回覆訊息'
