"""
ActivityDiscussion Model - 活動討論串
記錄活動參與者之間的討論訊息
"""
from models import db
from datetime import datetime

class ActivityDiscussion(db.Model):
    __tablename__ = 'activity_discussions'
    __table_args__ = {'extend_existing': True}
    
    discussion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image, announcement
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # 關聯
    activity = db.relationship('Activity', backref='discussions')
    user = db.relationship('User', backref='activity_messages')
    
    def to_dict(self, include_user_info=True):
        """轉換為字典格式"""
        data = {
            'discussion_id': self.discussion_id,
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'message': self.message,
            'message_type': self.message_type,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,  # 添加 Z 表示 UTC
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
        
        if include_user_info and self.user:
            data['user'] = {
                'user_id': self.user.user_id,
                'name': self.user.name,
                'avatar': self.user.profile_picture
            }
        
        return data
    
    def soft_delete(self):
        """軟刪除訊息"""
        self.is_deleted = True
        db.session.commit()
    
    def __repr__(self):
        return f'<ActivityDiscussion {self.discussion_id} in Activity {self.activity_id}>'
