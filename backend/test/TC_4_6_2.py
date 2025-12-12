"""
TC 4.6.2 - 活動照片上傳：檔案規格單測
單一測試涵蓋：有效副檔名接受、大小寫不敏感、副檔名缺失、無檔案、空檔名、超出容量、非法類型。
"""

import pytest
from io import BytesIO


def _setup_creator(db):
    from datetime import date
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_format@test.com")
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


def _upload(client, activity_id, token=None, file_tuple=None):
    data = {"image": file_tuple} if file_tuple is not None else {}
    headers = {"Authorization": f"Bearer {token}"} if token else None
    return client.post(
        f"/api/activities/{activity_id}/photos",
        data=data,
        content_type="multipart/form-data",
        headers=headers,
    )


def test_verify_photo_format(client, test_app):
    """單測涵蓋檔案格式/大小/名稱/缺檔各情境。"""
    with test_app.app_context():
        from models import db

        activity, creator = _setup_creator(db)
        token = _login(client, creator.email)

        valid_files = [
            ("ok.png", BytesIO(b"img")),
            ("ok.jpg", BytesIO(b"img")),
            ("ok.jpeg", BytesIO(b"img")),
            ("ok.gif", BytesIO(b"img")),
            ("ok.webp", BytesIO(b"img")),
            ("OK.PNG", BytesIO(b"img")),
            ("UPPER.JPG", BytesIO(b"img")),
            ("CASE.JPEG", BytesIO(b"img")),
            ("GIF.GIF", BytesIO(b"img")),
        ]

        for fname, payload in valid_files:
            r = _upload(client, activity.activity_id, token, (payload, fname))
            assert r.status_code == 201, f"應接受有效格式: {fname}"
            assert "照片上傳成功" in r.json.get("message", "")

        invalid_ext = ["bad.txt", "bad.pdf", "bad.exe", "bad.doc", "bad.zip", "filenamewithoutextension"]
        for fname in invalid_ext:
            r = _upload(client, activity.activity_id, token, (BytesIO(b"file"), fname))
            assert r.status_code == 400, f"應拒絕無效格式: {fname}"
            assert "不支持的文件類型" in r.json.get("error", "")

        large_file = BytesIO(b"x" * (6 * 1024 * 1024))  # 6MB
        r = _upload(client, activity.activity_id, token, (large_file, "large.jpg"))
        assert r.status_code == 400
        assert "文件大小超過限制" in r.json.get("error", "")

        normal_file = BytesIO(b"x" * (4 * 1024 * 1024))  # 4MB
        r = _upload(client, activity.activity_id, token, (normal_file, "normal.jpg"))
        assert r.status_code == 201
        assert "照片上傳成功" in r.json.get("message", "")

        r = _upload(client, activity.activity_id, token, (BytesIO(b"content"), ""))
        assert r.status_code == 400
        assert "沒有選擇文件" in r.json.get("error", "")

        r = _upload(client, activity.activity_id, token, None)
        assert r.status_code == 400
        assert "沒有選擇文件" in r.json.get("error", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
