"""
測試活動管理 API

測試範圍：
- 建立活動
- 查詢活動
- 更新活動
- 刪除活動
"""

import pytest
from datetime import date, datetime
from models.activity import Activity


class TestActivityManagement:
    """活動管理測試類"""
    
    def test_create_activity(self, client, auth_headers, session):
        """測試建立活動"""
        activity_data = {
            'title': '陽明山一日遊',
            'date': '2025-12-25',
            'location': '陽明山國家公園',
            'description': '一起去爬山吧！',
            'category': 'outdoor',
            'max_participants': 10,
            'cost': 300
        }
        
        response = client.post('/api/activities', 
            json=activity_data, 
            headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == activity_data['title']
        assert data['location'] == activity_data['location']
        assert 'activity_id' in data
        
        # 驗證資料庫
        activity = session.query(Activity).filter_by(
            title=activity_data['title']
        ).first()
        assert activity is not None
    
    def test_create_activity_without_auth(self, client):
        """測試未認證建立活動應該失敗"""
        activity_data = {
            'title': '測試活動',
            'date': '2025-12-25',
            'location': '台北'
        }
        
        response = client.post('/api/activities', json=activity_data)
        assert response.status_code == 401
    
    def test_get_activity_list(self, client, sample_activity):
        """測試取得活動列表"""
        response = client.get('/api/activities')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_activity_detail(self, client, sample_activity):
        """測試取得活動詳情"""
        activity_id = sample_activity.activity_id
        
        response = client.get(f'/api/activities/{activity_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['activity_id'] == activity_id
        assert data['title'] == sample_activity.title
    
    def test_get_nonexistent_activity(self, client):
        """測試取得不存在的活動"""
        response = client.get('/api/activities/99999')
        assert response.status_code == 404
    
    def test_update_activity_by_creator(self, client, auth_headers, sample_activity):
        """測試創建者更新活動"""
        activity_id = sample_activity.activity_id
        update_data = {
            'title': '更新後的標題',
            'description': '更新後的描述'
        }
        
        response = client.put(f'/api/activities/{activity_id}',
            json=update_data,
            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == update_data['title']
        assert data['description'] == update_data['description']
    
    def test_delete_activity_by_creator(self, client, auth_headers, sample_activity, session):
        """測試創建者刪除活動"""
        activity_id = sample_activity.activity_id
        
        response = client.delete(f'/api/activities/{activity_id}',
            headers=auth_headers)
        
        assert response.status_code == 200
        
        # 驗證活動已被刪除（或狀態改為已取消）
        activity = session.query(Activity).filter_by(
            activity_id=activity_id
        ).first()
        # 根據實際實作：可能是真刪除或軟刪除
        assert activity is None or activity.status == 'cancelled'
    
    def test_search_activities_by_location(self, client, sample_activity):
        """測試按地點搜尋活動"""
        response = client.get('/api/activities?location=台北')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # 所有結果應該包含台北
        for activity in data:
            assert '台北' in activity.get('location', '')
    
    def test_filter_activities_by_category(self, client, sample_activity):
        """測試按類別篩選活動"""
        response = client.get('/api/activities?category=leisure')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


class TestActivityParticipation:
    """活動參與測試類"""
    
    def test_join_activity(self, client, auth_headers, sample_activity):
        """測試申請加入活動"""
        activity_id = sample_activity.activity_id
        join_data = {
            'message': '我想參加這個活動！'
        }
        
        response = client.post(f'/api/activities/{activity_id}/join',
            json=join_data,
            headers=auth_headers)
        
        # 可能是 200 (直接加入) 或 201 (申請待審核)
        assert response.status_code in [200, 201]
    
    def test_join_nonexistent_activity(self, client, auth_headers):
        """測試加入不存在的活動"""
        response = client.post('/api/activities/99999/join',
            json={'message': 'test'},
            headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_leave_activity(self, client, auth_headers, sample_activity):
        """測試離開活動"""
        activity_id = sample_activity.activity_id
        
        # 先加入
        client.post(f'/api/activities/{activity_id}/join',
            json={'message': 'test'},
            headers=auth_headers)
        
        # 再離開
        response = client.post(f'/api/activities/{activity_id}/leave',
            headers=auth_headers)
        
        assert response.status_code in [200, 204]


# 測試執行指南
"""
執行活動相關測試：
    pytest tests/test_activities.py -v

執行特定測試類：
    pytest tests/test_activities.py::TestActivityManagement -v

檢查測試覆蓋率：
    pytest tests/test_activities.py --cov=blueprints.activities --cov-report=term-missing
"""
