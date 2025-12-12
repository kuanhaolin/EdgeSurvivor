"""
TC 4.6.3 - 活動照片上傳：測試照片是否上傳成功
驗證照片檔案成功上傳至伺服器並儲存。
"""

import pytest
from io import BytesIO


def _setup_creator(db):
    from datetime import date
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_upload@test.com")
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


def test_photo_upload_success(client, test_app):
    """測試照片上傳成功。"""
    with test_app.app_context():
        from models import db
        import os
        import json

        activity, creator = _setup_creator(db)
        token = _login(client, creator.email)

        # 準備測試圖片
        test_image = BytesIO(b"test image content")
        data = {"image": (test_image, "test_photo.jpg")}

        # 上傳照片
        response = client.post(
            f"/api/activities/{activity.activity_id}/photos",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"},
        )

        # 驗證回應
        assert response.status_code == 201
        assert "照片上傳成功" in response.json.get("message", "")
        assert "url" in response.json
        
        # 驗證 URL 格式
        uploaded_url = response.json["url"]
        assert uploaded_url.startswith("/uploads/activities/")
        assert uploaded_url.endswith(".jpg")
        
        # 驗證檔案實際存在
        file_path = uploaded_url.lstrip("/")
        assert os.path.exists(file_path), f"上傳的檔案應該存在於 {file_path}"
        
        # 清理測試檔案
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
