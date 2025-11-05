#!/usr/bin/env python3
"""
Flask-Migrate 初始化腳本
用於首次設定資料庫遷移環境
"""

import os
import sys

def init_flask_migrate():
    """初始化 Flask-Migrate"""
    print("=" * 60)
    print("EdgeSurvivor - Flask-Migrate 初始化")
    print("=" * 60)
    print()
    
    # 檢查是否已經初始化
    if os.path.exists('migrations'):
        print("⚠️  警告：migrations 目錄已存在")
        response = input("是否要重新初始化？這將刪除現有的 migrations 目錄 (y/N): ")
        if response.lower() != 'y':
            print("❌ 操作已取消")
            return False
        
        import shutil
        shutil.rmtree('migrations')
        print("✅ 已刪除舊的 migrations 目錄")
    
    print("\n步驟 1/4: 初始化 Flask-Migrate...")
    result = os.system('flask db init')
    if result != 0:
        print("❌ 初始化失敗")
        return False
    print("✅ Flask-Migrate 初始化完成")
    
    print("\n步驟 2/4: 生成初始遷移腳本...")
    result = os.system('flask db migrate -m "Initial migration - create all tables"')
    if result != 0:
        print("❌ 生成遷移腳本失敗")
        return False
    print("✅ 初始遷移腳本生成完成")
    
    print("\n步驟 3/4: 應用遷移到資料庫...")
    result = os.system('flask db upgrade')
    if result != 0:
        print("❌ 應用遷移失敗")
        return False
    print("✅ 遷移已應用到資料庫")
    
    print("\n步驟 4/4: 驗證遷移狀態...")
    result = os.system('flask db current')
    if result != 0:
        print("⚠️  無法顯示當前版本，但遷移可能已成功")
    
    print("\n" + "=" * 60)
    print("🎉 Flask-Migrate 初始化完成！")
    print("=" * 60)
    print("\n📖 下一步：")
    print("1. 查看 migrations/versions/ 目錄中的遷移腳本")
    print("2. 閱讀 docs/database-migration-strategy.md 了解遷移最佳實踐")
    print("3. 當修改 Model 時，使用 'flask db migrate -m \"描述\"' 生成遷移")
    print("4. 使用 'flask db upgrade' 應用遷移")
    print("5. 使用 'flask db downgrade -1' 回滾遷移")
    print()
    
    return True

def show_migration_commands():
    """顯示常用的遷移命令"""
    print("=" * 60)
    print("Flask-Migrate 常用命令")
    print("=" * 60)
    print()
    print("📝 生成遷移：")
    print("  flask db migrate -m \"描述變更內容\"")
    print()
    print("⬆️  應用遷移：")
    print("  flask db upgrade          # 升級到最新版本")
    print("  flask db upgrade +2       # 升級 2 個版本")
    print()
    print("⬇️  回滾遷移：")
    print("  flask db downgrade -1     # 回滾 1 個版本")
    print("  flask db downgrade base   # 回滾到最初狀態")
    print()
    print("ℹ️  查看資訊：")
    print("  flask db current          # 查看當前版本")
    print("  flask db history          # 查看遷移歷史")
    print("  flask db show <revision>  # 查看特定遷移詳情")
    print()
    print("🔧 其他命令：")
    print("  flask db stamp head       # 標記資料庫為最新版本（不執行遷移）")
    print("  flask db merge heads      # 合併多個 head 版本")
    print()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        show_migration_commands()
    else:
        # 檢查是否在 backend 目錄
        if not os.path.exists('app.py'):
            print("❌ 錯誤：請在 backend 目錄中執行此腳本")
            print("   cd backend")
            print("   python init_migrations.py")
            sys.exit(1)
        
        success = init_flask_migrate()
        if not success:
            print("\n❌ 初始化過程中發生錯誤")
            print("\n🔧 排除建議：")
            print("1. 確認資料庫連線正常：python init_db.py test")
            print("2. 確認所有依賴已安裝：pip install -r requirements.txt")
            print("3. 檢查 .env 檔案配置")
            print("4. 查看錯誤訊息並參考 docs/database-migration-strategy.md")
            sys.exit(1)
        
        print()
        show_migration_commands()
