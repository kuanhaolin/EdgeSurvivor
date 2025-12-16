"""
整合測試專用的 fixtures
"""

import pytest
from flask_jwt_extended import create_access_token
from models import db
from models.user import User
from models.activity import Activity
from models.match import Match


@pytest.fixture
def db_session(test_app):
    """提供資料庫 session,每個測試後自動回滾"""
    with test_app.app_context():
        # 開始一個巢狀交易
        db.session.begin_nested()
        yield db.session
        # 測試結束後回滾
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def test_user(db_session, test_app):
    """建立測試用戶"""
    user = User(
        name='Test User',
        email='test@example.com',
        privacy_setting='public',
        location='Taipei',
        gender='male',
        age=25
    )
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()
    
    # 刷新以確保 user_id 被設定
    db_session.refresh(user)
    user_id = user.user_id
    
    # 返回 user_id 而不是 user 物件,避免 detached instance 問題
    yield user
    
    # 清理
    db_session.query(User).filter_by(user_id=user_id).delete()
    db_session.commit()


@pytest.fixture
def auth_headers(test_app, test_user):
    """建立認證標頭"""
    # Convert user_id to string to match API expectations
    access_token = create_access_token(identity=str(test_user.user_id))
    
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def multiple_users(db_session, test_app):
    """建立多個測試用戶"""
    users = []
    for i in range(5):
        user = User(
            name=f'User {i+1}',
            email=f'user{i+1}@example.com',
            privacy_setting='public',
            location='Taipei',
            gender='male' if i % 2 == 0 else 'female',
            age=20 + i
        )
        user.set_password('password123')
        db_session.add(user)
        users.append(user)
    
    db_session.commit()
    return users


@pytest.fixture
def test_activity(db_session, test_app, test_user):
    """建立測試活動"""
    from datetime import datetime, timedelta
    
    start_date = (datetime.utcnow() + timedelta(days=1)).date()
    activity = Activity(
        title='Test Activity',
        description='This is a test activity',
        location='Taipei',
        category='outdoor',
        max_participants=10,
        creator_id=test_user.user_id,
        date=start_date,
        start_date=start_date,
        start_time=(datetime.utcnow() + timedelta(days=1)).time(),
        end_time=(datetime.utcnow() + timedelta(days=1, hours=3)).time()
    )
    db_session.add(activity)
    db_session.commit()
    return activity


@pytest.fixture
def cleanup_uploads():
    """清理測試上傳的檔案"""
    import os
    import shutil
    
    yield
    
    # 測試結束後清理上傳目錄
    upload_dir = 'uploads'
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            if filename.startswith('test_'):
                file_path = os.path.join(upload_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error deleting {file_path}: {e}')
