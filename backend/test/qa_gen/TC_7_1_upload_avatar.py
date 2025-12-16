"""
TC 7.1 - 頭像上傳測試
測試說明: 測試用戶頭像上傳功能
Story: 7.1 - 上傳用戶頭像
"""

import pytest
import io
import os
from PIL import Image
from models.user import User
from models import db


def create_test_image(format='JPEG', size=(100, 100), color='red'):
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


def get_auth_token(client, email='test@example.com', password='password123'):
    """取得認證 token"""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    data = response.get_json()
    return data.get('access_token')


class TestAvatarUpload:
    """頭像上傳測試類別"""
    
    def test_upload_avatar_jpg_success(self, client, test_app):
        """測試：成功上傳 JPG 格式頭像"""
        with test_app.app_context():
            # 建立測試用戶
            user = create_test_user()
            token = get_auth_token(client)
            
            # 準備測試圖片
            img_data = create_test_image(format='JPEG')
            
            # 上傳頭像
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200, "上傳應該成功"
            data = response.get_json()
            assert 'url' in data, "回應應包含 URL"
            assert 'message' in data
            assert data['message'] == '上傳成功'
    
    def test_upload_avatar_png_success(self, client, test_app):
        """測試：成功上傳 PNG 格式頭像"""
        with test_app.app_context():
            user = create_test_user(email='png@example.com')
            token = get_auth_token(client, email='png@example.com')
            
            img_data = create_test_image(format='PNG')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.png', 'image/png')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'url' in data
    
    def test_upload_avatar_gif_success(self, client, test_app):
        """測試：成功上傳 GIF 格式頭像"""
        with test_app.app_context():
            user = create_test_user(email='gif@example.com')
            token = get_auth_token(client, email='gif@example.com')
            
            img_data = create_test_image(format='GIF')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.gif', 'image/gif')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'url' in data
    
    def test_upload_avatar_file_too_large(self, client, test_app):
        """測試：檔案大小超過 2MB 返回錯誤"""
        with test_app.app_context():
            user = create_test_user(email='large@example.com')
            token = get_auth_token(client, email='large@example.com')
            
            # 建立超過 2MB 的圖片（使用大尺寸和隨機噪點確保檔案大小）
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
                data={'image': (img_io, 'large_avatar.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400, "應該返回 400 錯誤"
            data = response.get_json()
            assert 'error' in data
            assert '超過限制' in data['error'] or '大小' in data['error']
    
    def test_upload_avatar_unsupported_format(self, client, test_app):
        """測試：不支援的檔案格式返回錯誤"""
        with test_app.app_context():
            user = create_test_user(email='bmp@example.com')
            token = get_auth_token(client, email='bmp@example.com')
            
            # 建立 BMP 格式圖片（不支援）
            img_data = create_test_image(format='BMP')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.bmp', 'image/bmp')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400, "應該返回 400 錯誤"
            data = response.get_json()
            assert 'error' in data
            assert '不支持' in data['error'] or '類型' in data['error']
    
    def test_upload_avatar_without_login(self, client, test_app):
        """測試：未登入用戶無法上傳（401）"""
        with test_app.app_context():
            img_data = create_test_image(format='JPEG')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.jpg', 'image/jpeg')},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 401, "應該返回 401 未授權"
    
    def test_upload_avatar_no_file(self, client, test_app):
        """測試：沒有選擇檔案返回錯誤"""
        with test_app.app_context():
            user = create_test_user(email='nofile@example.com')
            token = get_auth_token(client, email='nofile@example.com')
            
            response = client.post(
                '/api/upload/image',
                data={},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400, "應該返回 400 錯誤"
            data = response.get_json()
            assert 'error' in data
            assert '沒有選擇' in data['error'] or '文件' in data['error']
    
    def test_upload_avatar_updates_user_profile(self, client, test_app):
        """測試：上傳後 User.profile_picture 欄位正確更新"""
        with test_app.app_context():
            user = create_test_user(email='update@example.com')
            user_id = user.user_id
            token = get_auth_token(client, email='update@example.com')
            
            # 確認初始沒有頭像
            assert user.profile_picture is None
            
            # 上傳頭像
            img_data = create_test_image(format='JPEG')
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200
            data = response.get_json()
            uploaded_url = data['url']
            
            # 更新用戶資料
            client.put(
                '/api/users/profile',
                json={'profile_picture': uploaded_url},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            # 驗證資料庫中的 profile_picture 已更新
            updated_user = db.session.get(User, user_id)
            assert updated_user.profile_picture == uploaded_url, "profile_picture 應該已更新"
    
    def test_upload_avatar_file_saved_correctly(self, client, test_app):
        """測試：檔案正確儲存到 uploads 目錄"""
        with test_app.app_context():
            user = create_test_user(email='filesave@example.com')
            token = get_auth_token(client, email='filesave@example.com')
            
            img_data = create_test_image(format='JPEG')
            response = client.post(
                '/api/upload/image',
                data={'image': (img_data, 'test_avatar.jpg', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 200
            data = response.get_json()
            
            # 檢查檔案是否存在
            filename = data['filename']
            file_path = os.path.join('uploads', filename)
            assert os.path.exists(file_path), "檔案應該存在於 uploads 目錄"
            
            # 清理測試檔案
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def test_upload_avatar_empty_file(self, client, test_app):
        """測試：空檔案返回錯誤"""
        with test_app.app_context():
            user = create_test_user(email='empty@example.com')
            token = get_auth_token(client, email='empty@example.com')
            
            # 建立空檔案
            empty_file = io.BytesIO(b'')
            
            response = client.post(
                '/api/upload/image',
                data={'image': (empty_file, '', 'image/jpeg')},
                headers={'Authorization': f'Bearer {token}'},
                content_type='multipart/form-data'
            )
            
            assert response.status_code == 400, "應該返回 400 錯誤"
