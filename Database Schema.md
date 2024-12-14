import sqlite3
import bcrypt
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='billing_software.db'):
        """
        Initialize database connection and create tables
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.create_tables()

    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create all necessary tables for the billing software"""
        self.connect()
        
        # Users Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'staff')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # Categories Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # Products Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL CHECK(price >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )''')

        # Customers Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT UNIQUE,
            address TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # Invoices Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            discount REAL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )''')

        # Invoice Items Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),
            FOREIGN KEY (invoice_id) REFERENCES invoices(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')

        # Payments Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER UNIQUE,
            amount_paid REAL NOT NULL CHECK(amount_paid >= 0),
            payment_method TEXT DEFAULT 'cash',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        )''')

        self.conn.commit()

    def create_admin_user(self, username, password):
        """
        Create an admin user with hashed password
        
        :param username: Admin username
        :param password: Admin password in plain text
        """
        self.connect()
        
        # Hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        try:
            self.cursor.execute('''
            INSERT INTO users (username, password_hash, role) 
            VALUES (?, ?, ?)
            ''', (username, password_hash, 'admin'))
            self.conn.commit()
            print(f"Admin user {username} created successfully")
        except sqlite3.IntegrityError:
            print("Username already exists")
        finally:
            self.close()

    def seed_initial_data(self):
        """
        Seed initial data into the database
        """
        self.connect()
        
        # Seed initial categories
        initial_categories = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Books', 'Books and reading materials')
        ]
        
        self.cursor.executemany('''
        INSERT OR IGNORE INTO categories (name, description) 
        VALUES (?, ?)
        ''', initial_categories)
        
        # Seed initial products
        initial_products = [
            ('Smartphone', 1, 599.99, 50),
            ('Laptop', 1, 1299.99, 25),
            ('T-Shirt', 2, 29.99, 100),
            ('Jeans', 2, 59.99, 75),
            ('Programming Book', 3, 49.99, 30)
        ]
        
        self.cursor.executemany('''
        INSERT OR IGNORE INTO products (name, category_id, price, stock) 
        VALUES (?, ?, ?, ?)
        ''', initial_products)
        
        self.conn.commit()
        print("Initial data seeded successfully")
        self.close()

# Usage example
if __name__ == '__main__':
    # Initialize database
    db_manager = DatabaseManager()
    
    # Create admin user
    db_manager.create_admin_user('admin', 'strongpassword')
    
    # Seed initial data
    db_manager.seed_initial_data()