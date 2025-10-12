from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.activity import Activity
from models.user import User
from models.activity_participant import ActivityParticipant
from datetime import datetime

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('', methods=['GET'])
@jwt_required()
def get_activities():
    """獲取活動列表"""
    try:
        current_user_id = int(get_jwt_identity())
        activity_type = request.args.get('type')
        
        if activity_type == 'created':
            # 只返回我創建的活動
            activities = Activity.query.filter_by(creator_id=current_user_id).all()
        elif activity_type == 'joined':
            # 返回我參加的活動（包含 approved 和 joined 狀態，但不是我創建的）
            participant_records = ActivityParticipant.query.filter(
                ActivityParticipant.user_id == current_user_id,
                ActivityParticipant.status.in_(['approved', 'joined']),
                ActivityParticipant.role != 'creator'
            ).all()
            activities = [p.activity for p in participant_records if p.activity]
        else:
            # 返回所有活動，讓前端自己過濾
            activities = Activity.query.all()
        
        # 在返回的數據中加入當前參與人數
        result = []
        for activity in activities:
            activity_dict = activity.to_dict(include_creator_info=True)
            activity_dict['current_participants'] = activity.get_participant_count()
            
            # 如果是我創建的活動，加入待審核數量
            if activity.creator_id == current_user_id:
                pending_count = len(activity.get_pending_participants())
                activity_dict['pending_count'] = pending_count
            
            result.append(activity_dict)
        
        return jsonify({
            'activities': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('', methods=['POST'])
@jwt_required()
def create_activity():
    """創建新活動"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        required_fields = ['title', 'type', 'location', 'start_date', 'max_members']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # 解析日期
        activity_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')).date()
        
        activity = Activity(
            creator_id=current_user_id,
            title=data['title'],
            category=data['type'],  # 前端傳 type，後端存為 category
            location=data['location'],
            date=activity_date,  # 前端傳 start_date，後端存為 date
            max_participants=data['max_members'],  # 前端傳 max_members，後端存為 max_participants
            description=data.get('description', ''),
            status=data.get('status', 'open')  # 默認為 open（開放報名）
        )
        
        db.session.add(activity)
        db.session.flush()  # 確保獲得 activity_id
        
        # 自動將創建者添加為參與者
        creator_participant = ActivityParticipant(
            activity_id=activity.activity_id,
            user_id=current_user_id,
            status='joined',
            role='creator'
        )
        db.session.add(creator_participant)
        
        db.session.commit()
        
        activity_dict = activity.to_dict()
        activity_dict['current_participants'] = activity.get_participant_count()
        
        return jsonify({
            'message': '活動創建成功',
            'activity': activity_dict
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['GET'])
@jwt_required()
def get_activity(activity_id):
    """獲取活動詳情"""
    try:
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        activity_dict = activity.to_dict(include_creator_info=True)
        activity_dict['current_participants'] = activity.get_participant_count()
        
        # 獲取參與者列表
        participants = activity.get_participants()
        activity_dict['participants'] = []
        
        for participant in participants:
            user = User.query.get(participant.user_id)
            if user:
                activity_dict['participants'].append({
                    'user_id': user.user_id,
                    'name': user.name,
                    'avatar': user.profile_picture,
                    'role': participant.role,
                    'joined_at': participant.joined_at.isoformat() if participant.joined_at else None
                })
        
        return jsonify({
            'activity': activity_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    """更新活動"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id != current_user_id:
            return jsonify({'error': '無權限修改此活動'}), 403
        
        data = request.get_json()
        
        if 'title' in data:
            activity.title = data['title']
        if 'type' in data:
            activity.category = data['type']  # 前端傳 type，後端存為 category
        if 'location' in data:
            activity.location = data['location']
        if 'start_date' in data:
            activity.date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')).date()
        if 'max_members' in data:
            activity.max_participants = data['max_members']  # 前端傳 max_members，後端存為 max_participants
        if 'description' in data:
            activity.description = data['description']
        if 'status' in data:
            activity.status = data['status']
        if 'cover_image' in data:
            activity.cover_image = data['cover_image']
        if 'images' in data:
            activity.images = data['images']
        
        db.session.commit()
        
        return jsonify({
            'message': '活動更新成功',
            'activity': activity.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    """刪除活動"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id != current_user_id:
            return jsonify({'error': '無權限刪除此活動'}), 403
        
        db.session.delete(activity)
        db.session.commit()
        
        return jsonify({'message': '活動已刪除'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/join', methods=['POST'])
@jwt_required()
def join_activity(activity_id):
    """申請加入活動"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id == current_user_id:
            return jsonify({'error': '不能加入自己創建的活動'}), 400
        
        # 檢查是否已參與或已申請
        if activity.is_user_participant(current_user_id):
            return jsonify({'error': '您已經申請或參與此活動'}), 400
        
        # 檢查人數是否已滿
        if activity.get_participant_count() >= activity.max_participants:
            return jsonify({'error': '活動人數已滿'}), 400
        
        # 創建參與申請（狀態為 pending）
        participant = ActivityParticipant(
            activity_id=activity_id,
            user_id=current_user_id,
            status='pending',
            role='participant',
            message=data.get('message', '')
        )
        db.session.add(participant)
        db.session.commit()
        
        return jsonify({
            'message': '申請已發送，等待活動創建者審核',
            'participant_id': participant.participant_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/participants/pending', methods=['GET'])
@jwt_required()
def get_pending_participants(activity_id):
    """獲取活動的待審核申請列表（僅創建者可查看）"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動創建者可以查看待審核申請'}), 403
        
        pending_list = activity.get_pending_participants()
        result = []
        
        for participant in pending_list:
            user = User.query.get(participant.user_id)
            if user:
                result.append({
                    'participant_id': participant.participant_id,
                    'user_id': user.user_id,
                    'name': user.name,
                    'avatar': user.profile_picture,
                    'message': participant.message,
                    'joined_at': participant.joined_at.isoformat() if participant.joined_at else None
                })
        
        return jsonify({'pending_participants': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/participants/<int:participant_id>/approve', methods=['POST'])
@jwt_required()
def approve_participant(activity_id, participant_id):
    """批准參與申請"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動創建者可以批准申請'}), 403
        
        participant = ActivityParticipant.query.get(participant_id)
        
        if not participant or participant.activity_id != activity_id:
            return jsonify({'error': '找不到申請記錄'}), 404
        
        if participant.status != 'pending':
            return jsonify({'error': '此申請已處理'}), 400
        
        # 檢查人數是否已滿
        if activity.get_participant_count() >= activity.max_participants:
            return jsonify({'error': '活動人數已滿'}), 400
        
        participant.approve()
        
        return jsonify({
            'message': '已批准申請',
            'current_participants': activity.get_participant_count()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/participants/<int:participant_id>/reject', methods=['POST'])
@jwt_required()
def reject_participant(activity_id, participant_id):
    """拒絕參與申請"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動創建者可以拒絕申請'}), 403
        
        participant = ActivityParticipant.query.get(participant_id)
        
        if not participant or participant.activity_id != activity_id:
            return jsonify({'error': '找不到申請記錄'}), 404
        
        if participant.status != 'pending':
            return jsonify({'error': '此申請已處理'}), 400
        
        participant.reject(data.get('reason'))
        
        return jsonify({'message': '已拒絕申請'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/leave', methods=['POST'])
@jwt_required()
def leave_activity(activity_id):
    """離開活動"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if activity.creator_id == current_user_id:
            return jsonify({'error': '創建者不能離開活動，請刪除活動'}), 400
        
        # 查找參與記錄
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=current_user_id,
            status='joined'
        ).first()
        
        if not participant:
            return jsonify({'error': '您尚未參與此活動'}), 400
        
        # 標記為已離開
        participant.leave()
        
        return jsonify({
            'message': '已離開活動',
            'current_participants': activity.get_participant_count()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
