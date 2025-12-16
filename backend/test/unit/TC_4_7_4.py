"""
TC 4.7.4 - 活動討論區：刪除自己的留言
測試刪除自己的留言功能。
"""

import pytest
from datetime import date


def _setup_activity_with_discussions(db):
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant
    from models.activity_discussion import ActivityDiscussion

    creator = User(name="創建者", email="creator_4_7_4@test.com")
    creator.set_password("password123")
    db.session.add(creator)

    participant = User(name="參與者", email="participant_4_7_4@test.com")
    participant.set_password("password123")
    db.session.add(participant)

    other_user = User(name="其他用戶", email="other_4_7_4@test.com")
    other_user.set_password("password123")
    db.session.add(other_user)

    db.session.commit()

    activity = Activity(
        creator_id=creator.user_id,
        title="刪除測試活動",
        category="運動",
        location="測試地點",
        date=date.today(),
        max_participants=10,
    )
    db.session.add(activity)
    db.session.flush()

    creator_participant = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=creator.user_id,
        status="joined",
        role="creator",
    )
    db.session.add(creator_participant)

    participant_record = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=participant.user_id,
        status="joined",
        role="participant",
    )
    db.session.add(participant_record)

    other_participant = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=other_user.user_id,
        status="joined",
        role="participant",
    )
    db.session.add(other_participant)

    db.session.commit()

    # 創建討論訊息
    discussion1 = ActivityDiscussion(
        activity_id=activity.activity_id,
        user_id=participant.user_id,
        message="參與者的留言",
    )
    db.session.add(discussion1)

    discussion2 = ActivityDiscussion(
        activity_id=activity.activity_id,
        user_id=other_user.user_id,
        message="其他用戶的留言",
    )
    db.session.add(discussion2)

    db.session.commit()

    return activity, creator, participant, other_user, discussion1, discussion2


def _login(client, email):
    res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    return res.json["access_token"]


def test_delete_discussion(client, test_app):
    """TC 4.7.4 - 測試刪除留言（自己的留言、創建者權限、無法刪除他人、軟刪除）"""
    with test_app.app_context():
        from models import db
        from models.activity_discussion import ActivityDiscussion

        activity, creator, participant, other_user, discussion1, discussion2 = (
            _setup_activity_with_discussions(db)
        )
        
        # 用戶刪除自己的留言
        participant_token = _login(client, participant.email)
        response = client.delete(
            f"/api/discussions/{discussion1.discussion_id}",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        db.session.refresh(discussion1)
        assert discussion1.is_deleted is True
        
        # 創建者可以刪除任何留言
        creator_token = _login(client, creator.email)
        response = client.delete(
            f"/api/discussions/{discussion2.discussion_id}",
            headers={"Authorization": f"Bearer {creator_token}"},
        )
        assert response.status_code == 200
        
        # 用戶無法刪除他人的留言（創建新留言測試）
        discussion3 = ActivityDiscussion(
            activity_id=activity.activity_id,
            user_id=other_user.user_id,
            message="測試留言3",
        )
        db.session.add(discussion3)
        db.session.commit()
        
        response = client.delete(
            f"/api/discussions/{discussion3.discussion_id}",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 403
        
        # 刪除不存在的留言
        response = client.delete(
            "/api/discussions/99999", 
            headers={"Authorization": f"Bearer {participant_token}"}
        )
        assert response.status_code == 404
        
        # 驗證軟刪除機制：已刪除的不會出現在查詢中
        discussions = ActivityDiscussion.query.filter_by(
            activity_id=activity.activity_id, is_deleted=False
        ).all()
        discussion_ids = [d.discussion_id for d in discussions]
        assert discussion1.discussion_id not in discussion_ids
        assert discussion2.discussion_id not in discussion_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
