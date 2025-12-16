"""
互動與媒合整合測試
測試範圍:
1. 好友瀏覽與篩選
2. 申請好友
3. 審核好友申請
4. 私訊/傳訊息
5. 刪除好友
"""

import pytest
from models.user import User
from models.match import Match
from models.chat_message import ChatMessage
from flask_jwt_extended import create_access_token


class TestFriendMatching:
    """測試好友配對系統"""
    
    def test_complete_friend_request_flow(self, client, test_user, multiple_users,
                                         db_session, test_app):
        """
        測試完整好友申請流程:
        1. 用戶 A 瀏覽用戶列表
        2. 用戶 A 發送好友請求給用戶 B
        3. 用戶 B 收到通知並查看待審核請求
        4. 用戶 B 接受請求
        5. 雙方成為好友
        6. 驗證可以互相查看社群帳號(如果設定為僅好友可見)
        """
        user_a = test_user
        user_b = multiple_users[0]
        
        # 設定社群隱私為僅好友可見
        with test_app.app_context():
            user_a.social_privacy = 'friends_only'
            user_a.instagram_url = 'https://instagram.com/usera'
            user_b.social_privacy = 'friends_only'
            user_b.facebook_url = 'https://facebook.com/userb'
            db_session.commit()
        
        # 用戶 A 的 token
        token_a = create_access_token(identity=str(user_a.user_id))
        
        headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }
        
        # 1. 瀏覽用戶列表
        response = client.get('/api/users', headers=headers_a)
        assert response.status_code == 200
        users = response.get_json()
        assert any(u['user_id'] == user_b.user_id for u in users)
        
        # 2. 發送好友請求
        response = client.post('/api/matches',
                              json={'responder_id': user_b.user_id},
                              headers=headers_a)
        assert response.status_code == 201
        
        # 驗證配對請求已建立
        match = db_session.query(Match).filter(
            ((Match.user_a == user_a.user_id) & (Match.user_b == user_b.user_id)) |
            ((Match.user_a == user_b.user_id) & (Match.user_b == user_a.user_id))
        ).first()
        assert match is not None
        assert match.status == 'pending'
        
        # 3. 用戶 B 查看待審核請求
        token_b = create_access_token(identity=str(user_b.user_id))
        
        headers_b = {
            'Authorization': f'Bearer {token_b}',
            'Content-Type': 'application/json'
        }
        
        response = client.get('/api/matches/pending', headers=headers_b)
        assert response.status_code == 200
        pending = response.get_json()['matches']
        assert len(pending) > 0
        
        # 4. 接受好友請求
        match_id = pending[0]['match_id']
        response = client.put(f'/api/matches/{match_id}/accept',
                             headers=headers_b)
        assert response.status_code == 200
        
        # 5. 驗證配對狀態已更新
        with test_app.app_context():
            db_session.expire_all()
            match = db_session.query(Match).filter_by(match_id=match_id).first()
            assert match.status == 'accepted'
        
        # 6. 驗證用戶 A 可以看到用戶 B 的社群帳號
        response = client.get(f'/api/users/{user_b.user_id}', headers=headers_a)
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['social_links']['facebook'] is not None
        
        # 驗證用戶 B 也可以看到用戶 A 的社群帳號
        response = client.get(f'/api/users/{user_a.user_id}', headers=headers_b)
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['social_links']['instagram'] is not None
    
    def test_reject_friend_request(self, client, test_user, multiple_users,
                                   db_session, test_app):
        """測試拒絕好友請求"""
        user_a = test_user
        user_b = multiple_users[0]
        
        # 建立待審核的配對
        match = Match(
            user_a=user_a.user_id,
            user_b=user_b.user_id,
            status='pending'
        )
        db_session.add(match)
        db_session.commit()
        match_id = match.match_id
        
        # 用戶 B 拒絕請求
        token_b = create_access_token(identity=str(user_b.user_id))
        
        headers_b = {
            'Authorization': f'Bearer {token_b}',
            'Content-Type': 'application/json'
        }
        
        response = client.put(f'/api/matches/{match_id}/reject',
                             headers=headers_b)
        assert response.status_code == 200
        
        # 驗證狀態
        with test_app.app_context():
            db_session.expire_all()
            match = db_session.query(Match).filter_by(match_id=match_id).first()
            assert match.status == 'rejected'
    
    def test_delete_friend(self, client, test_user, multiple_users,
                          db_session, test_app):
        """測試刪除好友"""
        user_a = test_user
        user_b = multiple_users[0]
        
        # 建立已接受的配對
        match = Match(
            user_a=user_a.user_id,
            user_b=user_b.user_id,
            status='accepted'
        )
        db_session.add(match)
        db_session.commit()
        match_id = match.match_id
        
        # 用戶 A 刪除好友
        token_a = create_access_token(identity=str(user_a.user_id))
        
        headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }
        
        response = client.delete(f'/api/matches/{match_id}', headers=headers_a)
        assert response.status_code == 200
        
        # 驗證配對已刪除
        with test_app.app_context():
            db_session.expire_all()
            match = db_session.query(Match).filter_by(match_id=match_id).first()
            assert match is None
    
    def test_user_filtering_and_search(self, client, test_user, multiple_users, test_app):
        """測試用戶篩選與搜尋"""
        token = create_access_token(identity=str(test_user.user_id))
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # 測試按性別篩選
        response = client.get('/api/users?gender=male', headers=headers)
        assert response.status_code == 200
        users = response.get_json()
        assert all(u['gender'] == 'male' for u in users if u['gender'])
        
        # 測試按地點篩選
        response = client.get('/api/users?location=Taipei', headers=headers)
        assert response.status_code == 200
        users = response.get_json()
        assert all(u['location'] == 'Taipei' for u in users if u['location'])


class TestChatMessaging:
    """測試聊天訊息功能"""
    
    def test_send_message_between_friends(self, client, test_user, multiple_users,
                                         db_session, test_app):
        """測試好友間發送訊息"""
        user_a = test_user
        user_b = multiple_users[0]
        
        # 建立好友關係
        match = Match(
            user_a=user_a.user_id,
            user_b=user_b.user_id,
            status='accepted'
        )
        db_session.add(match)
        db_session.commit()
        
        # 用戶 A 發送訊息給用戶 B
        token_a = create_access_token(identity=str(user_a.user_id))
        
        headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }
        
        message_data = {
            'receiver_id': user_b.user_id,
            'content': 'Hello! 你好嗎?'
        }
        
        response = client.post('/api/chat/messages',
                              json=message_data,
                              headers=headers_a)
        assert response.status_code == 201
        
        # 驗證訊息已儲存
        message = db_session.query(ChatMessage).filter_by(
            sender_id=user_a.user_id,
            receiver_id=user_b.user_id
        ).first()
        assert message is not None
        assert message.content == 'Hello! 你好嗎?'
    
    def test_get_chat_history(self, client, test_user, multiple_users,
                             db_session, test_app):
        """測試取得聊天記錄"""
        user_a = test_user
        user_b = multiple_users[0]
        
        # 建立一些聊天記錄
        messages = [
            ChatMessage(
                sender_id=user_a.user_id,
                receiver_id=user_b.user_id,
                content=f'Message {i}'
            )
            for i in range(5)
        ]
        db_session.add_all(messages)
        db_session.commit()
        
        token_a = create_access_token(identity=str(user_a.user_id))
        
        headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }
        
        response = client.get(f'/api/chat/{user_b.user_id}/messages',
                             headers=headers_a)
        assert response.status_code == 200
        messages = response.get_json()['messages']
        assert len(messages) == 5
    
    def test_cannot_message_non_friend(self, client, test_user, multiple_users, test_app):
        """測試無法向非好友發送訊息"""
        user_a = test_user
        user_b = multiple_users[0]
        
        # 沒有建立好友關係
        
        token_a = create_access_token(identity=str(user_a.user_id))
        
        headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }
        
        message_data = {
            'receiver_id': user_b.user_id,
            'content': 'Hello!'
        }
        
        response = client.post('/api/chat/messages',
                              json=message_data,
                              headers=headers_a)
        # 應該返回錯誤(具體狀態碼取決於實作)
        assert response.status_code in [400, 403]


class TestMatchRecommendations:
    """測試配對推薦系統"""
    
    def test_get_recommended_users(self, client, test_user, multiple_users, test_app):
        """測試取得推薦用戶"""
        token = create_access_token(identity=str(test_user.user_id))
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = client.get('/api/matches/recommended', headers=headers)
        assert response.status_code == 200
        recommendations = response.get_json()['matches']
        assert isinstance(recommendations, list)
        # 推薦列表不應包含自己
        assert all(u['user_id'] != test_user.user_id for u in recommendations)
