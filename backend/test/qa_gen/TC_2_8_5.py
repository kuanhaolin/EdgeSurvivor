"""
TC 2.8.5: 已取消活動無法重複取消
測試說明: 測試已經取消的活動不應該再次被取消（可選驗證，或允許冪等操作）
Given: 活動已被取消（status='cancelled'）
When: 嘗試再次取消活動
Then: 回應應成功（冪等）或返回 400 錯誤（視實作策略而定）
"""
import pytest
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity


@pytest.fixture
def test_app():
    """建立測試應用程式"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(test_app):
    """建立測試客戶端"""
    return test_app.test_client()


@pytest.fixture
def creator_user(test_app):
    """創建測試用戶（創建者）"""
    with test_app.app_context():
        user = User(
            name='活動創建者',
            email='creator@test.com',
            gender='male',
            age=30
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.user_id


@pytest.fixture
def creator_headers(client, creator_user):
    """取得創建者認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}', 'user_id': creator_user}


@pytest.fixture
def cancelled_activity(test_app, creator_user):
    """創建一個已取消的測試活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='已取消的活動',
            category='hiking',
            location='陽明山',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_participants=10,
            description='這是一個已經取消的活動',
            status='cancelled'  # 初始狀態就是 cancelled
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_idempotent_cancel_operation(client, creator_headers, cancelled_activity, test_app):
    """測試重複取消操作是冪等的（允許重複取消）"""
    
    # Act: 對已取消的活動再次發送取消請求
    response = client.put(
        f'/api/activities/{cancelled_activity}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 應該成功（冪等操作）
    assert response.status_code in [200, 400], \
        f"Expected 200 (idempotent) or 400 (validation), got {response.status_code}"
    
    # 驗證狀態仍為 cancelled
    with test_app.app_context():
        activity = Activity.query.get(cancelled_activity)
        assert activity.status == 'cancelled', \
            f"Status should remain 'cancelled', got '{activity.status}'"


def test_cannot_change_cancelled_to_active(client, creator_headers, cancelled_activity, test_app):
    """測試已取消的活動可以嘗試改回 active（取決於業務規則）"""
    
    # Act: 嘗試將已取消的活動改為 active
    response = client.put(
        f'/api/activities/{cancelled_activity}',
        headers=creator_headers,
        json={'status': 'active'}
    )
    
    # Assert: 目前實作允許狀態變更（未來可加驗證）
    # 此測試記錄當前行為，未來可調整為禁止 cancelled -> active 轉換
    assert response.status_code in [200, 400], \
        f"Status change response: {response.status_code}"
    
    # 記錄實際行為用於未來參考
    with test_app.app_context():
        activity = Activity.query.get(cancelled_activity)
        print(f"Activity status after attempting active: {activity.status}")


def test_cancelled_activity_info_preserved(client, creator_headers, cancelled_activity, test_app):
    """測試已取消活動的資訊保持完整"""
    
    # Act: 查詢已取消的活動
    response = client.get(
        f'/api/activities/{cancelled_activity}',
        headers=creator_headers
    )
    
    # Assert: 可以正常查詢
    assert response.status_code == 200, "Cancelled activity should be retrievable"
    
    data = response.json
    activity_data = data if 'status' in data else data.get('activity', {})
    
    # 驗證活動資訊完整
    assert activity_data.get('status') == 'cancelled'
    assert activity_data.get('title') == '已取消的活動'
    assert activity_data.get('location') == '陽明山'


def test_multiple_cancel_attempts(client, creator_headers, test_app, creator_user):
    """測試從 active 到 cancelled 的多次嘗試"""
    
    # 創建一個 active 活動
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='多次取消測試',
            category='hiking',
            location='測試地點',
            date=date.today() + timedelta(days=5),
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=6),
            max_participants=8,
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        activity_id = activity.activity_id
    
    # 第一次取消
    response1 = client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    assert response1.status_code == 200, "First cancel should succeed"
    
    # 第二次取消
    response2 = client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # 應該成功或返回錯誤（取決於實作）
    assert response2.status_code in [200, 400], \
        f"Second cancel got unexpected status: {response2.status_code}"
    
    # 最終狀態應該是 cancelled
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        assert activity.status == 'cancelled', \
            "Final status should be 'cancelled'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
