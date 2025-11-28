# ✅ TESTING GUIDE - After Migration

This guide helps you verify that everything works after running the database migration.

---

## 📋 STEP 1: Verify Database Schema

Run the verification script to check if all columns were added:

```bash
python3 verify_database_schema.py
```

**Expected Output:**
```
✅ SUCCESS! All required columns are present!
Your database schema is correct and ready to use.
```

If you see errors, re-run the migration:
```bash
mysql -u root -p purchase_slips_db < migration_schema_update.sql
```

---

## 📋 STEP 2: Restart Backend Server

```bash
# Stop current server (Ctrl+C if running)
# Then start fresh:
python backend/app.py
```

**Expected Output:**
```
* Running on http://127.0.0.1:5000
```

---

## 📋 STEP 3: Test Creating a New Slip

### Open Browser:
```
http://127.0.0.1:5000
```

### Fill in Test Data:

**Basic Info:**
- Bill No: 1001
- Date: (today's date)
- Party Name: Test Party
- Material: Rice

**Weight Section:**
- Bags: 100
- Avg Bag Wt: 50 kg
- Net Weight KG: 5000
- Gunny Weight KG: 100
- Final Weight KG: 4900

**Rate Section:**
- Rate Basis: Quintal (select from dropdown)
- Rate Value: 3000
- Total Purchase Amount: 1470000

**Deductions:**
- Dalali Rate: 10
- Hammali Rate: 10
- (Other deductions can be 0)

**Payment Instalment 1:**
- Date: (today's date)
- Amount: 500000
- Payment Method: Cash
- Bank Account: (leave empty for cash)
- Comment: First instalment

### Click "Save Purchase Slip"

---

## ✅ EXPECTED RESULTS:

### 1. Success Message
```
✅ Purchase slip saved successfully!
   Bill No: 1001
```

### 2. No Console Errors
Open browser DevTools (F12) → Console tab
- Should be clean, no red errors

### 3. Backend Logs
Check your terminal running backend:
```
127.0.0.1 - - [27/Nov/2025 22:50:00] "POST /api/add-slip HTTP/1.1" 200 -
```

**Status 200** = Success! ✅
**Status 400/500** = Error ❌

---

## 📋 STEP 4: Test Calculations

Verify the automatic calculations are correct:

### Weight Calculations:
- **Final Weight KG** = Net Weight KG - Gunny Weight KG
- **Weight Quintal** = Final Weight KG ÷ 100
- **Weight Khandi** = Final Weight KG ÷ 150

**Example:**
- Net: 5000 kg
- Gunny: 100 kg
- Final: **4900 kg** ✓
- Quintal: **49.000** ✓
- Khandi: **32.667** ✓

### Dalali & Hammali (Based on Rate Basis):
If Rate Basis = **Quintal**:
- Dalali = Weight Quintal × Dalali Rate
- Example: 49.000 × 10 = **490.00** ✓

If Rate Basis = **Khandi**:
- Dalali = Weight Khandi × Dalali Rate
- Example: 32.667 × 10 = **326.67** ✓

### Total Amount:
- Total Purchase Amount = Weight × Rate Value
- Payable Amount = Total Purchase Amount - All Deductions

---

## 📋 STEP 5: Test View All Slips

### Navigate to Reports:
```
http://127.0.0.1:5000/reports.html
```

### Expected Table Columns:
```
Bill No | Date | Party Name | Final Wt (KG) | Rate Basis | Payable | Paid | Balance | Actions
```

### Verify Data:
- ✓ Bill No shows correctly (1001)
- ✓ Final Wt shows in KG (4900.00)
- ✓ Rate Basis shows (Quintal)
- ✓ Payable amount is correct
- ✓ Paid shows instalment 1 amount (500000.00)
- ✓ Balance = Payable - Paid

---

## 📋 STEP 6: Test Edit Slip

### Click "Edit" button on the slip

### Expected Sections:
1. ✓ Deduction Details
2. ✓ Payment Instalments (with Method & Bank Account fields)
3. ✓ Other Details
4. ✗ NO "Payment Info" section (should be removed)
5. ✗ NO "Payment Due" section (should be removed)

### Make a change:
- Update Instalment 1 Amount: 600000
- Click "Save Changes"

### Verify:
- ✓ Success message appears
- ✓ Table updates with new Paid amount
- ✓ Balance recalculates

---

## 📋 STEP 7: Test Print Slip

### Click "Print" button

### Expected Print Layout:
1. ✓ Company header
2. ✓ Basic slip details
3. ✓ Weight details (showing Final Wt KG)
4. ✓ Rate details (showing Rate Basis)
5. ✓ Deductions table
6. ✓ **Payment Instalments table with 6 columns:**
   - Sr | Date | Amount | **Method** | **Bank Account** | Comment
7. ✗ NO "Payment Information" section (removed)
8. ✓ Footer with signatures

### Verify Instalment Table:
```
Sr | Date       | Amount     | Method | Bank Account | Comment
1  | 27/11/2025 | ₹600000.00 | Cash   | -            | First instalment
```

---

## 📋 STEP 8: Test Dynamic Instalments

### On Create/Edit form:

1. **Initially:**
   - ✓ Only Instalment 1 visible
   - ✓ "+ Add Instalment" button visible

2. **Click "+ Add Instalment":**
   - ✓ Instalment 2 appears
   - ✓ Remove button on Instalment 2
   - ✓ "+ Add Instalment" still visible

3. **Add until Instalment 5:**
   - ✓ All 5 instalments visible
   - ✓ "+ Add Instalment" button HIDDEN

4. **Click "Remove" on Instalment 3:**
   - ✓ Instalment 3 hidden
   - ✓ Fields cleared
   - ✓ "+ Add Instalment" button visible again

---

## ✅ ALL TESTS PASSED?

If all tests above pass:
- ✅ Migration successful
- ✅ Database schema correct
- ✅ Backend working properly
- ✅ Frontend calculations accurate
- ✅ Dynamic UI functioning
- ✅ Print layout updated

**Your application is ready for production use!** 🎉

---

## ❌ IF TESTS FAIL:

### Error: "Unknown column..."
→ Re-run migration:
```bash
mysql -u root -p purchase_slips_db < migration_schema_update.sql
```

### Error: Calculations wrong
→ Check browser console (F12) for JavaScript errors
→ Verify script.js has the updated calculation functions

### Error: Print layout wrong
→ Clear browser cache (Ctrl+Shift+R)
→ Verify print_template_new.html was updated

### Error: Dynamic instalments not working
→ Check browser console for JavaScript errors
→ Verify script.js has addInstalment() and removeInstalment() functions

---

## 📞 SUPPORT CHECKLIST:

Before asking for help, verify:
- [ ] Migration ran without errors
- [ ] verify_database_schema.py shows all columns present
- [ ] Backend restarted after migration
- [ ] Browser cache cleared
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal

---

**Testing Time:** ~10 minutes
**Last Updated:** November 27, 2025
