"""
TC 2.1.3: 未登入無法建立活動
測試說明: 未登入狀態下，建立活動 API 應回傳 401 Unauthorized
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

def test_create_activity_without_login():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # 準備活動資料
            activity_data = {
                "title": "未登入測試活動",
                "type": "其他",
                "location": "中央大學",
                "start_date": "2025-12-10",
                "end_date": "2025-12-10",
                "max_members": 5
            }
            # 不帶 JWT token 發送 POST 請求
            response = client.post("/api/activities", json=activity_data)
            expected_status = 401
            actual_status = response.status_code
            # print(f"[未登入建立活動] 預期: {expected_status}, 實際: {actual_status}")
            assert actual_status == expected_status
