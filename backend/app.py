from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
import os

# 匯入資料庫實例
from models import db

# 初始化其他擴充套件
jwt = JWTManager()
socketio = SocketIO()
migrate = Migrate()

def create_app(config_name=None):
    """應用程式工廠函數"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化擴充套件
    db.init_app(app)
    jwt.init_app(app)
    # Socket.IO 配置 - 使用 threading 異步模式（開發環境）
    socketio.init_app(
        app, 
        cors_allowed_origins="*",
        async_mode='threading',  # 使用 threading 異步模式
        logger=True,
        engineio_logger=False
    )
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000", 
                "http://localhost:8080",
                "https://edgesurvivor.ddns.net",
                "http://edgesurvivor.ddns.net"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 註冊 Blueprints
    from blueprints.auth import auth_bp
    from blueprints.users import users_bp
    from blueprints.activities import activities_bp
    from blueprints.matches import matches_bp
    from blueprints.chat import chat_bp
    from blueprints.discussions import discussions_bp
    from blueprints.expenses import expenses_bp
    from blueprints.upload import upload_bp
    from blueprints.reviews import reviews_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(activities_bp, url_prefix='/api/activities')
    app.register_blueprint(matches_bp, url_prefix='/api/matches')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(discussions_bp, url_prefix='/api')
    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(reviews_bp, url_prefix='/api')
    
    # 匯入模型（確保資料表被建立）
    from models.user import User
    from models.activity import Activity
    from models.match import Match
    from models.chat_message import ChatMessage
    from models.activity_participant import ActivityParticipant
    from models.activity_discussion import ActivityDiscussion
    from models.expense import Expense
    
    # 基本路由
    @app.route('/')
    def index():
        return jsonify({
            'message': 'EdgeSurvivor API is running!',
            'version': '1.0.0',
            'status': 'healthy'
        })
    
    @app.route('/api/health')
    def health_check():
        try:
            # 測試資料庫連線 - 修正 SQLAlchemy 2.x 語法
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db_status = 'connected'
        except Exception:
            db_status = 'disconnected'
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'version': '1.0.0'
        })
    
    # 靜態文件服務（用於提供上傳的圖片）
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    
    # JWT 錯誤處理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'message': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'message': 'Authorization token is required'}), 401
    
    # Socket.IO 事件處理
    from socketio_events import register_socketio_events
    register_socketio_events(socketio, app)
    
    return app

# 只在直接執行時建立 app
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    # 在 Docker 開發環境中允許使用 Werkzeug
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)