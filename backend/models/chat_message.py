from models import db
from datetime import datetime

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    __table_args__ = {'extend_existing': True}
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), nullable=True)  # 改為可以為 NULL
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 添加接收者 ID
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='text')  # text, image, file
    status = db.Column(db.String(20), default='sent')  # sent, delivered, read
    is_read = db.Column(db.Boolean, default=False)  # 添加是否已讀欄位
    
    # 檔案相關（如果是圖片或檔案訊息）
    file_url = db.Column(db.String(255))
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    
    def to_dict(self, include_sender_info=False):
        """轉換為字典格式"""
        data = {
            'message_id': self.message_id,
            'match_id': self.match_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'created_at': self.timestamp.isoformat() + 'Z' if self.timestamp else None,  # 添加 Z 表示 UTC
            'timestamp': self.timestamp.isoformat() + 'Z' if self.timestamp else None,  # 添加 Z 表示 UTC
            'message_type': self.message_type,
            'status': self.status,
            'is_read': self.is_read,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'file_size': self.file_size
        }
        
        if include_sender_info and self.sender:
            data['sender_info'] = {
                'user_id': self.sender.user_id,
                'name': self.sender.name,
                'avatar': self.sender.to_dict().get('avatar')
            }
        
        return data
    
    def mark_as_read(self):
        """標記為已讀"""
        self.status = 'read'
        db.session.commit()
    
    def __repr__(self):
        return f'<ChatMessage {self.message_id}>'