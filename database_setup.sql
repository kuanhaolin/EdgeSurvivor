-- EdgeSurvivor MariaDB 資料庫初始化腳本
-- 使用方法：mysql -u root -p < database_setup.sql

-- 建立資料庫
CREATE DATABASE IF NOT EXISTS edgesurvivor 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 建立開發環境資料庫
CREATE DATABASE IF NOT EXISTS edgesurvivor_dev 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 建立專用使用者
CREATE USER IF NOT EXISTS 'edgesurvivor_user'@'localhost' IDENTIFIED BY 'your_password_here';

-- 授予權限
GRANT ALL PRIVILEGES ON edgesurvivor.* TO 'edgesurvivor_user'@'localhost';
GRANT ALL PRIVILEGES ON edgesurvivor_dev.* TO 'edgesurvivor_user'@'localhost';

-- 如果需要遠端連線，也可以授予 '%' 的權限
-- CREATE USER IF NOT EXISTS 'edgesurvivor_user'@'%' IDENTIFIED BY 'your_password_here';
-- GRANT ALL PRIVILEGES ON edgesurvivor.* TO 'edgesurvivor_user'@'%';
-- GRANT ALL PRIVILEGES ON edgesurvivor_dev.* TO 'edgesurvivor_user'@'%';

-- 重新載入權限
FLUSH PRIVILEGES;

-- 顯示建立的資料庫
SHOW DATABASES LIKE 'edgesurvivor%';

-- 顯示使用者權限
SHOW GRANTS FOR 'edgesurvivor_user'@'localhost';