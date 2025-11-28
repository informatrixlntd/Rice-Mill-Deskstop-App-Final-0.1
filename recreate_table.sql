-- RECREATE TABLE WITH EXACT SCHEMA
-- This will DROP the old table and create a new one with all correct columns

USE purchase_slips_db;

-- Backup existing data (if any)
CREATE TABLE IF NOT EXISTS purchase_slips_backup AS SELECT * FROM purchase_slips;

-- Drop old table
DROP TABLE IF EXISTS purchase_slips;

-- Create new table with EXACT schema matching backend code (69 columns)
CREATE TABLE purchase_slips (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- Basic Info (13 columns)
    company_name VARCHAR(255),
    company_address TEXT,
    document_type VARCHAR(50) DEFAULT 'Purchase Slip',
    vehicle_no VARCHAR(50),
    date DATE NOT NULL,
    bill_no INT NOT NULL,
    party_name VARCHAR(255),
    material_name VARCHAR(255),
    ticket_no VARCHAR(100),
    broker VARCHAR(255),
    terms_of_delivery TEXT,
    sup_inv_no VARCHAR(100),
    gst_no VARCHAR(50),

    -- Weight System (5 columns)
    bags DECIMAL(10,2) DEFAULT 0,
    avg_bag_weight DECIMAL(10,2) DEFAULT 0,
    net_weight_kg DECIMAL(10,2) DEFAULT 0,
    gunny_weight_kg DECIMAL(10,2) DEFAULT 0,
    final_weight_kg DECIMAL(10,2) DEFAULT 0,
    weight_quintal DECIMAL(10,3) DEFAULT 0,
    weight_khandi DECIMAL(10,3) DEFAULT 0,

    -- Rate System (3 columns)
    rate_basis VARCHAR(20) DEFAULT 'Quintal',
    rate_value DECIMAL(10,2) DEFAULT 0,
    total_purchase_amount DECIMAL(10,2) DEFAULT 0,

    -- Deductions (16 columns)
    bank_commission DECIMAL(10,2) DEFAULT 0,
    postage DECIMAL(10,2) DEFAULT 0,
    batav_percent DECIMAL(10,2) DEFAULT 0,
    batav DECIMAL(10,2) DEFAULT 0,
    shortage_percent DECIMAL(10,2) DEFAULT 0,
    shortage DECIMAL(10,2) DEFAULT 0,
    dalali_rate DECIMAL(10,2) DEFAULT 0,
    dalali DECIMAL(10,2) DEFAULT 0,
    hammali_rate DECIMAL(10,2) DEFAULT 0,
    hammali DECIMAL(10,2) DEFAULT 0,
    freight DECIMAL(10,2) DEFAULT 0,
    rate_diff DECIMAL(10,2) DEFAULT 0,
    quality_diff DECIMAL(10,2) DEFAULT 0,
    quality_diff_comment TEXT,
    moisture_ded DECIMAL(10,2) DEFAULT 0,
    tds DECIMAL(10,2) DEFAULT 0,
    total_deduction DECIMAL(10,2) DEFAULT 0,
    payable_amount DECIMAL(10,2) DEFAULT 0,

    -- Payment Instalments (25 columns = 5 instalments × 5 fields)
    instalment_1_date DATE,
    instalment_1_amount DECIMAL(10,2) DEFAULT 0,
    instalment_1_payment_method VARCHAR(50) DEFAULT '',
    instalment_1_payment_bank_account VARCHAR(255) DEFAULT '',
    instalment_1_comment TEXT,

    instalment_2_date DATE,
    instalment_2_amount DECIMAL(10,2) DEFAULT 0,
    instalment_2_payment_method VARCHAR(50) DEFAULT '',
    instalment_2_payment_bank_account VARCHAR(255) DEFAULT '',
    instalment_2_comment TEXT,

    instalment_3_date DATE,
    instalment_3_amount DECIMAL(10,2) DEFAULT 0,
    instalment_3_payment_method VARCHAR(50) DEFAULT '',
    instalment_3_payment_bank_account VARCHAR(255) DEFAULT '',
    instalment_3_comment TEXT,

    instalment_4_date DATE,
    instalment_4_amount DECIMAL(10,2) DEFAULT 0,
    instalment_4_payment_method VARCHAR(50) DEFAULT '',
    instalment_4_payment_bank_account VARCHAR(255) DEFAULT '',
    instalment_4_comment TEXT,

    instalment_5_date DATE,
    instalment_5_amount DECIMAL(10,2) DEFAULT 0,
    instalment_5_payment_method VARCHAR(50) DEFAULT '',
    instalment_5_payment_bank_account VARCHAR(255) DEFAULT '',
    instalment_5_comment TEXT,

    -- Other (3 columns)
    prepared_by VARCHAR(255),
    authorised_sign VARCHAR(255),
    paddy_unloading_godown TEXT,

    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verify table was created
DESCRIBE purchase_slips;

-- Show column count
SELECT COUNT(*) as total_columns
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'purchase_slips';
