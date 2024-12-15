import sqlite3
import bcrypt
from config.database import DatabaseManager

class AuthController:
    def __init__(self):
        self.db = DatabaseManager()

    def login(self, username, password):
        """
        Authenticate user by validating username and password.

        :param username: Input username
        :param password: Input password
        :return: User role if authenticated, None otherwise
        """
        try:
            query = 'SELECT id, password_hash, role FROM users WHERE username = ?'
            result = self.db.execute_query(query, (username,))
            if result:
                user = result.fetchone()
                if user:
                    user_id, password_hash, role = user['id'], user['password_hash'], user['role']
                    if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                        return role  # Return the user's role (e.g., admin or staff)
            return None  # Authentication failed
        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def register_user(self, username, password, role='staff'):
        """
        Register a new user with a hashed password.
        
        :param username: New username
        :param password: New password in plain text
        :param role: User role (default is 'staff')
        :return: Success or error message
        """
        self.db.connect()
        try:
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.db.cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', (username, password_hash, role))
            self.db.conn.commit()
            return f"User '{username}' registered successfully as '{role}'"
        except sqlite3.IntegrityError:
            return "Error: Username already exists"
        finally:
            self.db.close()
