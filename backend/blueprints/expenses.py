"""
活動費用 API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.activity import Activity
from models.expense import Expense
from models.user import User
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
        
        # 計算總費用和每人平均（只計算全體平攤的費用）
        participant_count = activity.get_participant_count()
        all_split_amount = sum(float(e.amount) for e in expenses if e.split_type == 'all')
        total_amount = all_split_amount
        per_person = all_split_amount / participant_count if participant_count > 0 else 0
        
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
        
        # 驗證必填欄位
        description = data.get('description', '').strip()
        if not description:
            return jsonify({'error': '費用項目為必填'}), 400
        
        amount = data.get('amount')
        if not amount or amount <= 0:
            return jsonify({'error': '金額必須大於0'}), 400
        
        category = data.get('category', '').strip()
        valid_categories = ['transport', 'accommodation', 'food', 'ticket', 'other']
        if not category or category not in valid_categories:
            return jsonify({'error': '請選擇有效的類別'}), 400
        
        # 獲取代墊人（付款人）
        payer_id = data.get('payer_id')
        if not payer_id:
            return jsonify({'error': '請選擇代墊人'}), 400
        
        # 驗證代墊人是否存在
        payer = User.query.get(payer_id)
        if not payer:
            return jsonify({'error': '代墊人不存在'}), 404
        
        # 獲取分攤類型
        split_type = data.get('split_type', '').strip()
        valid_split_types = ['all', 'selected', 'borrow']
        if not split_type or split_type not in valid_split_types:
            return jsonify({'error': '請選擇有效的分攤方式'}), 400
        
        # 處理參與分攤的人員
        split_participants = data.get('split_participants', [])
        
        # 如果是 selected 模式，必須有參與者且包含代墊人
        if split_type == 'selected':
            if not split_participants or len(split_participants) == 0:
                return jsonify({'error': '請選擇至少一位參與分攤的人'}), 400
            if payer_id not in split_participants:
                return jsonify({'error': '代墊人必須參與分攤'}), 400
        
        # 如果是全體分攤且未指定參與者，預設為所有參與者
        if split_type == 'all' and not split_participants:
            split_participants = [p.user_id for p in activity.get_participants()]
        
        # 借款人
        borrower_id = data.get('borrower_id', None)
        if split_type == 'borrow':
            if not borrower_id:
                return jsonify({'error': '請選擇借款人'}), 400
            # 驗證借款人是否存在
            borrower = User.query.get(borrower_id)
            if not borrower:
                return jsonify({'error': '借款人不存在'}), 404
        
        expense = Expense(
            activity_id=activity_id,
            payer_id=payer_id,
            amount=amount,
            description=description,
            category=category,
            split_type=split_type,
            is_split=(split_type != 'borrow'),  # 借款不分攤
            split_method='equal',
            split_participants=json.dumps(split_participants) if split_participants else None,
            borrower_id=borrower_id
        )
        
        if data.get('expense_date'):
            try:
                expense.expense_date = datetime.fromisoformat(data['expense_date'].replace('Z', '+00:00')).date()
            except:
                expense.expense_date = datetime.fromisoformat(data['expense_date']).date()
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': '費用記錄已創建',
            'expense': expense.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"創建費用失敗: {str(e)}")
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
            # 處理借款邏輯（不計入 total_amount）
            if expense.split_type == 'borrow' and expense.borrower_id:
                # 借款人欠代墊人
                balance[expense.borrower_id] = balance.get(expense.borrower_id, 0) - float(expense.amount)
                balance[expense.payer_id] = balance.get(expense.payer_id, 0) + float(expense.amount)
                # 借款不計入總費用
                continue
            
            # 處理分攤邏輯
            if expense.is_split or expense.split_type in ['all', 'selected']:
                # 解析參與分攤的人員
                try:
                    split_participants = json.loads(expense.split_participants) if expense.split_participants else []
                    # 向後兼容：如果沒有 split_participants 但有 participants
                    if not split_participants and expense.participants:
                        split_participants = json.loads(expense.participants)
                    # 如果還是沒有，預設為所有參與者
                    if not split_participants:
                        split_participants = participant_ids
                except:
                    split_participants = participant_ids
                
                split_count = len(split_participants)
                if split_count > 0:
                    per_person = float(expense.amount) / split_count
                    
                    # 付款者的餘額增加
                    balance[expense.payer_id] = balance.get(expense.payer_id, 0) + float(expense.amount)
                    
                    # 每個參與分攤的人減少
                    for pid in split_participants:
                        if pid in balance:  # 確保參與者在活動中
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

@expenses_bp.route('/expenses/user/<int:user_id>/stats', methods=['GET'])
@jwt_required()
def get_user_expense_stats(user_id):
    """獲取用戶個人費用統計"""
    try:
        from sqlalchemy.orm import joinedload
        from datetime import date
        
        current_user_id = int(get_jwt_identity())
        
        # 權限檢查：用戶只能查看自己的統計
        if current_user_id != user_id:
            return jsonify({'error': '無權限查看其他用戶的統計'}), 403
        
        # 驗證用戶是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用戶不存在'}), 404
        
        # 獲取 query 參數
        group_by = request.args.get('group_by', None)
        start_date_str = request.args.get('start_date', None)
        end_date_str = request.args.get('end_date', None)
        
        # 驗證和解析日期參數
        start_date = None
        end_date = None
        
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '無效的 start_date 格式，請使用 YYYY-MM-DD'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '無效的 end_date 格式，請使用 YYYY-MM-DD'}), 400
        
        # 驗證 group_by 參數
        if group_by and group_by != 'activity':
            return jsonify({'error': '無效的 group_by 參數，只支援 "activity"'}), 400
        
        # 構建基礎查詢
        query = Expense.query
        
        # 應用日期篩選
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)
        
        # 預載活動資料以避免 N+1 查詢
        if group_by == 'activity':
            query = query.options(joinedload(Expense.activity))
        
        # 獲取所有相關費用
        all_expenses = query.all()
        
        # 計算統計資料
        def calculate_user_split_amount(expense, user_id):
            """計算用戶在單一費用中的分攤金額"""
            amount = float(expense.amount)
            
            # 借款類型
            if expense.split_type == 'borrow':
                if expense.borrower_id == user_id:
                    return amount  # 借款人欠全額
                return 0
            
            # 分攤類型
            if expense.split_type in ['all', 'selected'] or expense.is_split:
                try:
                    # 解析分攤參與者
                    split_participants = []
                    if expense.split_participants:
                        split_participants = json.loads(expense.split_participants)
                    elif expense.participants:  # 向後兼容
                        split_participants = json.loads(expense.participants)
                    
                    # 如果是 'all' 類型且沒有明確的參與者列表
                    if expense.split_type == 'all' and not split_participants:
                        # 獲取活動的所有參與者
                        if expense.activity:
                            activity = expense.activity
                            split_participants = [p.user_id for p in activity.get_participants()]
                    
                    # 檢查用戶是否在分攤列表中
                    if split_participants and user_id in split_participants:
                        return amount / len(split_participants)
                    
                except (json.JSONDecodeError, TypeError):
                    pass
            
            return 0
        
        # 計算整體統計
        total_paid = 0.0
        total_owed = 0.0
        expense_count = 0
        activities_set = set()
        
        for expense in all_expenses:
            # 計算支付金額
            if expense.payer_id == user_id:
                total_paid += float(expense.amount)
            
            # 計算應分攤金額
            split_amount = calculate_user_split_amount(expense, user_id)
            if split_amount > 0:
                total_owed += split_amount
                expense_count += 1
            
            # 記錄涉及的活動
            if expense.activity_id:
                activities_set.add(expense.activity_id)
        
        net_balance = total_paid - total_owed
        
        overall_stats = {
            'total_paid': round(total_paid, 2),
            'total_owed': round(total_owed, 2),
            'net_balance': round(net_balance, 2),
            'expense_count': expense_count,
            'activities_count': len(activities_set)
        }
        
        # 如果需要按活動分組
        if group_by == 'activity':
            activity_stats = {}
            
            for expense in all_expenses:
                activity_id = expense.activity_id
                if not activity_id:
                    continue
                
                if activity_id not in activity_stats:
                    activity_stats[activity_id] = {
                        'activity_id': activity_id,
                        'activity_title': expense.activity.title if expense.activity else '未知活動',
                        'total_paid': 0.0,
                        'total_owed': 0.0,
                        'expense_count': 0
                    }
                
                # 累加支付金額
                if expense.payer_id == user_id:
                    activity_stats[activity_id]['total_paid'] += float(expense.amount)
                
                # 累加應分攤金額
                split_amount = calculate_user_split_amount(expense, user_id)
                if split_amount > 0:
                    activity_stats[activity_id]['total_owed'] += split_amount
                    activity_stats[activity_id]['expense_count'] += 1
            
            # 計算每個活動的淨餘額並格式化
            by_activity = []
            for stats in activity_stats.values():
                stats['total_paid'] = round(stats['total_paid'], 2)
                stats['total_owed'] = round(stats['total_owed'], 2)
                stats['net_balance'] = round(stats['total_paid'] - stats['total_owed'], 2)
                by_activity.append(stats)
            
            # 按活動 ID 排序
            by_activity.sort(key=lambda x: x['activity_id'])
            
            return jsonify({
                'by_activity': by_activity,
                'overall': overall_stats
            }), 200
        
        # 返回整體統計
        return jsonify(overall_stats), 200
        
    except Exception as e:
        print(f"查詢個人費用統計失敗: {str(e)}")
        return jsonify({'error': str(e)}), 500
