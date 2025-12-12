"""
TC 4.7.1 - 活動討論區：驗證用戶狀態
測試用戶是否為活動參與者才能查看討論區。
"""

import pytest
from datetime import date


def _setup_activity_with_participants(db):
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    # 創建活動創建者
    creator = User(name="創建者", email="creator_4_7_1@test.com")
    creator.set_password("password123")
    db.session.add(creator)

    # 創建參與者
    participant = User(name="參與者", email="participant_4_7_1@test.com")
    participant.set_password("password123")
    db.session.add(participant)

    # 創建非參與者
    non_participant = User(name="非參與者", email="non_participant_4_7_1@test.com")
    non_participant.set_password("password123")
    db.session.add(non_participant)

    db.session.commit()

    # 創建活動
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

    # 創建者自動成為參與者
    creator_participant = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=creator.user_id,
        status="joined",
        role="creator",
    )
    db.session.add(creator_participant)

    # 添加參與者
    participant_record = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=participant.user_id,
        status="joined",
        role="participant",
    )
    db.session.add(participant_record)

    db.session.commit()

    return activity, creator, participant, non_participant


def _login(client, email):
    res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    return res.json["access_token"]


def test_user_status_verification(client, test_app):
    """TC 4.7.1 - 測試用戶狀態驗證（參與者可查看，非參與者不可查看）"""
    with test_app.app_context():
        from models import db

        activity, creator, participant, non_participant = _setup_activity_with_participants(db)
        
        # 創建者可以查看
        creator_token = _login(client, creator.email)
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {creator_token}"},
        )
        assert response.status_code == 200
        
        # 參與者可以查看
        participant_token = _login(client, participant.email)
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        
        # 非參與者無法查看
        non_participant_token = _login(client, non_participant.email)
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {non_participant_token}"},
        )
        assert response.status_code == 403
        
        # 未認證用戶無法查看
        response = client.get(f"/api/activities/{activity.activity_id}/discussions")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
