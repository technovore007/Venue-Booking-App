# login_page.py
import tkinter as tk
import customtkinter as ctk
import mysql.connector
import bcrypt
from tkinter import messagebox
from common import connect_db

# Function to validate the user login
def validate_login(user_id, password):
    """Validate the user's credentials against the database."""
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        
        # Fetch user details from the database
        cursor.execute("SELECT user_id, user_name, role, pswd FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return None, "Invalid User ID or Password."

        # Verify password
        if bcrypt.checkpw(password.encode(), user['pswd'].encode()):
            return user, None
        else:
            return None, "Invalid User ID or Password."
    
    except mysql.connector.Error as err:
        return None, f"Database Error: {err}"
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

# Function to handle login action
def login_action(root, user_id_entry, password_entry):
    """Perform login action when the login button is clicked."""
    user_id = user_id_entry.get().strip()
    password = password_entry.get().strip()
    
    if not user_id or not password:
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return
    
    user, error = validate_login(user_id, password)
    
    if error:
        messagebox.showerror("Login Error", error)
        return

    # Successful login
    messagebox.showinfo("Login Success", f"Welcome {user['user_name']}!")
    root.destroy()  # Close the login window

    # Import UserConsole inside this function to avoid circular import
    from user_console import UserConsole
    UserConsole(user).mainloop()  # Open the User Console

# Main Login Page UI
def setup_login_page():
    """Setup and display the login page."""
    root = ctk.CTk()
    root.title("Venue Booking App - Login")
    root.geometry("400x300")
    root.resizable(False, False)

    # Header
    header_frame = ctk.CTkFrame(root, height=60)
    header_frame.pack(fill="x", padx=10, pady=10)

    header_label = ctk.CTkLabel(header_frame, text="Login", font=("Arial", 24))
    header_label.pack(pady=10)

    # User ID Entry
    user_id_label = ctk.CTkLabel(root, text="User ID", font=("Arial", 14))
    user_id_label.pack(pady=5)
    
    user_id_entry = ctk.CTkEntry(root, font=("Arial", 14))
    user_id_entry.pack(pady=5)

    # Password Entry
    password_label = ctk.CTkLabel(root, text="Password", font=("Arial", 14))
    password_label.pack(pady=5)
    
    password_entry = ctk.CTkEntry(root, show="*", font=("Arial", 14))
    password_entry.pack(pady=5)

    # Login Button
    login_button = ctk.CTkButton(
        root, text="Login", font=("Arial", 14), 
        command=lambda: login_action(root, user_id_entry, password_entry)
    )
    login_button.pack(pady=20)

    root.mainloop()

# Start the application
if __name__ == "__main__":
    setup_login_page()
