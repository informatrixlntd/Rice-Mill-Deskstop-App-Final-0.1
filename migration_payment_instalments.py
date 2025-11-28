"""
DATABASE MIGRATION: Payment Info & Instalments Update

This migration:
1. Removes Payment Info section (4 columns)
2. Removes Payment Due fields (2 columns)
3. Adds Payment Method & Bank Account to each instalment (10 new columns)

Total: Remove 6 columns, Add 10 columns

IMPORTANT: This will NOT delete existing slip data!
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

def run_migration():
    print("=" * 60)
    print("DATABASE MIGRATION: Payment Info & Instalments Update")
    print("=" * 60)
    print()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Remove Payment Info columns
        print("Step 1: Removing Payment Info columns...")
        columns_to_remove = [
            'payment_method',
            'payment_date',
            'payment_amount',
            'payment_bank_account'
        ]

        for column in columns_to_remove:
            try:
                cursor.execute(f'''
                    ALTER TABLE purchase_slips
                    DROP COLUMN {column}
                ''')
                print(f"  ✓ Removed column: {column}")
            except mysql.connector.Error as e:
                if "Unknown column" in str(e) or "Can't DROP" in str(e):
                    print(f"  ⚠ Column '{column}' doesn't exist (skipping)")
                else:
                    raise

        conn.commit()
        print()

        # Step 2: Remove Payment Due columns
        print("Step 2: Removing Payment Due columns...")
        payment_due_columns = [
            'payment_due_date',
            'payment_due_comment'
        ]

        for column in payment_due_columns:
            try:
                cursor.execute(f'''
                    ALTER TABLE purchase_slips
                    DROP COLUMN {column}
                ''')
                print(f"  ✓ Removed column: {column}")
            except mysql.connector.Error as e:
                if "Unknown column" in str(e) or "Can't DROP" in str(e):
                    print(f"  ⚠ Column '{column}' doesn't exist (skipping)")
                else:
                    raise

        conn.commit()
        print()

        # Step 3: Add Payment Method & Bank Account to each instalment
        print("Step 3: Adding Payment Method & Bank Account to instalments...")

        new_columns = []
        for i in range(1, 6):
            new_columns.append(f'instalment_{i}_payment_method')
            new_columns.append(f'instalment_{i}_payment_bank_account')

        for column in new_columns:
            try:
                if 'payment_method' in column:
                    cursor.execute(f'''
                        ALTER TABLE purchase_slips
                        ADD COLUMN {column} VARCHAR(50) DEFAULT ''
                    ''')
                else:  # payment_bank_account
                    cursor.execute(f'''
                        ALTER TABLE purchase_slips
                        ADD COLUMN {column} VARCHAR(255) DEFAULT ''
                    ''')
                print(f"  ✓ Added column: {column}")
            except mysql.connector.Error as e:
                if "Duplicate column" in str(e):
                    print(f"  ⚠ Column '{column}' already exists (skipping)")
                else:
                    raise

        conn.commit()
        print()

        # Step 4: Verify schema
        print("Step 4: Verifying new schema...")
        cursor.execute("DESCRIBE purchase_slips")
        columns = cursor.fetchall()

        instalment_payment_columns = [col[0] for col in columns if 'instalment' in col[0] and ('payment_method' in col[0] or 'payment_bank_account' in col[0])]

        print(f"  ✓ Found {len(instalment_payment_columns)} new instalment payment columns")
        for col in instalment_payment_columns:
            print(f"    - {col}")

        print()
        print("=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Summary:")
        print("  • Removed Payment Info section (4 columns)")
        print("  • Removed Payment Due fields (2 columns)")
        print("  • Added Payment Method & Bank Account to instalments (10 columns)")
        print()
        print("Next steps:")
        print("  1. Update backend INSERT/UPDATE statements")
        print("  2. Update frontend UI with new instalment fields")
        print("  3. Test slip creation with new schema")
        print()

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
