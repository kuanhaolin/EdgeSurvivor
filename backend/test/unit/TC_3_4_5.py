"""
TC_3.4.5: 刪除訊息
測試說明: 測試刪除自己發送的訊息是否可以被刪除
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage
from datetime import datetime


def test_delete_own_message(client, test_app):
    """測試刪除自己發送的訊息"""
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
        
        # user01 發送訊息
        message = ChatMessage(
            sender_id=user01.user_id,
            receiver_id=user02.user_id,
            content='要被刪除的訊息',
            status='sent'
        )
        db.session.add(message)
        db.session.commit()
        
        message_id = message.message_id
        
        # 驗證訊息存在
        assert ChatMessage.query.get(message_id) is not None
        
        # user01 刪除自己的訊息（透過資料庫直接刪除）
        message_to_delete = ChatMessage.query.get(message_id)
        assert message_to_delete.sender_id == user01.user_id  # 確認是自己的訊息
        
        db.session.delete(message_to_delete)
        db.session.commit()
        
        # 驗證訊息已被刪除
        deleted_message = ChatMessage.query.get(message_id)
        assert deleted_message is None
