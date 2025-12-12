"""
TC 4.6.4 - 活動照片上傳：驗證活動相簿更新
測試上傳照片後，活動的相簿資料是否正確更新。
"""

import pytest
from io import BytesIO
import json


def _setup_creator(db):
    from datetime import date
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_album@test.com")
    creator.set_password("password123")
    db.session.add(creator)
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

    participant = ActivityParticipant(
        activity_id=activity.activity_id,
        user_id=creator.user_id,
        status="joined",
        role="creator",
    )
    db.session.add(participant)
    db.session.commit()

    return activity, creator


def _login(client, email):
    res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    return res.json["access_token"]


def test_album_update_after_upload(client, test_app):
    """測試上傳照片後活動相簿正確更新。"""
    with test_app.app_context():
        from models import db
        from models.activity import Activity
        import os

        activity, creator = _setup_creator(db)
        token = _login(client, creator.email)

        # 驗證初始狀態：相簿為空
        db.session.refresh(activity)
        initial_images = json.loads(activity.images) if activity.images else []
        assert len(initial_images) == 0, "初始相簿應該為空"

        # 上傳第一張照片
        test_image1 = BytesIO(b"test image 1")
        data1 = {"image": (test_image1, "photo1.jpg")}
        response1 = client.post(
            f"/api/activities/{activity.activity_id}/photos",
            data=data1,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response1.status_code == 201
        url1 = response1.json["url"]

        # 驗證相簿包含一張照片
        db.session.refresh(activity)
        images_after_1 = json.loads(activity.images)
        assert len(images_after_1) == 1
        assert url1 in images_after_1

        # 上傳第二張照片
        test_image2 = BytesIO(b"test image 2")
        data2 = {"image": (test_image2, "photo2.png")}
        response2 = client.post(
            f"/api/activities/{activity.activity_id}/photos",
            data=data2,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response2.status_code == 201
        url2 = response2.json["url"]

        # 驗證相簿包含兩張照片
        db.session.refresh(activity)
        images_after_2 = json.loads(activity.images)
        assert len(images_after_2) == 2
        assert url1 in images_after_2
        assert url2 in images_after_2
        
        # 驗證照片順序（新照片應該在後面）
        assert images_after_2[0] == url1
        assert images_after_2[1] == url2

        # 清理測試檔案
        for url in images_after_2:
            file_path = url.lstrip("/")
            if os.path.exists(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
