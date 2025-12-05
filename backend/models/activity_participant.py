"""
ActivityParticipant Model - 活動參與者關聯表
記錄用戶參與活動的關係
"""
from models import db
from datetime import datetime

class ActivityParticipant(db.Model):
    __tablename__ = 'activity_participants'
    __table_args__ = {'extend_existing': True}
    
    participant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending(待審核), approved(已批准), joined(已加入), rejected(已拒絕), left(已離開), removed(被移除)
    role = db.Column(db.String(20), default='participant')  # creator, participant
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)  # 批准時間
    left_at = db.Column(db.DateTime)
    message = db.Column(db.Text)  # 申請訊息
    rejection_reason = db.Column(db.Text)  # 拒絕原因
    
    # 唯一約束：一個用戶在同一個活動中只能有一條記錄
    __table_args__ = (
        db.UniqueConstraint('activity_id', 'user_id', name='unique_activity_user'),
    )
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'participant_id': self.participant_id,
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'status': self.status,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'left_at': self.left_at.isoformat() if self.left_at else None,
            'message': self.message,
            'rejection_reason': self.rejection_reason
        }
    
    def approve(self):
        """批准申請"""
        self.status = 'approved'
        self.approved_at = datetime.utcnow()
        db.session.commit()
    
    def reject(self, reason=None):
        """拒絕申請"""
        self.status = 'rejected'
        self.rejection_reason = reason
        db.session.commit()
    
    def leave(self):
        """離開活動"""
        self.status = 'left'
        self.left_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<ActivityParticipant user:{self.user_id} activity:{self.activity_id} status:{self.status}>'
