-- 創建活動評價表
CREATE TABLE IF NOT EXISTS `activity_reviews` (
  `review_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `reviewer_id` int(11) NOT NULL,
  `reviewee_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 AND `rating` <= 5),
  `comment` text DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `unique_review` (`activity_id`, `reviewer_id`, `reviewee_id`),
  KEY `activity_id` (`activity_id`),
  KEY `reviewer_id` (`reviewer_id`),
  KEY `reviewee_id` (`reviewee_id`),
  CONSTRAINT `activity_reviews_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
  CONSTRAINT `activity_reviews_ibfk_2` FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `activity_reviews_ibfk_3` FOREIGN KEY (`reviewee_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 為 users 表新增評價統計欄位
ALTER TABLE `users` 
ADD COLUMN IF NOT EXISTS `rating_avg` decimal(3,2) DEFAULT NULL COMMENT '平均評分',
ADD COLUMN IF NOT EXISTS `rating_count` int(11) DEFAULT 0 COMMENT '評價數量';
