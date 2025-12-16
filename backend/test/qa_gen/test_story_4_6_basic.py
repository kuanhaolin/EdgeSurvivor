import pytest
from models.chat_message import ChatMessage
from models.user import User
from datetime import datetime, timedelta

def test_get_messages_with_pagination(client, auth_headers):
    '''測試訊息分頁載入'''
    user1 = User(email='user1@test.com', name='User1')
    user1.set_password('password123')
    user2 = User(email='user2@test.com', name='User2')
    user2.set_password('password123')
    
    from models import db
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # 創建 60 條測試訊息
    for i in range(60):
        msg = ChatMessage(
            sender_id=user1.user_id if i % 2 == 0 else user2.user_id,
            receiver_id=user2.user_id if i % 2 == 0 else user1.user_id,
            content=f'Test message {i}',
            timestamp=datetime.utcnow() + timedelta(seconds=i)
        )
        db.session.add(msg)
    db.session.commit()
    
    # 測試第一頁
    response = client.get(
        f'/chat/{user2.user_id}/messages?limit=50&offset=0',
        headers=auth_headers(user1.user_id)
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'messages' in data
    assert 'total' in data
    assert 'has_more' in data
    assert data['total'] == 60
    assert len(data['messages']) == 50
    assert data['has_more'] == True
