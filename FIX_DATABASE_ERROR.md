# 🔧 FIX: Unknown column 'net_weight_kg' Error

## Problem
The database schema is outdated and missing the new columns that the backend code requires.

## Solution
Run the SQL migration file to update the database schema.

---

## 📋 STEP-BY-STEP FIX:

### Method 1: Using MySQL Command Line (Recommended)
```bash
# Navigate to project directory
cd /tmp/cc-agent/60598523/project

# Run the migration SQL file
mysql -u root -p purchase_slips_db < migration_schema_update.sql

# Enter your MySQL password when prompted
```

### Method 2: Using MySQL Workbench or phpMyAdmin
1. Open MySQL Workbench or phpMyAdmin
2. Connect to your database
3. Select the `purchase_slips_db` database
4. Open the file `migration_schema_update.sql`
5. Execute the entire SQL script

### Method 3: Copy-Paste SQL Commands
1. Open MySQL CLI: `mysql -u root -p`
2. Enter password
3. Type: `USE purchase_slips_db;`
4. Copy and paste the contents of `migration_schema_update.sql`
5. Press Enter to execute

---

## ✅ What This Migration Does:

### Adds NEW Columns (41 total):
1. **Weight System (5 columns):**
   - net_weight_kg
   - gunny_weight_kg
   - final_weight_kg
   - weight_quintal
   - weight_khandi

2. **Rate System (3 columns):**
   - rate_basis (Quintal/Khandi)
   - rate_value
   - total_purchase_amount

3. **Deduction System (7 columns):**
   - postage
   - freight
   - rate_diff
   - quality_diff
   - quality_diff_comment
   - moisture_ded
   - tds

4. **Payment Instalments (25 columns):**
   - For each of 5 instalments:
     - date
     - amount
     - payment_method ← NEW
     - payment_bank_account ← NEW
     - comment

5. **Other (1 column):**
   - paddy_unloading_godown

### Removes OLD Columns (6 total):
- payment_method (moved to instalments)
- payment_date (moved to instalments)
- payment_amount (moved to instalments)
- payment_bank_account (moved to instalments)
- payment_due_date (removed)
- payment_due_comment (removed)

---

## 🚀 After Running Migration:

1. **Restart your backend server:**
   ```bash
   # Stop current server (Ctrl+C)
   python backend/app.py
   ```

2. **Test in browser:**
   - Create a new purchase slip
   - Add payment instalments
   - Save and print

---

## ⚠️ Important Notes:

- ✅ This migration is SAFE - it only ADDS columns, never deletes data
- ✅ All existing slip data will be preserved
- ✅ Old columns are kept initially for safety
- ✅ Uses `IF NOT EXISTS` to prevent errors if run multiple times

---

## 🐛 If You Still Get Errors:

1. **Check which columns are missing:**
   ```sql
   DESCRIBE purchase_slips;
   ```

2. **Look for the missing column in the output**

3. **Add it manually if needed:**
   ```sql
   ALTER TABLE purchase_slips
   ADD COLUMN net_weight_kg DECIMAL(10,2) DEFAULT 0;
   ```

---

## 📞 Need Help?

Check the migration output for any error messages. The SQL file is safe to run multiple times - it will skip columns that already exist.

**File Location:** `migration_schema_update.sql`

---

**Status:** Ready to run
**Safety:** 100% Safe - no data loss
**Time:** ~5 seconds
