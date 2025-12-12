"""
TC_3.1.5: 查看用戶資料
測試說明: 測試是否顯示用戶資料
"""
import pytest
import json
from models.user import User
from models import db
from flask_jwt_extended import create_access_token

def test_view_user_profile(client, test_app):
    """測試查看用戶資料"""
    with test_app.app_context():
        # 創建測試用戶
        target_user = User(
            name='測試用戶',
            email='target@test.com',
            gender='male',
            age=28,
            location='台北市',
            bio='這是個人簡介',
            interests=json.dumps(['登山', '攝影']),  # 轉成 JSON 字串
            is_active=True
        )
        target_user.set_password('password123')
        
        current_user = User(
            name='當前用戶',
            email='current@test.com',
            is_active=True
        )
        current_user.set_password('password123')
        
        db.session.add_all([target_user, current_user])
        db.session.commit()
        
        token = create_access_token(identity=str(current_user.user_id))
        target_user_id = target_user.user_id
    
    # 測試查看用戶資料
    response = client.get(
        f'/api/users/{target_user_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    
    # 驗證回應結構
    assert 'user' in data
    user_data = data['user']
    
    # 驗證用戶資料完整性
    assert user_data['name'] == '測試用戶'
    assert user_data['gender'] == 'male'
    assert user_data['age'] == 28
    assert user_data['location'] == '台北市'
    assert user_data['bio'] == '這是個人簡介'
    assert 'interests' in user_data
    assert '登山' in user_data['interests']
    assert '攝影' in user_data['interests']
    
    # 驗證統計資料存在
    assert 'stats' in user_data
    assert 'activities' in user_data['stats']
    assert 'matches' in user_data['stats']
    assert 'reviews' in user_data['stats']
