"""
TC 2.8.4: 取消後狀態驗證
測試說明: 測試活動取消後，狀態正確設定為 'cancelled' 且可被正確查詢
Given: 用戶已登入且為活動創建者
When: 取消活動後查詢活動詳情
Then: 活動狀態為 'cancelled'，且其他資訊保持不變
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
def test_activity(test_app, creator_user):
    """創建測試活動"""
    with test_app.app_context():
        activity = Activity(
            creator_id=creator_user,
            title='狀態驗證測試活動',
            category='hiking',
            location='陽明山國家公園',
            date=date.today() + timedelta(days=10),
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=11),
            max_participants=15,
            description='用於測試取消狀態的活動',
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        
        # 返回活動的所有原始資訊用於驗證
        return {
            'activity_id': activity.activity_id,
            'title': activity.title,
            'category': activity.category,
            'location': activity.location,
            'max_participants': activity.max_participants,
            'description': activity.description
        }


def test_cancelled_status_in_database(client, creator_headers, test_activity, test_app):
    """測試取消後資料庫中狀態正確"""
    
    activity_id = test_activity['activity_id']
    
    # Act: 取消活動
    response = client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 操作成功
    assert response.status_code == 200
    
    # 驗證資料庫中的狀態
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        assert activity is not None, "Activity should exist"
        assert activity.status == 'cancelled', \
            f"Database status should be 'cancelled', got '{activity.status}'"


def test_cancelled_status_in_api_response(client, creator_headers, test_activity):
    """測試 GET API 回傳正確的 cancelled 狀態"""
    
    activity_id = test_activity['activity_id']
    
    # Act: 取消活動
    client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Act: 查詢活動
    response = client.get(
        f'/api/activities/{activity_id}',
        headers=creator_headers
    )
    
    # Assert: API 回傳正確狀態
    assert response.status_code == 200
    data = response.json
    
    # 處理不同的回應格式
    activity_data = data if 'status' in data else data.get('activity', {})
    
    assert activity_data.get('status') == 'cancelled', \
        f"API should return status 'cancelled', got '{activity_data.get('status')}'"


def test_other_fields_unchanged_after_cancel(client, creator_headers, test_activity, test_app):
    """測試取消活動後其他欄位保持不變"""
    
    activity_id = test_activity['activity_id']
    original_data = test_activity
    
    # Act: 取消活動
    client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 驗證其他欄位未改變
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        
        assert activity.title == original_data['title'], "Title should not change"
        assert activity.category == original_data['category'], "Category should not change"
        assert activity.location == original_data['location'], "Location should not change"
        assert activity.max_participants == original_data['max_participants'], \
            "Max participants should not change"
        assert activity.description == original_data['description'], "Description should not change"


def test_status_transition_from_active_to_cancelled(client, creator_headers, test_activity, test_app):
    """測試狀態從 active 轉換到 cancelled 的完整流程"""
    
    activity_id = test_activity['activity_id']
    
    # 驗證初始狀態
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        assert activity.status == 'active', "Initial status should be 'active'"
    
    # Act: 取消活動
    response = client.put(
        f'/api/activities/{activity_id}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 狀態轉換成功
    assert response.status_code == 200
    
    with test_app.app_context():
        activity = Activity.query.get(activity_id)
        assert activity.status == 'cancelled', \
            f"Status should transition to 'cancelled', got '{activity.status}'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
