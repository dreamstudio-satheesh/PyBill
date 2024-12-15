import sqlite3
import bcrypt
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='pybill.db'):
        """
        Initialize the database manager.
        Ensures the database and required tables are created.
        """
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        """Establish a connection to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable named column access
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def execute_query(self, query, params=None, commit=False):
        """
        Execute a query with optional parameters.
        
        :param query: SQL query to execute
        :param params: Parameters to pass to the query (tuple or list)
        :param commit: Whether to commit changes to the database
        :return: Cursor object or None
        """
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                if commit:
                    conn.commit()
                return cursor
            except sqlite3.Error as e:
                print(f"SQL error: {e}")
            finally:
                conn.close()
        return None

    def create_tables(self):
        """Create all necessary tables for the billing software."""
        create_table_queries = [
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'staff')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category_id INTEGER,
                price REAL NOT NULL CHECK(price >= 0),
                stock INTEGER NOT NULL CHECK(stock >= 0),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total_amount REAL NOT NULL CHECK(total_amount >= 0),
                discount REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                subtotal REAL NOT NULL CHECK(subtotal >= 0),
                FOREIGN KEY (invoice_id) REFERENCES invoices(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER UNIQUE,
                amount_paid REAL NOT NULL CHECK(amount_paid >= 0),
                payment_method TEXT DEFAULT 'cash',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id)
            )
            '''
        ]
        for query in create_table_queries:
            self.execute_query(query)

    def create_admin_user(self, username, password):
        """
        Create an admin user with a hashed password.
        
        :param username: Admin username
        :param password: Plain-text password
        """
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        result = self.execute_query(
            '''
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            ''', (username, password_hash, 'admin'), commit=True
        )
        if result:
            print(f"Admin user '{username}' created successfully.")
        else:
            print(f"Failed to create admin user '{username}'. Username might already exist.")

    def seed_initial_data(self):
        """
        Seed initial data for categories and products.
        """
        # Seed categories
        initial_categories = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Books', 'Books and reading materials')
        ]
        self.execute_query(
            '''
            INSERT OR IGNORE INTO categories (name, description)
            VALUES (?, ?)
            ''', initial_categories, commit=True
        )

        # Seed products
        initial_products = [
            ('Smartphone', 1, 599.99, 50),
            ('Laptop', 1, 1299.99, 25),
            ('T-Shirt', 2, 29.99, 100),
            ('Jeans', 2, 59.99, 75),
            ('Programming Book', 3, 49.99, 30)
        ]
        self.execute_query(
            '''
            INSERT OR IGNORE INTO products (name, category_id, price, stock)
            VALUES (?, ?, ?, ?)
            ''', initial_products, commit=True
        )
        print("Initial data seeded successfully.")
