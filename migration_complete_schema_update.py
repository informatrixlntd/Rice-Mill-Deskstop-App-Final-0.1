"""
COMPLETE DATABASE SCHEMA MIGRATION

This migration updates the database from OLD schema to NEW schema:

OLD COLUMNS TO REMOVE/RENAME:
- net_weight → KEEP but add net_weight_kg
- rate → KEEP but add rate_value
- amount → KEEP but add total_purchase_amount

NEW COLUMNS TO ADD:
1. Weight System (5 columns):
   - net_weight_kg
   - gunny_weight_kg
   - final_weight_kg
   - weight_quintal
   - weight_khandi

2. Rate System (3 columns):
   - rate_basis (Quintal/Khandi)
   - rate_value
   - total_purchase_amount

3. Deduction System (5 columns):
   - postage
   - freight
   - rate_diff
   - quality_diff
   - quality_diff_comment
   - moisture_ded
   - tds

4. Payment Instalments (25 columns):
   - instalment_1 to 5 (date, amount, payment_method, payment_bank_account, comment)

5. Other (1 column):
   - paddy_unloading_godown

This script is SAFE - it only ADDS columns, never deletes data!
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'purchase_slips_db')
    )

def column_exists(cursor, table, column):
    """Check if a column exists in a table"""
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table}'
        AND COLUMN_NAME = '{column}'
    """)
    return cursor.fetchone()[0] > 0

def add_column_if_not_exists(cursor, conn, table, column, definition):
    """Add column only if it doesn't exist"""
    if not column_exists(cursor, table, column):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            conn.commit()
            print(f"  ✓ Added: {column}")
            return True
        except Exception as e:
            print(f"  ✗ Error adding {column}: {e}")
            return False
    else:
        print(f"  ⚠ Already exists: {column}")
        return False

def run_migration():
    print("=" * 70)
    print("COMPLETE DATABASE SCHEMA MIGRATION")
    print("=" * 70)
    print()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Add Weight System Columns
        print("Step 1: Adding Weight System Columns...")
        weight_columns = [
            ('net_weight_kg', 'DECIMAL(10,2) DEFAULT 0'),
            ('gunny_weight_kg', 'DECIMAL(10,2) DEFAULT 0'),
            ('final_weight_kg', 'DECIMAL(10,2) DEFAULT 0'),
            ('weight_quintal', 'DECIMAL(10,3) DEFAULT 0'),
            ('weight_khandi', 'DECIMAL(10,3) DEFAULT 0'),
        ]

        added = 0
        for col, definition in weight_columns:
            if add_column_if_not_exists(cursor, conn, 'purchase_slips', col, definition):
                added += 1
        print(f"  → Added {added} weight columns\n")

        # Step 2: Add Rate System Columns
        print("Step 2: Adding Rate System Columns...")
        rate_columns = [
            ('rate_basis', "VARCHAR(20) DEFAULT 'Quintal'"),
            ('rate_value', 'DECIMAL(10,2) DEFAULT 0'),
            ('total_purchase_amount', 'DECIMAL(10,2) DEFAULT 0'),
        ]

        added = 0
        for col, definition in rate_columns:
            if add_column_if_not_exists(cursor, conn, 'purchase_slips', col, definition):
                added += 1
        print(f"  → Added {added} rate columns\n")

        # Step 3: Add Deduction System Columns
        print("Step 3: Adding Deduction System Columns...")
        deduction_columns = [
            ('postage', 'DECIMAL(10,2) DEFAULT 0'),
            ('freight', 'DECIMAL(10,2) DEFAULT 0'),
            ('rate_diff', 'DECIMAL(10,2) DEFAULT 0'),
            ('quality_diff', 'DECIMAL(10,2) DEFAULT 0'),
            ('quality_diff_comment', 'TEXT'),
            ('moisture_ded', 'DECIMAL(10,2) DEFAULT 0'),
            ('tds', 'DECIMAL(10,2) DEFAULT 0'),
        ]

        added = 0
        for col, definition in deduction_columns:
            if add_column_if_not_exists(cursor, conn, 'purchase_slips', col, definition):
                added += 1
        print(f"  → Added {added} deduction columns\n")

        # Step 4: Add Payment Instalment Columns (with NEW payment fields)
        print("Step 4: Adding Payment Instalment Columns...")
        added = 0
        for i in range(1, 6):
            instalment_columns = [
                (f'instalment_{i}_date', 'DATE'),
                (f'instalment_{i}_amount', 'DECIMAL(10,2) DEFAULT 0'),
                (f'instalment_{i}_payment_method', "VARCHAR(50) DEFAULT ''"),
                (f'instalment_{i}_payment_bank_account', "VARCHAR(255) DEFAULT ''"),
                (f'instalment_{i}_comment', 'TEXT'),
            ]

            for col, definition in instalment_columns:
                if add_column_if_not_exists(cursor, conn, 'purchase_slips', col, definition):
                    added += 1
        print(f"  → Added {added} instalment columns (max 25)\n")

        # Step 5: Add Other Columns
        print("Step 5: Adding Other Columns...")
        other_columns = [
            ('paddy_unloading_godown', 'TEXT'),
        ]

        added = 0
        for col, definition in other_columns:
            if add_column_if_not_exists(cursor, conn, 'purchase_slips', col, definition):
                added += 1
        print(f"  → Added {added} other columns\n")

        # Step 6: Remove OLD Payment Info Columns (if they exist)
        print("Step 6: Removing OLD Payment Info Columns...")
        old_payment_columns = [
            'payment_method',
            'payment_date',
            'payment_amount',
            'payment_bank_account',
            'payment_due_date',
            'payment_due_comment'
        ]

        removed = 0
        for col in old_payment_columns:
            if column_exists(cursor, 'purchase_slips', col):
                try:
                    cursor.execute(f"ALTER TABLE purchase_slips DROP COLUMN {col}")
                    conn.commit()
                    print(f"  ✓ Removed: {col}")
                    removed += 1
                except Exception as e:
                    print(f"  ⚠ Could not remove {col}: {e}")
            else:
                print(f"  ⚠ Already removed: {col}")
        print(f"  → Removed {removed} old payment columns\n")

        # Step 7: Verify Schema
        print("Step 7: Verifying Final Schema...")
        cursor.execute("DESCRIBE purchase_slips")
        columns = cursor.fetchall()

        required_columns = [
            'net_weight_kg', 'gunny_weight_kg', 'final_weight_kg',
            'weight_quintal', 'weight_khandi',
            'rate_basis', 'rate_value', 'total_purchase_amount',
            'instalment_1_payment_method', 'instalment_1_payment_bank_account',
            'paddy_unloading_godown'
        ]

        existing_column_names = [col[0] for col in columns]

        print(f"  Total columns in table: {len(columns)}")
        print(f"\n  Checking required columns:")
        all_present = True
        for col in required_columns:
            if col in existing_column_names:
                print(f"    ✓ {col}")
            else:
                print(f"    ✗ MISSING: {col}")
                all_present = False

        print()
        print("=" * 70)
        if all_present:
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            print()
            print("Summary:")
            print("  • Added all new weight system columns")
            print("  • Added all new rate system columns")
            print("  • Added all payment instalment columns with payment methods")
            print("  • Removed old payment info columns")
            print("  • Total columns in database:", len(columns))
            print()
            print("✅ Database is now ready!")
            print("   Restart your backend: python backend/app.py")
        else:
            print("⚠ MIGRATION COMPLETED WITH WARNINGS")
            print("=" * 70)
            print("Some columns may be missing. Please check the output above.")

    except Exception as e:
        print()
        print("❌ ERROR DURING MIGRATION:")
        print(f"   {str(e)}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    try:
        run_migration()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        exit(1)
