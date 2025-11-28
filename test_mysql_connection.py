#!/usr/bin/env python3
"""
MySQL Connection Diagnostic Test
Run this to check if MySQL is accessible
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("MYSQL CONNECTION DIAGNOSTIC TEST")
print("=" * 60)
print()

# Test 1: Check if mysql.connector is installed
print("1. Checking mysql.connector installation...")
try:
    import mysql.connector
    print("   ✓ mysql.connector is installed")
    print(f"   Version: {mysql.connector.__version__}")
except ImportError as e:
    print(f"   ❌ mysql.connector NOT installed: {e}")
    print()
    print("   FIX: Run: pip install mysql-connector-python")
    sys.exit(1)

print()

# Test 2: Check database configuration
print("2. Checking database configuration...")
try:
    from database import DB_CONFIG
    print("   ✓ Database config loaded")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Port: {DB_CONFIG['port']}")
    print(f"   User: {DB_CONFIG['user']}")
    print(f"   Database: {DB_CONFIG['database']}")
except Exception as e:
    print(f"   ❌ Failed to load config: {e}")
    sys.exit(1)

print()

# Test 3: Try to connect to MySQL server (without database)
print("3. Testing MySQL server connection...")
try:
    temp_config = DB_CONFIG.copy()
    database_name = temp_config.pop('database')

    conn = mysql.connector.connect(**temp_config)
    print("   ✓ MySQL server is accessible")
    conn.close()
except mysql.connector.Error as err:
    print(f"   ❌ Cannot connect to MySQL server: {err}")
    print()
    print("   POSSIBLE CAUSES:")
    print("   - MySQL server not running")
    print("   - Wrong host/port (check if MySQL is on localhost:1396)")
    print("   - Wrong username/password")
    print()
    print("   FIX:")
    print("   1. Check if MySQL is running: Check your MySQL service")
    print("   2. Verify port 1396 is correct")
    print("   3. Verify username 'root' and password 'root' are correct")
    sys.exit(1)

print()

# Test 4: Check if database exists
print("4. Checking if database exists...")
try:
    temp_config = DB_CONFIG.copy()
    database_name = temp_config.pop('database')

    conn = mysql.connector.connect(**temp_config)
    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]

    if database_name in databases:
        print(f"   ✓ Database '{database_name}' exists")
    else:
        print(f"   ⚠️  Database '{database_name}' does NOT exist")
        print(f"   Available databases: {', '.join(databases)}")
        print()
        print("   FIX: Database will be created automatically when app starts")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"   ❌ Error checking database: {e}")
    sys.exit(1)

print()

# Test 5: Try to connect to the application database
print("5. Testing full database connection...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print(f"   ✓ Successfully connected to database '{DB_CONFIG['database']}'")
    conn.close()
except mysql.connector.Error as err:
    if err.errno == 1049:
        print(f"   ⚠️  Database '{DB_CONFIG['database']}' doesn't exist yet")
        print("   This is normal for first run - it will be created automatically")
    else:
        print(f"   ❌ Connection failed: {err}")
        sys.exit(1)

print()

# Test 6: Check if users table exists
print("6. Checking users table...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    if 'users' in tables:
        print("   ✓ 'users' table exists")

        # Count users
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"   Found {count} user(s) in database")

        if count == 0:
            print("   ⚠️  No users in database")
            print("   FIX: Run the app once to create default admin user")
    else:
        print("   ⚠️  'users' table does NOT exist")
        print(f"   Available tables: {', '.join(tables) if tables else 'None'}")
        print("   FIX: Run the app once to initialize tables")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"   ⚠️  Could not check users table: {e}")

print()
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print()
print("NEXT STEPS:")
print("1. If MySQL server is not running, start it")
print("2. If database doesn't exist, start the Flask app once")
print("3. If users table is empty, the app will create admin user")
print("4. Then try accessing Manage Users page again")
