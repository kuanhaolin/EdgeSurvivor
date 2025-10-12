#!/usr/bin/env python3
"""
EdgeSurvivor 資料庫初始化腳本
"""

import os
import sys
from datetime import datetime, date

# 添加父目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity
from models.match import Match
from models.chat_message import ChatMessage

def init_database():
    """初始化資料庫"""
    app = create_app('development')
    
    with app.app_context():
        try:
            print("正在建立資料庫表格...")
            db.create_all()
            print("✅ 資料庫表格建立完成！")
            
            # 檢查是否需要建立測試資料
            if os.environ.get('CREATE_TEST_DATA', 'false').lower() == 'true':
                create_test_data()
            else:
                print("💡 如需建立測試資料，請設定環境變數：CREATE_TEST_DATA=true")
                
        except Exception as e:
            print(f"❌ 建立資料庫表格時發生錯誤：{e}")
            return False
    
    return True

def create_test_data():
    """建立測試資料"""
    print("正在建立測試資料...")
    
    try:
        # 建立測試使用者
        users_data = [
            {
                'name': '小明',
                'email': 'ming@example.com',
                'password': 'password123',
                'gender': 'male',
                'age': 25,
                'location': '台北市',
                'bio': '喜歡旅行和探索新地方！'
            },
            {
                'name': '小花',
                'email': 'hua@example.com',
                'password': 'password123',
                'gender': 'female',
                'age': 23,
                'location': '新北市',
                'bio': '熱愛美食和攝影的女孩'
            },
            {
                'name': '阿傑',
                'email': 'jay@example.com',
                'password': 'password123',
                'gender': 'male',
                'age': 28,
                'location': '桃園市',
                'bio': '戶外運動愛好者'
            }
        ]
        
        created_users = []
        for user_data in users_data:
            # 檢查用戶是否已存在
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    gender=user_data['gender'],
                    age=user_data['age'],
                    location=user_data['location'],
                    bio=user_data['bio']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                created_users.append(user)
        
        db.session.commit()
        print(f"✅ 建立了 {len(created_users)} 個測試使用者")
        
        # 建立測試活動
        if created_users:
            activities_data = [
                {
                    'title': '陽明山賞花一日遊',
                    'date': date(2024, 3, 15),
                    'location': '陽明山國家公園',
                    'description': '春天到了！一起去陽明山看櫻花吧～',
                    'category': 'leisure',
                    'max_participants': 4,
                    'cost': 500,
                    'creator_id': created_users[0].user_id
                },
                {
                    'title': '九份老街美食之旅',
                    'date': date(2024, 3, 20),
                    'location': '九份老街',
                    'description': '探索九份的美食和歷史文化',
                    'category': 'food',
                    'max_participants': 3,
                    'cost': 800,
                    'creator_id': created_users[1].user_id
                },
                {
                    'title': '大稻埕河濱腳踏車',
                    'date': date(2024, 3, 25),
                    'location': '大稻埕碼頭',
                    'description': '騎腳踏車沿著淡水河畔，享受悠閒時光',
                    'category': 'sports',
                    'max_participants': 5,
                    'cost': 200,
                    'creator_id': created_users[2].user_id
                }
            ]
            
            created_activities = []
            for activity_data in activities_data:
                activity = Activity(**activity_data)
                db.session.add(activity)
                created_activities.append(activity)
            
            db.session.commit()
            print(f"✅ 建立了 {len(created_activities)} 個測試活動")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ 建立測試資料時發生錯誤：{e}")

def drop_all_tables():
    """刪除所有表格"""
    app = create_app('development')
    
    with app.app_context():
        print("⚠️  警告：即將刪除所有資料庫表格...")
        confirm = input("確定要繼續嗎？(y/N): ")
        
        if confirm.lower() == 'y':
            try:
                db.drop_all()
                print("✅ 所有表格已刪除！")
            except Exception as e:
                print(f"❌ 刪除表格時發生錯誤：{e}")
        else:
            print("操作已取消")

def test_connection():
    """測試資料庫連線"""
    app = create_app('development')
    
    with app.app_context():
        try:
            # 執行簡單查詢測試連線 - 修正 SQLAlchemy 2.x 語法
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ 資料庫連線成功！")
            
            # 顯示連線資訊
            engine = db.engine
            print(f"📊 資料庫類型：{engine.dialect.name}")
            print(f"🔗 連線字串：{str(engine.url).replace(str(engine.url.password), '***')}")
            
            return True
        except Exception as e:
            print(f"❌ 資料庫連線失敗：{e}")
            print("\n🔧 請檢查：")
            print("1. MariaDB 服務是否已啟動")
            print("2. .env 檔案中的資料庫設定是否正確")
            print("3. 資料庫使用者權限是否正確")
            return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'drop':
            drop_all_tables()
        elif command == 'test':
            test_connection()
        elif command == 'reset':
            print("正在重置資料庫...")
            drop_all_tables()
            if init_database():
                print("✅ 資料庫重置完成！")
        else:
            print("使用方法：")
            print("  python init_db.py        # 初始化資料庫")
            print("  python init_db.py test   # 測試資料庫連線")
            print("  python init_db.py drop   # 刪除所有表格")
            print("  python init_db.py reset  # 重置資料庫")
    else:
        # 先測試連線
        if test_connection():
            # 連線成功才初始化
            if init_database():
                print("\n🎉 資料庫初始化完成！")
                print("\n📖 下一步：")
                print("1. 啟動後端服務：python app.py")
                print("2. 前端開發伺服器：cd frontend && npm run dev")
                print("3. 測試 API：http://localhost:5000/api/health")
                print("4. 前端應用：http://localhost:3000")
            else:
                print("❌ 資料庫初始化失敗")
        else:
            print("❌ 無法連接到資料庫，請檢查設定")