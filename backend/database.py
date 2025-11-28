import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import os

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 1396,
    'user': 'root',
    'password': 'root',
    'database': 'purchase_slips_db'
}

# Global connection pool
connection_pool = None

def init_connection_pool():
    """
    Initialize MySQL connection pool using mysql.connector
    """
    global connection_pool
    try:
        connection_pool = MySQLConnectionPool(
            pool_name="purchase_pool",
            pool_size=10,
            pool_reset_session=True,
            **DB_CONFIG
        )
        print("✓ MySQL connection pool created successfully (size: 10)")
    except mysql.connector.Error as err:
        if err.errno == 1049:
            print("Database doesn't exist. Creating database...")
            create_database()
            connection_pool = MySQLConnectionPool(
                pool_name="purchase_pool",
                pool_size=10,
                pool_reset_session=True,
                **DB_CONFIG
            )
        else:
            print(f"❌ Error creating connection pool: {err}")
            raise

def create_database():
    """Create the database if it doesn't exist"""
    conn = None
    cursor = None
    try:
        temp_config = DB_CONFIG.copy()
        database_name = temp_config.pop('database')

        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✓ Database '{database_name}' created successfully")
    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_db_connection():
    """
    Get a database connection from the pool
    ALWAYS returns a connection with dictionary cursor support
    """
    global connection_pool
    if connection_pool is None:
        init_connection_pool()

    try:
        conn = connection_pool.get_connection()
        conn.ping(reconnect=True, attempts=3, delay=2)
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error getting connection from pool: {e}")
        raise

def init_db():
    """
    Initialize the database and create tables if they don't exist
    """
    conn = None
    cursor = None
    try:
        init_connection_pool()

        print(f"✓ Initializing database: {DB_CONFIG['database']}")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create purchase_slips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_slips (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name TEXT,
                company_address TEXT,
                document_type VARCHAR(255) DEFAULT 'Purchase Slip',
                vehicle_no VARCHAR(255),
                date VARCHAR(50) NOT NULL,
                bill_no INT NOT NULL,
                party_name TEXT,
                material_name TEXT,
                ticket_no VARCHAR(255),
                broker VARCHAR(255),
                terms_of_delivery TEXT,
                sup_inv_no VARCHAR(255),
                gst_no VARCHAR(255),
                bags DOUBLE DEFAULT 0,
                avg_bag_weight DOUBLE DEFAULT 0,
                net_weight DOUBLE DEFAULT 0,
                shortage_kg DOUBLE DEFAULT 0,
                rate DOUBLE DEFAULT 0,
                rate_basis VARCHAR(10) DEFAULT '100',
                calculated_rate DOUBLE DEFAULT 0,
                amount DOUBLE DEFAULT 0,
                bank_commission DOUBLE DEFAULT 0,
                postage DOUBLE DEFAULT 0,
                batav_percent DOUBLE DEFAULT 0,
                batav DOUBLE DEFAULT 0,
                shortage_percent DOUBLE DEFAULT 0,
                shortage DOUBLE DEFAULT 0,
                dalali_rate DOUBLE DEFAULT 0,
                dalali DOUBLE DEFAULT 0,
                hammali_rate DOUBLE DEFAULT 0,
                hammali DOUBLE DEFAULT 0,
                freight DOUBLE DEFAULT 0,
                rate_diff DOUBLE DEFAULT 0,
                quality_diff DOUBLE DEFAULT 0,
                quality_diff_comment TEXT,
                moisture_ded DOUBLE DEFAULT 0,
                moisture_ded_percent DOUBLE DEFAULT 0,
                tds DOUBLE DEFAULT 0,
                total_deduction DOUBLE DEFAULT 0,
                payable_amount DOUBLE DEFAULT 0,
                payment_method VARCHAR(255),
                payment_date VARCHAR(50),
                payment_amount DOUBLE DEFAULT 0,
                payment_bank_account TEXT,
                payment_due_date VARCHAR(50),
                payment_due_comment TEXT,
                instalment_1_date VARCHAR(50),
                instalment_1_amount DOUBLE DEFAULT 0,
                instalment_1_comment TEXT,
                instalment_2_date VARCHAR(50),
                instalment_2_amount DOUBLE DEFAULT 0,
                instalment_2_comment TEXT,
                instalment_3_date VARCHAR(50),
                instalment_3_amount DOUBLE DEFAULT 0,
                instalment_3_comment TEXT,
                instalment_4_date VARCHAR(50),
                instalment_4_amount DOUBLE DEFAULT 0,
                instalment_4_comment TEXT,
                instalment_5_date VARCHAR(50),
                instalment_5_amount DOUBLE DEFAULT 0,
                instalment_5_comment TEXT,
                prepared_by VARCHAR(255),
                authorised_sign VARCHAR(255),
                paddy_unloading_godown TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                role VARCHAR(50) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL
            )
        ''')

        # Create unloading_godowns table for dynamic dropdown
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unloading_godowns (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Check and add missing columns to purchase_slips
        cursor.execute("SHOW COLUMNS FROM purchase_slips")
        existing_columns = {row['Field'] for row in cursor.fetchall()}

        columns_to_add = {
            'shortage_kg': "DOUBLE DEFAULT 0",
            'rate_basis': "VARCHAR(10) DEFAULT '100'",
            'calculated_rate': "DOUBLE DEFAULT 0",
            'postage': "DOUBLE DEFAULT 0",
            'payment_due_date': "VARCHAR(50)",
            'payment_due_comment': "TEXT",
            'payment_bank_account': "TEXT",
            'instalment_1_date': "VARCHAR(50)",
            'instalment_1_amount': "DOUBLE DEFAULT 0",
            'instalment_1_comment': "TEXT",
            'instalment_2_date': "VARCHAR(50)",
            'instalment_2_amount': "DOUBLE DEFAULT 0",
            'instalment_2_comment': "TEXT",
            'instalment_3_date': "VARCHAR(50)",
            'instalment_3_amount': "DOUBLE DEFAULT 0",
            'instalment_3_comment': "TEXT",
            'instalment_4_date': "VARCHAR(50)",
            'instalment_4_amount': "DOUBLE DEFAULT 0",
            'instalment_4_comment': "TEXT",
            'instalment_5_date': "VARCHAR(50)",
            'instalment_5_amount': "DOUBLE DEFAULT 0",
            'instalment_5_comment': "TEXT",
            'quality_diff_comment': "TEXT",
            'moisture_ded_percent': "DOUBLE DEFAULT 0",
            'prepared_by': "VARCHAR(255)",
            'authorised_sign': "VARCHAR(255)",
            'paddy_unloading_godown': "TEXT"
        }

        for col_name, col_type in columns_to_add.items():
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE purchase_slips ADD COLUMN {col_name} {col_type}")
                    print(f"✓ Added column: {col_name}")
                except mysql.connector.Error as err:
                    if err.errno != 1060:  # Ignore duplicate column error
                        print(f"Warning: Could not add column {col_name}: {err}")

        # Create default admin user if no users exist
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        user_count = result['count']

        if user_count == 0:
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (%s, %s, %s, %s)
            ''', ('admin', 'admin', 'Administrator', 'admin'))
            print("✓ Default admin user created (username: admin, password: admin)")

        # Add default unloading godowns if table is empty
        cursor.execute("SELECT COUNT(*) as count FROM unloading_godowns")
        result = cursor.fetchone()
        godown_count = result['count']

        if godown_count == 0:
            default_godowns = [
                'Godown A',
                'Godown B',
                'Main Warehouse',
                'Storage Unit 1'
            ]
            for godown in default_godowns:
                cursor.execute('INSERT IGNORE INTO unloading_godowns (name) VALUES (%s)', (godown,))
            print(f"✓ Added {len(default_godowns)} default unloading godowns")

        conn.commit()
        print("✓ Database tables initialized successfully")

    except mysql.connector.Error as err:
        print(f"❌ Error initializing database: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_next_bill_no():
    """
    Get the next bill number
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT MAX(bill_no) as max_bill FROM purchase_slips')
        result = cursor.fetchone()

        if result['max_bill'] is None:
            return 1
        return result['max_bill'] + 1

    except mysql.connector.Error as err:
        print(f"❌ Error getting next bill number: {err}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
