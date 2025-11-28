# Rice Mill Purchase Slip Manager

A complete offline desktop application for managing purchase slips with real-time auto-calculation and direct printing.

## Features

- **Real-time Auto-Calculation** - All computed fields update instantly as you type
- **Modern Web UI** - Clean, responsive interface using Bootstrap
- **Offline Operation** - Works completely offline with SQLite database
- **Direct Printing** - Opens system print dialog for A4 layout
- **Reports Dashboard** - View, search, and manage all purchase slips
- **Auto Bill Numbers** - Automatically increments bill numbers

## Requirements

- Python 3.8 or higher
- Windows OS (recommended)

## Installation & Setup

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. IMPORTANT: Check "Add Python to PATH" during installation
4. Complete the installation

### Step 2: Install Dependencies

Open Command Prompt in the project folder and run:

```bash
pip install flask
```

### Step 3: Migrate Database (IMPORTANT - First Time Only)

If you have an existing database, run this migration script:

```bash
python migrate_database.py
```

This will update the database schema to support the new fields and calculations.

### Step 4: Run the Application

**Option A: Using the batch file (Easy)**
- Double-click `run.bat`

**Option B: Using Command Prompt**
```bash
python backend/app.py
```

### Step 5: Access the Application

1. Open your web browser
2. Go to: `http://127.0.0.1:5000`
3. Start creating purchase slips!

## Project Structure

```
purchase_slip_app/
│
├── backend/
│   ├── app.py                  # Flask application
│   ├── database.py             # Database operations
│   ├── routes/
│   │   └── slips.py           # API endpoints
│   └── templates/
│       └── print_template.html # Print layout
│
├── frontend/
│   ├── index.html             # Main form page
│   ├── reports.html           # Reports page
│   └── static/
│       ├── css/style.css      # Styling
│       └── js/script.js       # Real-time calculations
│
├── purchase_slips.db          # SQLite database (created automatically)
├── migrate_database.py        # Database migration script
├── run.bat                    # Windows launcher
└── requirements.txt           # Python dependencies
```

## Usage Guide

### Creating a Purchase Slip

#### Company Details
- Company Name
- Address
- Document Type (default: "Purchase Slip")

#### Vehicle & Party Details
- Vehicle No
- Date
- Party Name
- Material Name
- Ticket No
- Broker
- Terms of Delivery
- Sup. Inv. No
- GST No

#### Quantity Details (Auto-Calculated)
- Bags (enter number)
- Avg Bag Weight (enter weight in kg)
- **Net Weight** (auto-calculated: Bags × Avg Bag Weight)
- Rate (enter rate)
- **Amount** (auto-calculated: Net Weight × Rate)

#### Deductions (Auto-Calculated)
- Bank Commission & Postage (enter amount)
- Batav % (default: 1%)
- **Batav Amount** (auto-calculated: Amount × Batav%)
- Shortage % (default: 1%)
- **Shortage Amount** (auto-calculated: Amount × Shortage%)
- Dalali Rate (default: 10)
- **Dalali Amount** (auto-calculated: Net Weight × Dalali Rate)
- Hammali Rate (default: 10)
- **Hammali Amount** (auto-calculated: Net Weight × Hammali Rate)
- **Total Deduction** (auto-calculated sum)

#### Payable Section
- **Payable Amount** (auto-calculated: Amount - Total Deduction)
  - Displayed in bold green with large font

#### Payment Info
- Payment Method (Cash / Online Transfer)
- Payment Date
- Payment Amount (auto-filled from Payable Amount)

#### Signatures
- Prepared By
- Authorised Sign

### Real-Time Auto-Calculation

All computed fields update **instantly** as you enter values:

1. **Net Weight** = Bags × Avg Bag Weight
2. **Amount** = Net Weight × Rate
3. **Batav** = Amount × (Batav% / 100)
4. **Shortage** = Amount × (Shortage% / 100)
5. **Dalali** = Net Weight × Dalali Rate
6. **Hammali** = Net Weight × Hammali Rate
7. **Total Deduction** = Bank Commission + Batav + Shortage + Dalali + Hammali
8. **Payable Amount** = Amount - Total Deduction

No need to click any button - calculations happen automatically!

### Viewing Reports

1. Click "View Reports" in the top navigation
2. Browse all saved purchase slips
3. Use the search box to filter by party or material
4. Click "Print" to reprint any slip
5. Click "Delete" to remove a slip

## Print Layout

- A4 size (portrait orientation)
- Professional structured format
- Includes all slip details including:
  - Company information
  - Vehicle and party details
  - Quantity calculations
  - Detailed deduction breakdown
  - Payment information
  - Signatures
- Ready for immediate printing

## Database

- All data stored in `purchase_slips.db`
- SQLite format (no server required)
- Automatic table creation on first run
- Backs up easily by copying the .db file

## Troubleshooting

**"python is not recognized"**
- Reinstall Python and check "Add Python to PATH"

**"No module named flask"**
- Run: `pip install flask`

**Port already in use**
- Close any other application using port 5000
- Or change the port in `backend/app.py`

**Database locked**
- Close all running instances of the application
- Delete `purchase_slips.db` if corrupted (you'll lose data)

**Need to update database schema**
- Run: `python migrate_database.py`
- A backup will be created automatically

## Data Backup

To backup your data:
1. Copy the `purchase_slips.db` file
2. Store it in a safe location
3. To restore, replace the .db file with your backup

## Notes

- This application runs entirely offline
- No internet connection required
- All data stored locally
- Print directly from browser print dialog
- Compatible with all modern web browsers
- Real-time calculations work without any delays

## Support

For issues or questions, please refer to the troubleshooting section above.

---

**Made for offline desktop use on Windows**
