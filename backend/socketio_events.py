"""
Socket.IO 事件處理
處理即時通訊相關的 Socket.IO 事件
"""
from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from models import db
from models.chat_message import ChatMessage
from models.match import Match
from models.activity_discussion import ActivityDiscussion
from models.user import User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 儲存在線用戶 {user_id: sid}
online_users = {}

def register_socketio_events(socketio, app):
    """註冊所有 Socket.IO 事件處理器"""
    
    @socketio.on('connect')
    def handle_connect(auth):
        """處理客戶端連線"""
        try:
            # 驗證 JWT Token
            if not auth or 'token' not in auth:
                logger.warning('連線缺少認證 token')
                return False
            
            token = auth['token']
            with app.app_context():
                decoded = decode_token(token)
                user_id = int(decoded['sub'])
                
                # 記錄在線用戶
                from flask import request
                online_users[user_id] = request.sid
                
                logger.info(f'用戶 {user_id} 已連線 (SID: {request.sid})')
                
                # 廣播用戶上線
                emit('user_online', {'user_id': user_id}, broadcast=True)
                
                return True
                
        except Exception as e:
            logger.error(f'連線錯誤: {str(e)}')
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """處理客戶端斷線"""
        try:
            from flask import request
            # 找到斷線的用戶
            user_id = None
            for uid, sid in online_users.items():
                if sid == request.sid:
                    user_id = uid
                    break
            
            if user_id:
                del online_users[user_id]
                logger.info(f'用戶 {user_id} 已斷線')
                
                # 廣播用戶離線
                emit('user_offline', {'user_id': user_id}, broadcast=True)
                
        except Exception as e:
            logger.error(f'斷線處理錯誤: {str(e)}')
    
    @socketio.on('join_chat')
    def handle_join_chat(data):
        """加入聊天室"""
        try:
            match_id = data.get('match_id')
            user_id = data.get('user_id')
            
            if not match_id:
                return {'error': '缺少 match_id'}
            
            room = f'chat_{match_id}'
            join_room(room)
            
            logger.info(f'用戶 {user_id} 加入聊天室 {room}')
            
            # 通知房間內其他人
            emit('user_joined', {
                'user_id': user_id,
                'match_id': match_id,
                'timestamp': datetime.utcnow().isoformat()
            }, room=room, skip_sid=True)
            
            return {'success': True, 'room': room}
            
        except Exception as e:
            logger.error(f'加入聊天室錯誤: {str(e)}')
            return {'error': str(e)}
    
    @socketio.on('leave_chat')
    def handle_leave_chat(data):
        """離開聊天室"""
        try:
            match_id = data.get('match_id')
            user_id = data.get('user_id')
            
            room = f'chat_{match_id}'
            leave_room(room)
            
            logger.info(f'用戶 {user_id} 離開聊天室 {room}')
            
            # 通知房間內其他人
            emit('user_left', {
                'user_id': user_id,
                'match_id': match_id,
                'timestamp': datetime.utcnow().isoformat()
            }, room=room)
            
        except Exception as e:
            logger.error(f'離開聊天室錯誤: {str(e)}')
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """發送聊天訊息"""
        try:
            with app.app_context():
                match_id = data.get('match_id')
                sender_id = data.get('sender_id')
                content = data.get('content')
                message_type = data.get('message_type', 'text')
                
                # 驗證參數
                if not all([match_id, sender_id, content]):
                    return {'error': '缺少必要參數'}
                
                # 驗證媒合是否存在
                match = Match.query.get(match_id)
                if not match:
                    return {'error': '媒合不存在'}
                
                # 驗證發送者是否為媒合參與者
                if sender_id not in [match.user_a, match.user_b]:
                    return {'error': '無權限發送訊息'}
                
                # 確定接收者 ID（媒合中的另一方）
                receiver_id = match.user_b if match.user_a == sender_id else match.user_a
                
                # 儲存訊息到資料庫
                message = ChatMessage(
                    match_id=match_id,
                    sender_id=sender_id,
                    receiver_id=receiver_id,  # 添加接收者 ID
                    content=content,
                    message_type=message_type,
                    status='sent'
                )
                db.session.add(message)
                db.session.commit()
                
                # 獲取發送者資訊
                sender = User.query.get(sender_id)
                
                # 建立訊息資料
                message_data = {
                    'message_id': message.message_id,
                    'match_id': match_id,
                    'sender_id': sender_id,
                    'sender_name': sender.name if sender else 'Unknown',
                    'sender_avatar': sender.profile_picture if sender else None,
                    'content': content,
                    'message_type': message_type,
                    'timestamp': message.timestamp.isoformat(),
                    'status': 'sent'
                }
                
                # 廣播到聊天室
                room = f'chat_{match_id}'
                emit('new_message', message_data, room=room)
                
                logger.info(f'訊息已發送到聊天室 {room}')
                
                return {'success': True, 'message': message_data}
                
        except Exception as e:
            logger.error(f'發送訊息錯誤: {str(e)}')
            db.session.rollback()
            return {'error': str(e)}
    
    @socketio.on('typing')
    def handle_typing(data):
        """處理輸入狀態"""
        try:
            match_id = data.get('match_id')
            user_id = data.get('user_id')
            is_typing = data.get('is_typing', False)
            
            room = f'chat_{match_id}'
            
            # 廣播輸入狀態（排除自己）
            emit('user_typing', {
                'user_id': user_id,
                'is_typing': is_typing
            }, room=room, skip_sid=True)
            
        except Exception as e:
            logger.error(f'處理輸入狀態錯誤: {str(e)}')
    
    @socketio.on('join_activity_discussion')
    def handle_join_activity_discussion(data):
        """加入活動討論室"""
        try:
            activity_id = data.get('activity_id')
            user_id = data.get('user_id')
            
            if not activity_id:
                return {'error': '缺少 activity_id'}
            
            room = f'activity_{activity_id}'
            join_room(room)
            
            logger.info(f'用戶 {user_id} 加入活動討論室 {room}')
            
            return {'success': True, 'room': room}
            
        except Exception as e:
            logger.error(f'加入活動討論室錯誤: {str(e)}')
            return {'error': str(e)}
    
    @socketio.on('leave_activity_discussion')
    def handle_leave_activity_discussion(data):
        """離開活動討論室"""
        try:
            activity_id = data.get('activity_id')
            
            room = f'activity_{activity_id}'
            leave_room(room)
            
            logger.info(f'離開活動討論室 {room}')
            
        except Exception as e:
            logger.error(f'離開活動討論室錯誤: {str(e)}')
    
    @socketio.on('send_discussion')
    def handle_send_discussion(data):
        """發送活動討論訊息"""
        try:
            with app.app_context():
                activity_id = data.get('activity_id')
                user_id = data.get('user_id')
                message = data.get('message')
                message_type = data.get('message_type', 'text')
                
                # 驗證參數
                if not all([activity_id, user_id, message]):
                    return {'error': '缺少必要參數'}
                
                # 儲存討論訊息到資料庫
                discussion = ActivityDiscussion(
                    activity_id=activity_id,
                    user_id=user_id,
                    message=message,
                    message_type=message_type
                )
                db.session.add(discussion)
                db.session.commit()
                
                # 獲取發送者資訊
                sender = User.query.get(user_id)
                
                # 建立訊息資料
                discussion_data = {
                    'discussion_id': discussion.discussion_id,
                    'activity_id': activity_id,
                    'user_id': user_id,
                    'user': {
                        'user_id': sender.user_id,
                        'name': sender.name,
                        'avatar': sender.profile_picture
                    } if sender else None,
                    'message': message,
                    'message_type': message_type,
                    'created_at': discussion.created_at.isoformat()
                }
                
                # 廣播到活動討論室
                room = f'activity_{activity_id}'
                emit('new_discussion', discussion_data, room=room)
                
                logger.info(f'討論訊息已發送到活動討論室 {room}')
                
                return {'success': True, 'discussion': discussion_data}
                
        except Exception as e:
            logger.error(f'發送討論訊息錯誤: {str(e)}')
            db.session.rollback()
            return {'error': str(e)}
    
    @socketio.on('mark_as_read')
    def handle_mark_as_read(data):
        """標記訊息為已讀"""
        try:
            with app.app_context():
                match_id = data.get('match_id')
                user_id = data.get('user_id')
                
                if not match_id or not user_id:
                    return {'error': '缺少必要參數'}
                
                # 獲取媒合資訊
                match = Match.query.get(match_id)
                if not match:
                    return {'error': '媒合不存在'}
                
                # 確定對方的 user_id
                other_user_id = match.user_b if match.user_a == user_id else match.user_a
                
                # 將對方發給我的訊息標記為已讀
                from models.chat_message import ChatMessage
                ChatMessage.query.filter(
                    ChatMessage.match_id == match_id,
                    ChatMessage.sender_id == other_user_id,
                    ChatMessage.status != 'read'
                ).update({'status': 'read'})
                
                db.session.commit()
                
                # 通知對方訊息已被讀取
                room = f'chat_{match_id}'
                emit('messages_read', {
                    'match_id': match_id,
                    'reader_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                }, room=room, skip_sid=True)
                
                return {'success': True}
                
        except Exception as e:
            logger.error(f'標記已讀錯誤: {str(e)}')
            db.session.rollback()
            return {'error': str(e)}
    
    @socketio.on('get_online_users')
    def handle_get_online_users():
        """獲取在線用戶列表"""
        try:
            return {'online_users': list(online_users.keys())}
        except Exception as e:
            logger.error(f'獲取在線用戶錯誤: {str(e)}')
            return {'error': str(e)}
    
    logger.info('Socket.IO 事件處理器已註冊')
