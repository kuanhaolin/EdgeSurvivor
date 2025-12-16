"""
TC_4.5: 接收即時訊息與通知測試
Story 4.5: 接收即時訊息與通知
"""
import pytest
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage


class TestMessageReceiving:
    """測試訊息接收功能"""
    
    def test_unread_count_api(self, client, test_app):
        """測試未讀訊息計數 API (AC: 2, 4)"""
        with test_app.app_context():
            # 建立測試用戶
            user1 = User(name='User1', email='user1@test.com', password_hash='hash1')
            user2 = User(name='User2', email='user2@test.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # 建立媒合
            match = Match(user_a=user1.user_id, user_b=user2.user_id, status='accepted')
            db.session.add(match)
            db.session.commit()
            
            # user2 發送 3 條未讀訊息給 user1
            for i in range(3):
                msg = ChatMessage(
                    match_id=match.match_id,
                    sender_id=user2.user_id,
                    receiver_id=user1.user_id,
                    content=f'Test message {i}',
                    status='sent'
                )
                db.session.add(msg)
            db.session.commit()
            
            # 測試 user1 的未讀計數
            token = create_access_token(identity=str(user1.user_id))
            response = client.get(
                '/api/chat/unread-count',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            data = response.json
            assert 'unread_count' in data
            assert data['unread_count'] == 3
    
    def test_conversation_unread_count(self, client, test_app):
        """測試聊天列表中的未讀數 (AC: 2)"""
        with test_app.app_context():
            # 建立測試用戶
            user1 = User(name='User1', email='user1@test.com', password_hash='hash1')
            user2 = User(name='User2', email='user2@test.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # 建立媒合
            match = Match(user_a=user1.user_id, user_b=user2.user_id, status='accepted')
            db.session.add(match)
            db.session.commit()
            
            # user2 發送 5 條未讀訊息
            for i in range(5):
                msg = ChatMessage(
                    match_id=match.match_id,
                    sender_id=user2.user_id,
                    receiver_id=user1.user_id,
                    content=f'Message {i}',
                    status='sent'
                )
                db.session.add(msg)
            db.session.commit()
            
            # 取得 user1 的聊天列表
            token = create_access_token(identity=str(user1.user_id))
            response = client.get(
                '/api/chat/conversations',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            conversations = response.json['conversations']
            assert len(conversations) > 0
            
            # 找到與 user2 的對話
            conv = next((c for c in conversations if c['other_user']['user_id'] == user2.user_id), None)
            assert conv is not None
            assert conv['unread_count'] == 5
    
    def test_mark_as_read(self, client, test_app):
        """測試標記為已讀 (AC: 2)"""
        with test_app.app_context():
            # 建立測試用戶
            user1 = User(name='User1', email='user1@test.com', password_hash='hash1')
            user2 = User(name='User2', email='user2@test.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # user2 發送訊息給 user1
            msg = ChatMessage(
                sender_id=user2.user_id,
                receiver_id=user1.user_id,
                content='Test message',
                status='sent'
            )
            db.session.add(msg)
            db.session.commit()
            
            # user1 標記為已讀
            token = create_access_token(identity=str(user1.user_id))
            response = client.put(
                f'/api/chat/conversations/{user2.user_id}/read',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            
            # 驗證訊息狀態已更新
            msg_updated = ChatMessage.query.get(msg.message_id)
            assert msg_updated.status == 'read'
            
            # 驗證未讀數為 0
            response = client.get(
                '/api/chat/unread-count',
                headers={'Authorization': f'Bearer {token}'}
            )
            assert response.json['unread_count'] == 0


class TestSystemMessages:
    """測試系統訊息功能 (待實作)"""
    
    @pytest.mark.skip(reason="系統訊息功能待實作")
    def test_match_success_system_message(self, client, test_app):
        """測試媒合成功時自動生成系統訊息 (AC: 7)"""
        with test_app.app_context():
            # 建立測試用戶
            user1 = User(name='User1', email='user1@test.com', password_hash='hash1')
            user2 = User(name='User2', email='user2@test.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # 建立並確認媒合
            match = Match(user_a=user1.user_id, user_b=user2.user_id, status='accepted')
            db.session.add(match)
            db.session.commit()
            
            # 檢查是否自動生成系統訊息
            system_msg = ChatMessage.query.filter_by(
                match_id=match.match_id,
                message_type='system'
            ).first()
            
            assert system_msg is not None
            assert '成功媒合' in system_msg.content or '已成功配對' in system_msg.content


# 整合測試：完整流程
class TestMessageFlow:
    """測試完整訊息流程"""
    
    def test_complete_message_flow(self, client, test_app):
        """測試完整訊息接收流程 (AC: 1, 2, 4, 5)"""
        with test_app.app_context():
            # 1. 建立用戶和媒合
            user1 = User(name='User1', email='user1@test.com', password_hash='hash1')
            user2 = User(name='User2', email='user2@test.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            match = Match(user_a=user1.user_id, user_b=user2.user_id, status='accepted')
            db.session.add(match)
            db.session.commit()
            
            # 2. user2 發送訊息
            msg = ChatMessage(
                match_id=match.match_id,
                sender_id=user2.user_id,
                receiver_id=user1.user_id,
                content='Hello!',
                status='sent'
            )
            db.session.add(msg)
            db.session.commit()
            
            # 3. 驗證 user1 可以看到訊息
            token1 = create_access_token(identity=str(user1.user_id))
            response = client.get(
                f'/api/chat/{user2.user_id}/messages',
                headers={'Authorization': f'Bearer {token1}'}
            )
            
            assert response.status_code == 200
            messages = response.json['messages']
            assert len(messages) == 1
            assert messages[0]['content'] == 'Hello!'
            
            # 4. 驗證未讀數為 1
            response = client.get(
                '/api/chat/unread-count',
                headers={'Authorization': f'Bearer {token1}'}
            )
            assert response.json['unread_count'] == 1
            
            # 5. user1 標記為已讀
            client.put(
                f'/api/chat/conversations/{user2.user_id}/read',
                headers={'Authorization': f'Bearer {token1}'}
            )
            
            # 6. 驗證未讀數變為 0
            response = client.get(
                '/api/chat/unread-count',
                headers={'Authorization': f'Bearer {token1}'}
            )
            assert response.json['unread_count'] == 0
