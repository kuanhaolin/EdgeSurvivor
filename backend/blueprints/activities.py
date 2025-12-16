from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db
from models.activity import Activity
from models.user import User
from models.activity_participant import ActivityParticipant
from datetime import datetime
import os
import uuid
import json

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
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')).date()
        end_date = None
        if data.get('end_date'):
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')).date()
            
            # 驗證日期範圍：開始日期必須早於或等於結束日期
            if start_date > end_date:
                return jsonify({'error': 'start_date must be before or equal to end_date'}), 400
        
        # 解析時間
        start_time = None
        end_time = None
        if data.get('start_time'):
            time_str = data['start_time']
            # 支援 HH:MM:SS 和 HH:MM 格式
            if len(time_str) == 8:  # HH:MM:SS
                start_time = datetime.strptime(time_str, '%H:%M:%S').time()
            else:  # HH:MM
                start_time = datetime.strptime(time_str, '%H:%M').time()
        if data.get('end_time'):
            time_str = data['end_time']
            if len(time_str) == 8:
                end_time = datetime.strptime(time_str, '%H:%M:%S').time()
            else:
                end_time = datetime.strptime(time_str, '%H:%M').time()
        
        activity = Activity(
            creator_id=current_user_id,
            title=data['title'],
            category=data['type'],  # 前端傳 type，後端存為 category
            location=data['location'],
            date=start_date,  # 保留舊欄位以向後兼容
            start_date=start_date,  # 新增開始日期
            end_date=end_date,  # 新增結束日期
            start_time=start_time,  # 新增開始時間
            end_time=end_time,  # 新增結束時間
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
                    'participant_id': participant.participant_id,
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
        
        # 驗證必填欄位
        if 'title' in data:
            if not data['title'] or not data['title'].strip():
                return jsonify({'error': '標題不能為空'}), 400
            activity.title = data['title']
        
        if 'type' in data:
            if not data['type'] or not data['type'].strip():
                return jsonify({'error': '類型不能為空'}), 400
            activity.category = data['type']  # 前端傳 type，後端存為 category
        
        if 'location' in data:
            if not data['location'] or not data['location'].strip():
                return jsonify({'error': '地點不能為空'}), 400
            activity.location = data['location']
        if 'start_date' in data:
            if not data['start_date'] or not data['start_date'].strip():
                return jsonify({'error': '開始日期不能為空'}), 400
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')).date()
            activity.date = start_date  # 保留舊欄位
            activity.start_date = start_date
        if 'end_date' in data:
            activity.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')).date()
        
        # 驗證日期範圍：開始日期必須早於或等於結束日期
        if activity.start_date and activity.end_date:
            if activity.start_date > activity.end_date:
                return jsonify({'error': 'start_date must be before or equal to end_date'}), 400
        
        if 'start_time' in data:
            time_str = data['start_time']
            if len(time_str) == 8:  # HH:MM:SS
                activity.start_time = datetime.strptime(time_str, '%H:%M:%S').time()
            else:  # HH:MM
                activity.start_time = datetime.strptime(time_str, '%H:%M').time()
        if 'end_time' in data:
            time_str = data['end_time']
            if len(time_str) == 8:
                activity.end_time = datetime.strptime(time_str, '%H:%M:%S').time()
            else:
                activity.end_time = datetime.strptime(time_str, '%H:%M').time()
        if 'max_members' in data:
            if not isinstance(data['max_members'], int) or data['max_members'] <= 0:
                return jsonify({'error': '最大人數必須大於0'}), 400
            activity.max_participants = data['max_members']  # 前端傳 max_members，後端存為 max_participants
        if 'description' in data:
            activity.description = data['description']
        if 'status' in data:
            # 如果要標記為已完成，需驗證活動是否已結束
            if data['status'] == 'completed':
                from datetime import date
                activity_end_date = activity.end_date or activity.start_date or activity.date
                if activity_end_date and activity_end_date > date.today():
                    return jsonify({'error': '活動尚未結束，無法標記為已完成'}), 400
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
        
        # 先刪除相關的討論記錄
        from models.activity_discussion import ActivityDiscussion
        ActivityDiscussion.query.filter_by(activity_id=activity_id).delete()
        
        # 再刪除活動（participants 會因 cascade 自動刪除）
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
        
        # 檢查是否已參與或已申請（pending, joined, approved）
        if activity.is_user_participant(current_user_id):
            return jsonify({'error': '您已經申請或參與此活動'}), 400
        
        # 檢查人數是否已滿
        if activity.get_participant_count() >= activity.max_participants:
            return jsonify({'error': '活動人數已滿'}), 400
        
        # 檢查是否存在歷史記錄（left, rejected 等狀態）
        existing_participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=current_user_id
        ).first()
        
        if existing_participant:
            # 如果存在歷史記錄，更新狀態為 pending 並重置相關欄位
            existing_participant.status = 'pending'
            existing_participant.message = data.get('message', '')
            existing_participant.rejection_reason = None
            existing_participant.left_at = None
            existing_participant.joined_at = datetime.utcnow()
            existing_participant.approved_at = None
            db.session.commit()
            participant = existing_participant
        else:
            # 創建新的參與申請（狀態為 pending）
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
        
        # 查找參與記錄（包含 approved 和 joined 狀態）
        participant = ActivityParticipant.query.filter(
            ActivityParticipant.activity_id == activity_id,
            ActivityParticipant.user_id == current_user_id,
            ActivityParticipant.status.in_(['approved', 'joined'])
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

@activities_bp.route('/<int:activity_id>/participants/<int:participant_id>', methods=['DELETE'])
@jwt_required()
def remove_participant(activity_id, participant_id):
    """創建者移除參與者"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 驗證權限：只有創建者可以移除參與者
        if activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動創建者可以移除參與者'}), 403
        
        participant = ActivityParticipant.query.get(participant_id)
        
        if not participant or participant.activity_id != activity_id:
            return jsonify({'error': '找不到參與者記錄'}), 404
        
        # 檢查是否為創建者自己
        if participant.user_id == current_user_id:
            return jsonify({'error': '創建者不能移除自己'}), 400
        
        # 檢查參與者狀態（只能移除已加入或已批准的參與者）
        if participant.status not in ['approved', 'joined']:
            return jsonify({'error': '只能移除已加入的參與者'}), 400
        
        # 標記為已移除
        participant.remove()
        
        return jsonify({
            'message': '已移除參與者',
            'current_participants': activity.get_participant_count()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/photos', methods=['POST'])
@jwt_required()
def upload_activity_photo(activity_id):
    """上傳活動照片（只有參與者可以上傳）"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 檢查活動是否存在
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 檢查是否為已批准的參與者（不包含 pending）
        participant = ActivityParticipant.query.filter_by(
            activity_id=activity_id,
            user_id=current_user_id
        ).filter(
            ActivityParticipant.status.in_(['joined', 'approved'])
        ).first()
        
        is_creator = activity.creator_id == current_user_id
        
        if not participant and not is_creator:
            return jsonify({'error': '只有活動參與者可以上傳照片'}), 403
        
        # 檢查是否有文件
        if 'image' not in request.files:
            return jsonify({'error': '沒有選擇文件'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': '沒有選擇文件'}), 400
        
        # 檢查文件類型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if '.' not in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': '不支持的文件類型，只允許 PNG、JPG、JPEG、GIF、WEBP'}), 400
        
        # 檢查文件大小 (5MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        max_size = 5 * 1024 * 1024  # 5MB
        if file_size > max_size:
            return jsonify({'error': '文件大小超過限制（最大 5MB）'}), 400
        
        # 確保上傳目錄存在
        upload_folder = 'uploads/activities'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{activity_id}_{current_user_id}_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        
        # 保存文件
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # 獲取當前照片列表
        current_images = []
        if activity.images:
            try:
                current_images = json.loads(activity.images)
            except:
                current_images = []
        
        # 添加新照片URL
        new_url = f"/uploads/activities/{filename}"
        current_images.append(new_url)
        
        # 更新活動
        activity.images = json.dumps(current_images)
        db.session.commit()
        
        return jsonify({
            'message': '照片上傳成功',
            'url': new_url,
            'total_photos': len(current_images)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"上傳照片失敗: {str(e)}")
        return jsonify({'error': '上傳照片失敗'}), 500
