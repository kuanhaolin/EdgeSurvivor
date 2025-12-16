"""
TC 4.6.1 - 活動照片上傳：驗證用戶狀態（精簡版）
允許：creator/approved/joined；拒絕：pending/rejected/left/非參與者/未登入。
"""

import pytest
from io import BytesIO


def _setup_activity(db):
    from datetime import date
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator@test.com")
    creator.set_password("password123")
    member = User(name="已批准", email="member@test.com")
    pending = User(name="待審", email="pending@test.com")
    rejected = User(name="拒絕", email="rejected@test.com")
    left = User(name="已離開", email="left@test.com")
    outsider = User(name="外人", email="outsider@test.com")
    member.set_password("password123")
    pending.set_password("password123")
    rejected.set_password("password123")
    left.set_password("password123")
    outsider.set_password("password123")
    db.session.add_all([creator, member, pending, rejected, left, outsider])
    db.session.commit()

    activity = Activity(
        creator_id=creator.user_id,
        title="測試活動",
        category="運動",
        location="測試地點",
        date=date.today(),
        max_participants=10,
    )
    db.session.add(activity)
    db.session.flush()

    creator_p = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=creator.user_id,
        status="joined",
        role="creator",
    )
    member_p = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=member.user_id,
        status="approved",
        role="participant",
    )
    pending_p = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=pending.user_id,
        status="pending",
        role="participant",
    )
    rejected_p = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=rejected.user_id,
        status="rejected",
        role="participant",
    )
    left_p = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=left.user_id,
        status="left",
        role="participant",
    )
    db.session.add_all([creator_p, member_p, pending_p, rejected_p, left_p])
    db.session.commit()

    return activity, creator, member, pending, rejected, left, outsider


def _login(client, email, password="password123"):
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    return res.json["access_token"]


def _upload(client, activity_id, token=None, filename="test.jpg"):
    data = {"image": (BytesIO(b"fake image content"), filename)}
    headers = {"Authorization": f"Bearer {token}"} if token else None
    return client.post(
        f"/api/activities/{activity_id}/photos",
        data=data,
        content_type="multipart/form-data",
        headers=headers,
    )


def test_participant_status_check(client, test_app):
    """允許 creator/approved/joined，其餘身份拒絕；未登入 401。"""
    with test_app.app_context():
        from models import db

        activity, creator, member, pending, rejected, left, outsider = _setup_activity(db)

        token = _login(client, creator.email)
        assert _upload(client, activity.activity_id, token).status_code == 201

        token = _login(client, member.email)
        assert _upload(client, activity.activity_id, token, filename="ok.png").status_code == 201

        token = _login(client, pending.email)
        assert _upload(client, activity.activity_id, token).status_code == 403

        token = _login(client, rejected.email)
        assert _upload(client, activity.activity_id, token).status_code == 403

        token = _login(client, left.email)
        assert _upload(client, activity.activity_id, token).status_code == 403

        token = _login(client, outsider.email)
        assert _upload(client, activity.activity_id, token).status_code == 403

        assert _upload(client, activity.activity_id, token=None).status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
