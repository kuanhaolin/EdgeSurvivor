"""
TC 7.2 - 活動圖片上傳測試
測試說明: 測試活動封面圖片上傳功能
Story: 7.2 - 上傳活動圖片
"""

import pytest
import io
import os
from PIL import Image
from datetime import datetime, timedelta
from models.user import User
from models.activity import Activity
from models import db


def create_test_image(format='JPEG', size=(100, 100), color='blue'):
    """建立測試用圖片"""
    img = Image.new('RGB', size, color=color)
    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)
    return img_io


def create_test_user(email='test@example.com', password='password123'):
    """建立測試用戶"""
    user = User(
        email=email,
        name='Test User'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def create_test_activity(creator_id, title='Test Activity'):
    """建立測試活動"""
    activity = Activity(
        creator_id=creator_id,
        title=title,
        category='hiking',
        location='Test Location',
        date=datetime.now().date() + timedelta(days=7),
        start_date=datetime.now().date() + timedelta(days=7),
        max_participants=5,
        description='Test activity description',
        status='open'
    )
    db.session.add(activity)
    db.session.commit()
    return activity


def get_auth_token(client, email='test@example.com', password='password123'):
    """取得認證 token"""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    data = response.get_json()
    return data.get('access_token')


class TestActivityImageUpload:
    """活動圖片上傳測試類別"""
    
    def test_upload_activity_image_jpg_success(self, client, test_app):
        """
        測試：成功上傳 JPG 格式活動圖片
        
        Given: 已登入用戶和已建立的活動
        When: 上傳 JPG 格式圖片
        Then: 上傳成功並返回圖片 URL
        """
        with test_app.app_context():
            # 建立測試用戶和活動
            user = create_test_user()
            activity = create_test_activity(creator_id=user.user_id)
            token = get_auth_token(client)
            
            # 準備測試圖片
            img_data = create_test_image(format='JPEG')
            
            # 上傳活動圖片
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'activity_cover.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200, "上傳應該成功"
            data = response.get_json()
            assert 'url' in data, "回應應包含 URL"
            assert 'message' in data
            assert data['message'] == '上傳成功'
    
    def test_upload_activity_image_png_success(self, client, test_app):
        """
        測試：成功上傳 PNG 格式活動圖片
        
        Given: 已登入用戶
        When: 上傳 PNG 格式圖片
        Then: 上傳成功
        """
        with test_app.app_context():
            user = create_test_user(email='png@example.com')
            token = get_auth_token(client, email='png@example.com')
            
            img_data = create_test_image(format='PNG')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'activity_cover.png', 'image/png')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'url' in data
    
    def test_upload_activity_image_file_too_large(self, client, test_app):
        """
        測試：檔案大小超過 2MB 返回錯誤
        
        Given: 已登入用戶
        When: 上傳超過 2MB 的圖片檔案
        Then: 返回 400 錯誤
        """
        with test_app.app_context():
            user = create_test_user(email='large@example.com')
            token = get_auth_token(client, email='large@example.com')
            
            # 建立超過 2MB 的圖片
            from PIL import ImageDraw
            import random
            
            img = Image.new('RGB', (4000, 4000), color='white')
            draw = ImageDraw.Draw(img)
            # 添加隨機噪點增加檔案大小
            for _ in range(50000):
                x, y = random.randint(0, 3999), random.randint(0, 3999)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
            
            img_io = io.BytesIO()
            img.save(img_io, 'JPEG', quality=95)
            img_io.seek(0)
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_io, 'large_activity.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400, "應該返回 400 錯誤"
            data = response.get_json()
            assert 'error' in data
            assert '超過限制' in data['error'] or '大小' in data['error']
    
    def test_upload_activity_image_unsupported_format(self, client, test_app):
        """
        測試：不支援的檔案格式返回錯誤
        
        Given: 已登入用戶
        When: 上傳 BMP 格式（不支援）
        Then: 返回 400 錯誤
        """
        with test_app.app_context():
            user = create_test_user(email='bmp@example.com')
            token = get_auth_token(client, email='bmp@example.com')
            
            # 建立 BMP 格式圖片
            img_data = create_test_image(format='BMP')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'activity.bmp', 'image/bmp')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
    
    def test_upload_activity_image_unauthorized(self, client, test_app):
        """
        測試：未登入用戶無法上傳圖片
        
        Given: 未登入用戶
        When: 嘗試上傳活動圖片
        Then: 返回 401 未授權錯誤
        """
        with test_app.app_context():
            img_data = create_test_image(format='JPEG')
            
            # 不提供 token
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'activity.jpg', 'image/jpeg')},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 401
    
    def test_upload_activity_image_no_file(self, client, test_app):
        """
        測試：未選擇檔案返回錯誤
        
        Given: 已登入用戶
        When: 提交空的上傳請求
        Then: 返回 400 錯誤
        """
        with test_app.app_context():
            user = create_test_user(email='nofile@example.com')
            token = get_auth_token(client, email='nofile@example.com')
            
            response = client.post(
                '/api/upload/image',
                data={},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
            assert '沒有選擇文件' in data['error'] or '文件' in data['error']
    
    def test_update_activity_with_cover_image(self, client, test_app):
        """
        測試：上傳後更新活動封面圖片欄位
        
        Given: 已建立的活動和已上傳的圖片
        When: 更新活動的 cover_image 欄位
        Then: 活動記錄成功更新
        """
        with test_app.app_context():
            # 建立測試用戶和活動
            user = create_test_user(email='update@example.com')
            activity = create_test_activity(creator_id=user.user_id, title='Activity to Update')
            token = get_auth_token(client, email='update@example.com')
            
            # 上傳圖片
            img_data = create_test_image(format='JPEG')
            upload_response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'cover.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert upload_response.status_code == 200
            upload_data = upload_response.get_json()
            image_url = upload_data['url']
            
            # 更新活動封面圖片
            update_response = client.put(
                f'/api/activities/{activity.activity_id}',
                json={'cover_image': image_url},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert update_response.status_code == 200
            
            # 驗證活動記錄已更新
            get_response = client.get(
                f'/api/activities/{activity.activity_id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert get_response.status_code == 200
            activity_data = get_response.get_json()['activity']
            assert activity_data['cover_image'] == image_url
    
    def test_only_creator_can_update_activity_image(self, client, test_app):
        """
        測試：只有活動建立者可以更新活動圖片
        
        Given: 活動由用戶A建立
        When: 用戶B嘗試更新活動圖片
        Then: 返回 403 權限錯誤
        """
        with test_app.app_context():
            # 建立兩個用戶
            creator = create_test_user(email='creator@example.com')
            other_user = create_test_user(email='other@example.com', password='password456')
            
            # 用戶A建立活動
            activity = create_test_activity(creator_id=creator.user_id)
            
            # 用戶B取得 token
            other_token = get_auth_token(client, email='other@example.com', password='password456')
            
            # 用戶B上傳圖片
            img_data = create_test_image(format='JPEG')
            upload_response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'cover.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {other_token}'},
                content_type='multipart/form-data'
            )
            image_url = upload_response.get_json()['url']
            
            # 用戶B嘗試更新活動圖片
            update_response = client.put(
                f'/api/activities/{activity.activity_id}',
                json={'cover_image': image_url},
                headers={'Authorization': f'Bearer {other_token}'}
            )
            
            assert update_response.status_code == 403, "應該返回 403 權限錯誤"
            data = update_response.get_json()
            assert 'error' in data
            assert '權限' in data['error'] or '無法' in data['error']
    
    def test_upload_and_display_activity_image(self, client, test_app):
        """
        測試：完整流程 - 上傳圖片並在活動詳情中顯示
        
        Given: 已建立的活動
        When: 上傳封面圖片並更新活動
        Then: 查詢活動詳情時返回正確的圖片 URL
        """
        with test_app.app_context():
            user = create_test_user(email='flow@example.com')
            activity = create_test_activity(creator_id=user.user_id, title='Activity with Image')
            token = get_auth_token(client, email='flow@example.com')
            
            # 步驟1: 上傳圖片
            img_data = create_test_image(format='JPEG', size=(800, 600))
            upload_response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'beautiful_mountain.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            image_url = upload_response.get_json()['url']
            
            # 步驟2: 更新活動封面圖片
            client.put(
                f'/api/activities/{activity.activity_id}',
                json={'cover_image': image_url},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            # 步驟3: 查詢活動詳情
            get_response = client.get(
                f'/api/activities/{activity.activity_id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            activity_data = get_response.get_json()['activity']
            assert activity_data['cover_image'] == image_url, "活動詳情應返回正確的封面圖片 URL"
            assert activity_data['title'] == 'Activity with Image'


class TestActivityImageStorage:
    """活動圖片儲存測試"""
    
    def test_uploaded_image_file_exists(self, client, test_app):
        """
        測試：上傳的圖片檔案實際儲存到檔案系統
        
        Given: 已上傳圖片
        When: 檢查檔案系統
        Then: 檔案應存在於 uploads/ 目錄
        """
        with test_app.app_context():
            user = create_test_user(email='storage@example.com')
            token = get_auth_token(client, email='storage@example.com')
            
            img_data = create_test_image(format='JPEG')
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'activity_test.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            data = response.get_json()
            file_url = data['url']
            
            # 從 URL 提取檔名（假設格式為 /uploads/filename）
            filename = file_url.split('/')[-1]
            file_path = os.path.join('uploads', filename)
            
            # 驗證檔案存在
            assert os.path.exists(file_path), f"檔案應存在於 {file_path}"
