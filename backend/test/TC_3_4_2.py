"""
TC_3.4.2: 訊息未讀狀態
測試說明: 測試未讀訊息數與訊息列表顯示
"""
import pytest
import json
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage
from datetime import datetime


def test_unread_message_display(client, test_app):
    """測試未讀訊息列表與數量顯示"""
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
        
        # 創建已接受的媒合關係
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
        
        # user02 發送 3 條未讀訊息給 user01
        message1 = ChatMessage(
            match_id=match1.match_id,
            sender_id=user02.user_id,
            receiver_id=user01.user_id,
            content='訊息1',
            status='sent'
        )
        message2 = ChatMessage(
            match_id=match1.match_id,
            sender_id=user02.user_id,
            receiver_id=user01.user_id,
            content='訊息2',
            status='sent'
        )
        message3 = ChatMessage(
            match_id=match1.match_id,
            sender_id=user02.user_id,
            receiver_id=user01.user_id,
            content='訊息3',
            status='sent'
        )
        
        # user03 發送 2 條未讀訊息給 user01
        message4 = ChatMessage(
            match_id=match2.match_id,
            sender_id=user03.user_id,
            receiver_id=user01.user_id,
            content='訊息4',
            status='sent'
        )
        message5 = ChatMessage(
            match_id=match2.match_id,
            sender_id=user03.user_id,
            receiver_id=user01.user_id,
            content='訊息5',
            status='sent'
        )
        
        db.session.add_all([message1, message2, message3, message4, message5])
        db.session.commit()
        
        # 查詢 user01 的對話列表
        token = create_access_token(identity=str(user01.user_id))
        
        response = client.get(
            '/api/chat/conversations',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'conversations' in data
        assert len(data['conversations']) == 2
        
        # 驗證未讀訊息數量
        unread_counts = [conv['unread_count'] for conv in data['conversations']]
        assert 3 in unread_counts  # user02 的 3 條未讀
        assert 2 in unread_counts  # user03 的 2 條未讀
        
        # 驗證總未讀數
        total_unread = sum(unread_counts)
        assert total_unread == 5
