"""
TC 4.6.5 - 活動照片上傳：驗證照片 URL 正確存入資料庫
測試照片 URL 是否正確格式化並存入資料庫。
"""

import pytest
from io import BytesIO
import json
import re


def _setup_creator(db):
    from datetime import date
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_url@test.com")
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


def test_photo_url_stored_correctly(client, test_app):
    """測試照片 URL 正確存入資料庫。"""
    with test_app.app_context():
        from models import db
        from models.activity import Activity
        import os

        activity, creator = _setup_creator(db)
        token = _login(client, creator.email)

        # 上傳照片
        test_image = BytesIO(b"test image content")
        data = {"image": (test_image, "test_photo.jpg")}
        response = client.post(
            f"/api/activities/{activity.activity_id}/photos",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        uploaded_url = response.json["url"]

        # 驗證 URL 格式：應該是 /uploads/activities/{activity_id}_{user_id}_{uuid}_{timestamp}.{ext}
        url_pattern = r'^/uploads/activities/\d+_\d+_[a-f0-9]+_\d+\.(jpg|png|jpeg|gif|webp)$'
        assert re.match(url_pattern, uploaded_url), f"URL 格式不正確: {uploaded_url}"

        # 從資料庫重新讀取活動
        db.session.refresh(activity)
        stored_images = json.loads(activity.images)
        
        # 驗證資料庫中的 URL
        assert len(stored_images) > 0, "資料庫中應該有照片"
        assert uploaded_url in stored_images, "上傳的 URL 應該存在於資料庫中"
        
        # 驗證 URL 中包含 activity_id
        assert f"{activity.activity_id}_" in uploaded_url, "URL 應該包含 activity_id"
        
        # 驗證 URL 中包含 user_id
        assert f"_{creator.user_id}_" in uploaded_url, "URL 應該包含 user_id"
        
        # 驗證回應中的 URL 與資料庫中的一致
        assert response.json["url"] == stored_images[-1], "回應的 URL 應與資料庫中最新的 URL 一致"

        # 清理測試檔案
        file_path = uploaded_url.lstrip("/")
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
