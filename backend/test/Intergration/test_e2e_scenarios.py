"""
端到端整合測試
測試完整的使用者流程場景
"""

import pytest
from datetime import datetime, timedelta
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.activity_discussion import ActivityDiscussion
from models.expense import Expense
from models.activity_review import ActivityReview
from flask_jwt_extended import create_access_token


class TestCompleteActivityLifecycle:
    """測試完整活動生命週期"""
    
    def test_full_activity_flow(self, client, db_session, test_app):
        """
        完整活動流程測試:
        1. 用戶註冊並登入
        2. 建立活動
        3. 其他用戶申請參加
        4. 審核並接受申請
        5. 活動進行中發表討論
        6. 新增費用並分攤
        7. 活動結束後互評
        8. 驗證評分更新
        """
        # 1. 建立活動建立者
        creator_data = {
            'name': 'Activity Creator',
            'email': 'creator@example.com',
            'password': 'SecurePass123!',
            'location': 'Taipei',
            'gender': 'male',
            'age': 28
        }
        
        response = client.post('/api/auth/register', json=creator_data)
        assert response.status_code == 201
        creator_id = response.get_json()['user']['user_id']
        
        # 登入
        login_data = {
            'email': 'creator@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        creator_token = response.get_json()['access_token']
        
        creator_headers = {
            'Authorization': f'Bearer {creator_token}',
            'Content-Type': 'application/json'
        }
        
        # 2. 建立活動
        start_date = (datetime.utcnow() + timedelta(days=1)).date()
        activity_data = {
            'title': '完整測試活動',
            'description': '測試完整流程的活動',
            'location': 'Test Location',
            'type': 'outdoor',
            'max_members': 5,
            'start_date': start_date.isoformat(),
            'start_time': '09:00',
            'end_time': '12:00'
        }
        
        response = client.post('/api/activities',
                              json=activity_data,
                              headers=creator_headers)
        assert response.status_code == 201
        activity_id = response.get_json()['activity']['activity_id']
        
        # 3. 建立參與者並申請
        participants = []
        participant_tokens = []
        participant_ids = []
        
        for i in range(3):
            # 註冊參與者
            participant_data = {
                'name': f'Participant {i+1}',
                'email': f'participant{i+1}@example.com',
                'password': 'SecurePass123!',
                'location': 'Taipei',
                'gender': 'male' if i % 2 == 0 else 'female',
                'age': 25 + i
            }
            
            response = client.post('/api/auth/register', json=participant_data)
            assert response.status_code == 201
            participant_id = response.get_json()['user']['user_id']
            participants.append(participant_id)
            
            # 登入
            login_data = {
                'email': f'participant{i+1}@example.com',
                'password': 'SecurePass123!'
            }
            
            response = client.post('/api/auth/login', json=login_data)
            assert response.status_code == 200
            token = response.get_json()['access_token']
            participant_tokens.append(token)
            
            # 申請加入
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = client.post(f'/api/activities/{activity_id}/join',
                                  headers=headers)
            assert response.status_code == 200
            participant_ids.append(response.get_json()['participant_id'])
        
        # 5. 建立者審核申請
        # 5. 建立者審核申請
        for pid in participant_ids:
            response = client.post(
                f'/api/activities/{activity_id}/participants/{pid}/approve',
                headers=creator_headers
            )
            assert response.status_code == 200
        
        # 6. 發表討論
        discussion_data = {
            'message': '大家準時集合喔!'
        }
        
        response = client.post(
            f'/api/activities/{activity_id}/discussions',
            json=discussion_data,
            headers=creator_headers
        )
        assert response.status_code == 201
        
        # 參與者也發表討論
        participant_headers = {
            'Authorization': f'Bearer {participant_tokens[0]}',
            'Content-Type': 'application/json'
        }
        
        discussion_data = {
            'message': '好的,我會準時到!'
        }
        
        response = client.post(
            f'/api/activities/{activity_id}/discussions',
            json=discussion_data,
            headers=participant_headers
        )
        assert response.status_code == 201
        
        # 7. 新增費用
        print("Creating expense...")
        expense_data = {
            'description': '交通費',
            'amount': 1200,
            'category': 'transport',
            'payer_id': creator_id,
            'split_type': 'all'
        }
        
        response = client.post(f'/api/activities/{activity_id}/expenses',
                              json=expense_data,
                              headers=creator_headers)
        print(f"Expense creation response: {response.status_code}")
        if response.status_code != 201:
            print(f"Error: {response.get_data(as_text=True)}")
        assert response.status_code == 201
        
        # 8. 活動結束後互評
        # Update activity to be in the past and completed
        yesterday = (datetime.utcnow() - timedelta(days=1)).date()
        update_data = {
            'start_date': yesterday.isoformat(),
            'end_date': yesterday.isoformat(),
            'status': 'completed'
        }
        response = client.put(f'/api/activities/{activity_id}',
                             json=update_data,
                             headers=creator_headers)
        assert response.status_code == 200

        for i, token in enumerate(participant_tokens):
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            review_data = {
                'reviewee_id': creator_id,
                'rating': 5,
                'comment': f'活動很棒! - 參與者 {i+1}'
            }
            
            response = client.post(f'/api/activities/{activity_id}/reviews',
                                  json=review_data,
                                  headers=headers)
            assert response.status_code == 201
        
        # 9. 驗證建立者的評分更新
        response = client.get(f'/api/users/{creator_id}',
                             headers=creator_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['rating_count'] == 3
        assert data['user']['average_rating'] == 5.0
        
        # 10. 驗證活動詳情
        response = client.get(f'/api/activities/{activity_id}',
                             headers=creator_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['activity']['participants']) == 4
        # Creator is joined, others are approved
        assert all(p['status'] in ['approved', 'joined'] for p in data['activity']['participants'])


class TestSocialInteractionFlow:
    """測試社交互動流程"""
    
    def test_friend_and_activity_interaction(self, client, db_session, test_app):
        """
        測試好友與活動互動流程:
        1. 兩個用戶成為好友
        2. 用戶 A 建立活動
        3. 用戶 B 收到推薦並申請
        4. 活動進行中聊天
        5. 活動結束後互評
        """
        # 1. 建立兩個用戶
        users_data = [
            {
                'name': 'User A',
                'email': 'usera@example.com',
                'password': 'SecurePass123!',
                'location': 'Taipei',
                'gender': 'male',
                'age': 25
            },
            {
                'name': 'User B',
                'email': 'userb@example.com',
                'password': 'SecurePass123!',
                'location': 'Taipei',
                'gender': 'female',
                'age': 24
            }
        ]
        
        user_ids = []
        tokens = []
        
        for user_data in users_data:
            # 註冊
            response = client.post('/api/auth/register', json=user_data)
            assert response.status_code == 201
            user_ids.append(response.get_json()['user']['user_id'])
            
            # 登入
            login_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            
            response = client.post('/api/auth/login', json=login_data)
            assert response.status_code == 200
            tokens.append(response.get_json()['access_token'])
        
        user_a_headers = {
            'Authorization': f'Bearer {tokens[0]}',
            'Content-Type': 'application/json'
        }
        
        user_b_headers = {
            'Authorization': f'Bearer {tokens[1]}',
            'Content-Type': 'application/json'
        }
        
        # 2. 用戶 A 發送好友請求
        response = client.post('/api/matches',
                              json={'responder_id': user_ids[1]},
                              headers=user_a_headers)
        assert response.status_code == 201
        
        # 3. 用戶 B 接受好友請求
        response = client.get('/api/matches/pending', headers=user_b_headers)
        assert response.status_code == 200
        pending = response.get_json()['matches']
        match_id = pending[0]['match_id']
        
        response = client.put(f'/api/matches/{match_id}/accept',
                             headers=user_b_headers)
        assert response.status_code == 200
        
        # 4. 用戶 A 建立活動
        start_date = (datetime.utcnow() + timedelta(days=1)).date()
        activity_data = {
            'title': '好友活動',
            'description': '和好友一起的活動',
            'location': 'Taipei',
            'type': 'outdoor',
            'max_members': 5,
            'start_date': start_date.isoformat(),
            'start_time': '09:00',
            'end_time': '12:00'
        }
        
        response = client.post('/api/activities',
                              json=activity_data,
                              headers=user_a_headers)
        assert response.status_code == 201
        activity_id = response.get_json()['activity']['activity_id']
        
        # 5. 用戶 B 申請參加
        response = client.post(f'/api/activities/{activity_id}/join',
                              headers=user_b_headers)
        assert response.status_code == 200
        participant_id = response.get_json()['participant_id']
        
        # 6. 用戶 A 批准申請
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers=user_a_headers
        )
        assert response.status_code == 200
        
        # 7. 好友間聊天
        message_data = {
            'receiver_id': user_ids[1],
            'content': '期待明天的活動!'
        }
        
        response = client.post('/api/chat/messages',
                              json=message_data,
                              headers=user_a_headers)
        assert response.status_code == 201
        
        # 8. 活動結束後互評
        # Update activity to be in the past and completed
        yesterday = (datetime.utcnow() - timedelta(days=1)).date()
        update_data = {
            'start_date': yesterday.isoformat(),
            'end_date': yesterday.isoformat(),
            'status': 'completed'
        }
        response = client.put(f'/api/activities/{activity_id}',
                             json=update_data,
                             headers=user_a_headers)
        assert response.status_code == 200
        
        review_data = {
            'reviewee_id': user_ids[0],
            'rating': 5,
            'comment': '很棒的活動!'
        }
        
        response = client.post(f'/api/activities/{activity_id}/reviews',
                              json=review_data,
                              headers=user_b_headers)
        assert response.status_code == 201
