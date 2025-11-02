-- 為活動表添加開始和結束日期欄位
-- Migration: Add start_date and end_date columns to activities table

-- 添加開始日期欄位（預設使用現有的date欄位值）
ALTER TABLE activities ADD COLUMN IF NOT EXISTS start_date DATE;

-- 添加結束日期欄位
ALTER TABLE activities ADD COLUMN IF NOT EXISTS end_date DATE;

-- 將現有的date欄位值複製到start_date（針對還沒有start_date的記錄）
UPDATE activities SET start_date = date WHERE start_date IS NULL;

-- 可選：如果沒有指定end_date，預設設為與start_date相同
-- UPDATE activities SET end_date = start_date WHERE end_date IS NULL;

-- 註釋：保留原有的date欄位以向後兼容
