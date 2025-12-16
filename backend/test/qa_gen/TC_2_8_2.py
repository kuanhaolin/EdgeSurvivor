"""
TC 2.8.2: 非創建者無法取消活動
測試說明: 測試非活動創建者嘗試取消活動時，應返回 403 禁止存取錯誤
Given: 用戶已登入但不是活動創建者
When: 提交 PUT /api/activities/<id> 請求，嘗試設定 status='cancelled'
Then: 回應 403 Forbidden，活動狀態不變
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
def users(test_app):
    """創建兩個測試用戶：創建者和其他用戶"""
    with test_app.app_context():
        creator = User(
            name='活動創建者',
            email='creator@test.com',
            gender='male',
            age=30
        )
        creator.set_password('password123')
        
        other_user = User(
            name='其他用戶',
            email='other@test.com',
            gender='female',
            age=25
        )
        other_user.set_password('password123')
        
        db.session.add_all([creator, other_user])
        db.session.commit()
        
        return {
            'creator_id': creator.user_id,
            'other_id': other_user.user_id
        }


@pytest.fixture
def creator_headers(client, users):
    """取得創建者認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'creator@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def other_headers(client, users):
    """取得其他用戶認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'other@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def test_activity(test_app, users):
    """創建測試活動（由創建者創建）"""
    with test_app.app_context():
        activity = Activity(
            creator_id=users['creator_id'],
            title='測試活動-權限測試',
            category='hiking',
            location='陽明山',
            date=date.today() + timedelta(days=7),
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=8),
            max_participants=10,
            description='這是一個測試用的活動',
            status='active'
        )
        db.session.add(activity)
        db.session.commit()
        return activity.activity_id


def test_non_creator_cannot_cancel_activity(client, other_headers, test_activity, test_app):
    """測試非創建者無法取消活動"""
    
    # Act: 非創建者嘗試取消活動
    response = client.put(
        f'/api/activities/{test_activity}',
        headers=other_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 應返回 403 禁止存取
    assert response.status_code == 403, \
        f"Non-creator should get 403 Forbidden, got {response.status_code}: {response.data}"
    
    # 驗證錯誤訊息
    data = response.json
    assert 'error' in data, "Response should contain error message"
    assert '權限' in data['error'] or 'permission' in data['error'].lower(), \
        f"Error message should mention permission, got: {data['error']}"
    
    # 驗證資料庫中的活動狀態未改變
    with test_app.app_context():
        activity = Activity.query.get(test_activity)
        assert activity is not None, "Activity should still exist"
        assert activity.status == 'active', \
            f"Activity status should remain 'active', got '{activity.status}'"


def test_creator_can_still_cancel_after_unauthorized_attempt(client, creator_headers, other_headers, test_activity, test_app):
    """測試非創建者失敗後，創建者仍可正常取消"""
    
    # Act: 非創建者嘗試取消（應失敗）
    response = client.put(
        f'/api/activities/{test_activity}',
        headers=other_headers,
        json={'status': 'cancelled'}
    )
    assert response.status_code == 403
    
    # Act: 創建者取消活動（應成功）
    response = client.put(
        f'/api/activities/{test_activity}',
        headers=creator_headers,
        json={'status': 'cancelled'}
    )
    
    # Assert: 創建者操作成功
    assert response.status_code == 200, \
        f"Creator should succeed, got {response.status_code}: {response.data}"
    
    # 驗證狀態已更新
    with test_app.app_context():
        activity = Activity.query.get(test_activity)
        assert activity.status == 'cancelled', \
            f"Activity should be cancelled by creator, got '{activity.status}'"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
