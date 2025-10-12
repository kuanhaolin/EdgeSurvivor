from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.chat_message import ChatMessage
from models.user import User
from sqlalchemy import or_, and_

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """獲取聊天列表"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 從 matches 表獲取所有相關的媒合記錄
        from models.match import Match
        matches = Match.query.filter(
            or_(
                Match.user_a == current_user_id,
                Match.user_b == current_user_id
            ),
            Match.status.in_(['accepted', 'confirmed'])
        ).all()
        
        # 獲取在線用戶列表（從 socketio_events 導入）
        try:
            from socketio_events import online_users
            online_user_ids = list(online_users.keys())
        except:
            online_user_ids = []
        
        conversations = []
        for match in matches:
            # 獲取對方用戶
            other_user_id = match.user_b if match.user_a == current_user_id else match.user_a
            other_user = User.query.get(other_user_id)
            
            if not other_user:
                continue
            
            # 獲取最後一條訊息
            last_message = ChatMessage.query.filter(
                ChatMessage.match_id == match.match_id
            ).order_by(ChatMessage.timestamp.desc()).first()
            
            # 計算未讀訊息數量（對方發給我的未讀訊息）
            unread_count = ChatMessage.query.filter(
                ChatMessage.match_id == match.match_id,
                ChatMessage.sender_id == other_user_id,
                ChatMessage.status != 'read'
            ).count()
            
            user_dict = other_user.to_dict()
            conversations.append({
                'match_id': match.match_id,
                'activity_id': match.activity_id,
                'other_user': {
                    'user_id': user_dict['user_id'],
                    'name': user_dict['name'],
                    'avatar': user_dict['avatar'],
                    'is_online': other_user_id in online_user_ids
                },
                'last_message': {
                    'content': last_message.content if last_message else '開始聊天吧',
                    'created_at': last_message.timestamp.isoformat() if last_message else None
                } if last_message else None,
                'unread_count': unread_count
            })
        
        return jsonify({
            'conversations': conversations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/<int:user_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(user_id):
    """獲取與特定用戶的訊息記錄"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 獲取兩人之間的所有訊息
        messages = ChatMessage.query.filter(
            or_(
                and_(ChatMessage.sender_id == current_user_id, ChatMessage.receiver_id == user_id),
                and_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == current_user_id)
            )
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    """發送訊息"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('receiver_id') or not data.get('content'):
            return jsonify({'error': 'receiver_id and content are required'}), 400
        
        # 創建訊息
        message = ChatMessage(
            sender_id=current_user_id,
            receiver_id=data['receiver_id'],
            content=data['content'],
            message_type=data.get('message_type', 'text')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(message_id):
    """標記訊息為已讀"""
    try:
        current_user_id = int(get_jwt_identity())
        message = ChatMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': '找不到訊息'}), 404
        
        if message.receiver_id != current_user_id:
            return jsonify({'error': '無權限操作此訊息'}), 403
        
        message.status = 'read'
        db.session.commit()
        
        return jsonify({'message': '已標記為已讀'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:user_id>/read', methods=['PUT'])
@jwt_required()
def mark_conversation_as_read(user_id):
    """標記與某用戶的所有訊息為已讀"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 將對方發給我的所有未讀訊息標記為已讀
        ChatMessage.query.filter(
            ChatMessage.sender_id == user_id,
            ChatMessage.receiver_id == current_user_id,
            ChatMessage.status != 'read'
        ).update({'status': 'read'})
        
        db.session.commit()
        
        return jsonify({'message': '已標記為已讀'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """獲取總未讀訊息數"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 計算所有未讀訊息數量
        unread_count = ChatMessage.query.filter(
            ChatMessage.receiver_id == current_user_id,
            ChatMessage.status != 'read'
        ).count()
        
        return jsonify({'unread_count': unread_count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/shared-activities/<int:user_id>', methods=['GET'])
@jwt_required()
def get_shared_activities(user_id):
    """獲取與某用戶共同參與的活動"""
    try:
        current_user_id = int(get_jwt_identity())
        
        from models.activity_participant import ActivityParticipant
        from models.activity import Activity
        
        # 查詢當前用戶參與的所有活動 ID
        my_activities = db.session.query(ActivityParticipant.activity_id).filter(
            ActivityParticipant.user_id == current_user_id,
            ActivityParticipant.status.in_(['approved', 'joined'])
        ).all()
        my_activity_ids = [a[0] for a in my_activities]
        
        # 查詢對方用戶參與的所有活動 ID
        their_activities = db.session.query(ActivityParticipant.activity_id).filter(
            ActivityParticipant.user_id == user_id,
            ActivityParticipant.status.in_(['approved', 'joined'])
        ).all()
        their_activity_ids = [a[0] for a in their_activities]
        
        # 找出共同參與的活動
        shared_activity_ids = list(set(my_activity_ids) & set(their_activity_ids))
        
        if not shared_activity_ids:
            return jsonify({'shared_activities': []}), 200
        
        # 獲取共同活動的詳細資訊
        shared_activities = Activity.query.filter(
            Activity.activity_id.in_(shared_activity_ids)
        ).all()
        
        return jsonify({
            'shared_activities': [activity.to_dict() for activity in shared_activities]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
