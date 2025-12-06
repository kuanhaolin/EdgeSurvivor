"""
TC 2.1.1: 活動欄位必填驗證
測試創建活動時必填欄位驗證（標題、類型、地點、開始日期、結束日期）
測試資料: "期末考", "其他", "中央大學", "2025-12-10", "2025-12-10", 5:201
          "放寒假", "", "", "", "", 5:400
          "開學", "其他", "", "", "", 5:400
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
    ('期末考', '其他', '中央大學', '2025-12-10', '2025-12-10', 5, 201),
    ('放寒假', '', '', '', '', 5, 400),
    ('開學', '其他', '', '', '', 5, 400),
]


@pytest.mark.parametrize("title,type_,location,start_date,end_date,max_members,expected_status", test_data)
def test_activity_required_fields(client, auth_headers, title, type_, location, start_date, end_date, max_members, expected_status):
    """測試活動必填欄位驗證 - 使用測試資料驗證是否符合預期"""
    
    # 準備請求資料
    request_data = {
        'title': title,
        'type': type_,
        'location': location,
        'start_date': start_date,
        'end_date': end_date,
        'max_members': max_members
    }
    
    # 發送請求
    response = client.post('/api/activities',
        headers=auth_headers,
        json=request_data
    )
    
    # 取得實際狀態碼
    actual_status = response.status_code
    
    # 顯示對比資訊
    # print(f'\n測試資料: title="{title}", type="{type_}", location="{location}", start_date="{start_date}", end_date="{end_date}", max_members={max_members}')
    # print(f'預期狀態碼: {expected_status}')
    # print(f'實際狀態碼: {actual_status}')
    # print(f'結果: {"✓ 通過" if actual_status == expected_status else "✗ 失敗"}')
    
    # 驗證狀態碼
    assert actual_status == expected_status, f"狀態碼不符 - title={title}"
    
    # 驗證回應資料內容
    data = response.get_json()
    if expected_status == 400:
        assert 'error' in data, f"錯誤回應應該包含 error 欄位"
    else:
        # 檢查回應結構
        if 'activity' in data:
            assert data['activity']['title'] == title
        else:
            assert data['title'] == title
