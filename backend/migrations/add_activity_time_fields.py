"""
資料庫遷移腳本：為 activities 表添加時間欄位
執行方式：python backend/migrations/add_activity_time_fields.py
"""

import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from sqlalchemy import text

def migrate():
    """執行資料庫遷移"""
    app = create_app()
    
    with app.app_context():
        try:
            # 檢查欄位是否已存在
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('activities')]
            
            print("📋 當前 activities 表的欄位：", columns)
            
            # 添加 start_time 和 end_time 欄位
            if 'start_time' not in columns:
                print("🔄 添加 start_time 欄位...")
                with db.engine.connect() as conn:
                    conn.execute(text("""
                        ALTER TABLE activities 
                        ADD COLUMN start_time TIME DEFAULT '09:00:00'
                    """))
                    conn.commit()
                print("✅ start_time 欄位添加成功")
            else:
                print("ℹ️  start_time 欄位已存在")
            
            if 'end_time' not in columns:
                print("🔄 添加 end_time 欄位...")
                with db.engine.connect() as conn:
                    conn.execute(text("""
                        ALTER TABLE activities 
                        ADD COLUMN end_time TIME DEFAULT '17:00:00'
                    """))
                    conn.commit()
                print("✅ end_time 欄位添加成功")
            else:
                print("ℹ️  end_time 欄位已存在")
            
            # 驗證遷移結果
            inspector = db.inspect(db.engine)
            columns_after = [col['name'] for col in inspector.get_columns('activities')]
            
            if 'start_time' in columns_after and 'end_time' in columns_after:
                print("\n✅ 遷移成功完成！")
                print("📋 新增欄位：start_time, end_time")
            else:
                print("\n⚠️  遷移可能未完全成功，請檢查資料庫")
                
        except Exception as e:
            print(f"\n❌ 遷移失敗：{str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("開始資料庫遷移：添加活動時間欄位")
    print("=" * 60)
    migrate()
