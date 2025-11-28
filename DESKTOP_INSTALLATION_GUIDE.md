# 🖥️ RICE MILL DESKTOP APPLICATION - INSTALLATION GUIDE

## 📋 Prerequisites

Before installing, ensure you have:

1. **Windows 10 or later** (64-bit)
2. **Python 3.8 or higher** installed
3. **Node.js 16 or higher** installed
4. **MySQL Server** installed and running
5. **Internet connection** (for initial setup only)

---

## 🚀 COMPLETE INSTALLATION STEPS

### **Step 1: Install Prerequisites**

#### **1.1 Install Python**
- Download from: https://www.python.org/downloads/
- During installation, **CHECK** "Add Python to PATH"
- Verify: Open CMD and type `python --version`

#### **1.2 Install Node.js**
- Download from: https://nodejs.org/
- Install LTS version
- Verify: Open CMD and type `node --version`

#### **1.3 Install MySQL**
- Download from: https://dev.mysql.com/downloads/mysql/
- Install MySQL Server
- Remember your **root password**
- Start MySQL service

---

### **Step 2: Setup Database**

1. **Open MySQL Command Line** or **MySQL Workbench**

2. **Create Database:**
```sql
CREATE DATABASE rice_mill_db;
USE rice_mill_db;
```

3. **Run Migration Script:**
```sql
SOURCE /path/to/project/backend/migrations/add_users_table.sql;
```

4. **Verify Tables Created:**
```sql
SHOW TABLES;
```
You should see: `users` and `purchase_slips`

5. **Update Database Connection:**
- Edit `/backend/database.py`
- Update these lines:
```python
'host': 'localhost',
'user': 'root',          # Your MySQL username
'password': 'your_password',  # Your MySQL password
'database': 'rice_mill_db'
```

---

### **Step 3: Install Python Dependencies**

1. **Open Command Prompt** in project folder
2. **Run:**
```bash
cd backend
pip install -r ../requirements.txt
```

3. **Install flask-cors:**
```bash
pip install flask-cors
```

---

### **Step 4: Install Desktop Application**

1. **Navigate to desktop folder:**
```bash
cd desktop
```

2. **Install Node.js packages:**
```bash
npm install
```

This will install:
- Electron
- Electron Builder
- All dependencies

---

### **Step 5: Test Installation**

#### **5.1 Test Backend Server**

1. Open CMD in `/backend` folder
2. Run:
```bash
python app.py
```

3. You should see:
```
🌾 RICE MILL PURCHASE SLIP MANAGER
✅ Server starting...
📍 Open your browser and go to: http://127.0.0.1:5000
```

4. **Keep this running**

#### **5.2 Test Desktop App**

1. Open **NEW** CMD window in `/desktop` folder
2. Run:
```bash
npm start
```

3. Desktop application window should open
4. You should see **Login Screen**

---

### **Step 6: First Login**

**Default Credentials:**
- **Username:** admin
- **Password:** admin123

**Captcha:** Type the letters/numbers shown exactly

After login, you'll see the main application!

---

## 🎯 FEATURES OVERVIEW

### **1. Login System**
- Captcha protected
- User management (add/edit/delete users)
- Role-based access (admin/user)

### **2. Create Purchase Slip**
- All fields editable
- Real-time calculations
- Moisture percentage field
- Structured installments (Date + Amount + Method)
- Dynamic godown dropdown (stored in database)
- Auto-balance calculation
- Zero deduction handling

### **3. View All Slips**
- Table view of all slips
- View mode (read-only display)
- Edit button to load slip into form
- Direct print from table
- Delete slips

### **4. Printing**
- A4 auto-fit format
- Deductions shown in table format
- Only non-zero deductions printed
- Moisture % and amount shown
- Installment details
- Balance amount highlighted
- Direct Windows printing

### **5. User Management**
- Add new users
- Assign roles (admin/user)
- View last login
- Activate/deactivate users
- Cannot delete default admin

---

## 📝 USAGE INSTRUCTIONS

### **Creating a New Slip:**

1. Click **"Create New Slip"** tab
2. Fill all required fields:
   - Company details
   - Party name
   - Material details
   - Bags & Net Weight
   - Rate (select basis: 100kg or 150kg)
   - Shortage (if any)
   - Deductions (only fill non-zero values)
   - Moisture % (auto-calculates deduction)
   - Installments (Date, Amount, Method)
   - Godown (select or add new)

3. Click **"Save & Print"**
4. Slip saves to database and prints automatically

### **Viewing/Editing Slips:**

1. Click **"View All Slips"** tab
2. Click **"View"** button on any slip
3. View mode shows all details (read-only)
4. Click **"Edit Slip"** button at top
5. Form loads with all existing data
6. Make changes
7. Click **"Update & Print"**

### **Adding Godown:**

1. In Create Slip form
2. Find "Paddy Unloading Godown" dropdown
3. Click **"+ Add"** button
4. Enter new godown name
5. Immediately appears in dropdown
6. Auto-selected for current slip

### **Managing Users:**

1. Click **"Manage Users"** tab
2. Click **"Add New User"**
3. Fill: Username, Password, Full Name, Role
4. Click **"Add User"**
5. New user can now login

---

## 🔧 TROUBLESHOOTING

### **Problem: Backend won't start**
**Solution:**
- Check if MySQL is running
- Verify database credentials in `database.py`
- Check if port 5000 is free
- Run: `pip install flask flask-cors mysql-connector-python`

### **Problem: Desktop app shows "Cannot connect to backend"**
**Solution:**
- Ensure backend is running (`python app.py`)
- Check firewall settings
- Verify backend shows: "Running on http://127.0.0.1:5000"

### **Problem: Login fails**
**Solution:**
- Check captcha (case-sensitive)
- Verify users table exists in database
- Check default admin user exists:
```sql
SELECT * FROM users WHERE username = 'admin';
```

### **Problem: Print not working**
**Solution:**
- Check if printer is connected
- Ensure printer is set as default
- Try "Print Preview" first
- Check print_template_new.html exists

### **Problem: Calculations not updating**
**Solution:**
- Clear browser cache in iframe
- Refresh the form
- Check console for JavaScript errors

---

## 🏗️ BUILD STANDALONE EXECUTABLE

To create a standalone `.exe` installer:

1. Navigate to `/desktop` folder
2. Run:
```bash
npm run build-win
```

3. Installer will be created in `/desktop/dist/` folder
4. Share this installer with users
5. Users double-click to install (no dependencies needed)

**Note:** Backend still requires Python + MySQL on target machine.

---

## 📞 SUPPORT

### **Common Commands:**

**Start Backend:**
```bash
cd backend
python app.py
```

**Start Desktop:**
```bash
cd desktop
npm start
```

**Build Executable:**
```bash
cd desktop
npm run build-win
```

**Reset Admin Password:**
```sql
UPDATE users SET password = 'newpassword' WHERE username = 'admin';
```

---

## ✅ SYSTEM REQUIREMENTS

**Minimum:**
- Windows 10 (64-bit)
- 4GB RAM
- 1GB free disk space
- Screen resolution: 1280x720

**Recommended:**
- Windows 11 (64-bit)
- 8GB RAM
- 2GB free disk space
- Screen resolution: 1920x1080
- SSD for faster performance

---

## 🎉 CONGRATULATIONS!

Your Rice Mill Desktop Application is now installed and ready to use!

**Next Steps:**
1. Create your first purchase slip
2. Add more users if needed
3. Add your godown list
4. Test printing with a sample slip
5. Backup your database regularly

**Backup Command:**
```bash
mysqldump -u root -p rice_mill_db > backup.sql
```

---

## 📄 LICENSE

Copyright © 2024 - Rice Mill Management System
All rights reserved.

---

**Need Help?** Contact your system administrator or IT support.
