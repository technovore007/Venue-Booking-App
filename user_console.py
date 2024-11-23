# user_console.py
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from common import connect_db
from datetime import datetime
from tkcalendar import Calendar
from tkinter import Toplevel, Label, Button, messagebox

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
        def validate_and_confirm():
            """Validates the booking details and checks for clashes."""
            venue_type = venue_type_var.get()
            venue_name = venue_name_var.get()
            booking_date = cal.get_date()
            start_time = f"{start_hour.get()}:{start_minute.get()}:00"
            end_time = f"{end_hour.get()}:{end_minute.get()}:00"

            if not venue_type or not venue_name or not booking_date:
                messagebox.showerror("Validation Error", "All fields are required!")
                return

            if not (start_hour.get().isdigit() and start_minute.get().isdigit() and end_hour.get().isdigit() and end_minute.get().isdigit()):
                messagebox.showerror("Validation Error", "Invalid time format!")
                return

            # Convert times for comparison
            start_dt = datetime.strptime(start_time, '%H:%M:%S')
            end_dt = datetime.strptime(end_time, '%H:%M:%S')
            if start_dt >= end_dt:
                messagebox.showerror("Validation Error", "Start time must be before end time!")
                return

            try:
                # Fetch venue ID based on name
                cursor.execute("SELECT Venue_id FROM venues WHERE Venue_Name = %s", (venue_name,))
                venue_id = cursor.fetchone()
                if not venue_id:
                    messagebox.showerror("Validation Error", "Invalid venue selected!")
                    return
                venue_id = venue_id[0]

                # Check for clashes in booking_requests and approved_bookings
                query = """
                    SELECT COUNT(*)
                    FROM (
                        SELECT Date, start_time, end_time FROM booking_requests WHERE Venue_id = %s AND status IN ('PENDING', 'APPROVED')
                        UNION
                        SELECT booking_date AS Date, start_time, end_time FROM approved_bookings WHERE Venue_id = %s
                    ) AS combined
                    WHERE Date = %s
                    AND (
                        (%s BETWEEN start_time AND end_time)
                        OR (%s BETWEEN start_time AND end_time)
                        OR (start_time BETWEEN %s AND %s)
                    )
                """
                cursor.execute(query, (venue_id, venue_id, booking_date, start_time, end_time, start_time, end_time))
                clashes = cursor.fetchone()[0]

                if clashes > 0:
                    messagebox.showerror("Booking Clash", "The selected time and date are already booked.")
                    return

                # Show confirmation
                confirmation = messagebox.askyesno(
                    "Confirm Booking",
                    f"Venue: {venue_name}\nDate: {booking_date}\nTime: {start_time} to {end_time}\n\nConfirm Booking?"
                )
                if not confirmation:
                    return

                # Insert booking request
                insert_query = """
                    INSERT INTO booking_requests (User_id, Venue_id, Date, start_time, end_time, status)
                    VALUES (%s, %s, %s, %s, %s, 'PENDING')
                """
                cursor.execute(insert_query, (self.user['user_id'], venue_id, booking_date, start_time, end_time))
                db.commit()

                messagebox.showinfo("Booking Success", "Your booking request has been successfully placed!")
                add_booking_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        # Open a new window for adding a booking
        add_booking_window = Toplevel(self)
        add_booking_window.title("Add Booking")
        add_booking_window.geometry("500x500")

        # Database connection
        db = connect_db()
        cursor = db.cursor()

        # UI Components
        Label(add_booking_window, text="Select Venue Type").pack()
        venue_type_var = ctk.StringVar()
        venue_type_menu = ctk.CTkOptionMenu(
            add_booking_window, variable=venue_type_var,
            values=['Classroom', 'Auditorium', 'Lecture Theatre', 'Tutorial Room', 'Meeting Room', 'Laboratory']
        )
        venue_type_menu.pack()

        def populate_venue_names(*args):
            """Populate venue names based on selected type."""
            selected_type = venue_type_var.get()
            cursor.execute("SELECT Venue_Name FROM venues WHERE Type = %s", (selected_type,))
            venues = [row[0] for row in cursor.fetchall()]
            venue_name_menu.configure(values=venues)
            venue_name_var.set("")

        venue_type_var.trace("w", populate_venue_names)

        Label(add_booking_window, text="Select Venue Name").pack()
        venue_name_var = ctk.StringVar()
        venue_name_menu = ctk.CTkOptionMenu(add_booking_window, variable=venue_name_var, values=[])
        venue_name_menu.pack()

        Label(add_booking_window, text="Select Date").pack()
        cal = Calendar(add_booking_window, date_pattern='yyyy-mm-dd')
        cal.pack()

        Label(add_booking_window, text="Start Time (HH:MM)").pack()
        start_hour = ctk.StringVar(value="09")
        start_minute = ctk.StringVar(value="00")
        ctk.CTkEntry(add_booking_window, textvariable=start_hour, width=30).pack(side="left")
        ctk.CTkEntry(add_booking_window, textvariable=start_minute, width=30).pack(side="left")

        Label(add_booking_window, text="End Time (HH:MM)").pack()
        end_hour = ctk.StringVar(value="10")
        end_minute = ctk.StringVar(value="00")
        ctk.CTkEntry(add_booking_window, textvariable=end_hour, width=30).pack(side="left")
        ctk.CTkEntry(add_booking_window, textvariable=end_minute, width=30).pack(side="left")

        Button(add_booking_window, text="Submit Booking", command=validate_and_confirm).pack()

        add_booking_window.mainloop()

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

            # Clear previous labels
            for widget in self.current_bookings_list.winfo_children():
                widget.destroy()

            if bookings:
                for b in bookings:
                    venue, date, start_time, end_time, status = b
                    
                    # Convert start_time and end_time to AM/PM format
                    start_time = datetime.strptime(str(start_time), '%H:%M:%S').strftime('%I:%M %p')
                    end_time = datetime.strptime(str(end_time), '%H:%M:%S').strftime('%I:%M %p')

                    # Determine color for the status
                    if status.lower() == "approved":
                        color = "green"
                    elif status.lower() == "rejected":
                        color = "red"
                    elif status.lower() == "pending":
                        color = "orange"
                    else:
                        color = "black"  # Default color

                    # Create a new label for each booking
                    booking_text = f"Venue: {venue}, Date: {date}, From: {start_time} To: {end_time}, Status: "
                    booking_label = ctk.CTkLabel(self.current_bookings_list, text=booking_text, font=("Arial", 15))
                    booking_label.pack(anchor="w")

                    # Add the status with colored text
                    status_label = ctk.CTkLabel(self.current_bookings_list, text=status, font=("Arial", 15), text_color=color)
                    status_label.pack(anchor="w")
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