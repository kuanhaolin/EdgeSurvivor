from models import db
from sqlalchemy import Numeric
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    
    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # adventure, culture, leisure, food, sports, etc.
    max_participants = db.Column(db.Integer, default=2)
    cost = db.Column(Numeric(10, 2), default=0.00)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 額外的活動屬性
    meeting_point = db.Column(db.String(255))  # 集合地點
    duration_hours = db.Column(db.Integer)  # 預計時長（小時）
    difficulty_level = db.Column(db.String(20))  # easy, medium, hard
    gender_preference = db.Column(db.String(20))  # any, male, female
    age_min = db.Column(db.Integer)
    age_max = db.Column(db.Integer)
    notes = db.Column(db.Text)  # 特別注意事項
    
    # 圖片相關
    cover_image = db.Column(db.String(500))  # 封面圖片 URL
    images = db.Column(db.Text)  # 活動照片 URLs (JSON 格式存儲)
    
    # 關聯 - 使用字串引用避免循環匯入
    # creator 關聯已在 User 模型中透過 backref 定義
    matches = db.relationship('Match', backref='activity', lazy='dynamic')
    participants = db.relationship('ActivityParticipant', backref='activity', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_creator_info=False):
        """轉換為字典格式"""
        data = {
            'activity_id': self.activity_id,
            'title': self.title,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'description': self.description,
            'category': self.category,
            'max_participants': self.max_participants,
            'cost': float(self.cost) if self.cost else 0.0,
            'status': self.status,
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'meeting_point': self.meeting_point,
            'duration_hours': self.duration_hours,
            'difficulty_level': self.difficulty_level,
            'gender_preference': self.gender_preference,
            'age_min': self.age_min,
            'age_max': self.age_max,
            'notes': self.notes,
            'current_participants': self.get_participant_count(),
            'cover_image': self.cover_image,
            'images': self.images
        }
        
        if include_creator_info and self.creator:
            data['creator'] = {
                'user_id': self.creator.user_id,
                'name': self.creator.name,
                'profile_picture': self.creator.profile_picture
            }
        
        return data
    
    def get_participant_count(self):
        """取得當前參與人數（只計算已批准和創建者）"""
        from models.activity_participant import ActivityParticipant
        # 統計已批准的參與者（包括創建者的 joined 狀態）
        active_participants = ActivityParticipant.query.filter_by(
            activity_id=self.activity_id
        ).filter(
            ActivityParticipant.status.in_(['joined', 'approved'])
        ).count()
        return active_participants
    
    def get_participants(self):
        """獲取所有已批准的參與者列表"""
        from models.activity_participant import ActivityParticipant
        return ActivityParticipant.query.filter_by(
            activity_id=self.activity_id
        ).filter(
            ActivityParticipant.status.in_(['joined', 'approved'])
        ).all()
    
    def get_pending_participants(self):
        """獲取待審核的申請列表"""
        from models.activity_participant import ActivityParticipant
        return ActivityParticipant.query.filter_by(
            activity_id=self.activity_id,
            status='pending'
        ).all()
    
    def is_user_participant(self, user_id):
        """檢查用戶是否已參與活動（包括待審核）"""
        from models.activity_participant import ActivityParticipant
        participant = ActivityParticipant.query.filter_by(
            activity_id=self.activity_id,
            user_id=user_id
        ).filter(
            ActivityParticipant.status.in_(['pending', 'joined', 'approved'])
        ).first()
        return participant is not None
    
    def is_full(self):
        """檢查活動是否已滿"""
        return self.get_participant_count() >= self.max_participants
    
    def can_user_join(self, user):
        """檢查使用者是否可以加入活動"""
        if self.creator_id == user.user_id:
            return False, "不能加入自己創建的活動"
        
        if self.is_full():
            return False, "活動人數已滿"
        
        if self.status != 'active':
            return False, "活動已結束或取消"
        
        # 檢查是否已經有媒合紀錄 - 延遲匯入避免循環引用
        from models.match import Match
        existing_match = self.matches.filter(
            db.or_(
                db.and_(Match.user_a == user.user_id, Match.user_b == self.creator_id),
                db.and_(Match.user_a == self.creator_id, Match.user_b == user.user_id)
            )
        ).first()
        
        if existing_match:
            return False, "已經申請過此活動"
        
        # 檢查性別偏好
        if self.gender_preference and self.gender_preference != 'any':
            if user.gender != self.gender_preference:
                return False, f"此活動僅限 {self.gender_preference}"
        
        # 檢查年齡限制
        if self.age_min and user.age and user.age < self.age_min:
            return False, f"年齡需滿 {self.age_min} 歲"
        
        if self.age_max and user.age and user.age > self.age_max:
            return False, f"年齡不能超過 {self.age_max} 歲"
        
        return True, "可以加入"
    
    def __repr__(self):
        return f'<Activity {self.title}>'