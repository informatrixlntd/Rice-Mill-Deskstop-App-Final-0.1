-- ============================================================================
-- COMPLETE DATABASE SCHEMA MIGRATION SQL
-- ============================================================================
-- This SQL file updates the purchase_slips table to the new schema
-- Run this with: mysql -u root -p purchase_slips_db < migration_schema_update.sql
-- ============================================================================

USE purchase_slips_db;

-- Step 1: Add Weight System Columns
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS net_weight_kg DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS gunny_weight_kg DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS final_weight_kg DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS weight_quintal DECIMAL(10,3) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS weight_khandi DECIMAL(10,3) DEFAULT 0;

-- Step 2: Add Rate System Columns
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS rate_basis VARCHAR(20) DEFAULT 'Quintal';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS rate_value DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS total_purchase_amount DECIMAL(10,2) DEFAULT 0;

-- Step 3: Add Deduction System Columns
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS postage DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS freight DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS rate_diff DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS quality_diff DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS quality_diff_comment TEXT;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS moisture_ded DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS tds DECIMAL(10,2) DEFAULT 0;

-- Step 4: Add Payment Instalment Columns (All 5 instalments with payment method & bank account)
-- Instalment 1
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_1_date DATE;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_1_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_1_payment_method VARCHAR(50) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_1_payment_bank_account VARCHAR(255) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_1_comment TEXT;

-- Instalment 2
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_2_date DATE;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_2_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_2_payment_method VARCHAR(50) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_2_payment_bank_account VARCHAR(255) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_2_comment TEXT;

-- Instalment 3
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_3_date DATE;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_3_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_3_payment_method VARCHAR(50) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_3_payment_bank_account VARCHAR(255) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_3_comment TEXT;

-- Instalment 4
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_4_date DATE;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_4_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_4_payment_method VARCHAR(50) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_4_payment_bank_account VARCHAR(255) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_4_comment TEXT;

-- Instalment 5
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_5_date DATE;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_5_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_5_payment_method VARCHAR(50) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_5_payment_bank_account VARCHAR(255) DEFAULT '';
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS instalment_5_comment TEXT;

-- Step 5: Add Other Columns
ALTER TABLE purchase_slips ADD COLUMN IF NOT EXISTS paddy_unloading_godown TEXT;

-- Step 6: Remove OLD Payment Info Columns (these are no longer needed)
-- Note: Check if these columns exist before dropping
SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0;

ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_method;
ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_date;
ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_amount;
ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_bank_account;
ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_due_date;
ALTER TABLE purchase_slips DROP COLUMN IF EXISTS payment_due_comment;

SET SQL_NOTES=@OLD_SQL_NOTES;

-- Verification Query
SELECT
    'Migration Complete!' as status,
    COUNT(*) as total_columns
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'purchase_slips';

-- Show all columns
DESCRIBE purchase_slips;
