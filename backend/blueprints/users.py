from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.activity import Activity
from models.match import Match
from models.activity_participant import ActivityParticipant
from models.activity_review import ActivityReview
from sqlalchemy import func, or_, and_

users_bp = Blueprint('users', __name__)

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """獲取用戶統計數據"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 計算我創建的活動數量
        created_activities_count = Activity.query.filter_by(creator_id=current_user_id).count()
        
        # 計算我參加的活動數量（已批准或已加入，但排除自己創建的）
        # 先獲取所有創建的活動ID
        created_activity_ids = [a.activity_id for a in Activity.query.filter_by(creator_id=current_user_id).all()]
        
        # 計算參加的活動（排除自己創建的）
        if created_activity_ids:
            joined_activities_count = ActivityParticipant.query.filter(
                ActivityParticipant.user_id == current_user_id,
                ActivityParticipant.status.in_(['approved', 'joined']),
                ~ActivityParticipant.activity_id.in_(created_activity_ids)
            ).count()
        else:
            joined_activities_count = ActivityParticipant.query.filter(
                ActivityParticipant.user_id == current_user_id,
                ActivityParticipant.status.in_(['approved', 'joined'])
            ).count()
        
        # 總活動數 = 創建的 + 參加的（不重複）
        activities_count = created_activities_count + joined_activities_count
        
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
        
        # 計算旅遊天數（使用總活動數量）
        # 新增：計算評價數量（從 users.rating_count）
        user_obj = User.query.get(current_user_id)
        if user_obj:
            reviews_count = user_obj.rating_count or 0
        else:
            reviews_count = 0
        travel_days = activities_count
        
        return jsonify({
            'stats': {
                'activities': activities_count,
                'matches': matches_count,  # 只顯示已確認的
                'allMatches': all_matches_count,  # 所有媒合（可選）
                'unreadMessages': unread_messages,
                'travelDays': travel_days,
                'reviews': reviews_count
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"[get_user_stats] Error: {e}")
        print(f"[get_user_stats] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@users_bp.route('/recent-activities', methods=['GET'])
@jwt_required()
def get_recent_activities():
    """獲取最近的活動（包含創建的和參加的）"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 獲取最近創建的活動
        created_activities = Activity.query.filter_by(creator_id=current_user_id)\
            .order_by(Activity.created_at.desc())\
            .limit(5)\
            .all()
        
        # 獲取參加的活動（通過 ActivityParticipant）
        participant_records = ActivityParticipant.query.filter(
            ActivityParticipant.user_id == current_user_id,
            ActivityParticipant.status.in_(['approved', 'joined'])
        ).order_by(ActivityParticipant.joined_at.desc()).limit(5).all()
        
        joined_activities = [
            Activity.query.get(p.activity_id) 
            for p in participant_records 
            if Activity.query.get(p.activity_id)
        ]
        
        # 合併兩個列表並去重
        all_activities = {}
        for activity in created_activities:
            all_activities[activity.activity_id] = activity
        for activity in joined_activities:
            if activity:
                all_activities[activity.activity_id] = activity
        
        # 轉換為列表並按創建時間排序
        recent_activities = sorted(
            all_activities.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:5]
        
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
        
        # 更新社群帳號
        if 'social_links' in data:
            social = data['social_links']
            if 'instagram' in social:
                user.instagram_url = social['instagram']
            if 'facebook' in social:
                user.facebook_url = social['facebook']
            if 'line' in social:
                user.line_id = social['line']
            if 'twitter' in social:
                user.twitter_url = social['twitter']
        
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
        
        if 'social_privacy' in data:
            # 驗證值是否有效
            if data['social_privacy'] in ['public', 'friends_only']:
                user.social_privacy = data['social_privacy']
            else:
                return jsonify({'error': '無效的社群隱私設定值'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': '隱私設定已更新',
            'privacy_setting': user.privacy_setting,
            'social_privacy': user.social_privacy
        }), 200
        
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
        is_friend = False
        current_user_id = int(get_jwt_identity())
        
        if current_user_id == user_id:
            include_private = True
        else:
            # 檢查是否為好友（有 accepted 或 confirmed 的 match）
            friend_match = Match.query.filter(
                or_(
                    and_(Match.user_a == current_user_id, Match.user_b == user_id),
                    and_(Match.user_a == user_id, Match.user_b == current_user_id)
                ),
                Match.status.in_(['accepted', 'confirmed'])
            ).first()
            is_friend = friend_match is not None
        
        # 計算用戶的統計數據（公開資料）
        # 計算創建的活動數量
        created_activities = Activity.query.filter_by(creator_id=user_id).all()
        activities_count = len(created_activities)
        created_activity_ids = [a.activity_id for a in created_activities]
        
        # 計算參與的活動數量（排除自己創建的活動）
        if created_activity_ids:
            participated_count = ActivityParticipant.query.filter(
                ActivityParticipant.user_id == user_id,
                ActivityParticipant.status.in_(['approved', 'joined']),
                ~ActivityParticipant.activity_id.in_(created_activity_ids)
            ).count()
        else:
            participated_count = ActivityParticipant.query.filter(
                ActivityParticipant.user_id == user_id,
                ActivityParticipant.status.in_(['approved', 'joined'])
            ).count()
        
        # 總活動數 = 創建的 + 參加的（不重複）
        total_activities = activities_count + participated_count
        
        # 計算交友數量（confirmed 或 accepted 狀態的媒合）
        matches_count = Match.query.filter(
            or_(Match.user_a == user_id, Match.user_b == user_id),
            Match.status.in_(['confirmed', 'accepted'])
        ).count()
        
        # 計算評價數量
        reviews_count = user.rating_count or 0
        
        user_data = user.to_dict(include_private=include_private, is_friend=is_friend)
        user_data['stats'] = {
            'activities': total_activities,
            'matches': matches_count,
            'reviews': reviews_count
        }
        
        return jsonify({
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:user_id>/reviews', methods=['GET'])
@jwt_required()
def get_user_reviews(user_id):
    """獲取使用者的評價列表（公開資料）"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '找不到用戶'}), 404
        
        # 獲取該使用者收到的所有評價
        reviews = ActivityReview.query.filter_by(reviewee_id=user_id).order_by(ActivityReview.created_at.desc()).all()
        
        # 轉換為字典格式，包含評價者資訊
        reviews_data = []
        for review in reviews:
            reviewer = User.query.get(review.reviewer_id)
            activity = Activity.query.get(review.activity_id)
            review_dict = review.to_dict()
            review_dict['reviewer'] = {
                'user_id': reviewer.user_id,
                'name': reviewer.name,
                'avatar': reviewer.profile_picture or reviewer.avatar or 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
            } if reviewer else None
            review_dict['activity'] = {
                'activity_id': activity.activity_id,
                'title': activity.title
            } if activity else None
            reviews_data.append(review_dict)
        
        return jsonify({
            'reviews': reviews_data,
            'total': len(reviews_data),
            'average_rating': round(user.average_rating or 0.0, 1),
            'rating_count': user.rating_count or 0
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

@users_bp.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """刪除帳號"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': '找不到使用者'}), 404
        
        data = request.get_json()
        password = data.get('password')
        
        if not password:
            return jsonify({'error': '請提供密碼以確認刪除'}), 400
        
        # 驗證密碼
        if not user.check_password(password):
            return jsonify({'error': '密碼錯誤'}), 400
        
        # 刪除相關資料
        # 1. 刪除參與的活動記錄
        ActivityParticipant.query.filter_by(user_id=current_user_id).delete()
        
        # 2. 刪除媒合記錄
        Match.query.filter(
            or_(Match.user_a == current_user_id, Match.user_b == current_user_id)
        ).delete(synchronize_session=False)
        
        # 3. 刪除創建的活動（或轉移給其他管理員）
        Activity.query.filter_by(creator_id=current_user_id).delete()
        
        # 4. 最後刪除用戶
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': '帳號已刪除'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '刪除帳號失敗: ' + str(e)}), 500

# @users_bp.route('/account/delete', methods=['POST'])
# @jwt_required()
# def delete_account_post():
#     """POST 方式刪除帳號，解決 DELETE body 問題"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         user = User.query.get(current_user_id)
#         if not user:
#             return jsonify({'error': '找不到使用者'}), 404
#         data = request.get_json()
#         password = data.get('password')
#         if not password:
#             return jsonify({'error': '請提供密碼以確認刪除'}), 400
#         if not user.check_password(password):
#             return jsonify({'error': '密碼錯誤'}), 400
#         ActivityParticipant.query.filter_by(user_id=current_user_id).delete()
#         Match.query.filter(
#             or_(Match.user_a == current_user_id, Match.user_b == current_user_id)
#         ).delete(synchronize_session=False)
#         Activity.query.filter_by(creator_id=current_user_id).delete()
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'message': '帳號已刪除'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': '刪除帳號失敗: ' + str(e)}), 500
