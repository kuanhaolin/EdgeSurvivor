from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.activity_review import ActivityReview
from models.activity import Activity
from models.activity_participant import ActivityParticipant
from models.user import User
from sqlalchemy import func
from datetime import date
import sys

reviews_bp = Blueprint('reviews', __name__)

# 獲取活動的所有評價
@reviews_bp.route('/activities/<int:activity_id>/reviews', methods=['GET'])
@jwt_required()
def get_activity_reviews(activity_id):
    """獲取活動的所有評價（僅參與者可見）"""
    current_user_id = get_jwt_identity()
    
    # 檢查活動是否存在
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': '活動不存在'}), 404
    
    # 檢查是否為參與者或創建者（創建者為 joined，其他人為 approved）
    is_participant = ActivityParticipant.query.filter_by(
        activity_id=activity_id,
        user_id=current_user_id
    ).filter(
        ActivityParticipant.status.in_(['approved', 'joined'])
    ).first() is not None
    
    is_creator = activity.creator_id == current_user_id
    
    if not (is_participant or is_creator):
        return jsonify({'error': '只有參與者可以查看評價'}), 403
    
    # 獲取所有評價
    reviews = ActivityReview.query.filter_by(activity_id=activity_id).all()
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews]
    }), 200

# 獲取當前用戶在該活動中的評價狀態
@reviews_bp.route('/activities/<int:activity_id>/reviews/my-status', methods=['GET'])
@jwt_required()
def get_my_review_status(activity_id):
    """獲取當前用戶在該活動中已評價和待評價的人員"""
    current_user_id = int(get_jwt_identity())
    
    # 檢查活動是否存在且已完成
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': '活動不存在'}), 404
    
    # 檢查是否為參與者或創建者（創建者為 joined，其他人為 approved）
    is_participant = ActivityParticipant.query.filter_by(
        activity_id=activity_id,
        user_id=current_user_id
    ).filter(
        ActivityParticipant.status.in_(['approved', 'joined'])
    ).first() is not None
    
    is_creator = activity.creator_id == current_user_id
    
    if not (is_participant or is_creator):
        return jsonify({'error': '只有參與者可以進行評價'}), 403
    
    # 獲取所有參與者（不包括自己，包含 approved 和 joined 狀態）
    participants = ActivityParticipant.query.filter(
        ActivityParticipant.activity_id == activity_id,
        ActivityParticipant.status.in_(['approved', 'joined']),
        ActivityParticipant.user_id != current_user_id
    ).all()
    
    # 收集所有可評價的用戶 ID（參與者 + 創建者，但不包括自己）
    reviewable_user_ids = set([p.user_id for p in participants])
    
    # 如果創建者不是當前用戶，加入創建者
    if int(activity.creator_id) != current_user_id:
        reviewable_user_ids.add(activity.creator_id)
    
    # 確保自己不在可評價列表中（雙重保險）
    reviewable_user_ids.discard(current_user_id)
    
    # 獲取當前用戶已評價的人
    reviewed_ids = set([
        review.reviewee_id for review in ActivityReview.query.filter_by(
            activity_id=activity_id,
            reviewer_id=current_user_id
        ).all()
    ])
    
    # 分類參與者
    reviewed = []
    pending = []
    
    for user_id in reviewable_user_ids:
        user = User.query.get(user_id)
        if not user:
            continue
            
        user_data = {
            'user_id': user.user_id,
            'name': user.name,
            'profile_picture': user.profile_picture,
            'rating_count': user.rating_count or 0,
            'average_rating': round(user.average_rating or 0.0, 1)
        }
        
        if user.user_id in reviewed_ids:
            # 獲取評價詳情
            review = ActivityReview.query.filter_by(
                activity_id=activity_id,
                reviewer_id=current_user_id,
                reviewee_id=user.user_id
            ).first()
            user_data['my_review'] = {
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat() if review.created_at else None
            }
            reviewed.append(user_data)
        else:
            pending.append(user_data)
    
    # 檢查是否可以評價：活動必須是已完成狀態，且結束日期已過
    can_review = activity.status == 'completed'
    if not can_review:
        print(f"🔍 [Review Check] Activity {activity_id}: status={activity.status} (not completed), can_review=False", flush=True, file=sys.stderr)
    elif activity.end_date:
        today = date.today()
        # 結束日期必須是今天或更早（today >= end_date 表示結束日期已經到了或過了）
        date_passed = today >= activity.end_date
        can_review = can_review and date_passed
        print(f"🔍 [Review Check] Activity {activity_id}: status={activity.status}, end_date={activity.end_date}, today={today}, date_passed={date_passed}, can_review={can_review}", flush=True, file=sys.stderr)
    else:
        # 如果沒有結束日期，只要狀態是 completed 就可以評價
        print(f"🔍 [Review Check] Activity {activity_id}: status={activity.status}, no end_date, can_review={can_review}", flush=True, file=sys.stderr)
    
    return jsonify({
        'reviewed': reviewed,
        'pending': pending,
        'can_review': can_review
    }), 200

# 提交或更新評價
@reviews_bp.route('/activities/<int:activity_id>/reviews', methods=['POST'])
@jwt_required()
def submit_review(activity_id):
    """提交或更新對某位參與者的評價"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    reviewee_id = data.get('reviewee_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()
    
    # 驗證必要欄位
    if not reviewee_id:
        return jsonify({'error': '請指定被評價者'}), 400
    
    if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': '評分必填，且必須為 1-5 之間的整數'}), 400
    
    if not comment:
        return jsonify({'error': '請填寫評價內容'}), 400
    
    # 檢查活動是否存在
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': '活動不存在'}), 404
    
    # 檢查活動是否已完成且結束日期已過
    if activity.status != 'completed':
        return jsonify({'error': '只有已完成的活動才能進行評價'}), 403
    
    # 檢查結束日期（結束日期必須是今天或更早，即 today >= end_date）
    if activity.end_date:
        today = date.today()
        if today < activity.end_date:
            return jsonify({'error': f'活動結束日期為 {activity.end_date}，需等到 {activity.end_date} 當天或之後才能進行評價'}), 403
    
    # 不能評價自己
    if reviewee_id == current_user_id:
        return jsonify({'error': '不能評價自己'}), 400
    
    # 檢查是否為參與者（創建者為 joined，其他人為 approved）
    is_participant = ActivityParticipant.query.filter_by(
        activity_id=activity_id,
        user_id=current_user_id
    ).filter(
        ActivityParticipant.status.in_(['approved', 'joined'])
    ).first() is not None
    
    is_creator = activity.creator_id == current_user_id
    
    if not (is_participant or is_creator):
        return jsonify({'error': '只有參與者可以進行評價'}), 403
    
    # 檢查被評價者是否為參與者（創建者為 joined，其他人為 approved）
    reviewee_participant = ActivityParticipant.query.filter_by(
        activity_id=activity_id,
        user_id=reviewee_id
    ).filter(
        ActivityParticipant.status.in_(['approved', 'joined'])
    ).first()
    
    reviewee_is_creator = activity.creator_id == reviewee_id
    
    if not (reviewee_participant or reviewee_is_creator):
        return jsonify({'error': '只能評價活動參與者'}), 403
    
    # 查找是否已存在評價
    existing_review = ActivityReview.query.filter_by(
        activity_id=activity_id,
        reviewer_id=current_user_id,
        reviewee_id=reviewee_id
    ).first()
    
    if existing_review:
        # 更新現有評價
        existing_review.rating = rating
        existing_review.comment = comment
        review = existing_review
        message = '評價已更新'
    else:
        # 創建新評價
        review = ActivityReview(
            activity_id=activity_id,
            reviewer_id=current_user_id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        message = '評價已提交'
    
    db.session.commit()
    
    # 更新被評價者的評價數量與平均評分
    update_user_rating_stats(reviewee_id)
    
    return jsonify({
        'message': message,
        'review': review.to_dict()
    }), 200

# 更新用戶的評價數量與平均評分
def update_user_rating_stats(user_id):
    """重新計算並更新用戶的評價數量與平均評分"""
    reviews = ActivityReview.query.filter_by(reviewee_id=user_id).all()
    count = len(reviews)
    
    user = User.query.get(user_id)
    if user:
        user.rating_count = count
        if count > 0:
            total_rating = sum(review.rating for review in reviews)
            user.average_rating = total_rating / count
        else:
            user.average_rating = 0.0
        db.session.commit()
