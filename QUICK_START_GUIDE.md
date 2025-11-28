# Quick Start Guide - Purchase Slip Manager

## Starting the Application

### Desktop App (Recommended)
```
Double-click: START_DESKTOP_APP.bat
```
- Opens login window
- Login with your credentials
- Full featured desktop application

### Web Version
```
Double-click: run.bat
```
- Starts Flask server
- Open browser to: http://localhost:5000
- Better print preview in browser

---

## Navigation

### Main Navigation Bar
```
[Rice Mill Purchase Slip Manager]  [View Reports] [View All Slips]
```

- **Create New Slip:** Main page (default view)
- **View Reports:** See all slips in table format
- **View All Slips:** Same as View Reports

---

## Creating a Purchase Slip

### Step 1: Basic Details
1. Fill in Company Name and Address
2. Enter Vehicle No, Date (auto-filled), Party Name
3. Add Material Name, Ticket No, Broker details
4. Bill No is auto-generated

### Step 2: Weight & Rate
```
Bags: 100
Net Weight: 7500 kg
Shortage: 0 kg
Rate (100 kg): 3500
Rate Basis: 100 kg (Quintal) or 150 kg (Khandi)
```
- System auto-calculates: Avg Bag Weight, Calculated Rate, Amount

### Step 3: Deductions

**Category A: Direct ₹ Deductions**
- Bank Commission, Postage, Freight
- Rate Diff, Quality Diff, Moisture Ded, TDS
- Enter direct amounts

**Category B: Batav % Deduction**
- Default: 0 (enter percentage if needed)
- Calculates: Amount × (Batav % / 100)

**Category C: Fixed Formula Deductions**
- Dalali Rate (per kg): Default 0
- Hammali Rate (per kg): Default 0
- Calculates: Net Weight × Rate

**Important:** Only enter values if you want deductions!
- If field shows 0, no deduction is applied
- To apply deduction, enter the rate/percentage

### Step 4: Payment Info (Optional)
- Payment Method: Cash or Online Transfer
- Payment Date
- Payment Amount
- Bank Account Details

### Step 5: Installments (Optional)
```
Instalment 1: Date: 2025-11-25, Amount: ₹5000, Method: Cash
Instalment 2: Paid ₹3000 on 30-Nov-2025 via Online
```
- Free text format
- Enter up to 5 installments
- Use any format you prefer

### Step 6: Save & Print
1. Click "Save & Print"
2. Print dialog opens automatically
3. Select printer or "Save as PDF"
4. Adjust settings and print

---

## Viewing & Editing Slips

### View All Slips Page
1. Click "View Reports" or "View All Slips"
2. See table of all slips
3. Use search box to filter

### Actions Available
- **Edit:** Update payment info, installments, comments
- **Print:** Reprint any slip
- **Delete:** Remove slip (with confirmation)

### Edit a Slip
1. Click "Edit" button on any slip
2. Modal opens with editable fields:
   - Payment details
   - Payment due info
   - Installments
   - Quality/Moisture comments
   - Signatures
3. Click "Save Changes"

---

## Understanding the Deduction System

### When Deductions Apply
```
Batav %:     0  → No deduction
Batav %:     2  → Deducts 2% of Amount

Dalali Rate: 0  → No deduction
Dalali Rate: 5  → Deducts 5 × Net Weight

Hammali Rate: 0  → No deduction
Hammali Rate: 5  → Deducts 5 × Net Weight
```

### Example Calculation
```
Net Weight: 1000 kg
Rate: 3500
Amount: 35000

Batav %: 0        → ₹0
Dalali: 0/kg      → ₹0
Hammali: 0/kg     → ₹0
Bank Commission: 50  → ₹50

Total Deduction: ₹50
Payable Amount: ₹34,950
```

---

## Print Template Features

### What's Included
✓ All company and party details
✓ Complete weight and rate information
✓ All deductions with rates/percentages shown
✓ Payment information
✓ All filled installments
✓ Comments and notes
✓ Signatures

### Smart Display
- Empty fields are hidden
- Only shows deductions that have values
- Categories clearly labeled
- Professional formatting

---

## Common Tasks

### Task: Create slip with no Dalali/Hammali
**Solution:** Leave Dalali Rate and Hammali Rate at 0

### Task: Apply 2% Batav deduction
**Solution:** Enter 2 in Batav % field

### Task: Record installment payments
**Solution:**
1. Edit slip from View All Slips page
2. Fill installment fields with payment details
3. Save changes
4. Reprint slip to see updated installments

### Task: Change payment method after creation
**Solution:**
1. Go to View All Slips
2. Click Edit on the slip
3. Update Payment Method field
4. Save changes

---

## Troubleshooting

### Print shows "app doesn't support preview"
- **Normal behavior** for Electron apps
- Use "Save as PDF" to preview first
- Or use web version for browser print preview

### Deductions showing when rates are 0
- Check that default values are actually 0
- Clear form and try again
- Restart application if persists

### Bill number not auto-incrementing
- Database connection issue
- Check backend is running
- Restart application

### Can't see installments on print
- Make sure installment fields have text
- Empty fields are automatically hidden
- Try reprinting after saving

---

## Tips & Best Practices

1. **Fill fields as you go** - Form auto-calculates
2. **Double-check rates** - Especially Batav/Dalali/Hammali
3. **Use Clear Form** - If you need to start over
4. **Save regularly** - When creating multiple slips
5. **Print immediately** - After saving each slip
6. **Use installments** - For tracking partial payments
7. **Add comments** - For quality issues or special conditions

---

## Keyboard Shortcuts

- **Tab:** Move to next field
- **Shift+Tab:** Move to previous field
- **Ctrl+P:** Print (on print preview page)
- **Esc:** Close modal dialogs

---

## Getting Help

1. Read this guide
2. Check `FIXES_APPLIED_SUMMARY.md` for recent changes
3. See `INSTALLMENT_LOGIC_EXPLANATION.md` for installment details
4. Review form field tooltips (hover over labels)

---

## System Requirements

- **OS:** Windows 7 or later
- **Python:** 3.x
- **Browser:** Modern browser (Chrome, Firefox, Edge)
- **Printer:** Any Windows-compatible printer or PDF writer

---

Last Updated: 2025-11-23
Version: 2.0
