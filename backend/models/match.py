from models import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    __table_args__ = {'extend_existing': True}
    
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=True)  # 改為可以為 NULL
    user_a = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 申請者
    user_b = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 活動創建者
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, rejected, cancelled
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_date = db.Column(db.DateTime)
    cancel_date = db.Column(db.DateTime)
    
    # 額外資訊
    message = db.Column(db.Text)  # 申請時的訊息
    rejection_reason = db.Column(db.Text)  # 拒絕原因
    
    # 關聯 - 使用字串引用避免循環匯入
    chat_messages = db.relationship('ChatMessage', backref='match', lazy='dynamic')
    
    def to_dict(self, include_users_info=False):
        """轉換為字典格式"""
        data = {
            'match_id': self.match_id,
            'activity_id': self.activity_id,
            'user_a': self.user_a,
            'user_b': self.user_b,
            'status': self.status,
            'match_date': self.match_date.isoformat() if self.match_date else None,
            'confirmed_date': self.confirmed_date.isoformat() if self.confirmed_date else None,
            'cancel_date': self.cancel_date.isoformat() if self.cancel_date else None,
            'message': self.message,
            'rejection_reason': self.rejection_reason
        }
        
        if include_users_info:
            data['activity_info'] = self.activity.to_dict() if self.activity else None
            data['user_a_info'] = self.user_a_ref.to_dict() if self.user_a_ref else None
            data['user_b_info'] = self.user_b_ref.to_dict() if self.user_b_ref else None
        
        return data
    
    def confirm(self):
        """確認媒合"""
        self.status = 'confirmed'
        self.confirmed_date = datetime.utcnow()
        db.session.commit()
    
    def reject(self, reason=None):
        """拒絕媒合"""
        self.status = 'rejected'
        self.rejection_reason = reason
        db.session.commit()
    
    def cancel(self):
        """取消媒合"""
        self.status = 'cancelled'
        self.cancel_date = datetime.utcnow()
        db.session.commit()
    
    def get_other_user(self, current_user_id):
        """取得對方使用者ID"""
        return self.user_b if current_user_id == self.user_a else self.user_a
    
    def is_participant(self, user_id):
        """檢查使用者是否參與此媒合"""
        return user_id in [self.user_a, self.user_b]
    
    def __repr__(self):
        return f'<Match {self.match_id}: {self.user_a} <-> {self.user_b}>'