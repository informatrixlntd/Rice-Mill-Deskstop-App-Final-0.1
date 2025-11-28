-- Create users table for login system
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Insert default admin user (password: admin123)
INSERT INTO users (username, password, full_name, role, is_active)
VALUES ('admin', 'admin123', 'Administrator', 'admin', TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Add moisture_percent column to purchase_slips table
ALTER TABLE purchase_slips
ADD COLUMN IF NOT EXISTS moisture_percent DECIMAL(5,2) DEFAULT 0 AFTER moisture_ded;
