-- MySQL Database Dump

DROP TABLE IF EXISTS `expenses`;
DROP TABLE IF EXISTS `chat_messages`;
DROP TABLE IF EXISTS `activity_participants`;
DROP TABLE IF EXISTS `activity_discussions`;
DROP TABLE IF EXISTS `matches`;
DROP TABLE IF EXISTS `activities`;
DROP TABLE IF EXISTS `places`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `privacy_setting` varchar(20) DEFAULT NULL,
  `social_privacy` varchar(20) DEFAULT 'public',
  `location` varchar(100) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `interests` text DEFAULT NULL,
  `join_date` datetime DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `instagram_url` varchar(255) DEFAULT NULL,
  `facebook_url` varchar(255) DEFAULT NULL,
  `line_id` varchar(100) DEFAULT NULL,
  `twitter_url` varchar(255) DEFAULT NULL,
  `two_factor_enabled` tinyint(1) DEFAULT 0,
  `two_factor_secret` varchar(32) DEFAULT NULL,
  `rating_count` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `ix_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `activities`
CREATE TABLE `activities` (
  `activity_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `location` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `max_participants` int(11) DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `creator_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `meeting_point` varchar(255) DEFAULT NULL,
  `duration_hours` int(11) DEFAULT NULL,
  `difficulty_level` varchar(20) DEFAULT NULL,
  `gender_preference` varchar(20) DEFAULT NULL,
  `age_min` int(11) DEFAULT NULL,
  `age_max` int(11) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `cover_image` varchar(500) DEFAULT NULL,
  `images` text DEFAULT NULL,
  PRIMARY KEY (`activity_id`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `activities_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `matches`
CREATE TABLE `matches` (
  `match_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) DEFAULT NULL,
  `user_a` int(11) NOT NULL,
  `user_b` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `match_date` datetime DEFAULT NULL,
  `confirmed_date` datetime DEFAULT NULL,
  `cancel_date` datetime DEFAULT NULL,
  `message` text DEFAULT NULL,
  `rejection_reason` text DEFAULT NULL,
  PRIMARY KEY (`match_id`),
  KEY `activity_id` (`activity_id`),
  KEY `user_a` (`user_a`),
  KEY `user_b` (`user_b`),
  CONSTRAINT `matches_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
  CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`user_a`) REFERENCES `users` (`user_id`),
  CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`user_b`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `activity_discussions`
CREATE TABLE `activity_discussions` (
  `discussion_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `message_type` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`discussion_id`),
  KEY `activity_id` (`activity_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `activity_discussions_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
  CONSTRAINT `activity_discussions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `activity_participants`
CREATE TABLE `activity_participants` (
  `participant_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `joined_at` datetime DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `left_at` datetime DEFAULT NULL,
  `message` text DEFAULT NULL,
  `rejection_reason` text DEFAULT NULL,
  PRIMARY KEY (`participant_id`),
  UNIQUE KEY `unique_activity_user` (`activity_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `activity_participants_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
  CONSTRAINT `activity_participants_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `chat_messages`
CREATE TABLE `chat_messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) DEFAULT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `message_type` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `file_url` varchar(255) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_size` int(11) DEFAULT NULL,
  PRIMARY KEY (`message_id`),
  KEY `match_id` (`match_id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`),
  CONSTRAINT `chat_messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `chat_messages_ibfk_3` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `expenses`
CREATE TABLE `expenses` (
  `expense_id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `payer_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `expense_date` date DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `is_split` tinyint(1) DEFAULT NULL,
  `split_method` varchar(20) DEFAULT NULL,
  `participants` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`expense_id`),
  KEY `activity_id` (`activity_id`),
  KEY `payer_id` (`payer_id`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`activity_id`),
  CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`payer_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
