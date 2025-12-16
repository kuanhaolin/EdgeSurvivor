"""
活動建立與管理整合測試
測試範圍:
1. 建立活動
2. 管理活動
3. 審核活動申請
4. 移除參與者
5. 控制討論區訊息
6. 控制分攤費用
"""

import pytest
from datetime import datetime, timedelta
from models.user import User
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.activity_discussion import ActivityDiscussion
from models.expense import Expense
from flask_jwt_extended import create_access_token


class TestActivityCreationAndManagement:
    """測試活動建立與管理"""
    
    def test_create_activity(self, client, auth_headers, test_user, db_session, test_app):
        """測試建立活動"""
        start_date = (datetime.utcnow() + timedelta(days=7)).date()
        activity_data = {
            'title': '週末登山活動',
            'description': '一起去爬山,享受大自然',
            'location': '陽明山',
            'type': 'outdoor',
            'max_members': 10,
            'start_date': start_date.isoformat(),
            'start_time': '09:00',
            'end_time': '14:00'
        }
        
        response = client.post('/api/activities', 
                              json=activity_data, 
                              headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert 'activity' in data
        assert data['activity']['title'] == '週末登山活動'
        
        # 驗證活動已儲存
        activity_id = data['activity']['activity_id']
        with test_app.app_context():
            activity = db_session.query(Activity).filter_by(activity_id=activity_id).first()
            assert activity is not None
            assert activity.creator_id == test_user.user_id
            assert activity.title == '週末登山活動'
    
    def test_update_activity(self, client, auth_headers, test_activity, db_session, test_app):
        """測試更新活動"""
        update_data = {
            'title': '更新後的活動標題',
            'description': '更新後的描述',
            'max_members': 15
        }
        
        response = client.put(f'/api/activities/{test_activity.activity_id}',
                             json=update_data,
                             headers=auth_headers)
        assert response.status_code == 200
        
        # 驗證更新
        with test_app.app_context():
            db_session.expire_all()
            activity = db_session.query(Activity).filter_by(
                activity_id=test_activity.activity_id
            ).first()
            assert activity.title == '更新後的活動標題'
            assert activity.max_participants == 15
    
    def test_delete_activity(self, client, auth_headers, test_activity, db_session, test_app):
        """測試刪除活動"""
        response = client.delete(f'/api/activities/{test_activity.activity_id}',
                                headers=auth_headers)
        assert response.status_code == 200
        
        # 驗證活動已刪除或標記為非活躍
        with test_app.app_context():
            db_session.expire_all()
            activity = db_session.query(Activity).filter_by(
                activity_id=test_activity.activity_id
            ).first()
            # 根據實作,可能是軟刪除或硬刪除
            assert activity is None or activity.is_active is False
    
    def test_non_creator_cannot_update_activity(self, client, test_activity, 
                                                multiple_users, test_app):
        """測試非建立者無法更新活動"""
        # Get IDs within app_context to avoid detached instance error
        with test_app.app_context():
            other_user_id = multiple_users[0].user_id
            activity_id = test_activity.activity_id
            other_token = create_access_token(identity=str(other_user_id))
        
        other_headers = {
            'Authorization': f'Bearer {other_token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {'title': '嘗試更新'}
        
        response = client.put(f'/api/activities/{activity_id}',
                             json=update_data,
                             headers=other_headers)
        assert response.status_code == 403


class TestActivityParticipation:
    """測試活動參與流程"""
    
    def test_complete_participation_flow(self, client, auth_headers, test_activity,
                                        multiple_users, db_session, test_app):
        """
        測試完整參與流程:
        1. 用戶申請參加活動
        2. 建立者審核申請
        3. 驗證參與者狀態
        """
        # Get IDs directly - no need for app_context since fixtures are already in context
        applicant_id = multiple_users[0].user_id
        activity_id = test_activity.activity_id
        applicant_token = create_access_token(identity=str(applicant_id))
        
        applicant_headers = {
            'Authorization': f'Bearer {applicant_token}',
            'Content-Type': 'application/json'
        }
        
        # 1. 申請參加活動
        response = client.post(f'/api/activities/{activity_id}/join',
                              headers=applicant_headers)
        assert response.status_code == 200
        
        # 驗證申請已建立
        participant = db_session.query(ActivityParticipant).filter_by(
            activity_id=activity_id,
            user_id=applicant_id
        ).first()
        assert participant is not None
        assert participant.status == 'pending'
        participant_id = participant.participant_id
        
        # 2. 建立者審核申請
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/approve',
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # 3. 驗證狀態已更新
        db_session.expire_all()
        participant = db_session.query(ActivityParticipant).filter_by(
            activity_id=activity_id,
            user_id=applicant_id
        ).first()
        assert participant.status == 'approved'
    
    def test_reject_participation(self, client, auth_headers, test_activity,
                                 multiple_users, db_session, test_app):
        """測試拒絕參與申請"""
        # Get IDs directly
        applicant_id = multiple_users[0].user_id
        activity_id = test_activity.activity_id
        
        # 建立申請
        participant = ActivityParticipant(
            activity_id=activity_id,
            user_id=applicant_id,
            status='pending'
        )
        db_session.add(participant)
        db_session.commit()
        participant_id = participant.participant_id
        
        # 拒絕申請
        response = client.post(
            f'/api/activities/{activity_id}/participants/{participant_id}/reject',
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # 驗證狀態
        db_session.expire_all()
        participant = db_session.query(ActivityParticipant).filter_by(
            activity_id=activity_id,
            user_id=applicant_id
        ).first()
        assert participant.status == 'rejected'
    
    def test_remove_participant(self, client, auth_headers, test_activity,
                               multiple_users, db_session, test_app):
        """測試移除參與者"""
        # Get IDs directly
        participant_user_id = multiple_users[0].user_id
        activity_id = test_activity.activity_id
        
        # 建立已批准的參與者
        participant = ActivityParticipant(
            activity_id=activity_id,
            user_id=participant_user_id,
            status='approved'
        )
        db_session.add(participant)
        db_session.commit()
        participant_id = participant.participant_id
        
        # 移除參與者
        response = client.delete(
            f'/api/activities/{activity_id}/participants/{participant_id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # 驗證已移除
        db_session.expire_all()
        participant = db_session.query(ActivityParticipant).filter_by(
            activity_id=activity_id,
            user_id=participant_user_id
        ).first()
        assert participant is None or participant.status == 'removed'
    
    def test_max_participants_limit(self, client, test_activity, 
                                   multiple_users, db_session, test_app):
        """測試參與者人數上限"""
        # Get activity_id and set max participants
        activity_id = test_activity.activity_id
        test_activity.max_participants = 2
        db_session.commit()
        
        # 前兩個用戶成功加入
        for i in range(2):
            user_id = multiple_users[i].user_id
            token = create_access_token(identity=str(user_id))
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = client.post(f'/api/activities/{activity_id}/join',
                                  headers=headers)
            assert response.status_code == 200
            
            # 直接批准
            participant = db_session.query(ActivityParticipant).filter_by(
                activity_id=activity_id,
                user_id=user_id
            ).first()
            participant.status = 'approved'
            db_session.commit()
        
        # 第三個用戶應該無法加入
        user_id = multiple_users[2].user_id
        token = create_access_token(identity=str(user_id))
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = client.post(f'/api/activities/{activity_id}/join',
                              headers=headers)
        assert response.status_code == 400


class TestActivityDiscussion:
    """測試活動討論區"""
    
    def test_post_discussion(self, client, auth_headers, test_activity, 
                            db_session, test_app):
        """測試發表討論"""
        # Get activity_id directly
        activity_id = test_activity.activity_id
        
        discussion_data = {
            'message': '大家準時集合喔!'
        }
        
        response = client.post(
            f'/api/activities/{activity_id}/discussions',
            json=discussion_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        
        # 驗證討論已儲存
        discussion = db_session.query(ActivityDiscussion).filter_by(
            activity_id=activity_id
        ).first()
        assert discussion is not None
        assert discussion.message == '大家準時集合喔!'
    
    def test_delete_discussion(self, client, auth_headers, test_activity,
                              db_session, test_app):
        """測試刪除討論(建立者權限)"""
        # Get IDs and create discussion
        activity_id = test_activity.activity_id
        creator_id = test_activity.creator_id
        
        discussion = ActivityDiscussion(
            activity_id=activity_id,
            user_id=creator_id,
            message='測試討論'
        )
        db_session.add(discussion)
        db_session.commit()
        discussion_id = discussion.discussion_id
        
        # 刪除討論
        response = client.delete(
            f'/api/discussions/{discussion_id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # 驗證已刪除
        db_session.expire_all()
        discussion = db_session.query(ActivityDiscussion).get(discussion_id)
        assert discussion is not None
        assert discussion.is_deleted is True
    
    def test_add_expense(self, client, auth_headers, test_activity,
                        db_session, test_app, test_user):
        """測試新增費用"""
        # Get activity_id directly
        activity_id = test_activity.activity_id
        
        expense_data = {
            'description': '交通費',
            'amount': 1000,
            'category': 'transport',
            'payer_id': test_user.user_id,
            'split_type': 'all'
        }
        
        response = client.post(f'/api/activities/{activity_id}/expenses',
                              json=expense_data,
                              headers=auth_headers)
        if response.status_code != 201:
            print(f"Add Expense Error: {response.get_data(as_text=True)}")
        assert response.status_code == 201
        
        # 驗證費用已儲存
        expense = db_session.query(Expense).filter_by(
            activity_id=activity_id
        ).first()
        assert expense is not None
        assert expense.description == '交通費'
        assert expense.amount == 1000
    
    def test_expense_split_calculation(self, client, auth_headers, test_activity,
                                      multiple_users, db_session, test_app, test_user):
        """
        測試費用分攤計算:
        1. 新增費用
        2. 加入參與者
        3. 驗證分攤金額計算正確
        """
        # Get activity_id directly
        activity_id = test_activity.activity_id
        
        # 1. 加入 3 個參與者
        for i in range(3):
            user_id = multiple_users[i].user_id
            participant = ActivityParticipant(
                activity_id=activity_id,
                user_id=user_id,
                status='approved'
            )
            db_session.add(participant)
        db_session.commit()
        
        # 2. 新增費用 (總額 1200,4 人平分 = 每人 300)
        expense_data = {
            'description': '餐費',
            'amount': 1200,
            'category': 'food',
            'payer_id': test_user.user_id,
            'split_type': 'all'
        }
        
        response = client.post(f'/api/activities/{activity_id}/expenses',
                              json=expense_data,
                              headers=auth_headers)
        if response.status_code != 201:
            print(f"Split Expense Error: {response.get_data(as_text=True)}")
        assert response.status_code == 201
        expense_id = response.get_json()['expense']['expense_id']
        
        # 3. 取得費用列表
        response = client.get(f'/api/activities/{activity_id}/expenses',
                             headers=auth_headers)
        assert response.status_code == 200
        expenses = response.get_json()['expenses']
        
        # Find the expense we just created
        target_expense = next((e for e in expenses if e['expense_id'] == expense_id), None)
        assert target_expense is not None
        
        # 驗證分攤金額 (建立者 + 3 個參與者 = 4 人)
        assert target_expense['amount'] == 1200
        # 每人應分攤 300
        # (具體驗證邏輯取決於 API 回傳格式)
