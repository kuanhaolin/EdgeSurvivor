"""
TC_3.4.3: 即時訊息傳遞
測試說明: 測試WebSocket即時傳遞訊息
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage
from datetime import datetime


def test_socketio_send_message(socketio_client, test_app):
    """測試透過 WebSocket 發送即時訊息"""
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
        
        # 生成 JWT token
        token = create_access_token(identity=str(user01.user_id))
        
        # 重新建立帶認證的 socketio_client
        from app import socketio
        authenticated_client = socketio.test_client(test_app, auth={'token': token})
        
        # 透過 WebSocket 發送訊息
        authenticated_client.emit('send_message', {
            'match_id': match.match_id,
            'sender_id': user01.user_id,
            'content': 'WebSocket 即時訊息測試',
            'message_type': 'text'
        })
        
        # 等待訊息處理
        received = authenticated_client.get_received()
        
        # 驗證訊息被儲存到資料庫
        message = ChatMessage.query.filter_by(
            sender_id=user01.user_id,
            receiver_id=user02.user_id
        ).first()
        
        assert message is not None
        assert message.content == 'WebSocket 即時訊息測試'
        assert message.match_id == match.match_id
        assert message.status == 'sent'
        
        # 驗證訊息的即時性
        time_diff = (datetime.utcnow() - message.timestamp).total_seconds()
        assert time_diff < 2  # 訊息應該在 2 秒內產生
        
        # 斷開連接
        authenticated_client.disconnect()
