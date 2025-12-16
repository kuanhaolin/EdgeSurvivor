"""
TC 4.7.5 - 活動討論區：更新討論區
測試訊息是否會在介面同步更新（透過 REST API）。
"""

import pytest
from datetime import date


def _setup_activity_with_participant(db):
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_4_7_5@test.com")
    creator.set_password("password123")
    db.session.add(creator)

    participant = User(name="參與者", email="participant_4_7_5@test.com")
    participant.set_password("password123")
    db.session.add(participant)

    db.session.commit()

    activity = Activity(
        creator_id=creator.user_id,
        title="更新測試活動",
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


def test_discussion_list_updates(client, test_app):
    """TC 4.7.5 - 測試討論區列表更新（新增、刪除後重新查詢）"""
    with test_app.app_context():
        from models import db

        activity, creator, participant = _setup_activity_with_participant(db)
        participant_token = _login(client, participant.email)
        
        # 初始查詢：應該沒有訊息
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        assert len(response.json["discussions"]) == 0
        
        # 發送第一則訊息
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": "第一則訊息"},
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 201
        discussion1_id = response.json["discussion"]["discussion_id"]
        
        # 重新查詢：應該有一則訊息
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        assert len(response.json["discussions"]) == 1
        assert response.json["discussions"][0]["message"] == "第一則訊息"
        
        # 發送第二則訊息
        response = client.post(
            f"/api/activities/{activity.activity_id}/discussions",
            json={"message": "第二則訊息"},
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 201
        
        # 重新查詢：應該有兩則訊息
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        assert len(response.json["discussions"]) == 2
        
        # 刪除第一則訊息
        response = client.delete(
            f"/api/discussions/{discussion1_id}",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        
        # 重新查詢：應該只剩一則訊息（已刪除的不會出現）
        response = client.get(
            f"/api/activities/{activity.activity_id}/discussions",
            headers={"Authorization": f"Bearer {participant_token}"},
        )
        assert response.status_code == 200
        discussions = response.json["discussions"]
        assert len(discussions) == 1
        assert discussions[0]["message"] == "第二則訊息"
        
        # 驗證訊息順序（按時間排序）
        assert discussions[0]["discussion_id"] != discussion1_id


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
