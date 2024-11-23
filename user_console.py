# user_console.py
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from common import connect_db

class UserConsole(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.geometry("650x600")
        self.title("User Console")
        self.resizable(True, True)

        self.user = user  # User dictionary containing user_id and user_name
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = ctk.CTkFrame(self, height=50, fg_color="gray")
        header_frame.pack(side="top", fill="x")

        # Display username as a button
        user_button = ctk.CTkButton(
            header_frame, text=self.user['user_name'], command=self.user_options
        )
        user_button.pack(side="left", padx=10, pady=10)

        # Hamburger menu button
        burger_button = ctk.CTkButton(
            header_frame, text="☰", command=self.show_sidebar
        )
        burger_button.pack(side="right", padx=10, pady=10)

        # Current Bookings Section
        current_bookings_frame = ctk.CTkFrame(self, fg_color="gray")
        current_bookings_frame.pack(expand=True, fill="both", pady=20, padx=20)

        current_label = ctk.CTkLabel(
            current_bookings_frame, text="Current Bookings", font=("Arial", 18)
        )
        current_label.pack(pady=10)

        self.current_bookings_list = ctk.CTkLabel(
            current_bookings_frame, text="Loading...", font=("Arial", 14)
        )
        self.current_bookings_list.pack()

        # Add Booking Button
        add_button = ctk.CTkButton(
            self, text="+", width=50, height=50, command=self.add_booking
        )
        add_button.place(relx=0.9, rely=0.9, anchor="center")

        self.load_current_bookings()

    def user_options(self):
        option = messagebox.askquestion("User Options", "Do you want to log out?")
        if option == "yes":
            self.destroy()

            # Import setup_login_page inside this function to avoid circular import
            from login_page import setup_login_page
            setup_login_page()  # Reopen the login page

    def show_sidebar(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            query = """
                SELECT b.log_id, v.Venue_Name, b.booking_date, b.start_time, b.end_time 
                FROM booking_logs b 
                JOIN venues v ON b.venue_id = v.Venue_id 
                WHERE b.user_id = %s
            """
            cursor.execute(query, (self.user['user_id'],))
            bookings = cursor.fetchall()

            if bookings:
                booking_info = "\n".join([
                    f"Log ID: {b[0]}, Venue: {b[1]}, Date: {b[2]}, Time: {b[3]} - {b[4]}" 
                    for b in bookings
                ])
                messagebox.showinfo("Past Bookings", booking_info)
            else:
                messagebox.showinfo("Past Bookings", "No past bookings found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    def add_booking(self):
        messagebox.showinfo("New Booking", "Booking flow coming soon!")

    def load_current_bookings(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            # Query to fetch data from both tables
            query = """
                SELECT 
                    v.Venue_Name, 
                    b.Date AS booking_date, 
                    b.start_time, 
                    b.end_time, 
                    b.status 
                FROM booking_requests b
                JOIN venues v ON b.Venue_id = v.Venue_id
                WHERE b.user_id = %s
                UNION
                SELECT 
                    v.Venue_Name, 
                    b.booking_date, 
                    b.start_time, 
                    b.end_time, 
                    b.status 
                FROM approved_bookings b
                JOIN venues v ON b.venue_id = v.Venue_id
                WHERE b.user_id = %s
            """
            cursor.execute(query, (self.user['user_id'], self.user['user_id']))
            bookings = cursor.fetchall()

            # Format the bookings for display
            if bookings:
                booking_info = ""
                for b in bookings:
                    venue, date, start_time, end_time, status = b
                    # Apply color formatting for status
                    if status.lower() == "approved":
                        status_text = f"[green]{status}[/green]"
                    elif status.lower() == "rejected":
                        status_text = f"[red]{status}[/red]"
                    elif status.lower() == "pending":
                        status_text = f"[orange]{status}[/orange]"
                    else:
                        status_text = status  # Default, in case of unexpected status

                    booking_info += (
                        f"Venue: {venue}, Date: {date}, From: {start_time} To: {end_time}, "
                        f"Status: {status_text}\n"
                    )
                self.current_bookings_list.configure(text=booking_info.strip())
            else:
                self.current_bookings_list.configure(text="No current bookings found.")

        except mysql.connector.Error as err:
            self.current_bookings_list.configure(text="Error loading bookings.")
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()
