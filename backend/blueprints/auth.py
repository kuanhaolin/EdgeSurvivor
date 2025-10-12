from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db
from models.user import User
from werkzeug.security import check_password_hash
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """驗證電子郵件格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """驗證密碼強度"""
    if len(password) < 6:
        return False, "密碼長度至少需要 6 個字元"
    return True, "密碼格式正確"

@auth_bp.route('/register', methods=['POST'])
def register():
    """使用者註冊"""
    try:
        data = request.get_json()
        
        # 檢查必填欄位
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # 驗證電子郵件格式
        if not validate_email(email):
            return jsonify({'error': '電子郵件格式不正確'}), 400
        
        # 驗證密碼
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # 檢查電子郵件是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '此電子郵件已被註冊'}), 400
        
        # 建立新使用者
        user = User(
            name=name,
            email=email,
            gender=data.get('gender'),
            age=data.get('age'),
            location=data.get('location'),
            bio=data.get('bio', ''),
            privacy_setting=data.get('privacy_setting', 'public')
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # 建立 JWT Token - 使用字串格式的 user_id
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        return jsonify({
            'message': '註冊成功',
            'user': user.to_dict(include_private=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '註冊失敗，請稍後再試'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """使用者登入"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': '請提供電子郵件和密碼'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # 查找使用者
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': '電子郵件或密碼錯誤'}), 401
        
        if not user.is_active:
            return jsonify({'error': '帳號已被停用'}), 401
        
        # 更新最後上線時間
        user.update_last_seen()
        
        # 建立 JWT Token - 使用字串格式的 user_id
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        return jsonify({
            'message': '登入成功',
            'user': user.to_dict(include_private=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': '登入失敗，請稍後再試'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新 Access Token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))  # 轉換回整數
        
        if not user or not user.is_active:
            return jsonify({'error': '無效的使用者'}), 401
        
        new_token = create_access_token(identity=str(user.user_id))  # 使用字串
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': '刷新 Token 失敗'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """取得當前使用者資訊"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))  # 轉換回整數
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        return jsonify({
            'user': user.to_dict(include_private=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': '取得使用者資訊失敗'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """使用者登出"""
    # 在實際應用中，您可能需要將 Token 加入黑名單
    return jsonify({'message': '登出成功'}), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密碼"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))  # 轉換回整數
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': '請提供舊密碼和新密碼'}), 400
        
        # 驗證舊密碼
        if not user.check_password(old_password):
            return jsonify({'error': '舊密碼錯誤'}), 400
        
        # 驗證新密碼
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # 更新密碼
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': '密碼修改成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '密碼修改失敗'}), 500