"""
TC_3.4.1: 發送訊息給用戶
測試說明: 測試發送訊息給任何用戶是否成功
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.chat_message import ChatMessage
from datetime import datetime


def test_send_message_success(client, test_app):
    """測試成功發送訊息"""
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
        
        # user01 發送訊息給 user02
        token = create_access_token(identity=str(user01.user_id))
        
        message_data = {
            'receiver_id': user02.user_id,
            'content': '你好，希望能成為旅伴！',
            'message_type': 'text'
        }
        
        response = client.post(
            '/api/chat/messages',
            headers={'Authorization': f'Bearer {token}'},
            json=message_data
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['message']['sender_id'] == user01.user_id
        assert data['message']['receiver_id'] == user02.user_id
        assert data['message']['content'] == '你好，希望能成為旅伴！'
        assert data['message']['message_type'] == 'text'
        
        # 驗證資料庫中已儲存訊息
        message = ChatMessage.query.filter_by(
            sender_id=user01.user_id,
            receiver_id=user02.user_id
        ).first()
        assert message is not None
        assert message.content == '你好，希望能成為旅伴！'
