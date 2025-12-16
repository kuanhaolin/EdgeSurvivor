"""
TC_2_6_A5: 後端：未登入用戶無法訪問（401 錯誤）
測試說明: 測試未提供認證 token 時返回 401 錯誤
"""
import pytest
from flask import json

def test_get_activities_without_auth_token(client, test_app):
    """測試未登入用戶無法訪問活動列表"""
    with test_app.app_context():
        # 不提供 Authorization header
        response = client.get('/api/activities?type=created')
        
        assert response.status_code == 401  # Unauthorized


def test_get_joined_activities_without_auth_token(client, test_app):
    """測試未登入用戶無法訪問參加的活動列表"""
    with test_app.app_context():
        response = client.get('/api/activities?type=joined')
        
        assert response.status_code == 401  # Unauthorized


def test_get_activities_with_invalid_token(client, test_app):
    """測試使用無效 token 無法訪問"""
    with test_app.app_context():
        response = client.get(
            '/api/activities?type=created',
            headers={'Authorization': 'Bearer invalid_token_12345'}
        )
        
        # 無效 token 返回 401 或 422 都是合理的
        assert response.status_code in [401, 422]
