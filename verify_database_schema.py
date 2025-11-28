"""
VERIFY DATABASE SCHEMA

This script checks if all required columns exist in the database.
Run this AFTER running the migration to verify everything is correct.
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Required columns for the new schema
REQUIRED_COLUMNS = [
    # Weight System
    'net_weight_kg',
    'gunny_weight_kg',
    'final_weight_kg',
    'weight_quintal',
    'weight_khandi',

    # Rate System
    'rate_basis',
    'rate_value',
    'total_purchase_amount',

    # Deductions
    'postage',
    'freight',
    'rate_diff',
    'quality_diff',
    'quality_diff_comment',
    'moisture_ded',
    'tds',

    # Instalments (just check instalment 1 as example)
    'instalment_1_date',
    'instalment_1_amount',
    'instalment_1_payment_method',
    'instalment_1_payment_bank_account',
    'instalment_1_comment',

    # Other
    'paddy_unloading_godown'
]

def verify_schema():
    print("=" * 70)
    print("DATABASE SCHEMA VERIFICATION")
    print("=" * 70)
    print()

    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'purchase_slips_db')
        )

        cursor = conn.cursor()
        cursor.execute("DESCRIBE purchase_slips")
        columns = cursor.fetchall()

        existing_columns = [col[0] for col in columns]

        print(f"✓ Connected to database successfully")
        print(f"✓ Table 'purchase_slips' exists")
        print(f"✓ Total columns in table: {len(existing_columns)}")
        print()
        print("-" * 70)
        print("CHECKING REQUIRED COLUMNS:")
        print("-" * 70)

        missing_columns = []
        present_columns = []

        for col in REQUIRED_COLUMNS:
            if col in existing_columns:
                print(f"  ✓ {col:40} PRESENT")
                present_columns.append(col)
            else:
                print(f"  ✗ {col:40} MISSING")
                missing_columns.append(col)

        print()
        print("=" * 70)
        print("SUMMARY:")
        print("=" * 70)
        print(f"  Required columns checked: {len(REQUIRED_COLUMNS)}")
        print(f"  Present: {len(present_columns)}")
        print(f"  Missing: {len(missing_columns)}")
        print()

        if len(missing_columns) == 0:
            print("✅ SUCCESS! All required columns are present!")
            print()
            print("Your database schema is correct and ready to use.")
            print("You can now restart your backend and create slips.")
            print()
            return True
        else:
            print("❌ ERROR! Some columns are missing!")
            print()
            print("Missing columns:")
            for col in missing_columns:
                print(f"  - {col}")
            print()
            print("Please run the migration again:")
            print("  mysql -u root -p purchase_slips_db < migration_schema_update.sql")
            print()
            return False

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"❌ DATABASE ERROR: {e}")
        print()
        print("Please check:")
        print("  - Is MySQL running?")
        print("  - Are the credentials in .env correct?")
        print("  - Does the database exist?")
        print()
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == '__main__':
    success = verify_schema()
    exit(0 if success else 1)
