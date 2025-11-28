import sqlite3
import os

DATABASE_PATH = 'purchase_slips.db'

def migrate_database():
    """Migrate the existing database to the new schema"""

    backup_path = 'purchase_slips_backup.db'
    if os.path.exists(DATABASE_PATH):
        import shutil
        shutil.copy(DATABASE_PATH, backup_path)
        print(f"✓ Backup created: {backup_path}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS purchase_slips")
    print("✓ Dropped old table")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_slips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            company_address TEXT,
            document_type TEXT DEFAULT 'Purchase Slip',
            vehicle_no TEXT,
            date TEXT NOT NULL,
            bill_no INTEGER NOT NULL,
            party_name TEXT,
            material_name TEXT,
            ticket_no TEXT,
            broker TEXT,
            terms_of_delivery TEXT,
            sup_inv_no TEXT,
            gst_no TEXT,
            bags REAL DEFAULT 0,
            avg_bag_weight REAL DEFAULT 0,
            net_weight REAL DEFAULT 0,
            rate REAL DEFAULT 0,
            amount REAL DEFAULT 0,
            bank_commission REAL DEFAULT 0,
            batav_percent REAL DEFAULT 1,
            batav REAL DEFAULT 0,
            shortage_percent REAL DEFAULT 1,
            shortage REAL DEFAULT 0,
            dalali_rate REAL DEFAULT 10,
            dalali REAL DEFAULT 0,
            hammali_rate REAL DEFAULT 10,
            hammali REAL DEFAULT 0,
            total_deduction REAL DEFAULT 0,
            payable_amount REAL DEFAULT 0,
            payment_method TEXT,
            payment_date TEXT,
            payment_amount REAL DEFAULT 0,
            prepared_by TEXT,
            authorised_sign TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created new table with updated schema")

    conn.commit()
    conn.close()

    print("\n✅ Database migration completed successfully!")
    print("You can now start the application.\n")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("DATABASE MIGRATION SCRIPT")
    print("="*60 + "\n")
    migrate_database()
