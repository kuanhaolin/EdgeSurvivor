from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.match import Match
from models.user import User
from models.activity import Activity

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/recommended', methods=['GET'])
@jwt_required()
def get_recommended_matches():
    """獲取推薦媒合（返回所有活躍用戶，排除自己和已發送請求的用戶）"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 獲取已經發送過媒合請求的用戶 ID（作為 user_a 發送的）
        sent_match_user_ids = db.session.query(Match.user_b).filter(
            Match.user_a == current_user_id,
            Match.status.in_(['pending', 'accepted'])
        ).all()
        sent_match_user_ids = [uid[0] for uid in sent_match_user_ids]
        
        # 獲取已經收到媒合請求的用戶 ID（作為 user_b 收到的）
        received_match_user_ids = db.session.query(Match.user_a).filter(
            Match.user_b == current_user_id,
            Match.status.in_(['pending', 'accepted'])
        ).all()
        received_match_user_ids = [uid[0] for uid in received_match_user_ids]
        
        # 合併排除列表
        excluded_user_ids = set(sent_match_user_ids + received_match_user_ids + [current_user_id])
        
        # 獲取其他活躍用戶（排除已媒合或待處理的用戶）
        users = User.query.filter(
            User.user_id.notin_(excluded_user_ids),
            User.is_active == True
        ).limit(20).all()
        
        return jsonify({
            'matches': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_matches():
    """獲取待處理的媒合請求"""
    try:
        current_user_id = int(get_jwt_identity())
        
        print(f"[DEBUG] 查詢待處理媒合，當前用戶 ID: {current_user_id}")
        
        # 獲取待處理的媒合（user_b 是當前用戶且狀態為 pending）
        matches = Match.query.filter(
            Match.user_b == current_user_id,
            Match.status == 'pending'
        ).all()
        
        print(f"[DEBUG] 找到 {len(matches)} 個待處理媒合")
        
        result = []
        for match in matches:
            print(f"[DEBUG] 媒合 ID: {match.match_id}, 發送者: {match.user_a}, 接收者: {match.user_b}, 狀態: {match.status}")
            
            match_dict = {
                'match_id': match.match_id,
                'created_at': match.match_date.isoformat() if match.match_date else None,
                'message': match.message
            }
            
            # 添加發送者資訊
            requester = User.query.get(match.user_a)
            if requester:
                requester_dict = requester.to_dict()
                match_dict['requester'] = {
                    'user_id': requester_dict['user_id'],
                    'name': requester_dict['name'],
                    'avatar': requester_dict['avatar'],
                    'interests': requester_dict.get('interests', [])
                }
            
            # 添加活動資訊
            if match.activity_id:
                activity = Activity.query.get(match.activity_id)
                if activity:
                    match_dict['activity'] = {
                        'activity_id': activity.activity_id,
                        'title': activity.title,
                        'start_date': activity.date.isoformat() if activity.date else None
                    }
            
            result.append(match_dict)
        
        print(f"[DEBUG] 返回 {len(result)} 個待處理媒合")
        
        return jsonify({'matches': result}), 200
        
    except Exception as e:
        print(f"[ERROR] 載入待處理媒合失敗: {e}")
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/sent', methods=['GET'])
@jwt_required()
def get_sent_matches():
    """獲取已發送的媒合請求"""
    try:
        current_user_id = int(get_jwt_identity())
        
        print(f"[DEBUG] 查詢已發送媒合，當前用戶 ID: {current_user_id}")
        
        # 獲取已發送的媒合（user_a 是當前用戶）
        matches = Match.query.filter(
            Match.user_a == current_user_id
        ).all()
        
        print(f"[DEBUG] 找到 {len(matches)} 個已發送媒合")
        
        result = []
        for match in matches:
            print(f"[DEBUG] 媒合 ID: {match.match_id}, 接收者: {match.user_b}, 狀態: {match.status}")
            
            match_dict = {
                'match_id': match.match_id,
                'created_at': match.match_date.isoformat() if match.match_date else None,
                'status': match.status
            }
            
            # 添加接收者資訊
            responder = User.query.get(match.user_b)
            if responder:
                responder_dict = responder.to_dict()
                match_dict['responder'] = {
                    'user_id': responder_dict['user_id'],
                    'name': responder_dict['name'],
                    'avatar': responder_dict['avatar'],
                    'interests': responder_dict.get('interests', [])
                }
            
            # 添加活動資訊
            if match.activity_id:
                activity = Activity.query.get(match.activity_id)
                if activity:
                    match_dict['activity'] = {
                        'activity_id': activity.activity_id,
                        'title': activity.title,
                        'start_date': activity.date.isoformat() if activity.date else None
                    }
            
            result.append(match_dict)
        
        print(f"[DEBUG] 返回 {len(result)} 個已發送媒合")
        
        return jsonify({'matches': result}), 200
        
    except Exception as e:
        print(f"[ERROR] 載入已發送媒合失敗: {e}")
        return jsonify({'error': str(e)}), 500

@matches_bp.route('', methods=['GET'])
@jwt_required()
def get_matches():
    """獲取已媒合列表"""
    try:
        current_user_id = int(get_jwt_identity())
        status_filter = request.args.get('status', 'accepted')
        
        # 獲取符合條件的媒合
        matches = Match.query.filter(
            db.or_(
                Match.user_a == current_user_id,
                Match.user_b == current_user_id
            ),
            Match.status == status_filter
        ).all()
        
        result = []
        for match in matches:
            # 確定對方用戶
            other_user_id = match.user_b if match.user_a == current_user_id else match.user_a
            other_user = User.query.get(other_user_id)
            
            match_dict = {
                'match_id': match.match_id,
                'status': match.status,
                'created_at': match.match_date.isoformat() if match.match_date else None,
                'requester_id': match.user_a,
                'responder_id': match.user_b
            }
            
            # 添加對方用戶資訊
            if other_user:
                other_user_dict = other_user.to_dict()
                match_dict['requester' if match.user_a != current_user_id else 'responder'] = {
                    'user_id': other_user_dict['user_id'],
                    'name': other_user_dict['name'],
                    'avatar': other_user_dict['avatar'],
                    'interests': other_user_dict.get('interests', [])
                }
            
            # 添加活動資訊
            if match.activity_id:
                activity = Activity.query.get(match.activity_id)
                if activity:
                    match_dict['activity'] = {
                        'activity_id': activity.activity_id,
                        'title': activity.title,
                        'start_date': activity.date.isoformat() if activity.date else None
                    }
            
            result.append(match_dict)
        
        return jsonify({'matches': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('', methods=['POST'])
@jwt_required()
def create_match():
    """發送媒合請求"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        print(f"[DEBUG] 創建媒合請求，當前用戶: {current_user_id}, 請求數據: {data}")
        
        # 支持兩種方式：1) responder_id (一般媒合), 2) user_id + activity_id (活動媒合)
        target_user_id = data.get('responder_id') or data.get('user_id')
        activity_id = data.get('activity_id')
        message = data.get('message', '希望能成為旅伴！')
        
        if not target_user_id:
            return jsonify({'error': 'responder_id 或 user_id 是必需的'}), 400
        
        print(f"[DEBUG] 目標用戶: {target_user_id}, 活動 ID: {activity_id}")
        
        # 檢查是否為自己
        if current_user_id == target_user_id:
            return jsonify({'error': '不能對自己發送交友請求'}), 400
        
        # 檢查目標用戶是否存在
        target_user = User.query.get(target_user_id)
        if not target_user:
            return jsonify({'error': '找不到目標用戶'}), 404
        
        # 如果有 activity_id，檢查活動是否存在
        if activity_id:
            activity = Activity.query.get(activity_id)
            if not activity:
                return jsonify({'error': '找不到活動'}), 404
        
        # 檢查是否已存在媒合請求（雙向檢查）
        # 檢查 A -> B 方向
        existing_match_ab = Match.query.filter(
            Match.user_a == current_user_id,
            Match.user_b == target_user_id
        )
        
        # 檢查 B -> A 方向（對方發給我的）
        existing_match_ba = Match.query.filter(
            Match.user_a == target_user_id,
            Match.user_b == current_user_id
        )
        
        if activity_id:
            existing_match_ab = existing_match_ab.filter(Match.activity_id == activity_id)
            existing_match_ba = existing_match_ba.filter(Match.activity_id == activity_id)
        else:
            existing_match_ab = existing_match_ab.filter(Match.activity_id.is_(None))
            existing_match_ba = existing_match_ba.filter(Match.activity_id.is_(None))
        
        match_ab = existing_match_ab.first()
        match_ba = existing_match_ba.first()
        
        # 檢查是否已經發送過請求（任何狀態）
        if match_ab:
            if match_ab.status == 'pending':
                print(f"[DEBUG] 已存在待處理的媒合請求: {match_ab.match_id}")
                return jsonify({'error': '已發送過交友請求，請等待對方回應'}), 400
            elif match_ab.status in ['accepted', 'confirmed']:
                print(f"[DEBUG] 已經是好友: {match_ab.match_id}")
                return jsonify({'error': '你們已經是好友了'}), 400
        
        # 檢查對方是否已經發送過請求給我
        if match_ba:
            if match_ba.status == 'pending':
                print(f"[DEBUG] 對方已發送交友請求: {match_ba.match_id}")
                return jsonify({'error': '對方已向你發送交友請求，請到「待處理」頁面查看'}), 400
            elif match_ba.status in ['accepted', 'confirmed']:
                print(f"[DEBUG] 已經是好友: {match_ba.match_id}")
                return jsonify({'error': '你們已經是好友了'}), 400
        
        # 創建媒合請求
        match = Match(
            activity_id=activity_id,
            user_a=current_user_id,
            user_b=target_user_id,
            status='pending',
            message=message
        )
        
        db.session.add(match)
        db.session.commit()
        
        print(f"[DEBUG] 媒合請求創建成功: {match.match_id}")
        
        return jsonify({
            'message': '媒合請求已發送',
            'match': match.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] 創建媒合請求失敗: {e}")
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/<int:match_id>/accept', methods=['PUT'])
@jwt_required()
def accept_match(match_id):
    """接受媒合請求"""
    try:
        current_user_id = int(get_jwt_identity())
        match = Match.query.get(match_id)
        
        if not match:
            return jsonify({'error': '找不到媒合請求'}), 404
        
        if match.user_b != current_user_id:
            return jsonify({'error': '無權限操作此媒合請求'}), 403
        
        match.status = 'accepted'
        db.session.commit()
        
        return jsonify({
            'message': '已接受媒合請求',
            'match': match.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/<int:match_id>/reject', methods=['PUT'])
@jwt_required()
def reject_match(match_id):
    """拒絕媒合請求"""
    try:
        current_user_id = int(get_jwt_identity())
        match = Match.query.get(match_id)
        
        if not match:
            return jsonify({'error': '找不到媒合請求'}), 404
        
        if match.user_b != current_user_id:
            return jsonify({'error': '無權限操作此媒合請求'}), 403
        
        match.status = 'rejected'
        db.session.commit()
        
        return jsonify({
            'message': '已拒絕媒合請求',
            'match': match.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/<int:match_id>', methods=['DELETE'])
@jwt_required()
def cancel_match(match_id):
    """取消/刪除媒合請求
    - pending 狀態：只有發送者可以取消
    - accepted 狀態：雙方都可以刪除好友關係
    """
    try:
        current_user_id = int(get_jwt_identity())
        match = Match.query.get(match_id)
        
        if not match:
            return jsonify({'error': '找不到媒合請求'}), 404
        
        # 檢查權限
        if match.status == 'pending':
            # pending 狀態：只有發送者可以取消
            if match.user_a != current_user_id:
                return jsonify({'error': '只有發送者可以取消待審核的媒合請求'}), 403
        elif match.status == 'accepted':
            # accepted 狀態：雙方都可以刪除好友關係
            if match.user_a != current_user_id and match.user_b != current_user_id:
                return jsonify({'error': '無權刪除此好友關係'}), 403
        else:
            # rejected 等其他狀態不允許刪除
            return jsonify({'error': f'無法刪除 {match.status} 狀態的媒合請求'}), 400
        
        db.session.delete(match)
        db.session.commit()
        
        action = '已取消媒合請求' if match.status == 'pending' else '已刪除好友關係'
        print(f"[DEBUG] 媒合請求 {match_id} ({match.status}) 已被用戶 {current_user_id} 刪除")
        
        return jsonify({'message': action}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] 取消/刪除媒合請求失敗: {e}")
        return jsonify({'error': str(e)}), 500
