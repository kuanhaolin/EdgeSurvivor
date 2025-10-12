from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    privacy_setting = db.Column(db.String(20), default='public')  # public, partial, hidden
    location = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    interests = db.Column(db.Text)  # 存儲為 JSON 字串或逗號分隔
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯 - 使用字串引用避免循環匯入
    created_activities = db.relationship('Activity', backref='creator', lazy='dynamic', foreign_keys='Activity.creator_id')
    matches_as_user_a = db.relationship('Match', backref='user_a_ref', lazy='dynamic', foreign_keys='Match.user_a')
    matches_as_user_b = db.relationship('Match', backref='user_b_ref', lazy='dynamic', foreign_keys='Match.user_b')
    sent_messages = db.relationship('ChatMessage', backref='sender', lazy='dynamic', foreign_keys='ChatMessage.sender_id')
    activity_participations = db.relationship('ActivityParticipant', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """設定密碼雜湊"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """檢查密碼"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_private=False):
        """轉換為字典格式"""
        # 處理興趣標籤
        interests_list = []
        if self.interests:
            try:
                import json
                interests_list = json.loads(self.interests)
            except:
                # 如果不是 JSON,嘗試以逗號分隔
                interests_list = [i.strip() for i in self.interests.split(',') if i.strip()]
        
        data = {
            'user_id': self.user_id,
            'name': self.name,
            'location': self.location,
            'profile_picture': self.profile_picture,
            'avatar': self.profile_picture,  # 添加 avatar 別名
            'bio': self.bio,
            'gender': self.gender,
            'age': self.age,
            'interests': interests_list,  # 興趣標籤列表
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'is_verified': self.is_verified,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }
        
        if include_private:
            data.update({
                'email': self.email,
                'privacy_setting': self.privacy_setting,
                'is_active': self.is_active
            })
        
        return data
    
    def update_last_seen(self):
        """更新最後上線時間"""
        self.last_seen = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.email}>'