"""
活動費用 API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.activity import Activity
from models.expense import Expense
from datetime import datetime
import json

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/activities/<int:activity_id>/expenses', methods=['GET'])
@jwt_required()
def get_expenses(activity_id):
    """獲取活動費用列表"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 檢查權限
        if not activity.is_user_participant(current_user_id) and activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動參與者可以查看費用'}), 403
        
        expenses = Expense.query.filter_by(activity_id=activity_id).all()
        
        # 計算總費用和每人應分攤金額
        total_amount = sum(float(e.amount) for e in expenses)
        participant_count = activity.get_participant_count()
        per_person = total_amount / participant_count if participant_count > 0 else 0
        
        return jsonify({
            'expenses': [e.to_dict(include_details=True) for e in expenses],
            'summary': {
                'total_amount': total_amount,
                'participant_count': participant_count,
                'per_person': per_person
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/activities/<int:activity_id>/expenses', methods=['POST'])
@jwt_required()
def create_expense(activity_id):
    """創建費用記錄"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        # 檢查權限
        if not activity.is_user_participant(current_user_id) and activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動參與者可以添加費用'}), 403
        
        if not data.get('amount'):
            return jsonify({'error': '金額為必填'}), 400
        
        # 處理參與分攤的人員
        participants = data.get('participants', [])
        if not participants:
            # 默認所有參與者
            participants = [p.user_id for p in activity.get_participants()]
        
        expense = Expense(
            activity_id=activity_id,
            payer_id=current_user_id,
            amount=data['amount'],
            description=data.get('description', ''),
            category=data.get('category', 'other'),
            is_split=data.get('is_split', True),
            split_method=data.get('split_method', 'equal'),
            participants=json.dumps(participants)
        )
        
        if data.get('expense_date'):
            expense.expense_date = datetime.fromisoformat(data['expense_date']).date()
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': '費用記錄已創建',
            'expense': expense.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """刪除費用記錄"""
    try:
        current_user_id = int(get_jwt_identity())
        expense = Expense.query.get(expense_id)
        
        if not expense:
            return jsonify({'error': '找不到費用記錄'}), 404
        
        activity = Activity.query.get(expense.activity_id)
        
        # 只有付款者或活動創建者可以刪除
        if expense.payer_id != current_user_id and activity.creator_id != current_user_id:
            return jsonify({'error': '無權限刪除此費用記錄'}), 403
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': '費用記錄已刪除'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/activities/<int:activity_id>/expenses/settlement', methods=['GET'])
@jwt_required()
def get_settlement(activity_id):
    """計算費用結算（誰應該付誰多少錢）"""
    try:
        current_user_id = int(get_jwt_identity())
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': '找不到活動'}), 404
        
        if not activity.is_user_participant(current_user_id) and activity.creator_id != current_user_id:
            return jsonify({'error': '只有活動參與者可以查看結算'}), 403
        
        expenses = Expense.query.filter_by(activity_id=activity_id).all()
        participants = activity.get_participants()
        participant_ids = [p.user_id for p in participants]
        
        # 計算每個人的支出和應付金額
        balance = {}  # user_id: 餘額 (正數=別人欠我，負數=我欠別人)
        
        for participant_id in participant_ids:
            balance[participant_id] = 0
        
        total_amount = 0
        for expense in expenses:
            if expense.is_split:
                # 解析參與分攤的人員
                try:
                    split_participants = json.loads(expense.participants) if expense.participants else participant_ids
                except:
                    split_participants = participant_ids
                
                split_count = len(split_participants)
                if split_count > 0:
                    per_person = float(expense.amount) / split_count
                    
                    # 付款者的餘額增加
                    balance[expense.payer_id] = balance.get(expense.payer_id, 0) + float(expense.amount)
                    
                    # 每個參與分攤的人減少
                    for pid in split_participants:
                        balance[pid] = balance.get(pid, 0) - per_person
                
                total_amount += float(expense.amount)
        
        # 生成結算清單
        settlements = []
        creditors = {k: v for k, v in balance.items() if v > 0.01}  # 債權人
        debtors = {k: v for k, v in balance.items() if v < -0.01}   # 債務人
        
        for debtor_id, debt in debtors.items():
            for creditor_id, credit in list(creditors.items()):
                if credit < 0.01:
                    continue
                
                amount = min(abs(debt), credit)
                if amount > 0.01:
                    from models.user import User
                    debtor = User.query.get(debtor_id)
                    creditor = User.query.get(creditor_id)
                    
                    settlements.append({
                        'from_user_id': debtor_id,
                        'from_user_name': debtor.name if debtor else '未知',
                        'to_user_id': creditor_id,
                        'to_user_name': creditor.name if creditor else '未知',
                        'amount': round(amount, 2)
                    })
                    
                    creditors[creditor_id] -= amount
                    debt += amount
                    
                    if abs(debt) < 0.01:
                        break
        
        return jsonify({
            'settlements': settlements,
            'total_amount': total_amount,
            'participant_count': len(participant_ids)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
