import customtkinter as ctk
import mysql.connector

# Set the appearance mode (dark or light)
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"

# Set the color theme (optional)
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Create the main application window
app = ctk.CTk()
app.title("Venue Booking System")
app.geometry("800x600")  # Adjust the window size for better layout


# Function: Handle Login
def login_action():
    username = username_entry.get()
    password = password_entry.get()
    print(f"Login Attempt: {username}, {password}")
    # Add further validation logic as needed


# Function: Fetch Pending Bookings from Database
def fetch_pending_bookings():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ehnd11",  # Replace with your MySQL password
            database="venue_booking_system"  # Ensure this database exists
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE status='pending'")
        booking_list.delete("1.0", "end")  # Clear the list before adding new data
        for row in cursor.fetchall():
            booking_list.insert("end", f"Booking ID: {row[0]}, Venue: {row[1]}\n")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        booking_list.insert("end", "Failed to fetch data from database.\n")


# Function: Toggle Light/Dark Mode
def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")


# Login Widgets
username_label = ctk.CTkLabel(app, text="Username:", font=("Arial", 16))
username_label.pack(pady=10)

username_entry = ctk.CTkEntry(app, placeholder_text="Enter your username")
username_entry.pack(pady=10)

password_label = ctk.CTkLabel(app, text="Password:", font=("Arial", 16))
password_label.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Enter your password", show="*")
password_entry.pack(pady=10)

login_button = ctk.CTkButton(app, text="Login", command=login_action)
login_button.pack(pady=20)


# Navigation Frame
menu_frame = ctk.CTkFrame(app, width=200, height=400, corner_radius=10)
menu_frame.pack(side="left", fill="y", padx=10, pady=10)

pending_button = ctk.CTkButton(menu_frame, text="Pending Bookings", command=fetch_pending_bookings)
pending_button.pack(pady=10)

approved_button = ctk.CTkButton(menu_frame, text="Approved Bookings")
approved_button.pack(pady=10)

create_booking_button = ctk.CTkButton(menu_frame, text="Create Booking")
create_booking_button.pack(pady=10)

toggle_button = ctk.CTkButton(menu_frame, text="Toggle Light/Dark Mode", command=toggle_mode)
toggle_button.pack(pady=20)


# Booking List (Scrollable Textbox)
booking_list = ctk.CTkTextbox(app, height=300, width=500)
booking_list.pack(pady=20)


# Run the application
app.mainloop()
