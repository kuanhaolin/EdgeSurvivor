#!/usr/bin/env python3
"""
EdgeSurvivor 資料庫設定腳本
自動從 .env 檔案讀取設定並建立 MariaDB 資料庫和使用者
"""

import os
import mysql.connector
from dotenv import load_dotenv
import sys

def load_env_config():
    """載入 .env 檔案配置"""
    # 載入 .env 檔案
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'edgesurvivor_user'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'edgesurvivor'),
        'dev_database': os.getenv('DB_NAME', 'edgesurvivor') + '_dev'
    }
    
    if not config['password']:
        print("❌ 錯誤：.env 檔案中未設定 DB_PASSWORD")
        print("請編輯 .env 檔案，設定您的 MariaDB 密碼")
        return None
    
    return config

def connect_as_root():
    """以 root 身份連接 MariaDB"""
    root_password = input("請輸入 MariaDB root 密碼: ")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=root_password
        )
        return connection
    except mysql.connector.Error as e:
        print(f"❌ 連接失敗: {e}")
        return None

def create_database_and_user(config):
    """建立資料庫和使用者"""
    connection = connect_as_root()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        print("📊 正在建立資料庫...")
        
        # 建立生產資料庫
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {config['database']} 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        print(f"✅ 資料庫 '{config['database']}' 建立成功")
        
        # 建立開發資料庫
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {config['dev_database']} 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        print(f"✅ 開發資料庫 '{config['dev_database']}' 建立成功")
        
        print("👤 正在建立使用者...")
        
        # 建立使用者（如果不存在）
        cursor.execute(f"""
            CREATE USER IF NOT EXISTS '{config['user']}'@'localhost' 
            IDENTIFIED BY '{config['password']}'
        """)
        print(f"✅ 使用者 '{config['user']}' 建立成功")
        
        print("🔑 正在設定權限...")
        
        # 授予生產資料庫權限
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON {config['database']}.* 
            TO '{config['user']}'@'localhost'
        """)
        
        # 授予開發資料庫權限
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON {config['dev_database']}.* 
            TO '{config['user']}'@'localhost'
        """)
        
        # 重新載入權限
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ 權限設定完成")
        
        # 顯示建立的資料庫
        print("\n📋 已建立的資料庫:")
        cursor.execute("SHOW DATABASES LIKE 'edgesurvivor%'")
        databases = cursor.fetchall()
        for db in databases:
            print(f"  • {db[0]}")
        
        # 顯示使用者權限
        print(f"\n🔐 使用者 '{config['user']}' 的權限:")
        cursor.execute(f"SHOW GRANTS FOR '{config['user']}'@'localhost'")
        grants = cursor.fetchall()
        for grant in grants:
            print(f"  • {grant[0]}")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ 建立過程中發生錯誤: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection(config):
    """測試新建立的使用者連線"""
    print(f"\n🔍 測試使用者 '{config['user']}' 的連線...")
    
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ 連線測試成功！")
            return True
        
    except mysql.connector.Error as e:
        print(f"❌ 連線測試失敗: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    
    return False

def generate_sql_file(config):
    """生成 SQL 腳本檔案"""
    sql_content = f"""-- EdgeSurvivor MariaDB 資料庫初始化腳本
-- 此檔案由 setup_database.py 自動生成，從 .env 檔案讀取設定
-- 使用方法：mysql -u root -p < database_setup_generated.sql

-- 建立生產資料庫
CREATE DATABASE IF NOT EXISTS {config['database']} 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 建立開發環境資料庫
CREATE DATABASE IF NOT EXISTS {config['dev_database']} 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 建立專用使用者
CREATE USER IF NOT EXISTS '{config['user']}'@'localhost' IDENTIFIED BY '{config['password']}';

-- 授予權限
GRANT ALL PRIVILEGES ON {config['database']}.* TO '{config['user']}'@'localhost';
GRANT ALL PRIVILEGES ON {config['dev_database']}.* TO '{config['user']}'@'localhost';

-- 重新載入權限
FLUSH PRIVILEGES;

-- 顯示建立的資料庫
SHOW DATABASES LIKE 'edgesurvivor%';

-- 顯示使用者權限
SHOW GRANTS FOR '{config['user']}'@'localhost';
"""
    
    with open('database_setup_generated.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"📄 已生成 SQL 腳本檔案: database_setup_generated.sql")

def main():
    print("🚀 EdgeSurvivor 資料庫設定工具")
    print("=" * 50)
    
    # 載入配置
    config = load_env_config()
    if not config:
        sys.exit(1)
    
    print(f"📖 從 .env 讀取的配置:")
    print(f"  • 主機: {config['host']}:{config['port']}")
    print(f"  • 使用者: {config['user']}")
    print(f"  • 生產資料庫: {config['database']}")
    print(f"  • 開發資料庫: {config['dev_database']}")
    print(f"  • 密碼: {'*' * len(config['password'])}")
    
    choice = input("\n選擇執行方式:\n1. 直接建立資料庫和使用者\n2. 只生成 SQL 腳本檔案\n請輸入 (1/2): ")
    
    if choice == '1':
        # 直接建立
        if create_database_and_user(config):
            print("\n🎉 資料庫設定完成！")
            
            # 測試連線
            if test_connection(config):
                print("\n📖 下一步:")
                print("  cd backend")
                print("  python init_db.py")
            else:
                print("\n⚠️  請檢查設定後再試")
        else:
            print("\n❌ 資料庫設定失敗")
    
    elif choice == '2':
        # 生成 SQL 檔案
        generate_sql_file(config)
        print("\n📖 使用生成的 SQL 檔案:")
        print("  mysql -u root -p < database_setup_generated.sql")
    
    else:
        print("❌ 無效選擇")

if __name__ == '__main__':
    main()