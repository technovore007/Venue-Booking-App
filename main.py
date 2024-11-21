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

# Function to open the "Past Bookings" view
def show_past_bookings():
    messagebox.showinfo("Past Bookings", "Past bookings functionality coming soon!")

# Function to handle the "Create New Booking" flow
def create_new_booking():
    def submit_booking():
        venue = venue_entry.get()
        booking_date = date_entry.get()
        booking_time = time_entry.get()
        
        if not venue or not booking_date or not booking_time:
            messagebox.showwarning("Input Error", "Please fill in all the fields.")
            return
        
        # Here, you would save the booking data to the database.
        # For now, we will just show a confirmation message.
        messagebox.showinfo("Booking Confirmed", f"Your booking for {venue} on {booking_date} at {booking_time} has been confirmed!")

    booking_window = ctk.CTkToplevel()
    booking_window.title("New Booking")
    booking_window.geometry("400x300")
    
    # Venue selection
    venue_label = ctk.CTkLabel(booking_window, text="Select Venue", font=("Arial", 14))
    venue_label.pack(pady=10)
    venue_entry = ctk.CTkEntry(booking_window, font=("Arial", 14))
    venue_entry.pack(pady=5)
    
    # Date selection
    date_label = ctk.CTkLabel(booking_window, text="Booking Date", font=("Arial", 14))
    date_label.pack(pady=10)
    date_entry = ctk.CTkEntry(booking_window, font=("Arial", 14))
    date_entry.pack(pady=5)
    
    # Time selection
    time_label = ctk.CTkLabel(booking_window, text="Booking Time", font=("Arial", 14))
    time_label.pack(pady=10)
    time_entry = ctk.CTkEntry(booking_window, font=("Arial", 14))
    time_entry.pack(pady=5)
    
    # Submit button
    submit_button = ctk.CTkButton(booking_window, text="Submit Booking", font=("Arial", 14), command=submit_booking)
    submit_button.pack(pady=20)

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

# User Console with Hamburger Menu
class UserConsole(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.geometry("600x600")
        self.title("User Console")
        self.resizable(False, False)

        self.user = user
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = ctk.CTkFrame(self, height=50, fg_color="gray")
        header_frame.pack(side="top", fill="x")

        user_button = ctk.CTkButton(header_frame, text=self.user['username'], command=self.user_options)
        user_button.pack(side="left", padx=10, pady=10)

        burger_button = ctk.CTkButton(header_frame, text="☰", command=self.show_sidebar)
        burger_button.pack(side="right", padx=10, pady=10)

        # Current Bookings Section
        current_bookings_frame = ctk.CTkFrame(self, fg_color="gray")
        current_bookings_frame.pack(expand=True, fill="both", pady=20, padx=20)

        current_label = ctk.CTkLabel(current_bookings_frame, text="Current Bookings", font=("Arial", 18))
        current_label.pack(pady=10)

        self.current_bookings_list = ctk.CTkLabel(current_bookings_frame, text="No records found", font=("Arial", 14))
        self.current_bookings_list.pack()

        # Add Booking Button
        add_button = ctk.CTkButton(self, text="+", width=50, height=50, command=self.add_booking)
        add_button.place(relx=0.9, rely=0.9, anchor="center")

    def user_options(self):
        option = messagebox.askquestion("User Options", "Do you want to log out?")
        if option == "yes":
            self.destroy()
            from login_page import LoginPage
            LoginPage().mainloop()

    def show_sidebar(self):
        sidebar_window = ctk.CTkToplevel(self)
        sidebar_window.geometry("250x200")
        sidebar_window.title("Hamburger Menu")
        
        past_bookings_button = ctk.CTkButton(sidebar_window, text="Past Bookings", font=("Arial", 14), command=show_past_bookings)
        past_bookings_button.pack(pady=10)

        new_booking_button = ctk.CTkButton(sidebar_window, text="Create New Booking", font=("Arial", 14), command=create_new_booking)
        new_booking_button.pack(pady=10)

if __name__ == "__main__":
    setup_login_page()
