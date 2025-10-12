from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

# 上傳配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# 確保上傳目錄存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """檢查文件類型是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上傳圖片"""
    try:
        user_id = get_jwt_identity()
        
        # 檢查是否有文件
        if 'image' not in request.files:
            return jsonify({'error': '沒有選擇文件'}), 400
        
        file = request.files['image']
        
        # 檢查文件名
        if file.filename == '':
            return jsonify({'error': '沒有選擇文件'}), 400
        
        # 檢查文件類型
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件類型，只允許 PNG、JPG、JPEG、GIF、WEBP'}), 400
        
        # 檢查文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'文件大小超過限制（最大 {MAX_FILE_SIZE // (1024*1024)}MB）'}), 400
        
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{user_id}_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        
        # 保存文件
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 返回文件 URL
        # 注意：在生產環境中應該使用完整的 URL，例如配置的 CDN 地址
        url = f"/uploads/{filename}"
        
        return jsonify({
            'message': '上傳成功',
            'url': url,
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"上傳失敗: {str(e)}")
        return jsonify({'error': '上傳失敗'}), 500

@upload_bp.route('/images', methods=['POST'])
@jwt_required()
def upload_multiple_images():
    """上傳多張圖片"""
    try:
        user_id = get_jwt_identity()
        
        # 檢查是否有文件
        if 'images' not in request.files:
            return jsonify({'error': '沒有選擇文件'}), 400
        
        files = request.files.getlist('images')
        
        if not files or len(files) == 0:
            return jsonify({'error': '沒有選擇文件'}), 400
        
        uploaded_urls = []
        
        for file in files:
            # 檢查文件名
            if file.filename == '':
                continue
            
            # 檢查文件類型
            if not allowed_file(file.filename):
                continue
            
            # 檢查文件大小
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                continue
            
            # 生成唯一文件名
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{user_id}_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            
            # 保存文件
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # 添加到結果列表
            url = f"/uploads/{filename}"
            uploaded_urls.append(url)
        
        if len(uploaded_urls) == 0:
            return jsonify({'error': '沒有成功上傳任何文件'}), 400
        
        return jsonify({
            'message': f'成功上傳 {len(uploaded_urls)} 張圖片',
            'urls': uploaded_urls
        }), 200
        
    except Exception as e:
        print(f"批量上傳失敗: {str(e)}")
        return jsonify({'error': '批量上傳失敗'}), 500
