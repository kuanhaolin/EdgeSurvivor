"""
TC_2_5_1: 創建者刪除任何訊息
測試說明: 測試創建者可以刪除任何活動討論訊息
"""
import pytest
from flask import json
from models.user import User
from models.activity import Activity
from models.activity_discussion import ActivityDiscussion
from models import db
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

def test_creator_can_delete_any_message(client, test_app):
    """測試創建者可以刪除任何人的訊息"""
    with test_app.app_context():
        # 創建創建者和其他用戶
        creator = User(name='creator', email='creator@test.com', password_hash='hash')
        other_user = User(name='other', email='other@test.com', password_hash='hash')
        db.session.add_all([creator, other_user])
        db.session.commit()
        
        # 創建活動
        activity = Activity(
            title='測試活動',
            category='hiking',
            location='陽明山',
            date=datetime.now().date() + timedelta(days=7),
            max_participants=10,
            creator_id=creator.user_id
        )
        db.session.add(activity)
        db.session.commit()
        
        # 其他用戶發送訊息
        discussion = ActivityDiscussion(
            activity_id=activity.activity_id,
            user_id=other_user.user_id,
            message='測試訊息'
        )
        db.session.add(discussion)
        db.session.commit()
        
        creator_token = create_access_token(identity=str(creator.user_id))
        discussion_id = discussion.discussion_id
        
        # 創建者刪除其他用戶的訊息（應該成功）
        response = client.delete(
            f'/api/discussions/{discussion_id}',
            headers={'Authorization': f'Bearer {creator_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert '已刪除' in data['message'] or 'deleted' in data['message'].lower()
