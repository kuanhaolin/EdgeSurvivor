-- 修改評價表：移除 rating 欄位
ALTER TABLE `activity_reviews` 
DROP COLUMN `rating`;

-- 修改 users 表：移除平均評分，保留評價數量
ALTER TABLE `users` 
DROP COLUMN IF EXISTS `rating_avg`;

-- 確保 rating_count 存在
ALTER TABLE `users` 
ADD COLUMN IF NOT EXISTS `rating_count` int(11) DEFAULT 0 COMMENT '評價數量';
