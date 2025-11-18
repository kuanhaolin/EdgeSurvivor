"""
添加用戶興趣標籤欄位
執行此腳本以更新資料庫架構
"""

from app import app
from models import db

def add_interests_field():
    with app.app_context():
        try:
            # 添加 interests 欄位到 users 表
            with db.engine.connect() as conn:
                # 檢查欄位是否已存在
                result = conn.execute(db.text("""
                    SELECT COUNT(*) 
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'interests'
                """))
                exists = result.scalar() > 0
                
                if not exists:
                    print("添加 interests 欄位到 users 表...")
                    conn.execute(db.text("""
                        ALTER TABLE users 
                        ADD COLUMN interests TEXT NULL 
                        AFTER age
                    """))
                    conn.commit()
                    print(" interests 欄位添加成功！")
                else:
                    print(" interests 欄位已存在，無需添加")
                    
        except Exception as e:
            print(f" 發生錯誤: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("=" * 50)
    print("添加用戶興趣標籤欄位")
    print("=" * 50)
    add_interests_field()
    print("=" * 50)
    print("完成！")
