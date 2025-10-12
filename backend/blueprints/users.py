from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.activity import Activity
from models.match import Match
from models.activity_participant import ActivityParticipant
from sqlalchemy import func, or_

users_bp = Blueprint('users', __name__)

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """獲取用戶統計數據"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 計算我創建的活動數量
        activities_count = Activity.query.filter_by(creator_id=current_user_id).count()
        
        # 計算媒合成功數量（confirmed 或 accepted 狀態的媒合）
        matches_count = Match.query.filter(
            or_(Match.user_a == current_user_id, Match.user_b == current_user_id),
            Match.status.in_(['confirmed', 'accepted'])
        ).count()
        
        # 計算所有媒合數量（包括 pending）
        all_matches_count = Match.query.filter(
            or_(Match.user_a == current_user_id, Match.user_b == current_user_id)
        ).count()
        
        # TODO: 計算未讀訊息數量（需要 messages 表）
        unread_messages = 0
        
        # 計算旅遊天數（統計所有參與過的活動）
        participated_activities = ActivityParticipant.query.filter(
            ActivityParticipant.user_id == current_user_id,
            ActivityParticipant.status.in_(['approved', 'joined'])
        ).count()
        
        # 加上創建的活動數量
        travel_days = activities_count + participated_activities
        
        return jsonify({
            'stats': {
                'activities': activities_count,
                'matches': matches_count,  # 只顯示已確認的
                'allMatches': all_matches_count,  # 所有媒合（可選）
                'unreadMessages': unread_messages,
                'travelDays': travel_days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/recent-activities', methods=['GET'])
@jwt_required()
def get_recent_activities():
    """獲取最近的活動"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 獲取最近創建的 5 個活動
        recent_activities = Activity.query.filter_by(creator_id=current_user_id)\
            .order_by(Activity.created_at.desc())\
            .limit(5)\
            .all()
        
        return jsonify({
            'activities': [activity.to_dict() for activity in recent_activities]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """獲取當前用戶資料"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到用戶'}), 404
        
        return jsonify({
            'user': user.to_dict(include_private=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新個人資料"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到用戶'}), 404
        
        data = request.get_json()
        
        # 更新允許修改的欄位
        if 'name' in data:
            user.name = data['name']
        if 'gender' in data:
            user.gender = data['gender']
        if 'age' in data:
            user.age = data['age']
        if 'location' in data:
            user.location = data['location']
        if 'bio' in data:
            user.bio = data['bio']
        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']
        if 'interests' in data:
            # 將興趣列表轉換為 JSON 字串儲存
            import json
            if isinstance(data['interests'], list):
                user.interests = json.dumps(data['interests'], ensure_ascii=False)
            elif isinstance(data['interests'], str):
                user.interests = data['interests']
        
        db.session.commit()
        
        return jsonify({
            'message': '個人資料更新成功',
            'user': user.to_dict(include_private=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/privacy', methods=['PUT'])
@jwt_required()
def update_privacy():
    """更新隱私設定"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到用戶'}), 404
        
        data = request.get_json()
        
        if 'privacy_setting' in data:
            user.privacy_setting = data['privacy_setting']
        
        db.session.commit()
        
        return jsonify({'message': '隱私設定已更新'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """獲取其他用戶資料"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '找不到用戶'}), 404
        
        # 根據隱私設定返回不同的資料
        include_private = False
        current_user_id = int(get_jwt_identity())
        if current_user_id == user_id:
            include_private = True
        
        return jsonify({
            'user': user.to_dict(include_private=include_private)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上傳頭像"""
    try:
        # TODO: 實現檔案上傳功能
        return jsonify({'message': '頭像上傳功能開發中'}), 501
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
