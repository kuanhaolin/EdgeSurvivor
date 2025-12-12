"""
TC 4.7.3 - 活動討論區：討論區訊息即時同步
測試 SocketIO 即時傳遞留言功能。
"""

import pytest
from datetime import date


def _setup_activity_with_participant(db):
    from models.user import User
    from models.activity import Activity
    from models.activity_participant import ActivityParticipant

    creator = User(name="創建者", email="creator_4_7_3@test.com")
    creator.set_password("password123")
    db.session.add(creator)

    participant = User(name="參與者", email="participant_4_7_3@test.com")
    participant.set_password("password123")
    db.session.add(participant)

    db.session.commit()

    activity = Activity(
        creator_id=creator.user_id,
        title="即時測試活動",
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


def test_socketio_realtime_sync(client, socketio_client, test_app):
    """TC 4.7.3 - 測試 SocketIO 即時同步（發送、加入/離開房間、廣播）"""
    with test_app.app_context():
        from models import db

        activity, creator, participant = _setup_activity_with_participant(db)
        
        # 使用 HTTP client 登入取得 token
        res = client.post("/api/auth/login", json={"email": participant.email, "password": "password123"})
        token = res.json["access_token"]

        # 連接到 SocketIO
        socketio_client.connect(auth={'token': token})
        assert socketio_client.is_connected()

        # 測試加入活動討論室
        socketio_client.emit('join_activity_discussion', {
            'activity_id': activity.activity_id,
            'user_id': participant.user_id
        })

        # 測試發送討論訊息
        socketio_client.emit('send_discussion', {
            'activity_id': activity.activity_id,
            'user_id': participant.user_id,
            'message': 'SocketIO 測試訊息'
        })

        # 接收訊息並驗證
        received = socketio_client.get_received()
        new_discussion_events = [r for r in received if r['name'] == 'new_discussion']
        assert len(new_discussion_events) > 0
        
        event_data = new_discussion_events[0]['args'][0]
        assert event_data['message'] == 'SocketIO 測試訊息'
        assert event_data['user_id'] == participant.user_id
        assert event_data['activity_id'] == activity.activity_id

        # 測試離開討論室
        socketio_client.emit('leave_activity_discussion', {
            'activity_id': activity.activity_id
        })

        # 確認連線仍然正常
        assert socketio_client.is_connected()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--no-cov"])
