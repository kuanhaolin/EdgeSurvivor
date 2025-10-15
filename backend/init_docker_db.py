#!/usr/bin/env python3
"""
Docker 環境資料庫初始化腳本
使用此腳本在 Docker 容器中初始化資料庫
"""

import os
import sys
from datetime import datetime, date

# 設定環境為 Docker
os.environ['FLASK_ENV'] = 'development'

# 添加父目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db
from models.user import User
from models.activity import Activity
from models.match import Match
from models.chat_message import ChatMessage
from models.activity_participant import ActivityParticipant
from models.activity_discussion import ActivityDiscussion
from models.expense import Expense

def init_docker_database():
    """初始化 Docker 資料庫"""
    print("=" * 60)
    print("  EdgeSurvivor Docker 資料庫初始化")
    print("=" * 60)
    print()
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # 1. 測試連接
            print("📡 測試資料庫連接...")
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ 資料庫連接成功！")
            print(f"🔗 連接字串：{str(db.engine.url).replace(str(db.engine.url.password), '***')}")
            print()
            
            # 2. 建立所有表格
            print("🔨 正在建立資料庫表格...")
            db.create_all()
            print("✅ 資料庫表格建立完成！")
            print()
            
            # 3. 檢查表格
            print("📋 檢查建立的表格：")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
            print(f"\n✅ 共建立 {len(tables)} 個表格")
            print()
            
            # 4. 建立測試資料（可選）
            create_test = input("是否建立測試資料？(y/N): ").lower()
            if create_test == 'y':
                create_test_data()
            else:
                print("⏭️  跳過測試資料建立")
            
            print()
            print("=" * 60)
            print("  ✅ 資料庫初始化完成！")
            print("=" * 60)
            print()
            print("📖 下一步：")
            print("  1. 前端：http://localhost:8080")
            print("  2. 後端 API：http://localhost:5001")
            print("  3. 資料庫：localhost:3306")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ 初始化失敗：{e}")
            import traceback
            traceback.print_exc()
            return False

def create_test_data():
    """建立測試資料"""
    print()
    print("🌱 正在建立測試資料...")
    
    try:
        # 1. 建立測試使用者
        print("  👥 建立測試使用者...")
        users_data = [
            {
                'name': '小明',
                'email': 'ming@example.com',
                'password': 'password123',
                'gender': 'male',
                'age': 25,
                'location': '台灣 - 台北市',
                'bio': '喜歡旅行和探索新地方！',
                'interests': '["登山", "攝影", "旅遊"]'
            },
            {
                'name': '小花',
                'email': 'hua@example.com',
                'password': 'password123',
                'gender': 'female',
                'age': 23,
                'location': '台灣 - 新北市',
                'bio': '熱愛美食和攝影的女孩',
                'interests': '["美食", "攝影", "咖啡"]'
            },
            {
                'name': '阿傑',
                'email': 'jay@example.com',
                'password': 'password123',
                'gender': 'male',
                'age': 28,
                'location': '台灣 - 桃園市',
                'bio': '戶外運動愛好者',
                'interests': '["運動", "健身", "登山"]'
            }
        ]
        
        created_users = []
        for user_data in users_data:
            # 檢查是否已存在
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    gender=user_data['gender'],
                    age=user_data['age'],
                    location=user_data['location'],
                    bio=user_data['bio'],
                    interests=user_data['interests']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                created_users.append(user)
            else:
                created_users.append(existing)
                print(f"    ⏭️  {user_data['name']} 已存在，跳過")
        
        db.session.commit()
        print(f"  ✅ 建立了 {len([u for u in created_users if u.user_id is None])} 個新使用者")
        
        # 2. 建立測試活動
        if created_users:
            print("  🎯 建立測試活動...")
            activities_data = [
                {
                    'title': '陽明山賞花一日遊',
                    'date': date(2025, 11, 15),
                    'start_time': '08:00',
                    'location': '台北市 - 陽明山國家公園',
                    'description': '春天到了！一起去陽明山看櫻花吧～',
                    'category': '休閒',
                    'max_participants': 4,
                    'cost': 500,
                    'duration_hours': 6,
                    'creator_id': created_users[0].user_id
                },
                {
                    'title': '九份老街美食之旅',
                    'date': date(2025, 11, 20),
                    'start_time': '10:00',
                    'location': '新北市 - 九份老街',
                    'description': '探索九份的美食和歷史文化',
                    'category': '美食',
                    'max_participants': 3,
                    'cost': 800,
                    'duration_hours': 5,
                    'creator_id': created_users[1].user_id
                },
                {
                    'title': '大稻埕河濱腳踏車',
                    'date': date(2025, 11, 25),
                    'start_time': '09:00',
                    'location': '台北市 - 大稻埕碼頭',
                    'description': '騎腳踏車沿著淡水河畔，享受悠閒時光',
                    'category': '運動',
                    'max_participants': 5,
                    'cost': 200,
                    'duration_hours': 4,
                    'creator_id': created_users[2].user_id
                }
            ]
            
            created_activities = 0
            for activity_data in activities_data:
                existing = Activity.query.filter_by(title=activity_data['title']).first()
                if not existing:
                    activity = Activity(**activity_data)
                    db.session.add(activity)
                    created_activities += 1
            
            db.session.commit()
            print(f"  ✅ 建立了 {created_activities} 個新活動")
        
        print()
        print("✅ 測試資料建立完成！")
        print()
        print("📝 測試帳號：")
        print("  Email: ming@example.com  | 密碼: password123")
        print("  Email: hua@example.com   | 密碼: password123")
        print("  Email: jay@example.com   | 密碼: password123")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 建立測試資料失敗：{e}")
        import traceback
        traceback.print_exc()

def show_tables():
    """顯示資料庫中的所有表格"""
    app = create_app('development')
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("=" * 60)
            print(f"  資料庫中的表格（共 {len(tables)} 個）")
            print("=" * 60)
            
            for i, table in enumerate(tables, 1):
                # 獲取表格的列資訊
                columns = inspector.get_columns(table)
                print(f"\n{i}. {table} ({len(columns)} 個欄位)")
                print("-" * 60)
                
                # 顯示欄位資訊
                for col in columns[:5]:  # 只顯示前5個欄位
                    print(f"   - {col['name']}: {col['type']}")
                
                if len(columns) > 5:
                    print(f"   ... 還有 {len(columns) - 5} 個欄位")
                
                # 顯示資料數量
                from sqlalchemy import text
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"   📊 資料筆數: {count}")
            
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"❌ 查詢失敗：{e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'show':
            show_tables()
        elif command == 'init':
            init_docker_database()
        elif command == 'test':
            app = create_app('development')
            with app.app_context():
                create_test_data()
        else:
            print("使用方法：")
            print("  python init_docker_db.py        # 初始化資料庫")
            print("  python init_docker_db.py init   # 初始化資料庫")
            print("  python init_docker_db.py show   # 顯示所有表格")
            print("  python init_docker_db.py test   # 只建立測試資料")
    else:
        init_docker_database()
