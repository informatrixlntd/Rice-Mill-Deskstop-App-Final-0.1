-- Migration: Add new columns to purchase_slips table
-- Run this SQL file against your MySQL database before using the updated application

ALTER TABLE purchase_slips
ADD COLUMN IF NOT EXISTS mobile_number VARCHAR(15) DEFAULT '' AFTER party_name;

ALTER TABLE purchase_slips
ADD COLUMN IF NOT EXISTS moisture_ded_comment TEXT DEFAULT '' AFTER moisture_ded;

-- Verify the columns were added
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'purchase_slips' AND COLUMN_NAME IN ('mobile_number', 'moisture_ded_comment');
