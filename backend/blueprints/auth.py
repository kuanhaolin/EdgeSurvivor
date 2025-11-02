from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db
from models.user import User
from werkzeug.security import check_password_hash
import re
import requests
import os
import random
import string
import pyotp
from datetime import datetime, timedelta
from utils.email import send_reset_password_email, send_welcome_email

auth_bp = Blueprint('auth', __name__)

# 臨時存儲驗證碼（實際應用中應該使用 Redis 或資料庫）
reset_codes = {}

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
        
        # 檢查是否啟用兩步驟驗證
        if user.two_factor_enabled:
            two_factor_code = data.get('two_factor_code')
            
            # 如果沒有提供驗證碼，返回需要驗證碼的狀態
            if not two_factor_code:
                return jsonify({
                    'require_2fa': True,
                    'message': '請輸入兩步驟驗證碼'
                }), 200
            
            # 驗證兩步驟驗證碼
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(two_factor_code, valid_window=1):
                return jsonify({'error': '驗證碼錯誤'}), 401
        
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

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    token = data.get('token')
    if not token:
        return jsonify({'msg': 'Missing Google token'}), 400

    # 驗證 Google ID Token
    try:
        # 使用 Google 的 tokeninfo 端點驗證 ID Token
        resp = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if resp.status_code != 200:
            return jsonify({'msg': 'Invalid Google token'}), 401

        userinfo = resp.json()

        # 檢查必要的欄位
        email = userinfo.get('email')
        name = userinfo.get('name')
        picture = userinfo.get('picture')

        if not email:
            return jsonify({'msg': 'Google account missing email'}), 400

    except Exception as e:
        print(f"Google token verification error: {e}")
        return jsonify({'msg': 'Token verification failed'}), 401

    # 檢查使用者是否已存在
    user = User.query.filter_by(email=email).first()
    if not user:
        # 新增使用者 (Google 登入不需要密碼，使用隨機密碼)
        import secrets
        user = User(
            name=name,
            email=email,
            profile_picture=picture,
            is_verified=True,
            is_active=True
        )
        # 設定一個隨機密碼 (Google 登入用戶不會使用)
        user.set_password(secrets.token_urlsafe(32))
        db.session.add(user)
        db.session.commit()

    # 建立 JWT Token
    access_token = create_access_token(identity=str(user.user_id))
    return jsonify({
        'access_token': access_token,
        'user': {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'profile_picture': user.profile_picture
        }
    })

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """發送重設密碼驗證碼"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': '請提供電子郵件'}), 400
        
        # 驗證電子郵件格式
        if not validate_email(email):
            return jsonify({'error': '電子郵件格式不正確'}), 400
        
        # 檢查用戶是否存在
        user = User.query.filter_by(email=email).first()
        if not user:
            # 為了安全性，不透露用戶是否存在
            return jsonify({'message': '如果該電子郵件已註冊，您將收到重設密碼的驗證碼'}), 200
        
        # 生成 6 位數驗證碼
        code = ''.join(random.choices(string.digits, k=6))
        
        # 儲存驗證碼（有效期 15 分鐘）
        reset_codes[email] = {
            'code': code,
            'expires_at': datetime.now() + timedelta(minutes=15)
        }
        
        # 發送郵件
        email_sent = send_reset_password_email(email, code)
        
        # 控制台輸出（用於除錯和測試）
        print(f"[重設密碼] 電子郵件: {email}, 驗證碼: {code}, 郵件發送: {'成功' if email_sent else '失敗'}")
        
        response_data = {
            'message': '驗證碼已發送到您的電子郵件'
        }
        
        # 如果郵件發送失敗，在測試模式下返回驗證碼
        if not email_sent and os.getenv('FLASK_ENV') == 'development':
            response_data['code'] = code
            response_data['warning'] = '郵件服務未配置，這是測試驗證碼'
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"發送驗證碼錯誤: {str(e)}")
        return jsonify({'error': '發送驗證碼失敗'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """驗證碼驗證並重設密碼"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        if not all([email, code, new_password]):
            return jsonify({'error': '請提供所有必填欄位'}), 400
        
        # 檢查驗證碼是否存在
        if email not in reset_codes:
            return jsonify({'error': '驗證碼無效或已過期'}), 400
        
        stored_data = reset_codes[email]
        
        # 檢查驗證碼是否過期
        if datetime.now() > stored_data['expires_at']:
            del reset_codes[email]
            return jsonify({'error': '驗證碼已過期'}), 400
        
        # 驗證驗證碼
        if stored_data['code'] != code:
            return jsonify({'error': '驗證碼錯誤'}), 400
        
        # 驗證新密碼
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # 更新密碼
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        user.set_password(new_password)
        db.session.commit()
        
        # 刪除已使用的驗證碼
        del reset_codes[email]
        
        return jsonify({'message': '密碼重設成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"重設密碼錯誤: {str(e)}")
        return jsonify({'error': '重設密碼失敗'}), 500

@auth_bp.route('/2fa/setup', methods=['POST'])
@jwt_required()
def setup_two_factor():
    """設定兩步驟驗證 - 生成密鑰"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        # 生成新的密鑰
        secret = pyotp.random_base32()
        
        # 暫時保存到 session 或臨時存儲，等待驗證後再寫入資料庫
        # 這裡我們直接保存，因為需要用它來驗證
        user.two_factor_secret = secret
        db.session.commit()
        
        return jsonify({
            'secret': secret,
            'qr_code_url': f'otpauth://totp/EdgeSurvivor:{user.email}?secret={secret}&issuer=EdgeSurvivor'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"設定兩步驟驗證錯誤: {str(e)}")
        return jsonify({'error': '設定失敗'}), 500

@auth_bp.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify_two_factor():
    """驗證兩步驟驗證碼並啟用"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        if not user.two_factor_secret:
            return jsonify({'error': '請先設定兩步驟驗證'}), 400
        
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': '請提供驗證碼'}), 400
        
        # 驗證碼
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code, valid_window=1):  # valid_window=1 允許前後30秒的誤差
            user.two_factor_enabled = True
            db.session.commit()
            return jsonify({'success': True, 'message': '兩步驟驗證已啟用'}), 200
        else:
            return jsonify({'success': False, 'error': '驗證碼錯誤'}), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"驗證兩步驟驗證錯誤: {str(e)}")
        return jsonify({'error': '驗證失敗'}), 500

@auth_bp.route('/2fa/disable', methods=['POST'])
@jwt_required()
def disable_two_factor():
    """停用兩步驟驗證"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        if not user.two_factor_enabled:
            return jsonify({'error': '兩步驟驗證未啟用'}), 400
        
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': '請提供驗證碼'}), 400
        
        # 驗證碼
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code, valid_window=1):
            user.two_factor_enabled = False
            user.two_factor_secret = None
            db.session.commit()
            return jsonify({'success': True, 'message': '兩步驟驗證已停用'}), 200
        else:
            return jsonify({'success': False, 'error': '驗證碼錯誤'}), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"停用兩步驟驗證錯誤: {str(e)}")
        return jsonify({'error': '停用失敗'}), 500