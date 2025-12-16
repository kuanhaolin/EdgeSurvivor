"""
TC 4.7.2 - 活動討論區：參與者發送留言
測試參與者是否成功發布留言。
"""

import pytest
from datetime import date


def _setup_activity_with_participant(db):
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_4_7_2@test.com")
    creator.set_password("password123")
    db.session.add(creator)

    participant = User(name="參與者", email="participant_4_7_2@test.com")
    participant.set_password("password123")
    db.session.add(participant)

    db.session.commit()

    activity = Activity(
        creator_id=creator.user_id,
        title="測試討論活動",
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

    db.session.commit()

    return activity, creator, participant


def _login(client, email):
    res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    return res.json["access_token"]


def test_send_discussion(client, test_app):
    """TC 4.7.2 - 測試參與者發送留言（成功、失敗、驗證）"""
    with test_app.app_context():
        from models import db
        from models.user import User
        from models.activity_discussion import ActivityDiscussion

        activity, creator, participant = _setup_activity_with_participant(db)
        
        # 參與者成功發布留言
        participant_token = _login(client, participant.email)
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": "參與者測試留言"},
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 201
        assert response.json["discussion"]["message"] == "參與者測試留言"
        assert response.json["discussion"]["user_id"] == participant.user_id
        
        # 創建者成功發布留言
        creator_token = _login(client, creator.email)
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": "創建者測試留言"},
            headers={"Authorization": f"Bearer {creator_token}"},
        )
        assert response.status_code == 201
        assert response.json["discussion"]["user_id"] == creator.user_id
        
        # 非參與者無法發布留言
        non_participant = User(name="非參與者", email="non_participant_4_7_2@test.com")
        non_participant.set_password("password123")
        db.session.add(non_participant)
        db.session.commit()
        
        non_participant_token = _login(client, non_participant.email)
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": "非參與者嘗試留言"},
            headers={"Authorization": f"Bearer {non_participant_token}"},
        )
        assert response.status_code == 403
        
        # 空訊息被拒絕
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": ""},
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 400
        
        # 驗證留言存入資料庫
        message_text = "資料庫驗證留言"
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": message_text},
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 201
        
        discussion = ActivityDiscussion.query.filter_by(
            activity_id=activity.activity_id, message=message_text
        ).first()
        assert discussion is not None
        assert discussion.user_id == participant.user_id


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
