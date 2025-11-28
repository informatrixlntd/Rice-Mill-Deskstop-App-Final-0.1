# Purchase Slip Application - Upgrade Notes

## What's New in This Version

### Real-Time Auto-Calculation
All computed fields now update **instantly** as you type - no need to click any buttons or submit the form first!

### New Fields & Structure

#### Company Details Section
- Company Name
- Company Address
- Document Type (default: "Purchase Slip")

#### Enhanced Vehicle & Party Details
- Vehicle No
- Date
- Party Name (previously "Supplier Name")
- Material Name (previously "Material Description")
- Ticket No (NEW)
- Broker (NEW)
- Terms of Delivery (NEW)
- Sup. Inv. No (NEW)
- GST No (NEW)

#### Quantity Details with Auto-Calculation
- Bags (input field)
- Avg Bag Weight (input field)
- **Net Weight** (auto-calculated: Bags × Avg Bag Weight)
- Rate (input field)
- **Amount** (auto-calculated: Net Weight × Rate)

#### Advanced Deductions System
- Bank Commission & Postage (input field)
- Batav % (input field, default: 1%)
- **Batav Amount** (auto-calculated)
- Shortage % (input field, default: 1%)
- **Shortage Amount** (auto-calculated)
- Dalali Rate (input field, default: 10)
- **Dalali Amount** (auto-calculated)
- Hammali Rate (input field, default: 10)
- **Hammali Amount** (auto-calculated)
- **Total Deduction** (auto-calculated sum)

#### Payable Section
- **Payable Amount** (auto-calculated, displayed in large bold green text)

#### Payment Information (NEW)
- Payment Method (Cash / Online Transfer)
- Payment Date
- Payment Amount (auto-filled from Payable Amount)

#### Signatures
- Prepared By
- Authorised Sign (previously just "Authorized Signature")

## Auto-Calculation Logic

### Formula Reference
1. **Net Weight** = Bags × Avg Bag Weight
2. **Amount** = Net Weight × Rate
3. **Batav** = Amount × (Batav% / 100)
4. **Shortage** = Amount × (Shortage% / 100)
5. **Dalali** = Net Weight × Dalali Rate
6. **Hammali** = Net Weight × Hammali Rate
7. **Total Deduction** = Bank Commission + Batav + Shortage + Dalali + Hammali
8. **Payable Amount** = Amount - Total Deduction

All calculations happen in real-time as you modify any input field!

## Database Changes

### New Schema
The database has been completely restructured to support the new fields and calculation system.

**IMPORTANT:** You must run the migration script before using the updated application:

```bash
python migrate_database.py
```

This will:
- Create a backup of your existing database
- Drop the old table structure
- Create the new table with all new fields
- Preserve your data structure for future use

### Field Mapping (Old → New)
- `supplier_name` → `party_name`
- `material_desc` → `material_name`
- `quantity` → split into `bags` and `avg_bag_weight`
- `subtotal` → `amount`
- Individual deduction fields → percentage-based calculations
- `net_total` → `payable_amount`

## Frontend Changes

### User Interface Improvements
- Clean section headers with gradient backgrounds
- Computed fields have gray background to indicate read-only status
- Payable amount displayed prominently in large green box
- Better visual hierarchy with section dividers
- Responsive 2-column grid layout

### JavaScript Enhancements
- Real-time calculation engine
- All input fields trigger instant recalculation
- Payment amount auto-fills from payable amount
- Form validation and error handling
- Clean reset functionality

## Backend Changes

### New Calculation Function
Added `calculate_fields()` function in `backend/routes/slips.py` that:
- Accepts form data
- Performs all calculations server-side
- Returns updated data with computed fields
- Ensures data consistency

### Updated API Endpoints
- `/api/add-slip` - Now saves all new fields
- `/api/slips` - Returns updated field names
- `/print/<slip_id>` - Uses new template with all fields

## Print Template Updates

The print template now includes:
- Company information header
- All vehicle and party details in a grid
- Quantity details section
- Detailed deduction breakdown showing both rates/percentages and amounts
- Payment information section
- Enhanced signature area

## Migration Instructions

### For Existing Users

1. **Backup Your Data**
   ```bash
   copy purchase_slips.db purchase_slips_backup.db
   ```

2. **Run Migration**
   ```bash
   python migrate_database.py
   ```

3. **Restart Application**
   ```bash
   python backend/app.py
   ```

4. **Test the New Features**
   - Create a new purchase slip
   - Enter values in the input fields
   - Watch the real-time calculations
   - Save and print to verify

### For New Users

Simply run the application - the database will be created automatically with the new schema:

```bash
python backend/app.py
```

## Files Modified

- `backend/database.py` - Updated schema
- `backend/routes/slips.py` - Added calculation logic
- `frontend/index.html` - Complete redesign with new fields
- `frontend/static/js/script.js` - Real-time calculation engine
- `frontend/static/css/style.css` - Enhanced styling
- `backend/templates/print_template.html` - Updated print layout
- `frontend/reports.html` - Updated field names

## Files Added

- `migrate_database.py` - Database migration script
- `UPGRADE_NOTES.md` - This file

## Benefits of the Upgrade

1. **Faster Data Entry** - See calculations instantly without clicking
2. **More Detailed Records** - Additional fields for better tracking
3. **Better Accuracy** - Automated calculations reduce errors
4. **Professional Look** - Enhanced UI with clear visual hierarchy
5. **Payment Tracking** - New payment information section
6. **Flexible Deductions** - Percentage and rate-based deductions

## Support

If you encounter any issues during the upgrade:

1. Check that you ran the migration script
2. Verify Flask is installed: `pip install flask`
3. Ensure Python 3.8+ is installed
4. Check the README.md for detailed instructions
5. Restore from backup if needed: Replace `purchase_slips.db` with `purchase_slips_backup.db`

---

**Version:** 2.0.0
**Date:** October 2024
**Upgrade Type:** Major - Requires Database Migration
