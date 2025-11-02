"""
活動討論串 API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.activity import Activity
from models.activity_discussion import ActivityDiscussion
from models.activity_participant import ActivityParticipant

discussions_bp = Blueprint('discussions', __name__)

@discussions_bp.route('/activities/<int:activity_id>/discussions', methods=['GET'])
@jwt_required()
def get_discussions(activity_id):
    """獲取活動討論訊息列表"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 檢查用戶是否有權限查看（必須是參與者）
        if not activity.is_user_participant(current_user_id) and activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動參與者可以查看討論'}), 403
        
        # 獲取討論訊息
        discussions = ActivityDiscussion.query.filter_by(
            activity_id=activity_id,
            is_deleted=False
        ).order_by(ActivityDiscussion.created_at.asc()).all()
        
        return jsonify({
            'discussions': [d.to_dict() for d in discussions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/activities/<int:activity_id>/discussions', methods=['POST'])
@jwt_required()
def post_discussion(activity_id):
    """發送討論訊息"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 檢查用戶是否有權限發送（必須是參與者）
        if not activity.is_user_participant(current_user_id) and activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動參與者可以發送訊息'}), 403
        
        if not data.get('message'):
            return jsonify({'error': '訊息內容不能為空'}), 400
        
        discussion = ActivityDiscussion(
            activity_id=activity_id,
            user_id=current_user_id,
            message=data['message'],
            message_type=data.get('message_type', 'text')
        )
        
        db.session.add(discussion)
        db.session.commit()
        
        return jsonify({
            'message': '訊息發送成功',
            'discussion': discussion.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/discussions/<int:discussion_id>', methods=['DELETE'])
@jwt_required()
def delete_discussion(discussion_id):
    """刪除討論訊息"""
    try:
        current_user_id = int(get_jwt_identity())
        discussion = ActivityDiscussion.query.get(discussion_id)
        
        if not discussion:
            return jsonify({'error': '找不到訊息'}), 404
        
        # 只有訊息發送者或活動創建者可以刪除
        activity = Activity.query.get(discussion.activity_id)
        if discussion.user_id != current_user_id and activity.creator_id != current_user_id:
            return jsonify({'error': '無權限刪除此訊息'}), 403
        
        activity_id = discussion.activity_id
        discussion.soft_delete()
        
        # 通過 Socket.IO 廣播刪除事件
        try:
            from flask_socketio import emit
            room = f'activity_{activity_id}'
            print(f'準備廣播刪除事件到房間: {room}, discussion_id: {discussion_id}')
            emit('discussion_deleted', {
                'discussion_id': discussion_id,
                'activity_id': activity_id
            }, room=room, namespace='/')
            print(f'✅ 已發送 discussion_deleted 事件到 {room}')
        except Exception as socket_error:
            # Socket.IO 廣播失敗不影響刪除操作
            print(f'❌ Socket.IO 廣播刪除事件失敗: {socket_error}')
        
        return jsonify({'message': '訊息已刪除'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
