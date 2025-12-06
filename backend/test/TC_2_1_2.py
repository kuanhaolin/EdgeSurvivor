"""
TC 2.1.2: 開始時間不可早於結束時間
測試開始日期必須早於或等於結束日期
測試資料: "2025-01-01", "2025-01-02":201
          "2026-01-01", "2025-01-01":400
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User


@pytest.fixture
def client():
    """建立測試客戶端"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # 創建測試用戶
            user = User(
                name='testuser',
                email='test@test.com',
                gender='male',
                age=25
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            yield client
            db.drop_all()


@pytest.fixture
def auth_headers(client):
    """取得認證 token"""
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


# 測試資料
test_data = [
    ('2025-01-01', '2025-01-02', 201),
    ('2026-01-01', '2025-01-01', 400),
]


@pytest.mark.parametrize("start_date,end_date,expected_status", test_data)
def test_date_range_validation(client, auth_headers, start_date, end_date, expected_status):
    """測試日期範圍驗證 - 開始日期必須早於或等於結束日期"""
    
    # 準備請求資料
    request_data = {
        'title': '測試活動',
        'type': '其他',
        'location': '測試地點',
        'start_date': start_date,
        'end_date': end_date,
        'max_members': 5
    }
    
    # 發送請求
    response = client.post('/api/activities',
        headers=auth_headers,
        json=request_data
    )
    
    # 取得實際狀態碼
    actual_status = response.status_code
    
    # 顯示對比資訊
    # print(f'\n測試資料: start_date="{start_date}", end_date="{end_date}"')
    # print(f'預期狀態碼: {expected_status}')
    # print(f'實際狀態碼: {actual_status}')
    # print(f'結果: {"✓ 通過" if actual_status == expected_status else "✗ 失敗"}')
    
    # 驗證狀態碼
    assert actual_status == expected_status, f"狀態碼不符 - start_date={start_date}, end_date={end_date}"
    
    # 驗證回應資料內容
    data = response.get_json()
    if expected_status == 400:
        assert 'error' in data, f"錯誤回應應該包含 error 欄位"
    else:
        # 成功創建，檢查日期
        if 'activity' in data:
            assert data['activity']['start_date'] == start_date
            assert data['activity']['end_date'] == end_date
        else:
            # 直接返回活動資料
            pass
