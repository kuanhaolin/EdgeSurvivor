"""
資料庫遷移腳本：新增評分功能相關欄位
Migration: Add rating fields to activity_reviews and users tables
Date: 2025-11-25
"""

from sqlalchemy import text
from models import db

def upgrade():
    """執行遷移：新增欄位"""
    
    # 1. 在 activity_reviews 表新增 rating 欄位
    # 設定預設值為 5 分，以便相容現有資料
    db.session.execute(text("""
        ALTER TABLE activity_reviews 
        ADD COLUMN rating INTEGER NOT NULL DEFAULT 5 
        COMMENT '評分 1-5 星';
    """))
    
    # 2. 在 users 表新增 average_rating 欄位
    db.session.execute(text("""
        ALTER TABLE users 
        ADD COLUMN average_rating FLOAT NOT NULL DEFAULT 0.0 
        COMMENT '平均評分';
    """))
    
    # 3. 根據現有評價計算每個用戶的平均評分
    db.session.execute(text("""
        UPDATE users u
        SET average_rating = (
            SELECT COALESCE(AVG(ar.rating), 0.0)
            FROM activity_reviews ar
            WHERE ar.reviewee_id = u.user_id
        );
    """))
    
    db.session.commit()
    print("✅ Migration completed: Added rating fields")

def downgrade():
    """回滾遷移：移除欄位"""
    
    # 移除 activity_reviews 表的 rating 欄位
    db.session.execute(text("""
        ALTER TABLE activity_reviews 
        DROP COLUMN rating;
    """))
    
    # 移除 users 表的 average_rating 欄位
    db.session.execute(text("""
        ALTER TABLE users 
        DROP COLUMN average_rating;
    """))
    
    db.session.commit()
    print("✅ Migration rolled back: Removed rating fields")

if __name__ == '__main__':
    """
    執行遷移的方式：
    
    在後端目錄執行：
    python -c "from migrations.add_rating_fields import upgrade; upgrade()"
    
    回滾遷移：
    python -c "from migrations.add_rating_fields import downgrade; downgrade()"
    """
    print("Migration script loaded. Use upgrade() or downgrade() to execute.")
