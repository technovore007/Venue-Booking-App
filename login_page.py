import tkinter as tk
import customtkinter as ctk
import mysql.connector
import bcrypt
from tkinter import messagebox
from user_console import UserConsole  # Assuming the UserConsole class is in 'user_console.py'

# MySQL Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="ehnd11", 
        database="venue_booking_system"
    )

# Function to validate the user login
def login(user_id_entry, password_entry):
    user_id = user_id_entry.get()
    password = password_entry.get()
    
    if not user_id or not password:
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return
    
    try:
        # Connect to the database
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        
        # Fetch user details from the database
        cursor.execute("SELECT user_id, user_name, role, pswd FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['pswd'].encode()):
            messagebox.showinfo("Login Success", f"Welcome {user['user_name']}!")
            
            # Check if the user is 'user' or 'admin'
            if user['role'].lower() == 'user':
                UserConsole(user).mainloop()
            else:
                # Placeholder for admin console, which will be implemented later
                messagebox.showinfo("Admin Login", "Admin role functionality coming soon.")
        else:
            messagebox.showerror("Login Error", "Invalid User ID or Password.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        # Close the database connection
        cursor.close()
        db.close()

# Main Login Page UI
def setup_login_page():
    root = ctk.CTk()
    root.title("Venue Booking App - Login")
    root.geometry("400x300")
    
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
    login_button = ctk.CTkButton(root, text="Login", font=("Arial", 14), command=lambda: login(user_id_entry, password_entry))
    login_button.pack(pady=20)

    root.mainloop()

# Start the application
if __name__ == "__main__":
    setup_login_page()
