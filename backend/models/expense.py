"""
Expense Model - 活動費用記錄
記錄活動的費用支出和分攤
"""
from models import db
from sqlalchemy import Numeric
from datetime import datetime

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 付款者
    amount = db.Column(Numeric(10, 2), nullable=False)  # 金額
    description = db.Column(db.Text)  # 費用描述
    expense_date = db.Column(db.Date, default=datetime.utcnow)  # 費用產生日期
    category = db.Column(db.String(50))  # 費用類別：交通、住宿、餐飲、門票、其他
    is_split = db.Column(db.Boolean, default=True)  # 是否需要分攤
    split_method = db.Column(db.String(20), default='equal')  # equal(平均), custom(自訂)
    participants = db.Column(db.Text)  # JSON 格式存儲參與分攤的人員 ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    activity = db.relationship('Activity', backref='expenses')
    payer = db.relationship('User', backref='paid_expenses')
    
    def to_dict(self, include_details=False):
        """轉換為字典格式"""
        data = {
            'expense_id': self.expense_id,
            'activity_id': self.activity_id,
            'payer_id': self.payer_id,
            'amount': float(self.amount),
            'description': self.description,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'category': self.category,
            'is_split': self.is_split,
            'split_method': self.split_method,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_details:
            if self.payer:
                data['payer'] = {
                    'user_id': self.payer.user_id,
                    'name': self.payer.name,
                    'avatar': self.payer.profile_picture
                }
            
            # 解析參與分攤的人員
            if self.participants:
                import json
                try:
                    data['participants'] = json.loads(self.participants)
                except:
                    data['participants'] = []
        
        return data
    
    def calculate_split_amount(self, participant_count):
        """計算每人應分攤金額"""
        if not self.is_split or participant_count == 0:
            return 0
        return float(self.amount) / participant_count
    
    def __repr__(self):
        return f'<Expense {self.expense_id}: {self.amount} for Activity {self.activity_id}>'
