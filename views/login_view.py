import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self):
        self.auth = AuthController()
        self.root = tk.Tk()
        self.root.title("PyBill - Login")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

    def run(self):
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        # Username Label and Entry
        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(self.root, text="Login", command=self._handle_login).pack(pady=20)

    def _handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        role = self.auth.login(username, password)
        if role:
            messagebox.showinfo("Login Successful", f"Welcome, {role.capitalize()}!")
            self.root.destroy()  # Close the login window
            # TODO: Launch dashboard based on user role
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
