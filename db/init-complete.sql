-- EdgeSurvivor 完整資料庫初始化腳本
-- 此腳本會在 Docker 容器首次啟動時自動執行

-- 確保使用 UTF-8 編碼
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 使用者表
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    privacy_setting VARCHAR(20) DEFAULT 'public',
    location VARCHAR(100),
    profile_picture VARCHAR(255),
    bio TEXT,
    gender VARCHAR(10),
    age INT,
    interests TEXT COMMENT 'JSON 格式的興趣標籤',
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 活動表
CREATE TABLE IF NOT EXISTS activities (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    date DATE,
    start_time VARCHAR(10),
    location VARCHAR(200),
    description TEXT,
    category VARCHAR(50),
    max_participants INT,
    cost DECIMAL(10,2),
    duration_hours INT,
    status VARCHAR(20) DEFAULT 'open',
    cover_image VARCHAR(255),
    images TEXT COMMENT 'JSON 格式的圖片列表',
    is_active BOOLEAN DEFAULT TRUE,
    creator_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_date (date),
    INDEX idx_location (location),
    INDEX idx_category (category),
    INDEX idx_creator (creator_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 活動參與者表
CREATE TABLE IF NOT EXISTS activity_participants (
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    role VARCHAR(20) DEFAULT 'participant',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    left_at DATETIME,
    message TEXT,
    rejection_reason TEXT,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY uk_activity_user (activity_id, user_id),
    INDEX idx_status (status),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 活動討論串表
CREATE TABLE IF NOT EXISTS activity_discussions (
    discussion_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_activity (activity_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 媒合表
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT,
    user_a INT NOT NULL COMMENT '申請者',
    user_b INT NOT NULL COMMENT '接收者',
    status VARCHAR(20) DEFAULT 'pending',
    message TEXT,
    match_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    confirmed_date DATETIME,
    cancel_date DATETIME,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE SET NULL,
    FOREIGN KEY (user_a) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_b) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_a (user_a),
    INDEX idx_user_b (user_b),
    INDEX idx_status (status),
    INDEX idx_activity (activity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 聊天訊息表
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    message_type VARCHAR(20) DEFAULT 'text',
    status VARCHAR(20) DEFAULT 'sent',
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_match (match_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_sender (sender_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 費用表
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    payer_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    expense_date DATE,
    description TEXT,
    paid BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE,
    FOREIGN KEY (payer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_activity (activity_id),
    INDEX idx_payer (payer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入測試資料（可選）
-- 測試使用者
INSERT INTO users (name, email, password_hash, gender, age, location, bio, interests) VALUES
('小明', 'ming@example.com', 'scrypt:32768:8:1$hT9xKkjH3TGfRqEe$e4c8f5e6a8d1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', 'male', 25, '台灣 - 台北市', '喜歡旅行和探索新地方！', '["登山", "攝影", "旅遊"]'),
('小花', 'hua@example.com', 'scrypt:32768:8:1$hT9xKkjH3TGfRqEe$e4c8f5e6a8d1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', 'female', 23, '台灣 - 新北市', '熱愛美食和攝影的女孩', '["美食", "攝影", "咖啡"]'),
('阿傑', 'jay@example.com', 'scrypt:32768:8:1$hT9xKkjH3TGfRqEe$e4c8f5e6a8d1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', 'male', 28, '台灣 - 桃園市', '戶外運動愛好者', '["運動", "健身", "登山"]')
ON DUPLICATE KEY UPDATE name=name;

-- 測試活動
INSERT INTO activities (title, date, start_time, location, description, category, max_participants, cost, duration_hours, creator_id) VALUES
('陽明山賞花一日遊', '2025-11-15', '08:00', '台北市 - 陽明山國家公園', '春天到了！一起去陽明山看櫻花吧～', '休閒', 4, 500, 6, 1),
('九份老街美食之旅', '2025-11-20', '10:00', '新北市 - 九份老街', '探索九份的美食和歷史文化', '美食', 3, 800, 5, 2),
('大稻埕河濱腳踏車', '2025-11-25', '09:00', '台北市 - 大稻埕碼頭', '騎腳踏車沿著淡水河畔，享受悠閒時光', '運動', 5, 200, 4, 3)
ON DUPLICATE KEY UPDATE title=title;

-- 顯示初始化完成訊息
SELECT '✅ 資料庫表格建立完成！' AS Status;
SELECT CONCAT('📊 共建立 ', COUNT(*), ' 個使用者') AS Users FROM users;
SELECT CONCAT('🎯 共建立 ', COUNT(*), ' 個活動') AS Activities FROM activities;
