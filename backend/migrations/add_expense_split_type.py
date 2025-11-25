"""
添加費用分攤類型和借款人欄位
執行方式：python backend/migrations/add_expense_split_type.py
"""
import sys
import os

# 添加父目錄到 path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db
from app import app
from sqlalchemy import text

def migrate():
    """執行遷移"""
    with app.app_context():
        try:
            # 檢查欄位是否已存在
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='expenses' AND column_name='split_type'
            """))
            
            if result.fetchone():
                print("欄位已存在，跳過遷移")
                return
            
            # 添加新欄位
            db.session.execute(text("""
                ALTER TABLE expenses 
                ADD COLUMN split_type VARCHAR(20) DEFAULT 'all'
            """))
            
            db.session.execute(text("""
                ALTER TABLE expenses 
                ADD COLUMN split_participants TEXT
            """))
            
            db.session.execute(text("""
                ALTER TABLE expenses 
                ADD COLUMN borrower_id INTEGER,
                ADD CONSTRAINT fk_expenses_borrower 
                    FOREIGN KEY (borrower_id) REFERENCES users(user_id)
            """))
            
            # 遷移舊數據：將 participants 複製到 split_participants
            db.session.execute(text("""
                UPDATE expenses 
                SET split_participants = participants
                WHERE participants IS NOT NULL
            """))
            
            # 根據 is_split 設定 split_type
            db.session.execute(text("""
                UPDATE expenses 
                SET split_type = CASE 
                    WHEN is_split = TRUE THEN 'all'
                    ELSE 'none'
                END
            """))
            
            db.session.commit()
            print("✅ 遷移成功完成！")
            print("已添加以下欄位：")
            print("  - split_type: 分攤類型 (all/selected/borrow)")
            print("  - split_participants: 參與分攤的人員")
            print("  - borrower_id: 借款人ID")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 遷移失敗: {str(e)}")
            raise

if __name__ == '__main__':
    migrate()
