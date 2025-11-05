"""
Pytest 配置檔案
提供測試所需的 fixtures 和設定
"""

import pytest
import sys
import os

# 將 backend 目錄加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db as _db
from models.user import User
from models.activity import Activity


@pytest.fixture(scope='session')
def app():
    """建立測試用的 Flask 應用程式"""
    app = create_app('testing')
    
    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app):
    """建立測試資料庫"""
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """為每個測試函數提供獨立的資料庫 session，並自動清理"""
    # 每個測試開始前清除所有表的資料
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    
    yield db.session
    
    # 每個測試後回滾
    db.session.rollback()


@pytest.fixture(scope='function')
def client(app):
    """提供測試客戶端"""
    return app.test_client()


@pytest.fixture
def sample_user(session):
    """建立範例使用者"""
    user = User(
        email='test@example.com',
        name='Test User',
        gender='male',
        age=25,
        location='台北市'
    )
    user.set_password('testpass123')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def sample_activity(session, sample_user):
    """建立範例活動"""
    from datetime import date, datetime
    
    activity = Activity(
        title='測試活動',
        date=date(2025, 12, 25),
        location='台北101',
        description='這是一個測試活動',
        category='leisure',
        max_participants=5,
        cost=500.0,
        status='open',
        creator_id=sample_user.user_id,
        created_at=datetime.now()
    )
    session.add(activity)
    session.commit()
    return activity


@pytest.fixture
def auth_headers(client, sample_user):
    """取得認證 headers"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    data = response.get_json()
    token = data.get('access_token')
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
